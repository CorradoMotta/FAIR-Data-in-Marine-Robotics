.. FAIR data in marine robotics documentation master file, created by
   sphinx-quickstart on Wed Aug 31 11:25:54 2022.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to FAIR data in marine robotics's documentation!
********************************************************

*Author*: Corrado Motta (corradomotta92@gmail.com)

The aim of this documentation is to describe how to make robotic data FAIR (Findability, Accessibility, Interoperability, and Reusability) by using a set of tools and script defined in python.

See it on GitHub_.

.. _GitHub: https://github.com/CorradoMotta/FAIR-data

======
Status
======

This is a work in progress. At the time of writing, this repository contains two notebooks:

1. *database.ipynb* : It shows how to create a light database in JSON format. Such database are used to store the standard names of global variables and the standard attributes of robotic and scientific variables. The products of such notebook are stored in the folder ``database`` and are used to fill the NetCDF files with standardized metadata.


2. *netcdf_conventions.ipynb*: It aims to show how to add and possibly extract descriptive and domain specific metadata from NetCDF files using python. It takes raw data in input, from folder ``data`` and creates FAIR NetCDF and ISO-199115-2 files in output. The products are saved in folder ``results``. All folders and files can be modified using the configuration file in the ``conf`` folder. More information are contained directly in the notebook.

.. toctree::
   :caption: Contents
   :maxdepth: 2
   
   global_metadata
   variable_metadata

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
