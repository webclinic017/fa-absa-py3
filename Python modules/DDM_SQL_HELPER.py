'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_SQL_HELPER
PROJECT                 :       Pegasus - Data Distribution Model (DDM)
PURPOSE                 :       Helper module for persistence to the DDM SQL database
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
import pyodbc
import DDM_ATS_PARAMS as params

#Globals
sqlConnection = None

def getSQLConnection():
    global sqlConnection
    if not sqlConnection:
        try:
            #Setup the SQL connection
            #constr = 'DSN=%s;UID=DDMATSUser;PWD=Barcap@123' % params.DSNName
            #constr = "DSN=DDMPEGASUS;UID=DDMATSUser;PWD=Barcap@123" 
            constr='DRIVER={SQL Server};SERVER=%s;DATABASE=%s' % (params.SQLServer, params.DatabaseName)
            sqlConnection = pyodbc.connect(constr)
        except Exception as error:
            raise Exception('SQL connection failed. %s' % str(error))
    if not sqlConnection:
        raise Exception('SQL connection not initialised.')    
    
    return sqlConnection
            
        
def callStoredProc(procName, *args):
    try:
        sqlConnection = getSQLConnection()
        sql = "%s %s" % (procName, ','.join(['?'] * len(args)))
        sqlConnection.execute(sql, args)
        sqlConnection.commit()
    except Exception as error:
        raise Exception('callStoredProc failed with error - %s' % str(error))
            
def callStoredProcMany(procName, params):
    try:
        sqlConnection = getSQLConnection()
        cursor = sqlConnection.cursor()
        args = params[0]
        sql = "%s %s" % (procName, ','.join(['?'] * len(args)))
        cursor.executemany(sql, params)
        sqlConnection.commit()
    except Exception as error:
        raise Exception('callStoredProc failed with error - %s' % str(error))
            
            
def callStoredProcWithCursor(procName, *args):
    try:
        sqlConnection = getSQLConnection()
        cursor = sqlConnection.cursor()
        sql = "%s %s" % (procName, ','.join(['?'] * len(args)))
        cursor.execute(sql, args)
        return cursor
    except Exception as error:
        raise Exception('callStoredProcWithCursor failed with error - %s' % str(error))

def insertBatchRequestTrades(trades):
    try:
        sqlConnection = getSQLConnection()
        cursor = sqlConnection.cursor()
        sql = "%s %s" % ('DDMInsertRequestTrade', ','.join(['?'] * 14))
        cursor.executemany(procName, params)
        return cursor
    except Exception as error:
        raise Exception('callStoredProcWithCursorForMany failed with error - %s' % str(error))


def commit():
    try:
        sqlConnection = getSQLConnection()
        sqlConnection.commit()
    except Exception as error:
        raise Exception('commit failed with error - %s' % str(error))

def rollback():
    try:
        sqlConnection = getSQLConnection()
        sqlConnection.rollback()
    except Exception as error:
        raise Exception('rollback failed with error - %s' % str(error))

'''
cursor = callStoredProcWithCursor('DDMGetProductMappingsByTradeDomain','Frontarena')
rows = cursor.fetchall()
for row in rows:
   print row
'''
