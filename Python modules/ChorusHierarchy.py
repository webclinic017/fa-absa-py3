
"""-----------------------------------------------------------------------------------------------------------------------------------------------

HISTORY
==================================================================================================================================================
Date                Change no Developer                 Description
--------------------------------------------------------------------------------------------------------------------------------------------------
                    Faize Adams                         Pulled the chorus hierarchy data from the RDS Hierarchy control
                                                        service into Front Arena ( https://confluence.barcapint.com/
                                                        display/AbCapRTB/RDS+-+Hierarchy+Control+Service )

2017-08-14           Sihle Gaxa                         Added the regulatory classification to chorus hierarchy data pulled into Front
--------------------------------------------------------------------------------------------------------------------------------------------------
"""
import time
import os
import json
import acm
import at_logging

LOGOUTPUT = True
LOGGER = at_logging.getLogger()


def log(message):
    if LOGOUTPUT:
        LOGGER.info(message)


class ChorusDelegate(object):
    """
    Class reads data from Front Arena Text Object table.
    The data is stored as JSON.
    This class read the chorus hierarchy from the text object table.
    When instantiating the class, a date can be passsed with format 'yyyy-mm-dd'
    to use historical chorus data."""
   
    TEXTOBJECTNAME = "chorusHierarchyData"
    HISTORYOBJECTNAME = 'chorusHistory'
    DATA = {}

    def __init__(self, date='TODAY'):
        log('Reading chorus data stored in Front Arena Text Object : "chorusHierarchyData"')
        try:
            objectToLoad = self.TEXTOBJECTNAME
            if date != 'TODAY':
                objectToUse = None
                epochDate = time.mktime(time.strptime(date, "%Y-%m-%d"))
                historyObjects = acm.FCustomTextObject.Select("name like %s*" % self.HISTORYOBJECTNAME)
                
                log('Loading historical chorus data for date %s' % epochDate)
                if historyObjects:
                    candidates = [text for text in historyObjects if text.CreateTime() <= epochDate]
                    for historyObj in historyObjects:
                        log('Historical chorus data from Front Arena Text Objects : %s ' %(historyObj.Name()))
                    if candidates:
                        objectToUse = max(candidates, key=lambda item: item.CreateTime())
                        for textObj in candidates:
                            log('Historical chorus text objects found, created before : %s are :%s ' %(date, textObj.Name()))
                    else:
                        log('Error retrieving chorus historical data created on or before date : %s' %(date))
                else:
                    log('No chorus data with name like %s found in FA for date %s' %(self.HISTORYOBJECTNAME, date))
                    
                if objectToUse:
                    objectToLoad = objectToUse.Name()
                    log("Loaded '%s' from FA database for date %s" % (objectToLoad.Name(), date))
                else:
                    log("Chorus data for date %s not found. Loading most recent data : %s" % (date, objectToLoad))
            textObject = acm.FCustomTextObject[objectToLoad]
            log('Loading text object %s' %(textObject.Name()))
            self.DATA = json.loads(textObject.Text())
            log('Latest historical data for date: %s is : %s' %(date, self.DATA))

        except Exception, e:
            log('Could not load data from FA database: %s' % str(e))

    def __str__(self):
        """Prints the data nicely."""
        return self.DATA

    def isValid(self, obj):
        obj_id = None
        if obj is None:
            return None
        if type(obj) is str:
            obj_id = obj
        elif type(obj) is int:
            obj_id = "%d" % obj
        elif obj.IsKindOf(acm.FPortfolio):
            obj_id = "%d" % obj.Oid()

        if obj_id is not None:
            if (obj_id in self.DATA.keys()):
                return obj_id
            else:
                return None
        else:
            return None

    def getData(self, bookID, field):
        log('Getting %s chorus data' %(field))
        obj_id = self.isValid(bookID)
        if obj_id is not None:
            log('Getting %s for portfolio %s' %(field, obj_id))
            return str(self.DATA[obj_id].get(field, None))
        else:
            log('Invalid portfolio id %s, Portfolio Number cannot be found in Front Arena' %(obj_id))
            return None

    def getAllData(self):
        log('Getting all stored chorus data, \n'
            '%s' %(self.DATA))
        return self.DATA

    def applyFilter(self, field, value):
        """Filters portfolios based on 'accountingTreatment', 'masterBook',
        'minorDesk', 'desk','subproduct' or bankingTrading. Returns a dictionary of portfolio
        numbers based on filtered field."""
        log('Getting all portfolios where %s is equal to %s' %(field, value))
        filteredDict = dict((k, v) for k, v in self.DATA.iteritems() if v.get(field, None) == value)
        log(filteredDict)
        return filteredDict

    def getMasterbook(self, book):
        chorusFieldName = "masterBook"
        return self.getData(book, chorusFieldName)

    def getMinordesk(self, book):
        chorusFieldName = "minorDesk"
        return self.getData(book, chorusFieldName)

    def getDesk(self, book):
        chorusFieldName = "desk"
        return self.getData(book, chorusFieldName)

    def getSubproduct(self, book):
        chorusFieldName = "subproduct"
        return self.getData(book, chorusFieldName)

    def getAccountingTreatment(self, book):
        chorusFieldName = "accountingTreatment"
        return self.getData(book, chorusFieldName)
        
    def getBankingTrading(self, book):
        chorusFieldName = "bankingTrading"
        return self.getData(book, chorusFieldName)

class ChorusStreamDelegate(object):
    """
    Class reads data from chorus server directly.
    This class is used to connect to the hierarchy control service directly.
    Might return nulls if it is unable to connect to remote server."""
    SOURCESYSTEM = "Frontarena"
    CHORUSFILE = "chorusHierarchyLibrary"
    DEFAULTLIBPATH = "S:\\Chorus\\chorusHierarchy\\"
    ERROR = None
    NOERROR = 5
    ADD = 1
    DELETE = 2
    CHECK = 3
    GET = 4
    HISTORY = {}

    def __str__(self):
        return self.HISTORY

    def __init__(self, newLibPath=None):
        import clr
        import System
        import sys
        
        log('Connecting directly from RDS Chorus Service')
        pathToLib = self.DEFAULTLIBPATH
        if newLibPath:
            log("Using custom path for chorusHierarchyLibrary.dll: \"%s\"" % newLibPath)
            pathToLib = newLibPath
        else:
            log('Invalid path to library, path to chorus library cannot be %s' % newLibPath)
        configDll = self.CHORUSFILE + ".dll.config"
        configFile = os.path.join(pathToLib, configDll)
        log('Configuration file: %s' %(configFile))
        try:
            if pathToLib not in sys.path:
                log('Adding new library path %s to the system path %s' %(pathToLib, sys.path))
                sys.path.append(pathToLib)
            log('Adding mscorlib reference') 
            clr.AddReference("mscorlib")
            log('Adding %s to References' %(self.CHORUSFILE)) 
            clr.AddReference(self.CHORUSFILE)
            
            global chorusHierarchyLibrary
            import chorusHierarchyLibrary
			
            log('Setting System App Domain app config file to %s' %(configFile))
            System.AppDomain.CurrentDomain.SetData("APP_CONFIG_FILE", configFile)
            log('Succesfully imported chorusHierarchyLibrary')
        except Exception, e:
            log('Unable to load \"chorusHierarchyLibrary.dll\" and \"chorusHierarchyLibrary.dll.config\" from %s.' % (pathToLib))
            log('Exception: %s' % str(e))

    def isValid(self, obj, field=''):
        obj_id = None
        if obj is None:
            return False, self.ERROR

        if type(obj) is str:
            obj_id = obj
        elif type(obj) is int:
            obj_id = "%d" % obj
        elif obj.IsKindOf(acm.FPortfolio):
            obj_id = "%d" % obj.Oid()

        if obj_id is not None:
            if (obj_id in self.HISTORY.keys()) and (field in self.HISTORY[obj_id].keys()):
                return True, obj_id
            else:
                return False, obj_id
        else:
            return False, self.ERROR

    def history(self, obj_id, action, fieldName='', fieldData=''):
        """Cache portfolio data for the current session.
        Once the data has been retrieved from the hierarchy control service
        for a specific portfolio, we cache the data so that subsequent request
        for the same portfolio is faster."""
        log('Caching portfolio data for the current session')
        try:
            if action == self.GET:
                return self.HISTORY[obj_id][fieldName]
            elif action == self.ADD:
                if obj_id not in self.HISTORY.keys():
                    self.HISTORY[obj_id] = {fieldName: fieldData}
                else:
                    details = self.HISTORY[obj_id]
                    details[fieldName] = fieldData
                    self.HISTORY[obj_id] = details
            elif action == self.DELETE:
                if obj_id in self.HISTORY.keys():
                    del self.HISTORY[obj_id]
            elif action == self.CHECK:
                if obj_id in self.HISTORY.keys():
                    bookHistory = self.HISTORY[obj_id]
                    if fieldName in bookHistory.keys():
                        return True
                    else:
                        return self.ERROR
                else:
                    return self.ERROR
        except:
            return self.ERROR

        return self.ERROR

    def getAllData(self, ports):
        log('Starting data retrieval process from chorus')
        func = chorusHierarchyLibrary.chorusHierarchy.getAllData
        cData = func(ports, self.SOURCESYSTEM)
        log('Source System %s' % self.SOURCESYSTEM)
        if cData:
            log('Connecting to RDS chorus hierarchy service')
            pyData = {}
            log ('Getting portfolio numbers from Chorus Hierarchy Service')
            for item in cData.GetEnumerator():
                pySubData = {}
                cSubData = item.Value
                if cSubData is not None:
                    for subItem in cSubData.GetEnumerator():
                        log('%s: %s' %(str(subItem.Key), str(subItem.Value)))
                        pySubData[str(subItem.Key)] = str(subItem.Value)
                        
                else:
                    log('Portfolio number %s could not be found in Chorus' %(cSubData))
                    
                pyData[str(item.Key)] = pySubData
            return pyData
        else:
            return None

    def getData(self, libFunc, book, chorusField):
        log('Checking if %s is in cached chorus data' %(book))
        inHistory, obj_id = self.isValid(book, chorusField)
        if obj_id:
            if inHistory:
                log('Getting cached chorus data for : %s for field : %s' %(book, chorusField))
                return self.history(obj_id, self.GET, chorusField)
            else:
                try:
                    
                    data = libFunc(obj_id, self.SOURCESYSTEM)
                    log('Adding : %s to cached chorus data with field : %s' %(book, chorusField))
                    log('Portfolio : %s for field : %s = %s' %(obj_id, data[obj_id][chorusField], chorusField))
                    self.history(obj_id, self.ADD, chorusField, data)
                    return data
                except Exception, e:
                    log(str(e))
                    return self.ERROR
        else:
            log('Invalid Id %s, Id must be of type string, int or portfolio' %(book))
            return self.ERROR

    def test(self, n):
        log('Running chorus test')
        return chorusHierarchyLibrary.chorusHierarchy.test(n)

    def getMasterbook(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getMasterBook
        chorusFieldName = "masterBook"
        log('Retrieving chorus data for %s for %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))

    def getMinordesk(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getMinordesk
        chorusFieldName = "minorDesk"
        log('Retrieving chorus data for %s at %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))
        

    def getDesk(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getDesk
        chorusFieldName = "desk"
        log('Retrieving chorus data for %s at %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))

    def getSubproduct(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getSubproduct
        chorusFieldName = "subproduct"
        log('Retrieving chorus data for %s at %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))

    def getAccountingTreatment(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getAccountingTreatment
        chorusFieldName = "accountingTreatment"
        log('Retrieving chorus data for %s at %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))
        
    def getBankingTrading(self, book):
        func = chorusHierarchyLibrary.chorusHierarchy.getBankingTrading
        chorusFieldName = "bankingTrading"
        log('Retrieving chorus data for %s at %s' %(book, chorusFieldName))

        return str(self.getData(func, book, chorusFieldName))

    def getSubHierarchy(self, book):
        log('Retrieving chorus sub-hierarchy for %s' %(book))
        func = chorusHierarchyLibrary.chorusHierarchy.getSubHierarchy
        chorusFieldName = "subhierarchy"
        cHierarchy = self.getData(func, book, chorusFieldName)
        if cHierarchy:
            pyHierarchy = {}
            for item in cHierarchy.GetEnumerator():
                pyHierarchy[str(item.Key)] = str(item.Value)
                log('chorus sub-hierarchy data for %s :' %(book))
                log('%s = %s' %(str(item.Key), str(item.Value)))
            return pyHierarchy
        else:
            log('Could not retrieve chorus sub-hierarchy data for %s'%(book))
            return None
