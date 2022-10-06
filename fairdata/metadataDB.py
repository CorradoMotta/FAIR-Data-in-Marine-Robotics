    # -*- coding: utf-8 -*-
"""
==========
metadataDB
==========

Author:         Corrado Motta  
Date:           10/2022

This module is a customized wrapper of PysonDB-V2, which implements a Lightweight JSON based database. 
Through the functions of this module it is possible to add, remove, edit and visualize the
metadata collected in the database.

-----------------
Other information
-----------------

This module requires the installation of PysonDB to work. Check https://pysondb.github.io/pysonDB-v2/ for 
installing into your python environment.

"""

#-----------------------------------
# list of packages
#-----------------------------------

# To generate JSON DB
from pysondb import PysonDB
from pysondb import errors as pErr
# To read CSV tables
import pandas as pd

#-----------------------------------
#-----------------------------------

class metadataDB:

    """ Class that contains the PysonDB object.
    TODO: in case it exists already, send back that info?

    Args:
        db (str): Path to the existing or new database.

    """

    def __init__(self, db):
        self.db_pointer = PysonDB(db)

    def add(self, metadata_entry):

        """ Adds a new entry to the current database if it does not
        exist yet.
        TODO: in case of wrong format?

        Args:
            metadata_entry(dict): Dict version of the metadata entry.
        """

        if(not self.dict_exists(metadata_entry)):
            self.db_pointer.add(metadata_entry)

    def dict_exists(self, item):

        """ Returns true if the dictionary exists.

        Args:
            item(dict) : The item to look for.

        Returns:
            bool: True if present, false if not present.
        """

        db_dict =  self.db_pointer.get_all().items()
        for key, value in db_dict:
            if (value == item):
                print("Element already present with key", key)
                return True

        return False


    def element_exists(self, key, name):

        """ Returns true if the element exists.

        Args:
            key(str) : Which key should be used for the look up.
            name(str) : The name that should be searched.

        Returns:
            bool: True if present, false if not present.
        """

        db_json = self.db_pointer.get_all()
        for key_index in db_json:
            if(db_json[key_index][key] == name):
                return True

        return False

    def id_exists(self, id):

        """ Returns true if ID exists. 

        Args:
            id(str) : The id of the element.

        Returns:
            bool: True if present, false if not present.
        """

        try:
            if(self.db_pointer.get_by_id(id)):
                return True

        except pErr.IdDoesNotExistError as err:             
            return False

        return False

    def getId(self, key, name):

        """ Returns the first database entry found for the required element.

        Args:
            key(str) : Which key should be used for the look up.
            name(str) : The name that should be searched.

        Returns:
            dict: The dictionary of the element. None if not present.
        """

        db_json = self.db_pointer.get_all()
        for key_index in db_json:
            if(db_json[key_index][key] == name):
                return db_json[key_index]

        return None


    def getAll(self):

        """ Returns all elements.

        Returns:
            dict: A dict containing all elements.
        """

        return self.db_pointer.get_all()