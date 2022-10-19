    # -*- coding: utf-8 -*-
"""
===================
Generator of netcdf
===================

Author:         Corrado Motta  

Simple script to generate netcdf files automatically based on the notebook example.

Terminal args:
1. Path to folder where the csv log files are stored.
2. Path to folder where to save the generated nc files.
3. Path and filename of the configuration file.

It is assumed that the JSON database files are stored in the database folder.

--------------
How to run it:
--------------

from terminal:
$ python nc_gen_script_example.py "new_data" "new_results" "conf/conf.ini"

from an empty notebook:
%run nc_gen_script_example.py "new_data" "new_results" "conf/conf.ini"

"""

#-----------------------------------
# list of packages
#-----------------------------------

# os miscellaneous
import os
from os import path
# append fairdata folder
import sys
sys.path.append(path.join(path.dirname(path.abspath(__file__))))
# To interact with the database
from fairdata import metadataDB
# to read netcdf file
import netCDF4 as nc
# numpy is used to work with n-dimensional arrays
import numpy as np
# work with table
import pandas as pd
# to make figures
import matplotlib
# to work on netcdf files
import xarray
# to read conf file
import configparser
# to work with path
import ntpath
# to add date
from datetime import date
# to generate ISO19115
from bas_metadata_library.standards.iso_19115_2 import MetadataRecordConfigV2, MetadataRecord
# for iso format
from datetime import datetime

#-----------------------------------
# list of functions
#-----------------------------------

def main_script(log_folder, result_folder, conf_path):

    if(not os.path.exists(result_folder)):
        os.makedirs(result_folder)
        print("Created directory for storing results.")

    for file_name in os.listdir(log_folder):
        if(ntpath.split(file_name)[1].split(".")[1] == "csv"):
            print("\nStarting netcdf generator script..")
            filePath = path.join(log_folder, file_name)
            filename = ntpath.split(filePath)[1].split(".")[0]

            # read generated file
            read_config = configparser.ConfigParser()
            read_config.read(conf_path)
            my_complete_dict = dict(read_config.items('mandatory_global_attributes'))
            my_complete_dict = my_complete_dict | dict(read_config.items('optional_global_attributes'))

            #print("The following attributes will be added:")
            cont = 0
            key_list = []
            for key, value in my_complete_dict.items():
                if(value):
                    cont +=1
                    my_complete_dict[key] = str(value).replace('"','')
                    key_list.append(key)
                    #print(str(cont) + ".", key, '->', value)

            # Opening JSON file
            global_db = metadataDB.metadataDB('database/global_metadata.json')

            # iterate over mandatory global metadata. When one is not present, stop and print it
            for key, value in global_db.getAll().items():
                if(value['required'] and not value['auto']):
                    if(value['ACDD'].lower() in key_list):
                        pass
                        #print(value['ACDD'] + ".. found")
                    else:
                        print(value['ACDD'], "NOT found!\n\nPlease add a value for ",value['ACDD'])
                        break

            # import raw data
            data = pd.read_table(filePath, delimiter = ',', converters={('time', 'time'):str,('date', 'date'): str}, header=[0,1])
            data_columns = data.columns

            # Remove header
            data = data.droplevel(1, axis=1)

            # join date and time
            data["datetime"] = data["date"].astype(str)+ " " + data["time"].astype(str)
            # create a datetime python object
            data["datetime"] = pd.to_datetime(data['datetime'], format='%yy%m%d %H%M%S.%s', infer_datetime_format=True)

            # add automatic global variables
            my_complete_dict["time_coverage_start"] = data["datetime"].min().isoformat()
            my_complete_dict["time_coverage_end"] =   data["datetime"].max().isoformat()
            my_complete_dict["geospatial_lat_max"] =  data['latitude'].max()
            my_complete_dict["geospatial_lat_min"] =  data['latitude'].min()
            my_complete_dict["geospatial_lat_units"] = "degree_north"
            my_complete_dict["geospatial_lon_min"] =  data['longitude'].min()
            my_complete_dict["geospatial_lon_max"] =  data['longitude'].max()
            my_complete_dict["geospatial_lon_units"] = "degree_east"
            my_complete_dict["date_created"] = datetime.now().isoformat()
            my_complete_dict["time_coverage_duration"] = (data["datetime"].max() - data["datetime"].min()).isoformat()
            my_complete_dict["time_coverage_resolution"] = "milliseconds"

            # add to keylist
            key_list = []
            for key, value in my_complete_dict.items():
                if(value):
                    key_list.append(key)

            # iterate over mandatory global metadata. When one is not present, stop and print it
            for key, value in global_db.getAll().items():
                if(value['required'] and value['auto']):
                    if(value['ACDD'].lower() in key_list):
                        pass
                        #print(value['ACDD'] + ".. found")
                    else:
                        print(value['ACDD'], "NOT found!\n\nPlease add a value for ",value['ACDD'])
                        break
           
            # If you want to plot data uncomment and use your telemetry variables
            #p = data.plot(x='datetime', y=['FL_thruster_speed','FR_thruster_speed','RL_thruster_speed','RR_thruster_speed'], title = filename, figsize=(30,12), grid = True).get_figure()
            #png_result_path = os.path.join(result_folder, "images")
            #p.savefig(os.path.join(png_result_path, filename + ".png"))
                        
                        
            # create dataset
            xr = xarray.Dataset.from_dataframe(data)

            # add global data
            for key, value in my_complete_dict.items():
                if(value):
                    xr.attrs[key] = value

            # Opening JSON file
            variable_db = metadataDB.metadataDB('database/variable_metadata.json')

            # get all data
            variables = variable_db.getAll()

            # iterate over each variable in the table and look for it in the database.
            for key in data_columns:
                attr = variable_db.getEntry('long_name', key[1])
                if(attr):
                    for attr_name, value in attr[0].items():
                        if(attr_name!='version' and value):
                            xr[key[0]].attrs[attr_name] = value
                else:
                    print("Attributes NOT found for variable", key[0])
            print("All done!")

            # create a result path for it
            result_path = os.path.join(result_folder, filename + ".nc")

            # save to nc
            xr.to_netcdf(result_path)
            print("saving netCDF4 to {0}".format(result_path))


if __name__ == "__main__":

    print("Arguments count: {0}".format(len(sys.argv)-1))

    # check the arguments are correct
    try:
        assert len(sys.argv) == 4

    except AssertionError as err:
        print("{0}Fatal error. Exactly 3 argument expected, {1} given".format(len(sys.argv)-1))
        sys.exit(0)

    log_folder = sys.argv[1]
    result_folder =  sys.argv[2]
    conf_folder = sys.argv[3]

    main_script(log_folder, result_folder, conf_folder)