
'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DATA_SEN_REPOSITORY
PROJECT                 :       Front Cache
PURPOSE                 :       This repository for settlement database operations
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       BBD
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
from FC_DATA_BASE_REPOSITORY import FC_DATA_BASE_REPOSITORY as fcDataBaseRepository
import pyodbc
from FC_UTILS import FC_UTILS as UTILS
#import FC_ENUMERATIONS
import acm

class FC_DATA_SEN_REPOSITORY(fcDataBaseRepository):
    def __init__(self, dbProvider):
        fcDataBaseRepository.__init__(self, dbProvider)      
    
    def create(self, requestId, reportDate, objectIndex, object):         
        createSql = UTILS.Constants.fcGenericConstants.FRONTCACHE_CREATE_SENSITIVITY_ENTITY
        params=self.createSqlParams(requestId, reportDate, objectIndex, object) 
        result = self.dbProvider.execute(createSql, params)
        return result[0]

    def createSqlParams(self, requestId, reportDate, objectIndex, object):
        #Values needed for StoredProcedure, in order
        #ReportDate
        #RequestId
        #ScopeType
        #ScopeName
        #InstrumentType
        #SensitivityData
        #dbCreateProcess
        if object.SensType==UTILS.Constants.fcGenericConstants.PORTFOLIO:
            ScopeType       = 2#FC_ENUMERATIONS.RequestType.PORTFOLIO_SENSITIVITIES
            ScopeName       = object.PortfolioName
            InstrumentType  = None
        else:
            ScopeType       = 1#FC_ENUMERATIONS.RequestType.INSTRUMENT_SENSITIVITIES
            ScopeName       = object.InstrumentName
            InstrumentType  = str(acm.FInstrument[object.InstrumentNumber].InsType()) #ael.enum_from_string('InsType', str(instrument.InsType()))
            #FC_ENUMERATIONS.InstrumentType.fromstring(object.InstrumentType) Instrument Type in FA have '/' and space in names

        SensitivityData = pyodbc.Binary(object._serializedData)
        dbCreateProcess = self.DBCreateProcess
        
        sqlParams =[reportDate,
                    requestId,
                    ScopeType,
                    ScopeName,
                    InstrumentType,
                    SensitivityData,
                    dbCreateProcess]
        return sqlParams
