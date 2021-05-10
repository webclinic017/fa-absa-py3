
import os
import acm

class SpanFileParser(object):
    def __init__(self, paramSource):
        self.fileDir = paramSource.replace('\n', '')
        self.dataTypesPerField = \
        {
         'INSID' : int, 'SHORT OPTION CHARGE' : float, 'EXPIRY YEAR': int, 'EXPIRY MONTH' : int,
         'DELTA SCALING FACTOR' : float, 'DELTA' : float, 'STRIKE' : int, 'PRICE RANGE' : float, 'VOLATILITY RANGE' : float,
         'RISK ARRAY 1' : float, 'RISK ARRAY 2' : float, 'RISK ARRAY 3' : float, 'RISK ARRAY 4' : float, 'RISK ARRAY 5' : float,
         'RISK ARRAY 6' : float, 'RISK ARRAY 7' : float, 'RISK ARRAY 8' : float, 'RISK ARRAY 9' : float, 'RISK ARRAY 10' : float,
         'RISK ARRAY 11' : float, 'RISK ARRAY 12' : float, 'RISK ARRAY 13' : float, 'RISK ARRAY 14' : float, 'RISK ARRAY 15' : float,
         'RISK ARRAY 16' : float, 'DELTA PER SPREAD RATIO 1' : float, 'DELTA PER SPREAD RATIO 2' : float, 'PRIORITY' : int, 
         'CREDIT' : float, 'DELTA RATIO 1' : float, 'TIER 1' : int, 'DELTA RATIO 2' : float, 'TIER 2' : int, 'CHARGE RATE' : float, 
         'SPOT MONTH' : int, 'SPOT YEAR' : int, 'OUTRIGHT CHARGE' : float, 'SPREAD CHARGE' : float, 'TIER' : int, 'START MONTH' : int, 
         'START YEAR' : int, 'END MONTH' : int, 'END YEAR' : int
        }
    
    def checkDataType(self, columnValues, header):
        for i in range(len(columnValues)):
            columnType = self.dataTypesPerField.get(header[i], str)
            if not isinstance(columnType(columnValues[i]), columnType):
                raise RuntimeError('Incorrect data type in column %i (%s), must be data of %s but is %s' % ( i + 1, columnValues[i], repr(columnType), type(columnValues[i])))

    def parse(self, folderName):
        data = []
        files = []
        
        try:
            files = os.listdir(self.fileDir + '/' + folderName)
        except WindowsError:
            acm.Log('Folder %s missing, could not retrieve parameters' % folderName)
        files.sort()

        for fileName in files:
            fileData = []
            fileSource = open(self.fileDir + '/' + folderName + '/' + fileName)
            header = fileSource.readline().replace('\n', '').split(';') # header is only used for type checking
            for line in fileSource.readlines():
                columns = line.replace('\n', '').split(';')
                if len(columns) != len(header):
                    acm.Log('Incorrect number of column on row "%s" in file %s, row ignored' % (line.replace('\n', ''), fileName))
                    continue
                try:
                    self.checkDataType(columns, header)
                except RuntimeError as msg:
                    acm.Log('File %s: %s, row ignored' % (fileName, msg))
                    continue
                fileData.append([i for i in line.replace('\n', '').split(';')])
            fileSource.close()
            data.append(fileData)
        return data
