# -*- coding: utf-8 -*-
"""
=====
model
=====

Author:         Corrado Motta  
Date:           11/2022

This module implements the model view delegate pattern of Qt interfaces. 
It reads a JSON database to get all global metadata and automatically updates the interface
with all fields. It allows to generated NetCDF files by using the nc_gen_script.py methods.
"""

#-----------------------------------
# list of packages
#-----------------------------------

# os miscellaneous
import os
from os import path
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))

# Qt packages
from PySide6.QtCore import (QAbstractListModel, QByteArray, QModelIndex, Qt,Slot)
from PySide6.QtQml import QmlElement

# to parse ini files
import configparser

# our own modules
from fairdata import metadataDB
import default_values
import nc_gen_script

# To be used on the @QmlElement decorator
QML_IMPORT_NAME = "BaseModel"
QML_IMPORT_MAJOR_VERSION = 1

#-----------------------------------
# class
#-----------------------------------

@QmlElement
class BaseModel(QAbstractListModel):

    """ Class that extends the QAbstractListModel python class.
    Roles are customized. The global metadata are stored within a list
    of dictionaries populated by the JSON databases. 

    Args:
        parent (str): Widget parent. Default is None.
    """

    # create my roles
    nameRole = Qt.UserRole + 1
    acddNameRole = Qt.UserRole + 2
    valueRole = Qt.UserRole + 3
    defaultValueRole = Qt.UserRole + 4
    levelRole = Qt.UserRole + 5
    autoRole = Qt.UserRole + 6
    descriptionRole = Qt.UserRole + 7

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        # Opening JSON file
        self.global_db = metadataDB.metadataDB('../database/global_metadata.json')
        self.metadata_list = self.populateFromDb()

    def rowCount(self, parent=QModelIndex()):
        # override. Gives the number of rows.
        return len(self.metadata_list)

    def roleNames(self):
        # override. If your model is used within QML and requires roles other than the default ones 
        # provided by the roleNames() function, you must override it.

        default = super().roleNames()
        default[self.nameRole] = QByteArray(b"name")
        default[self.acddNameRole] = QByteArray(b"acdd_name")
        default[self.valueRole] = QByteArray(b"value")
        default[self.defaultValueRole] = QByteArray(b"defaultValue")
        default[self.levelRole] = QByteArray(b"isMandatory")
        default[self.autoRole] = QByteArray(b"isAuto")
        default[self.descriptionRole] = QByteArray(b"description")
        return default

    def data(self, index, role: int):
        # override. Function to retrieve items from the list.

        if not self.metadata_list:
            ret = None
        elif not index.isValid():
            ret = None
        elif role == self.nameRole:
            ret = self.metadata_list[index.row()]["name"]
        elif role == self.acddNameRole:
            ret = self.metadata_list[index.row()]["acdd_name"]
        elif role == self.valueRole:
            ret = self.metadata_list[index.row()]["value"]
        elif role == self.defaultValueRole:
            ret = self.metadata_list[index.row()]["defaultValue"]
        elif role == self.levelRole:
            ret = self.metadata_list[index.row()]["isMandatory"]
        elif role == self.autoRole:
            ret = self.metadata_list[index.row()]["isAuto"]
        elif role == self.descriptionRole:
            ret = self.metadata_list[index.row()]["description"]

        else:
            ret = None
        return ret

    def setData(self, index, value, role):
        # override. Function to set a new value for a specific role
        # of one of your data

        if not index.isValid():
            return False
        if role == self.valueRole:
            self.metadata_list[index.row()]["value"] = value
        return True
    
    def populateFromDb(self):

        """ Populates the model with global metadata from JSON database.
        It also checks the custom default values and adds to the default section.

        Returns:
            list: List of dictionaries containing all fields of the JSON database entry.
        """
        
        metadata_list = []
        metadata_list_nm = [] # to append not mandatory elements afterwards

        custom_default = default_values.default_ini('custom_default/default.ini')
        custom_default.read_default()

        for key, value in self.global_db.getAll().items():
            if(not value["auto"]):

                # Adding custom default values
                if value["ACDD"] in custom_default.default_dict:
                    value["default"] = custom_default.default_dict[value["ACDD"]]

                if(value["required"]):
                    metadata_list.append({"name": value["name"], 
                                          "acdd_name": value["ACDD"], 
                                          "value": "", 
                                          "defaultValue": value["default"],
                                          "isMandatory": value["required"],
                                          "isAuto": value["auto"], 
                                          "description": value["description"]})
                else:
                    metadata_list_nm.append({"name": value["name"], 
                                          "acdd_name": value["ACDD"], 
                                          "value": "", 
                                          "defaultValue": value["default"],
                                          "isMandatory": value["required"],
                                          "isAuto": value["auto"], 
                                          "description": value["description"]})

        metadata_list.extend(metadata_list_nm)
        return metadata_list
                
    @Slot()
    def reset(self):

        """ Reset the view by removing all values from the value entry.
        """

        self.beginResetModel()
        self.metadata_list = self.populateFromDb()  # should work without calling it ?
        self.endResetModel()

    @Slot()
    def default(self):

        """ Adds the default values as values and display them.
        """

        for idx, data in enumerate(self.metadata_list):
            self.metadata_list[idx]["value"] = data["defaultValue"]
            self.dataChanged.emit(self.index(idx,0),self.index(idx,0), [self.valueRole])

    @Slot(bool, result = bool)
    def generateINI(self, check_file):

        """ Generates an ini file named conf.ini with all metadata that are filled. The file will
        be located in this very same folder.

        Args:
            check_file (bool): If true will first check if a conf.ini file is already existing.

        Returns:
            bool: True if a file with the same name is already existing, false in case is not.
                If True is returned a new file was NOT generated.
        """

        path_name = 'conf.ini'
        path_exist = path.exists(path_name)


        if(check_file):
            if(path_exist):
                return True

        if(path_exist):
            # remove file
            os.remove(path_name)

        config = configparser.ConfigParser()

        for idx, data in enumerate(self.metadata_list):
            if(data["value"]):
                if(data["isMandatory"]):
                    if(not config.has_section('mandatory_global_attributes')):
                        config.add_section('mandatory_global_attributes')
                    config['mandatory_global_attributes'][data["acdd_name"]] = data["value"]   # create
                else:
                    if(not config.has_section('optional_global_attributes')):
                        config.add_section('optional_global_attributes')
                    config['optional_global_attributes'][data["acdd_name"]] = data["value"]

        with open(path_name, 'w') as configfile:  # save
            config.write(configfile)

        return False

    @Slot(str, result = str)
    def generateNC(self, nc_path):

        """ Generates one or more NetCDF files by using nc_gen_script methods.

        Args:
            nc_path (str): Path to one specific CSV file or to a folder containing more CSV files.

        Returns:
            str: A message to display to the interface.
        """

        #self.generateINI(False)        
        ini_dict = {} 
        for idx, data in enumerate(self.metadata_list):
            ini_dict[data["acdd_name"]] = data["value"]

        if(nc_path.startswith("file:///")):
            nc_path = nc_path.replace("file:///", "")

        if(os.path.exists(nc_path)):
            result = nc_gen_script.main_script(nc_path, "results", ini_dict)
            if (result):
                return "File(s) generated and saved in results folder."
            else:
                return "An error occurred. Please check the console for more info."
        else: 
            return "Input CSV file not found!"