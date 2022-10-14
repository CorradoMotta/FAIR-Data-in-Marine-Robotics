# FAIR data in marine robotics

|Description	| Set of notebooks, scripts and modules to generate metadata in several formats, following FAIR principles. |
| :-------------| :----------------------------------------------------------- |
|Contacts		| corradomotta92@gmail.com |
|Date		| 08/2022 |

For more information check the [GitHub pages](https://corradomotta.github.io/FAIR-Data-in-Marine-Robotics/) of this project! 

This is a work in progress. At the time of writing, this repository contains several notebooks and python files. Here a short summary of the most important ones:

1. _database.ipynb_ : It shows how to create a light database in JSON format. Such database are used to store the standard names of global variables and the standard attributes of robotic and scientific variables. The products of such notebook are stored in the folder `database` and are used to fill the NetCDF files with standardized metadata.
2. _netcdf_conventions.ipynb_: It aims to show how to add and possibly extract descriptive and domain specific metadata from NetCDF files using python. It takes raw data in input and creates FAIR NetCDF and ISO-199115-2 files in output. The notebook interacts with the previously created database and with a configuration file that contains the values given to the global metadata. More information are contained directly in the notebook.
3. _nc_gen_script_example.py_: Simple script to generate netcdf files automatically based on the notebook example. It can be used to generate all nc files in once.
4. _fairdata_ folder: It contains our own python modules. Right now the only module present is _metadataDB_ which is the interface towards the JSON databases.
