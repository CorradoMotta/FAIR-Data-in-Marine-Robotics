# FAIR data

|Description	| Set of notebooks, scripts and modules to generate metadata in several formats, following FAIR principles. |
| :-------------| :----------------------------------------------------------- |
|Contacts		| corradomotta92@gmail.com |
|Date		| 08/2022 |

This is a work in progress. At the time of writing, this repository contains two notebooks:

1. _database.ipynb_ : It shows how to create a light database in JSON format. Such database are used to store the standard names of global variables and the standard attributes of robotic and scientific variables. The products of such notebook are stored in the folder `database` and are used to fill the NetCDF files with standardized metadata.
2. _netcdf_conventions.ipynb_: It aims to show how to add and possibly extract descriptive and domain specific metadata from NetCDF files using python. It takes raw data in input, from folder `data` and creates FAIR NetCDF and ISO-199115-2 files in output. The products are saved in folder `results`. All folders and files can be modified using the configuration file in the `conf` folder. More information are contained directly in the notebook.
