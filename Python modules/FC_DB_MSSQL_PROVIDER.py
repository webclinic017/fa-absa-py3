'''----------------------------------------------------------------------------------------------------------
MODULE                  :       FC_DB_MSSQL_PROVIDER
PROJECT                 :       Front Cache
PURPOSE                 :       Microsoft SQL server database provider
DEPARTMENT AND DESK     :       All Departments and all Desks.
REQUASTER               :       Front Cache
DEVELOPER               :       Heinrich Momberg
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------
'''
#pyodbc the data provider for MSSQL in python
import pyodbc as odbc
import os
from decimal import Decimal
from FC_UTILS import FC_UTILS as UTILS

class FC_DB_MSSQL_PROVIDER:
    sqlConnection = None

    def __init__(self, dataSource, initialCatalog):
        if os.name == 'nt':
            self.connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (dataSource, initialCatalog)
        else:
            self.connectionString = UTILS.Parameters.fcGenericParameters.UnixConnectionString
    
    def getSqlConnection(self):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                if not self.sqlConnection:
                    self.sqlConnection = odbc.connect(self.connectionString, autocommit=True)
                return self.sqlConnection
            except Exception, e:
                dbRetryCount = dbRetryCount + 1
                UTILS.Logger.flogger.warn(UTILS.Constants.fcFloggerConstants.COULD_NOT_GET_SQL_CONNECTION % (self.connectionString, dbRetryCount))
        raise Exception(UTILS.Constants.fcExceptionConstants.COULD_NOT_GET_THE_SQL_CONNECTION_S % (self.connectionString, str(e)))

    def executeNoReturn(self, par_sql, params):
        dbRetryCount = 0
        commitSuccessful = False
        while (not commitSuccessful) and dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                cursor.execute(sql, params)
                commitSuccessful = True
                #conn.commit()
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
                UTILS.Logger.flogger.warn("executeNoReturn failed. Retry atempt number: %i." % dbRetryCount)
        if not commitSuccessful:
            raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_NO_RETURN_FAILED_S % str(error))
            
    def execute(self, par_sql, params):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                result = cursor.execute(sql, params).fetchall()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_FAILED_S % str(error))

    def executeNoParams(self, par_sql):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                result = cursor.execute(sql).fetchall()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount += 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_FAILED_S % str(error))

    def executeNoParamsScalar(self, par_sql):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                result = cursor.execute(sql).fetchone()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount += 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_FAILED_S % str(error))

    def executeNoParamsNoReturn(self, par_sql):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                result = cursor.execute(sql)
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_FAILED_S % str(error))
    
    def executeScalar(self, par_sql, params):
        #print params
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = par_sql
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                result = cursor.execute(sql, params).fetchone()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_SCALAR_FAILED % str(error))


    def SQLEsc(self, s):
        if type(s) == int:
            return s
        elif type(s) == Decimal:
            return s
        elif s == None:
            return "NULL"
        elif str(s) == '':
            return "NULL"
        else:
            string = str(s)
            return "'"+ string.replace("'", "''")+"'"
            
    def BuildSqlString(self, tradeListItem):
        return_str = ''
        for itm in tradeListItem:
            return_str += str(self.SQLEsc(itm)) + ","
        return return_str[:-1]

    def executeTvp(self, sqlParam, params, controlMeasureResults):
        #print params
        dbRetryCount = 0

        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                
                sql_a = "DECLARE @TradeTVP As FrontCache.TradeTVP;"
                sql_b = ''
                for item in params:                    
                     sql_b += "INSERT INTO @TradeTVP VALUES (" + str(self.BuildSqlString(item)) + ");"

                sql_c = "DECLARE @ControlMeasureTVP As FrontCache.ControlMeasureTVP;"
                sql_d = ''
                if controlMeasureResults is not None:
                    for item in controlMeasureResults:
                         sql_d += "INSERT INTO @ControlMeasureTVP VALUES (" + str(self.BuildSqlString(item)) + ");"

                sql = sql_a + sql_b + sql_c + sql_d + "exec " + sqlParam + " @TradeTVP, @ControlMeasureTVP"
                
                result = cursor.execute(sql)
                #conn.commit()
                return result
            except Exception, error:
                UTILS.Logger.flogger.warn("TVP insert failed. Retry atempt number: %i. Reason:" % (dbRetryCount, str(error)))
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception('executeTvp failed %s' % str(error))        

    def executeScalarCustom(self, requestId, processedCount, errorCount, requestCollectionTrackerId, batchId,
                            errorTradeNumbers):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                #sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                result = cursor.execute("FrontCache.UpdateBatchRequestEnd ?, ?, ?, ?, ?, ?", requestId,
                                        processedCount, errorCount, requestCollectionTrackerId, batchId,
                                        errorTradeNumbers).fetchone()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_SCALAR_FAILED % str(error))

    def executeScalarFunction(self, sql, params):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = "SELECT %s(%s)" % (sql, ','.join(['?'] * len(params)))
                result = cursor.execute(sql, params).fetchone()
                #conn.commit()
                return result
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_SCALAR_FAILED % str(error))         
            
    def executeMany(self, sql, params):
        dbRetryCount = 0
        commitSuccessful = False
        while (not commitSuccessful) and dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                args = params[0]
                sql = "%s %s" % (sql, ','.join(['?'] * len(args)))
                cursor.executemany(sql, params)
                commitSuccessful = True
                #conn.commit()
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
                UTILS.Logger.flogger.warn("execute many failed. Retry atempt number: %i." % dbRetryCount)
        if not commitSuccessful:
            raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_MANY_FAILED % str(error))
            
    def executeNoReturnInTransaction(self, sql, params):
        dbRetryCount = 0
        commitSuccessful = False
        while (not commitSuccessful) and dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                cursor=None
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                cursor.execute(sql, params)
                commitSuccessful = True
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
                UTILS.Logger.flogger.warn("executeNoReturnInTransaction failed. Retry atempt number: %i." % dbRetryCount)
        if not commitSuccessful:
            raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_NO_RETURN_IN_TX_FAILED_S % str(error))
                            
    def executeInTransaction(self, sql, params):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                return cursor.execute(sql, params).fetchall()
            except Exception, error:
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_IN_TX_FAILED_S % str(error))
    
    def executeScalarInTransaction(self, sql, params):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                sql = "%s %s" % (sql, ','.join(['?'] * len(params)))
                return cursor.execute(sql, params).fetchone()
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_IN_TX_FAILED_S % str(error))
            
    def executeManyInTransaction(self, sql, params):
        dbRetryCount = 0
        while dbRetryCount < UTILS.Parameters.fcGenericParameters.DataBaseRetryThreshold:
            try:
                conn = self.getSqlConnection()
                cursor = conn.cursor()
                args = params[0]
                sql = "%s %s" % (sql, ','.join(['?'] * len(args)))
                return cursor.executemany(sql, params)
            except Exception, error:
                if cursor:
                    cursor.close()
                dbRetryCount = dbRetryCount + 1
        raise Exception(UTILS.Constants.fcExceptionConstants.EXECUTE_MANY_IN_TX_FAILED_S % str(error))
            
    def commit(self):
        try:
            conn = self.getSqlConnection()
            conn.commit()
        except Exception, error:
            raise Exception(UTILS.Constants.fcExceptionConstants.COMMIT_FAILED_S % str(error))

    def rollback(self):
        try:
            conn = self.getSqlConnection()
            conn.rollback()
        except Exception, error:
            raise Exception(UTILS.Constants.fcExceptionConstants.ROLLBACK_FAILED_S % str(error))

#Simple test
#print 'here we go'
#dataSource='JHBDSM05094\JF1_MAIN3_DEV'
#initialCatalog='MMG-DDM-PEGASUS'
#sqlProvider = FC_DB_MSSQL_PROVIDER(dataSource,initialCatalog)
#conn = sqlProvider.getSqlConnection()
#print sqlProvider.connectionString

#trying pyodbc
#3000+ inserts per second!!!
#dataSource='JHBDSM05094\JF1_MAIN3_DEV'
#initialCatalog='MMG-DDM-PEGASUS'
#connectionString = 'DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (dataSource, initialCatalog)
#conn = odbc.connect(connectionString)

#row = ['abc ']

#Many Rows
#rows=[]
#for i in range(10000):
    #rows.append(['abc %s' % str(i)])
#cursor = conn.cursor()
#result = cursor.executemany('FrontCache.InsertSampleTable ?', rows)
#conn.commit()


#One row
#cursor = conn.cursor()
#result = cursor.execute('FrontCache.InsertSampleTable ?', row).fetchone()[0]
#conn.commit()
#print result
#print cursor[0]

#print cursor.fetchone()
