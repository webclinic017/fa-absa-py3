"""-----------------------------------------------------------------------
MODULE
    PS_RepoBonds_RepoRates


DESCRIPTION
    Date                : 2013-05-17  
    Purpose             : Reads csv with repo rates and config and provides this info
    Department and Desk : Prime Services Desk
    Requester           : Francois Henrion & Kelly Hattingh
    Developer           : Peter Fabian
    CR Number           : CHNG0001033361
    
NOTES
    
    
HISTORY
================================================================================
Date       Change no    Developer          Description
--------------------------------------------------------------------------------
2013-05-21 C1056001     Peter Fabian       Adjustable price for BSB booking (YMtM column)
2013-07-26 C1197225     Peter Fabian       Added support for csv file for PrimeServices BSBack
ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import csv
from collections import namedtuple

INS_REPORATE_FIELD_NAMES = [
               'insid',
               'bid',
               'offer',
               'repo_to',
               'YMtM'
               ]

InsRepoRate = namedtuple("InsRepoRate", INS_REPORATE_FIELD_NAMES)

class InsRepoRatesReader(object):
    """
        This class is used as an abstraction above the simple csv config file for
        instruments' repo rates and is used for booking BSBacks between PS desk and credit desk.
        
        The structure of the csv is described in INS_REPORATE_FIELD_NAMES and is 
        checked when reading the csv file.
        
        The csv file allows the user to specify bid/offer repo rates for each instrument. Moreover, 
        the user can specify portfolio where the second leg of the mirror will be booked as well as
        the start price for the BSBack.
    """
    def __init__(self, fileName):
        self.fileName = fileName
        self.fieldNames = INS_REPORATE_FIELD_NAMES
        self.repoRates = {}

    def _readRates(self, force=False):
        """ Read the repo config from the csv file to internal 
            data structures
        """
        if force or not self.repoRates:
            with open(self.fileName, 'rb') as repoRatesFile:
                dictReader = csv.DictReader(repoRatesFile)
                # check if csv file has correct header
                if set(dictReader.fieldnames) != set(INS_REPORATE_FIELD_NAMES):
                    raise RuntimeError("File %s does not contain correct data!\
                        Expecting header with following fields: %s "
                        % (self.fileName, INS_REPORATE_FIELD_NAMES))
                # if the file has correct header, read its data
                for repoRateForIns in dictReader:
                    self.repoRates[repoRateForIns['insid']] = InsRepoRate(**repoRateForIns)

    def repoRateForIns(self, instrumentId):
        """ Returns InsRepoRate object for the specified instrument
            if it is present in the input csv file.
        """
        self._readRates()

        if instrumentId in self.repoRates:
            return self.repoRates[instrumentId]
        else:
            return None

class ClientRepoRate(object):
    """ Class to represent client specific information about 
        underlying instrument for BSBack -- bid, offer rates,
        portfolio where the instrument is booked, start price 
        for the BSBack trade and client's repo frequency for 
        this particular instrument.
    """
    def __init__(self, clientId, index):
        self.clientId = clientId
        self.repoRates = {}
        self.repoFreq = {}
        # column/position in the file where the client info starts 
        self.index = index
    
    def addRepoRate(self, insid, bid, offer, repo_to, YMtM, repoFreq):
        """ Adds client specific configuration and repo rate for the specified
            instrument
        """
        self.repoRates[insid] = InsRepoRate(insid, bid, offer, repo_to, YMtM)
        self.repoFreq[insid] = repoFreq
    
    def repoRate(self, insid):
        return self.repoRates[insid] if insid in self.repoRates else None
    
    def repoFrequency(self, insid):
        return self.repoFreq[insid] if insid in self.repoFreq else None


class CsvStruct(object):
    """ Class to verify the structure of the csv file for Prime Services
        repos. Also provides some basic info about file's structure.
    """
    def __init__(self, header, fileName):
        self.header = header
        self.fileName = fileName
        self.columnIndexCache = {}
    
    def _createIndexCache(self):
        """ We create an index cache so we would know which column represents which data.
            This is not very useful for repeating bid/offer/freq columns, but can be used
            for the rest of the columns.
        """
        for i, columnName in enumerate(self.header):
            self.columnIndexCache[columnName.lower()] = i
    
    def indexOfColumn(self, column):
        """ Returns index of last occurence of the specified column in the header 
            of the csv file.
        """
        if not self.columnIndexCache:
            self._createIndexCache()
        
        if column.lower() not in self.columnIndexCache:
            raise ValueError("No column with id '%s' in file '%s'" % (column, self.fileName))
        else:
            return self.columnIndexCache[column.lower()]
            
    def validateFile(self, clients):
        """ Validates CSV files using a couple of simple structural checks. 
        """
        errors = []
        
        # number of clients == no of bid, offer, freq columns
        header = [x.lower() for x in self.header]
        
        columnsForEachClient = ["bid", "offer", "freq"]
        for colName in columnsForEachClient:
            if len(clients) != header.count(colName):
                errors.append("Detected number of clients is different from the number of '%s' columns in the input file %s"
                            % (colName, self.fileName))
        
        
        # plus there are insid, repo_to and ymtm columns present in the file
        for columnName in ['insid', 'repo_to', 'ymtm']:
            if columnName not in header:
                errors.append("Column '%s' missing from the input file %s"
                              % (columnName, self.fileName))
                
        # validate client ids
        for clientId in clients:
            if not acm.FParty[clientId]:
                errors.append("Client '%s' not found in Front Arena"
                              % (clientId))
        
        if errors:
            raise RuntimeError("\n".join(errors))
    

class ClientRepoRatesReader(object):
    """ Provides access to all the information read from the input csv file for
        Prime Services repo booking. 
    """
    def __init__(self, fileName):
        self.fileName = fileName
        self.clientRepoRates = {}
    
    def _getClientNames(self, clients):
        """ Returns a list of client names in the same order as they are listed in 
            the input csv file
        """
        # save indices for clients and create a list of clients
        idxForClient = {}
        clientIds = []
        for i, clientName in enumerate(clients.rstrip().split(',')):
            if clientName:
                idxForClient[clientName] = i
                clientIds.append(clientName)

        # create objects for each client to hold the info about the rates and frequencies
        for clientId in clientIds:
            self.clientRepoRates[clientId] = ClientRepoRate(clientId, idxForClient[clientId])
        return clientIds
    
    
    def _readRates(self, force=False):
        """ Reads the input csv file and stores the info from the file in 
            internal data structures
        """
        if force or not self.clientRepoRates:
            with open(self.fileName, 'r') as repoRatesFile:
                # first line should contain client names -- create object for each client
                clientIds = self._getClientNames(repoRatesFile.readline())
                
                # then create a csv reader object and validate input file 
                csvReader = csv.reader(repoRatesFile)
                header = next(csvReader)
                csvStruct = CsvStruct(header, self.fileName)
                csvStruct.validateFile(self.clientRepoRates.keys())
            
                # process the file
                for dataLine in csvReader:
                    insId = dataLine[csvStruct.indexOfColumn('insid')]
                    repoPrf = dataLine[csvStruct.indexOfColumn('repo_to')]
                    startPrice = dataLine[csvStruct.indexOfColumn('ymtm')]
                    
                    # here the order is important, otherwise we would mix up the rates
                    for clientNo, clientId in enumerate(clientIds):
                        clientRepoRate = self.clientRepoRates[clientId]
                        # where the config for this client begins
                        firstColForClient = clientRepoRate.index
                        bidIdx = firstColForClient
                        offerIdx = firstColForClient + 1
                        freqIdx = firstColForClient + 2
                        # create the object from one line in the repo rate file
                        clientRepoRate.addRepoRate(insId, dataLine[bidIdx], dataLine[offerIdx], repoPrf, startPrice, dataLine[freqIdx])


    def getRate(self, instrumentId, clientId):
        self._readRates()

        if clientId in self.clientRepoRates:
            return self.clientRepoRates[clientId].repoRate(instrumentId)
        else:
            return None

    def getFrequency(self, instrumentId, clientId):
        self._readRates()

        if clientId in self.clientRepoRates:
            return self.clientRepoRates[clientId].repoFrequency(instrumentId)
        else:
            return None


