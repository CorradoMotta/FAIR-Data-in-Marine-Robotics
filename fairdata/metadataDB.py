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

# to check path
import os
import ntpath

#-----------------------------------
#-----------------------------------

class Error(Exception):

    """ Base class for exceptions.

    Args:
        method (str): Method in which the error occurred.
        message (str): Explanation of the error.
    """

    def __init__(self, method, message):
        
        self.method = method
        self.message = message

class notUniqueError(Error):

    """ Error that occur when more than one element is found in the database for a 
    query.

    Args:
        method (str): Method in which the error occurred.
        message (str): Explanation of the error.
        ids (list): List of IDs.
    """

    def __init__(self, method, message,ids):
        
        super().__init__(method,message)
        self.ids = ids

class uniqueKeyError(Error):

    """ Error that occur when a new entry has an already existing value for the unique key.

    Args:
        method (str): Method in which the error occurred.
        message (str): Explanation of the error.
        value (str): The unique value.
    """

    def __init__(self, method, message, value):
        
        super().__init__(method,message)
        self.value = value

class metadataDB:

    """ Class that contains the PysonDB object.
    If the database is not existing, it creates the database, 
    otherwise it connects to the existing file.

    Args:
        db (str): Path to the existing or new database.
        unique_key(str): Key that shall have a unique value in the entire dataset.

    """

    def __init__(self, db, unique_key = None):

        self.db_pointer = self._createDB(db)
        self.unique = unique_key

    def _createDB(self, db):

        """ Inner function to create a pysonDB.

        Args:
            db (str): Path to the existing or new database.
        """

        file_name = ntpath.split(db)[1]

        if(os.path.exists(db)):
            print("Database with name {0} already existing. \
                All further operation will directly connect to it.".format(file_name))
        else:
            print("Creating new database with name",file_name)

        return PysonDB(db)


    def add(self, metadata_entry):

        """ Adds a new entry to the current database if it does not
        exist yet or if some of the values contained are different.

        Args:
            metadata_entry (dict): Dictionary of the metadata entry.

        Returns:
            bool: True if added, false if not (because it already exists).
        """

        if(not self.dict_exists(metadata_entry)):
            if(self.unique):
                if(not self.unique_value_exists(metadata_entry[self.unique])):
                    self.db_pointer.add(metadata_entry)
                    return True
                else:
                    print("{0} key with value <{1}> already exists! Use the updateEntry method to update the entry instead."
                        .format(self.unique,metadata_entry[self.unique]))
                    return False

        else:
            return False

    def dict_exists(self, item):

        """ Returns true if the dictionary exists.

        Args:
            item (dict) : The item to look for.

        Returns:
            bool: True if present, false if not present.
        """

        db_dict =  self.db_pointer.get_all().items()

        for key, value in db_dict:
            if (value == item):
                return True

        return False

    def unique_value_exists(self, value):

        """ Returns true if the value is already
        used by the unique key of one of the entries.

        Args:
            value (str) : The value to look for.

        Returns:
            bool: True if present, false if not present.
        """

        db_json = self.db_pointer.get_all()
        if(self.unique):
            for key_index in db_json:
                if(db_json[key_index][self.unique] == value):
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
            id (str) : The id of the element.

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

        """ Returns the database entry found for the required element.

        Args:
            key (str) : Which key should be used for the look up.
            name (str) : The name that should be searched.

        Returns:
            dict: The dictionary of the element. None if not present.
        """

        db_json = self.db_pointer.get_all()
        ids = []

        for key_index in db_json:
            if(db_json[key_index][key] == name):
                 ids.append(key_index)

        if(len(ids)>1):
            raise notUniqueError("getId", "More than one ID found for the key and value pair!", ids)

        if(len(ids)==0):
            return None

        return ids[0]

    def getEntry(self, key, name):

        """ Returns the database entries found for the key value pair.

        Args:
            key (str) : Which key should be used for the look up.
            name (str) : The name that should be searched.

        Returns:
            list: The dictionaries of the found entries. None if not present.
        """

        db_json = self.db_pointer.get_all()
        entries = []

        for key_index in db_json:
            if(db_json[key_index][key] == name):
                 entries.append(db_json[key_index])

        return entries

    def getById(self, id):

        """ Returns the database entry found for the required ID.

        Args:
            id (str) : The database ID.

        Returns:
            dict: The dictionary of the element. None if not present.
        """

        return self.db_pointer.get_by_id(id)

    def updateEntry(self, id, updatedEntry):

        """ Update the specific entry by passing a new dictionary.
        It can contain the whole set of keys value of any of the subset.

        Args:
            id (str) : The database entry ID.
            updatedEntry (dict) : The new dictionary.

        Returns:
            dict: the updated dictionary.
        """

        # TODO check if is different from existing one
        return self.db_pointer.update_by_id(id, updatedEntry)

    def getAll(self):

        """ Returns all elements.

        Returns:
            dict: A dict containing all elements.
        """

        return self.db_pointer.get_all()