***************
Global Metadata
***************

With global metadata we refer to *descriptive metadata* which usually includes info such as title, author, subjects, keywords, publisher, urls, etc. Several standards exists such as DataCite, DublinCore and ISO 19115. They are mainly domain agnostic. 

Global Metadata is the term used to identify descriptive metadata in the NetCDF files. Our objective is to use NetCDF format for our robotic data. Therefore, we would like to add the appropriate global metadata directly within the NetCDF file, following the existing standard.

The ACDD convention (Attribute for Climate and Data Discovery) can be used to populate the global attributes. Such convention is adopted internationally and allows your NetCDF file to be self-describing, without the need of any additional file containing metadata information. When opened in python, using xarray, the dataset would look like the following:

.. image:: images/global_variable.png

As in any NetCDF file, the three main elements are present: Dimensions, Coordinates and Variables. Besides that, we can see a number of Attributes. Such attributes are not bound to any variable, that indicates they are global.

We agreed upon a set of minimum mandatory and optional global attributes to use in our datasets.

--------------------
Mandatory attributes
--------------------

These attributes shall always be included during dataset generation.

+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
| Name                         |                                              Description                                                | ACDD                         |
+==============================+=========================================================================================================+==============================+
|Title                         |A brief title for the dataset.                                                                           |title                         |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Abstract                      |A short summary for dataset, the content and potential linkages etc.                                     |summary                       |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|keywords                      |A comma separated list of key words and phrases.                                                         |keywords                      |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Conventions                   |A comma-separated list of the conventions that are followed by the dataset. For ACDD use 'ACDD-1.3'      |Conventions                   |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Principal investigator (PI)   |Name of the PI                                                                                           |creator_name                  |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|PI email                      |Email to the PI                                                                                          |creator_email                 |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|PI institution                |Affiliation of the PI                                                                                    |institution                   |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset start time            |ISO8601 reference for the dataset                                                                        |time_coverage_start           |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset end time              |ISO8601 reference for the dataset                                                                        |time_coverage_end             |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset northernmost latitude |Geographical northernmost position of the dataset (rectangular box)                                      |geospatial_lat_max            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset southernmost latitude |Geographical southernmost position of the dataset (rectangular box)                                      |geospatial_lat_min            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset latitude units        |Further refinement of the box                                                                            |geospatial_lat_units          |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset easternmost longitude |Geographical easternmost position of the dataset, positive east of Greenwich.                            |geospatial_lon_min            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset westernmost longitude |Geographical westernmost position of the dataset, negative west of Greenwich.                            |geospatial_lon_max            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset longitude units       |Further refinement of the box                                                                            |geospatial_lon_units          |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|date created                  |The date on which the data was created.                                                                  |date_created                  |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset language              |Language used in the dataset. Should be English                                                          |/                             |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Platform                      |Name of the platform(s) that supported the sensor data used to create this data set or product.          |platform                      |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|License                       |Describe the restrictions to data access and distribution.                                               |license                       |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Dataset version               |Version identifier of the data file or product as assigned by the data creator.                          |product_version               |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|time_coverage_duration        |Describes the duration of the data set. Use ISO 8601:2004 duration format.                               |time_coverage_duration        |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|time_coverage_resolution      |Describes the targeted time period between each value in the data set. Use ISO 8601:2004 duration format.|time_coverage_resolution      |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+

--------------------
Optional attributes
--------------------

These attributes are optional for two reasons:

1. They may or may not be needed.
2. They are not available during generation of NetcCDF, but are highly reccomended on a later stage (e.g. id).

+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
| Name                         |                                              Description                                                | ACDD                         |
+==============================+=========================================================================================================+==============================+
|keywords vocabulary           |Guideline for the words/phrases in your "keywords" attribute, if any                                     |keywords_vocabulary           |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|ISO Topic category            |List of topic categories for the dataset                                                                 | /                            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Project long name             |The scientific project that produced the data. Multiple names to be separated by comma.                  |project                       |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Data center (URL)             |URL to the data center hosting the data.                                                                 |publisher_url                 |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|Creator (URL)                 |URL to creator or to information                                                                         |creator_url                   |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|standard_name_vocabulary      |The name of the controlled vocabulary from which variable standard names are taken.                      |standard_name_vocabulary      |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|id                            |An identifier for the data set, it can be the DOI as well.                                               |id                            |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|processing_level              |A textual description of the processing (or quality control) level of the data.                          |processing_level              |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|geospatial_vertical_max       |Describes the numerically larger vertical limit                                                          |geospatial_vertical_max       |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|geospatial_vertical_min       |Describes the numerically smaller vertical limit                                                         |geospatial_vertical_min       |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|geospatial_vertical_positive  |"up" or "down". If down, vertical values are interpreted as 'depth'                                      |geospatial_vertical_positive  |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|geospatial_vertical_resolution|Further refinement of the box                                                                            |geospatial_vertical_resolution|
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+
|geospatial_vertical_units     |Further refinement of the box                                                                            |geospatial_vertical_units     |
+------------------------------+---------------------------------------------------------------------------------------------------------+------------------------------+

------------------------------
Integration and metadata check
------------------------------

The notebook explains in details how to generate the NetCDF and add the global metadata.
At the time of writing, the global metadata are set on a configuration file named ``conf.ini``. This file can be automatically generate from the interface that controls the vehicle. Then, the configuration file is taken in input from the notebook script, and the attributes where a value is found are added to the NetCDF, using ``xarray`` python package. 

Furthermore, the generated global metadata are checked against the table shown above, to verify that all mandatory elements are included. To do so, a light JSON database is generated, which includes all mandatory and optional elements. The JSON database is very simple and looks as the following snippet:


.. _interface: https://github.com/CorradoMotta/ASV_interface

.. code-block:: json

    "data": {
        "657500993870255894": {
            "name": "Title",
            "ACDD": "title",
            "required": true,
            "default": "",
            "description": "A brief title for the dataset",
            "auto": false
        },
        "220784140157161391": {
            "name": "Abstract",
            "ACDD": "summary",
            "required": true,
            "default": "",
            "description": "A short summary for dataset, the content and potential linkages etc.",
            "auto": false
        },
        "338703899268240663": {
            "name": "keywords",
            "ACDD": "keywords",
            "required": true,
            "default": "unmanned marine vehicles,marine robotics,autonomous systems",
            "description": "A comma separated list of key words and phrases",
            "auto": false
        }
		
At the moment, six fields are saved. The **name**, the **ACDD** standard name, if it is mandatorily **required**, the **default** value, if any, the **description** of the metadata, and if can be **automatically** generated from the dataset (e.g., Dataset northernmost latitude or Dataset start time). In this way, the validation is quickly done by using our own module:

.. code-block:: python

	# Opening JSON file
	global_db = metadataDB.metadataDB('database/global_metadata.json')

	# iterate over all the global metadata found in the database
	for key, value in global_db.getAll().items():
	
		# filter out the optional ones and the one we will automatically create
		if(value['required']) and not value['auto']):
		
			# key_list contains the metadata found in the configuration file with a valid value
			if(value['ACDD'].lower() in key_list):
				print(value['ACDD'] + ".. found")
			
			# alert in case a mandatory metadata is not found.
			else:
				print(value['ACDD'], "NOT found!\n\nPlease add a value for ",value['ACDD'])
				break