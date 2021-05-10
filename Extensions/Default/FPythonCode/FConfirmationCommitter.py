""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/confirmation/etc/FConfirmationCommitter.py"

import FOperationsUtils as Utils

class Committer:
    def __init__(self, fObject):
        self.__fObject = fObject

    def Commit(self):
        try:
            if self.__fObject.IsClone():
                clone = self.__fObject
                original = clone.Original()
                original.Apply(clone)
                original.Owner(clone.Owner())
                objectToCommmit = original
            else:
                objectToCommmit = self.__fObject

            objectToCommmit.Commit()
        except Exception as error:
            Utils.RaiseCommitException(error, self.__fObject)

    def Delete(self):
        try:
            if self.__fObject.IsClone():
                clone = self.__fObject
                original = clone.Original()
                objectToDelete = original
            else:
                objectToDelete = self.__fObject
                
            objectToDelete.Delete()
        except Exception as error:
            Utils.RaiseCommitException(error, self.__fObject)