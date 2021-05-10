""" Compiled: 2012-02-16 11:04:24 """

import acm

""" Implements default behavior """
class ObjectImportExportProcedure(object):
    """ Override this method for composite objects """
    def exportObject(self, o, file, messageGenerator):
        message = messageGenerator.Generate(o)
        try:
            file.write(message.AsString())
        except Exception as e:
            acm.Log("Could not export object: " + str(e))
            raise e

    """ Override this method for composite objects """
    def importObject(self, o, overwriteExistingObject):
        if self.__checkIfMemberObjectIsDuplicate(o):
            if overwriteExistingObject:
                self.__overwriteMember(o)
            else:
                acm.Log("Found duplicate member object of type '%s' - did not import."%str(o.Class().Name()))
        else:
            self.__saveImportedObject(o)

    """ If an import should not proceed in case referenced objects are missing in the ADS, override this function. """
    def checkForMissingReferences(self, object):
        return False

    def __checkIfMemberObjectIsDuplicate(self, memberObject):
        isDuplicate = False
        objectClass = memberObject.Class()
        queryResult = None
        queryResult = objectClass.Select("name = '%s' and oid > 0"%self.safeObjectName(memberObject))
        if queryResult and queryResult.Size() > 0:
            if next((dup for dup in queryResult if dup.Oid() > 0), None):
                isDuplicate = True
        return isDuplicate

    def __overwriteMember(self, importedMember):
        adsQueryMembers = importedMember.Class().Select("name = '%s' and oid > 0"%self.safeObjectName(importedMember))
        adsMember = adsQueryMembers.Size() and adsQueryMembers.First() or None
        if adsMember:
            adsMember.Apply(importedMember)
            adsMember.Commit()

    def __saveImportedObject(self, o):
        o.Commit()
        if o.IsKindOf(acm.FStoredASQLQuery):
            """ Delete left-over infant entities that otherwise show in the GUI """
            if o.Oid() < 0:
                try:
                    o.Delete()
                except:
                    pass
    
    @staticmethod
    def safeObjectName(o):
        safeName = None
        if o and o.Name():
            safeName = o.Name().replace('"', '\\"').replace("'", "\\'")
        return safeName

class BookProcedure(ObjectImportExportProcedure):
    def exportObject(self, o, file, messageGenerator):
        pass
    
    def importObject(self, o, overwriteExistingObject):
        pass
