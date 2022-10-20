from PySide6.QtCore import (QObject, Signal, Property, QByteArray, QModelIndex, Qt,Slot)
from PySide6.QtQml import QmlElement
import os
from os import path
from os.path import dirname, abspath
import sys
sys.path.append(dirname(dirname(abspath(__file__))))
# To interact with the database
from fairdata import metadataDB

# To be used on the @QmlElement decorator
# (QML_IMPORT_MINOR_VERSION is optional)
QML_IMPORT_NAME = "Paths"
QML_IMPORT_MAJOR_VERSION = 1

@QmlElement
class Paths(QObject):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.mainPath = "prova"

    def readPath(self):
        return self.mainPath

    def setPath(self, val):
        self.mainPath = val

    @Signal
    def path_changed(self):
        pass

    mainPath = Property(str, readPath, setPath, notify=path_changed)

# obj = MyObject()
# obj.pp = 47
# print(obj.pp)
