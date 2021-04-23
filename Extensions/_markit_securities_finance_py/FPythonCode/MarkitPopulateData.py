""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/MarkitPopulateData.py"
from __future__ import print_function
import acm
import os
import glob
import zipfile
import datetime
import json
import shutil
import FMarkitPerform

from MarkitDownloadData import LoadFromFile
import FSecLendUtils
from FSecLendMarkitData import ascii_encode_dict
from FSecLendRecordLookup import FInstrumentLookup
from FParameterSettings import ParameterSettingsCreator

def perform(log,dictionary):      
        
    filedir = dictionary['filedir'].SelectedDirectory().Text()
    filename = dictionary['filename']
    os.chdir(filedir)

    # Remove old processed files
    fileList = glob.glob('*tsv')
    for file in fileList:
        os.remove(file)
  
    # Extract new files
    fileList = glob.glob(filename)
    for file in fileList:
        with zipfile.ZipFile(file,'r') as h:
            h.extractall(filedir)

    # Process new files
    fileList = glob.glob('*tsv')
    
    markitUpload = _MarkitUpload(log)
    
    markitUpload._perform(dictionary,fileList)

    log.listTopWarningMessages()
    log.listTopErrorMessages()


class _MarkitUploadBase(FMarkitPerform.FBDPPerform):
    """
    """

    def __init__(self, log):
        FMarkitPerform.FBDPPerform.__init__(self, log)

    def _end(self):
        """
        """
        FMarkitPerform.FBDPPerform._end(self)        


class _MarkitUpload(_MarkitUploadBase):

    def __init__(self,log):
        _MarkitUploadBase.__init__(self, log)
        self.MARKITSETTINGS = ParameterSettingsCreator.FromRootParameter('MarkitSettings')
        self.Market = acm.FParty[self.MARKITSETTINGS.Market()]
        self.Cusip = self.MARKITSETTINGS.Cusip()
        self.Isin = self.MARKITSETTINGS.Isin()
        self.Sedol = self.MARKITSETTINGS.Sedol()
        self.MarkitRates = ['VWAF 1 Day','VWAF 3 Day','VWAF 7 Day','VWAF 30 Day','VWAF All', 'Tradable Fee']
        self.updatedUnderlyings = {}
        self.instrumentsThatHaveSedols = GetAllInstrumentsThatHaveSedols()
        self.markitMasterTextObject_dictionary = {}
        self.updatedSecurityLoans = {}
        
    def end(self):
        _MarkitUploadBase._end(self)
        
    def FindIdentifyingSecurity(self,identifier,instrumentLookup,markitData_subdictionary): 
        identifierValue = markitData_subdictionary[identifier]
        if identifierValue:
            if identifier == 'SEDOL':
                    ins = instrumentLookup([identifierValue])
                    if ins:
                        if self.updatedUnderlyings.get(ins[0].Name(), None):
                            warningMsg = ('SecLoan with underlying {0} has already been updated.  '.format(ins[0].Name()))
                            self._logWarning(warningMsg)                      
                        else:
                            return ins[0]
            else:
                    ins = instrumentLookup([identifierValue])
                    if ins:
                        if len(ins) == 1:
                            if ins[0].Name() in self.instrumentsThatHaveSedols and markitData_subdictionary['SEDOL']:
                                pass
                            else:
                                if self.updatedUnderlyings.get(ins[0].Name(), None):
                                    warningMsg = ('SecLoan with underlying {0} has already been updated.  '.format(ins[0].Name()))
                                    self._logWarning(warningMsg)                      
                                else:
                                    return ins[0]
                        else:  
                            ins = [instrument for instrument in ins if not(instrument.Name() in self.instrumentsThatHaveSedols and markitData_subdictionary['SEDOL'])]
                            if ins:
                                if len(ins) == 1:                                
                                    if self.updatedUnderlyings.get(ins[0].Name(), None):
                                        warningMsg = ('SecLoan with underlying {0} has already been updated.  '.format(ins[0].Name()))
                                        self._logWarning(warningMsg)                      
                                    else:
                                        return ins[0]                                
                                else:
                                    warning = 'Multiple Instruments found with {0} {1}. The following Instruments matched: '
                                    for instrument in ins:
                                        warning = warning + instrument.Name() + ','
                                    warningMsg = (warning[0:-1].format(identifier,identifierValue))
                                    warningMsg = warningMsg + '\n' + '\t' + str(markitData_subdictionary)
                                    
                                    self._logWarning(warningMsg)  
        return None

    def _perform(self,dictionary,fileList):
        
        masterSecloansAndUnderlyings = GetAllMasterSecLoansAndUnderlyings()

        markitMasterTextObject = self.GetMarkitMasterTextObject()
        if not dictionary['clearDataBeforeUpload']:
            if markitMasterTextObject.Text():
                self.markitMasterTextObject_dictionary = json.loads(markitMasterTextObject.Text(), object_hook=ascii_encode_dict)

        sedolLookup = FInstrumentLookup([self.Sedol])
        isinLookup = FInstrumentLookup([self.Isin])
        cusipLookup = FInstrumentLookup([self.Cusip])
        i = 0
        for file in fileList:
            tsvdoc = LoadFromFile(file)
            try:
                self._logInfo('Start reading file')
                if tsvdoc:
                    headers = tsvdoc[0]
                    filtered_reader = tsvdoc[1]
                    
                    identifier_priorityONE = 'SEDOL'
                    identifier_priorityTWO = 'ISIN'
                    identifier_priorityTHREE = 'CUSIP'
                    identifiers = [identifier_priorityONE,identifier_priorityTWO,identifier_priorityTHREE]
                    identifiersAndLookups_dictionary = {'SEDOL':sedolLookup,'ISIN':isinLookup,'CUSIP':cusipLookup}
                    
                    for identifier in identifiers:
                        self._logInfo('SecLoans Markit data imported with underlying\'s identifier {0}:'.format(identifier))
                        indicesOfUpdatedUnderlyings = []

                        for rowData in filtered_reader:
                            markitData_dictionary = dict(list(zip(headers,rowData)))
                            markitData_subdictionaryKeys = ['DXL Identifier','ISIN','SEDOL','CUSIP','Stock Description','Market Area']
                            markitData_subdictionary = {k:markitData_dictionary[k] for k in markitData_subdictionaryKeys if k in markitData_dictionary}

                            try:
                                ins_underlying = self.FindIdentifyingSecurity(identifier,identifiersAndLookups_dictionary[identifier],markitData_subdictionary)
                                try:
                                    if ins_underlying:
                                        sl = masterSecloansAndUnderlyings.get(ins_underlying,None) 
                                        if sl:
                                            try:
                                                self.PopulateMarkitData(ins_underlying,sl,markitData_dictionary)
                                                self._logInfo('    SecLoan {0} with Underlying {1}, {2} {3}'.format(sl.Name(),ins_underlying.Name(),identifier,markitData_subdictionary[identifier]))
                                                self._summaryAddOk('Underlying Security', ins_underlying.Oid(), 'Markit Import')   
                                                i = i + 1
                                            except Exception as ex:
                                                failMsg = ('Unable to import Markit Securities Finance data for Instrument {0}.  '
                                                        '{1}'.format(ins_underlying.Name(), ex))
                                                self._logError(failMsg)
                                                self._summaryAddFail('Underlying Security', ins_underlying.Oid(), 'Markit Import',
                                                        reasons=[failMsg])
                                        indicesOfUpdatedUnderlyings.append(filtered_reader.index(rowData))
                                except Exception as ex:
                                    failMsg = ('Unable to import Markit Securities Finance data for Instrument {0}.  '
                                            '{1}'.format(ins_underlying.Name(), ex))
                                    self._logError(failMsg)
                                    self._summaryAddFail('Underlying Security', ins_underlying.Oid(), 'Markit Import',
                                            reasons=[failMsg])
                            except Exception as ex:
                                failMsg = ('Unable to import Markit Securities Finance data for sedol {0}, isin {1}, cusip {2}.  '
                                        '{3}'.format(markitData_subdictionary['SEDOL'], markitData_subdictionary['ISIN'], markitData_subdictionary['CUSIP'], ex))
                                self._logError(failMsg)
                                raise ex
                        for index in sorted(indicesOfUpdatedUnderlyings, reverse=True):
                            del filtered_reader[index]

                    print('File: ', file, ' Master SecurityLoan, #: ', i)
                    directory = str(dictionary['filedir'])
                    source_file = file
                    archive_directory = os.path.join(directory, "archive", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
                    os.makedirs(archive_directory)
                    source_filename = os.path.join(directory, source_file)
                    if os.path.exists(source_filename):
                        shutil.copy(source_filename, archive_directory)
                    
                    
                else:
                    print("Invalid file path entered. Check path and file type.")
            except Exception as ex:
                directory = str(dictionary['filedir'])
                source_file = file
                archive_directory = os.path.join(directory, "error", datetime.datetime.now().strftime("%Y-%m-%d %H-%M-%S"))
                os.makedirs(archive_directory)
                source_filename = os.path.join(directory, source_file)
                shutil.copy(source_filename, archive_directory)
                msg = (
                    'Errors when processing file with exception %s' % (
                        str(ex)
                    )
                )
                self._logError(msg)
                raise

        updatedMarkit_dictionary = merge_two_dicts(self.markitMasterTextObject_dictionary, self.updatedUnderlyings)
        markitMasterTextObjectClone = markitMasterTextObject.Clone()
        markitMasterTextObjectClone.Text(json.dumps(updatedMarkit_dictionary, encoding='latin1'))
        markitMasterTextObject.Apply( markitMasterTextObjectClone )
        markitMasterTextObject.Commit()

        if dictionary['clearDataBeforeUpload']:
            for underlying in masterSecloansAndUnderlyings:
                master_sl = masterSecloansAndUnderlyings.get(underlying,None)
                if master_sl:
                    if master_sl not in self.updatedSecurityLoans:
                        p = master_sl.PriceFromMarket(self.Market)
                        if p:
                            p.Delete()

        self._logInfo('Markit Data Saved.')        
        
    def CreateMarkitPrice(self,sl,currency,ratesDictionary):
        p = acm.FPrice()
        p.Instrument(sl)
        p.Currency(currency)
        p.Market(self.Market)
        self.UpdateMarkitPrice(p,ratesDictionary)

    def UpdateMarkitPrice(self,p,ratesDictionary):  
        p.Bid(ratesDictionary.get('VWAF 1 Day', None))
        p.Ask(ratesDictionary.get('VWAF 3 Day', None))
        p.Last(ratesDictionary.get('VWAF 7 Day', None))
        p.High(ratesDictionary.get('VWAF 30 Day', None))
        p.Low(ratesDictionary.get('VWAF All', None))
        p.Settle(ratesDictionary.get('Tradable Fee', None))
        p.Day(acm.Time.DateNow())
        p.Commit()

    def SetMarkitPrice(self,sl,currency,ratesDictionary):
        sl_MarketPrice = sl.PriceFromMarket(self.Market) 
        if sl_MarketPrice:
            self.UpdateMarkitPrice(sl_MarketPrice,ratesDictionary)
        else:
            self.CreateMarkitPrice(sl,currency,ratesDictionary)

    def GetMarkitMasterTextObject(self):
        markitMasterTextObject = acm.FCustomTextObject['Markit Master Text Object']
        if not markitMasterTextObject:
            markitMasterTextObject = acm.FCustomTextObject()
            markitMasterTextObject.Name('Markit Master Text Object')
            markitMasterTextObject.SubType('Customizable')
            markitMasterTextObject.Commit()
            return markitMasterTextObject
        else:
            return markitMasterTextObject
        return None

    def PopulateMarkitData(self,ins_underlying,sl,markitData_dictionary): 
        self.updatedUnderlyings[ins_underlying.Name()] = markitData_dictionary
        self.updatedSecurityLoans[sl] = None
        ratesDictionary = {k:float(markitData_dictionary[k])/100 for k in self.MarkitRates if k in markitData_dictionary and markitData_dictionary[k]}
        self.SetMarkitPrice(sl,ins_underlying.Currency(),ratesDictionary)

def merge_two_dicts(x, y):
    z = x.copy()   
    z.update(y)    
    return z
    
def GetAllInstrumentsThatHaveSedols():
    aliases = {}
    query = acm.CreateFASQLQuery(acm.FInstrumentAlias, 'AND')
    type = query.AddOpNode('OR') 
    type.AddAttrNode('Type.Name', 'EQUAL',"SEDOL")
    queryResult = query.Select()
    for alias in queryResult:
        if alias.Instrument().Name() not in aliases:
            aliases.setdefault(alias.Instrument().Name(), alias.Alias())
    return aliases

def GetAllMasterSecLoansAndUnderlyings():
    masterSecloansAndUnderlyings = {}
    for master in acm.FInstrument.Select("insType='SecurityLoan' and productTypeChlItem = 'Master Security Loan'"):
        masterSecloansAndUnderlyings[master.Underlying()]=master
    return masterSecloansAndUnderlyings