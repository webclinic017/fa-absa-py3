""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/scripts/accountingtransporter/FAccountingBackup.py"
import acm
import urllib
import zipfile
import time
import FAccountingTransporter
from FBDPCurrentContext import Logme

class AccountingBackup:

    def __init__(self, fileNames, filePath):
        self.__fileNames = fileNames
        self.__filePath = filePath
        self.__entities = list()

    def GetEntityNames(self, fileExtensionKey):
        entityNames = list()
        fileExtension  = '.' + FAccountingTransporter.fileExtensionMap[fileExtensionKey]
        for fileName in self.__fileNames:
            endIndex = fileName.rfind(fileExtension)
            entityName = fileName[0:endIndex]
            entityNames.append(entityName)
        return entityNames

    def SetEntities(self, entityNames, entityType):
        for entityName in entityNames:
            entity = entityType[entityName]
            if None != entity:
                self.__entities.append(entity)

    def GetZipFile(self, entity, fileExtensionKey):
        timestr = time.strftime("%Y%m%d-%H%M%S")
        filename = "%s.%s" % (self.__filePath + "\\" + urllib.quote(entity.Name(), ' @.') + "_BACKUP_" + timestr, FAccountingTransporter.fileExtensionMap[fileExtensionKey])
        return zipfile.ZipFile(filename, "w", zipfile.ZIP_DEFLATED)

    def GetEntities(self):
        return self.__entities

    def ExportEntities(self):
        pass

    def BackupLogStart(self, entity):
        Logme()('Performing backup on %s %s' % (entity.ClassName(), entity.Name()))

    def BackupLogEnd(self, entity):
        Logme()('Backup on %s %s complete' % (entity.ClassName(), entity.Name()))


class BookBackup(AccountingBackup):

    def __init__(self, bookFileNames, filePath):
        AccountingBackup.__init__(self, bookFileNames, filePath)

    def __GetBookNames(self):
        return self.GetEntityNames(FAccountingTransporter.FileExtensionMapKey.KEY_BOOK)

    def __SetBooks(self):
        bookNames = self.__GetBookNames()
        self.SetEntities(bookNames, acm.FBook)

    def __ExportBooks(self):
        for book in self.GetEntities():
            self.BackupLogStart(book)
            zipFile = self.GetZipFile(book, FAccountingTransporter.FileExtensionMapKey.KEY_BOOK)
            FAccountingTransporter.ExportBooks(zipFile, [book])
            zipFile.close()
            self.BackupLogEnd(book)

    def ExportEntities(self):
        self.__SetBooks()
        self.__ExportBooks()
