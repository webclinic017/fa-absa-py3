""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitCorporateActions/./etc/FCorporateActionsPerformImport.py"
from __future__ import print_function
"""----------------------------------------------------------------------------
MODULE
    FCorporateActionsPerformImport

DESCRIPTION
    Module which performs the import of acm.FCorporateActions
    from Markit file format
----------------------------------------------------------------------------"""

import acm, ael
import os
import ast
import FBDPPerform
import FBDPCommon
import FBDPInstrument
import FTransactionHandler
from FBDPCurrentContext import Logme
from FBDPCurrentContext import Summary
from contextlib import contextmanager
import FMarkitLayout
import glob

contextParContext = None

def _QueryStringForLevel(level):
    query_string = None
    if level == 'User':
        query_string = 'user="%s" and ' % acm.User().Name()
    elif level == 'Group':
        query_string = 'userGroup="%s" and ' % acm.User().UserGroup().Name()
    elif level == 'Organisation':
        query_string = 'organisation="%s" and ' % acm.User().UserGroup().Organisation().Name()
    elif level == 'Global':
        query_string = ''
    return query_string

def _ContextGivenLevelAndQueryString(level, query_string):
    parMaps = acm.FParameterMapping.Select(query_string + 'overrideLevel="%s"' % level)
    context = None
    for parMap in parMaps:
        for instance in parMap.ParMappingInstances():
            if instance.ParameterType() == 'Context Par':
                context = instance.Context()
                break
        if context:
            break
    return context

def GetLevelContextParContext(level):
    query_string = _QueryStringForLevel(level)
    if query_string is None:
        return None
    context = _ContextGivenLevelAndQueryString(level, query_string)
    return context

def GetContextParContext():
    for level in ('User', 'Group', 'Organisation', 'Global'):
        context = GetLevelContextParContext(level)
        if context:
            return context
    return None

def GetContextParContextFunc():
    global contextParContext
    if contextParContext:
        return contextParContext
    
    contextParContext = GetContextParContext()
    return contextParContext
    

class CorporateActionImportTransactionHandler(FTransactionHandler.ACMHandler):

    def __init__(self):
        super(CorporateActionImportTransactionHandler, self).__init__()
        self.dataFromSource = []
        self.corporateAction = None
        self.caTemplate = None
        self.caDividend = None
        self.caDividendStream = None
        self.caDividendEstimate = None
        self.dividendContextLink = None
        self.caTextObject = None
        self.caAdditionalInfos = []
        self.caChoiceTextObjects = []
        self.caChoices = []
        self.caChoicesToBeDeleted = []
        self.caPayoutTextObjects = []
        self.caPayouts = []
        self.caPayoutsToBeDeleted = []
        self.logOks = []
        self.summaryOks = []
        self.logIgnores = []
        self.ignore_ca_update = False
        self.caTemplatesToBeDeleted = None

    def CommitCorporateActionEntities(self):

        for oid in self.caPayoutsToBeDeleted:
            acm.FCorporateActionPayout[oid].Delete()
        for oid in self.caChoicesToBeDeleted:
            acm.FCorporateActionChoice[oid].Delete()
        self.caTemplatesToBeDeleted.Delete()
        if self.caDividend:
            self.caDividend.Commit()
        if self.caDividendStream:
            self.caDividendStream.Commit()
        if self.caDividendEstimate:
            self.caDividendEstimate.Commit()
        if self.dividendContextLink:
            self.dividendContextLink.Commit()
        if self.caTextObject:
            self.caTextObject.Commit()
        if self.corporateAction and not self.ignore_ca_update:
            self.corporateAction.Commit()
        if self.caTemplate:
            self.caTemplate.Commit()
        for addInfo in self.caAdditionalInfos:
            addInfo.Commit()

        for obj in self.caChoiceTextObjects:
            obj.Commit()
        for caChoice, update in self.caChoices:
            if update:
                caChoice.Commit()
        for obj in self.caPayoutTextObjects:
            obj.Commit()
        for caPayout, update in self.caPayouts:
            if update:
                caPayout.Commit()

    def GetCaChoiceFromTransactonCache(self, optionNumber):
        for singleCaChoice, update in self.caChoices:
            if str(singleCaChoice.ChoiceName()).startswith(optionNumber):
                return singleCaChoice
        return None

    def CleanTransactionLists(self):
        self.dataFromSource[:] = []
        self.corporateAction = None
        self.caTextObject = None
        self.caTemplate = None
        self.caDividend = None
        self.caDividendStream = None
        self.caDividendEstimate = None
        self.dividendContextLink = None
        self.caAdditionalInfos[:] = []
        self.caChoices[:] = []
        self.caChoiceTextObjects[:] = []
        self.caPayouts[:] = []
        self.caPayoutTextObjects[:] = []
        self.logOks[:] = []
        self.summaryOks[:] = []
        self.logIgnores[:] = []
        self.caPayoutsToBeDeleted[:] = []
        self.caChoicesToBeDeleted[:] = []
        self.ignore_ca_update = False
        self.caTemplatesToBeDeleted = None

    @contextmanager
    def Transaction(self):
        try:
            acm.BeginTransaction()
            yield
            acm.CommitTransaction()

            for ignoreMessage in self.logIgnores:
                Logme()(ignoreMessage, 'WARNING')
            for logOk in self.logOks:
                Logme()(logOk[0], 'INFO')
            for summaryOk in self.summaryOks:
                Summary().ok(
                    summaryOk[0], 
                    getattr(Summary(),summaryOk[1]), 
                    summaryOk[0].Oid())

        except Exception as ex:
            print(ex)

            failMessage = 'Unable to create Corporate Action for {0}. {1}'.format(
                    self.corporateAction.Name(), ex)
            Summary().notOk(
                result = getattr(Summary(), 'FAIL'), 
                entity = self.corporateAction, 
                action = getattr(Summary(),self.summaryOks[0][1]), 
                reason = [failMessage], 
                objectId = self.corporateAction.Oid())
            Logme()(failMessage, 'ERROR')

            acm.AbortTransaction()

        finally:
            self.CleanTransactionLists()


# Expand the list with tuple (caType, caChoiceType)
# if Markit file doesn't provide a closing payout for CA type
PayoutGenerationCandidates = \
[
    ('MergerStock', 'Mandatory'),
    ('MergerStock', 'Voluntary'),
    ('ExerciseRights', 'Voluntary'),
    ('TenderOfferStock', 'Voluntary')
]

# Payout properties which should be zero for closing payout
ZeroReadPropertiesForClosingPayout = \
[
    'PayoutRate',
    'PayoutAmount',
    'PayoutNetAmount',
    'PayoutGrossAmount',
    'Price',
    'Fee',
    'NewInstrument'
]

#Zero properties for closing payout
ZeroWritePropertiesForClosingPayout = \
[
    singleProperty 
    for singleProperty in ZeroReadPropertiesForClosingPayout[:-1] # omit NewInstrument
]


# Checks if a payout is a closing payout 
def IsClosingPayout(payout):
    retVal = True
    for attribute in ZeroReadPropertiesForClosingPayout:
        if getattr(payout, attribute)():
            retVal = False;
            break;

    return retVal

def isOverSubscription(choice):
    choiceRecord = choice.ChoiceRecord()
    if choiceRecord:
        dict = eval(choiceRecord.Text())
        if dict['Option Action'] == 'OVER':
            return True
    
    return False

def CreateRowDictionary(detailRecord, layoutDict):
    dictionary = {}
    for name in layoutDict['name']:
        fromIndex = layoutDict['from'][layoutDict['name'].index(name)] - 1
        toIndex = layoutDict['to'][layoutDict['name'].index(name)]
        dictionary[name] = detailRecord[fromIndex:toIndex].strip()

    return dictionary


def ExtractRow(x):
    return {
        'D1': ExtractTypeD1,
        'D2': ExtractTypeD2,
        'D3': ExtractTypeD3,
    }.get(x, None)


def ExtractTypeD1(detailRecord, *kwargs):
    dictionary = CreateRowDictionary(detailRecord, FMarkitLayout.D1)
    return ('D1', dictionary)


def ExtractTypeD2(detailRecord, *kwargs):
    dictionary = CreateRowDictionary(detailRecord, FMarkitLayout.D2)
    return ('D2', dictionary)


def ExtractTypeD3(detailRecord, *kwargs):
    dictionary = CreateRowDictionary(detailRecord, FMarkitLayout.D3)
    return ('D3', dictionary)


def ExtractCorporateActionData(detailRecord, transactionHandler):
    if not detailRecord[:2].startswith('D'):
        return False
    Extract = ExtractRow(detailRecord[:2])
    if Extract:
        transactionHandler.dataFromSource.append(
            Extract(detailRecord, transactionHandler))
    return True


def ProcessTypeD1(log, dictionary, transactionHandler, *kwargs):
    overrideExisting = kwargs[0]
    createNew = kwargs[1]
    caDefFileName = kwargs[2]
    preProcessResults = kwargs[3]
    markitCAStatuses = kwargs[4]
    markitImportUsers = kwargs[5]
    r = _CreateOrUpdateFCorporateAction(log, caDefFileName, preProcessResults, markitImportUsers) 
    r._perform(dictionary, overrideExisting, createNew, transactionHandler, markitCAStatuses)
    r.end()


def ProcessTypeD2(log, dictionary, transactionHandler, *kwargs):
    if not transactionHandler.corporateAction:
        return
    overrideExisting = kwargs[0]
    createNew = kwargs[1]
    markitImportUsers = kwargs[5]
    r = _CreateorUpdateFCorporateActionChoice(log, markitImportUsers) 
    r._perform(dictionary, overrideExisting, createNew, transactionHandler)
    r.end()


def ProcessTypeD3(log, dictionary, transactionHandler, *kwargs):
    if not transactionHandler.corporateAction:
        return
    overrideExisting = kwargs[0]
    createNew = kwargs[1]
    markitImportUsers = kwargs[5]
    r = _CreateorUpdateFCorporateActionPayout(log, markitImportUsers) 
    r._perform(dictionary, overrideExisting, createNew, transactionHandler)
    r.end()


def ProcessRecord(x):
    return {
        'D1': ProcessTypeD1,
        'D2': ProcessTypeD2,
        'D3': ProcessTypeD3,
    }.get(x, None)


def PreprocessRecord(transactionHandler):
    dictionary = {'dividendsFields' : []}
    foundQuantity = False
    for recType, rowKeyVale in transactionHandler.dataFromSource:
        if recType == 'D3':
            if not foundQuantity and (abs(float(rowKeyVale['Old Shares'])) > 0  or \
                    abs(float(rowKeyVale['New Shares']))):
                dictionary['OldQuantity'] = rowKeyVale['Old Shares']
                dictionary['NewQuantity'] = rowKeyVale['New Shares']
                foundQuantity = True
            
            if rowKeyVale['Currency Code']:
                dictionary['dividendsFields'].append((rowKeyVale['Currency Code'], rowKeyVale['Payout Gross Amount']))
    return {'ca' : dictionary}


def ChoiceHasOnlyOnePayout(transactionHandler, optionNumber):
    numberOfPayouts = 0
    for recType, rowKeyVale in transactionHandler.dataFromSource:
        if recType == 'D3':
            if rowKeyVale['Option Number'] == optionNumber:
                numberOfPayouts += 1
            if numberOfPayouts > 1:
                break
    
    return numberOfPayouts == 1


def _CreateClosingPayout(transactionHandler, choice):
    logMessage = '    Creation of compensation payout on {} for choice {}'.format(
                                    transactionHandler.corporateAction.Name(), choice.Name().strip())
    payout = acm.FCorporateActionPayout()
    payout.CaChoice(choice)
    payout.Name('Closing')
    for attribute in ZeroWritePropertiesForClosingPayout:
        setattr(payout, attribute, 0)
    transactionHandler.logOks.append((logMessage, 'CREATE'))
    transactionHandler.summaryOks.append((payout, 'CREATE'))
    return payout

def _GeneratePayoutForRequiredAction(transactionHandler):

    if (transactionHandler.corporateAction == None):
        return

    templateName = transactionHandler.caTemplate.Name() if transactionHandler.caTemplate else None
    if (templateName,
        transactionHandler.corporateAction.CaChoiceType()) in PayoutGenerationCandidates:
        caChoicesList, updates = list(zip(*transactionHandler.caChoices))
        for currentChoice in caChoicesList:
            payoutsList, updates = list(zip(*transactionHandler.caPayouts))
            payouts = [payout for payout in payoutsList
                        if payout.CaChoice() == currentChoice]
            if len(payouts) == 0 or isOverSubscription(currentChoice):
                continue

            closingPayouts = [payout for payout in currentChoice.CaPayouts() if IsClosingPayout(payout)]
            if (len(closingPayouts) == 0):
                closingPayouts = [payout for payout in payouts if IsClosingPayout(payout)]
            if (len(closingPayouts) == 0):
                transactionHandler.caPayouts.append(
                    (_CreateClosingPayout(transactionHandler,
                                        currentChoice), True))


def PerformCorporateActionsImport(log, dictionary):
    
    overrideExisting = dictionary['override_existing']
    createNew = dictionary['create_new']
    filedir = dictionary['filedir'].SelectedDirectory().Text()
    filename = dictionary['filename'][0]
    markitCAStatuses = dictionary['MarkitCAStatuses']
    os.chdir(filedir)
    fileList = glob.glob(filename)
    markitImportUsers = FBDPCommon.valueFromFParameter(
                'FCAVariables', 'MarkitImportUsers')
    if not markitImportUsers:
        markitImportUsers = ['ATSUSER']
    else:
        markitImportUsers = [name.strip().upper() for name in markitImportUsers.split(',')]

    transactionHandler = CorporateActionImportTransactionHandler()
    log.logInfo('Start reading file')
    for singleFile in fileList:
        fileInfo = 'File: ' + singleFile
        log.logInfo(fileInfo)
        with open(singleFile, 'r') as markitFile:
            detailRecord = markitFile.readline()
            while(detailRecord):
                while (True):
                    recordTypeD = ExtractCorporateActionData(detailRecord,
                                                        transactionHandler)
                    detailRecord = markitFile.readline()
                    if not recordTypeD and detailRecord:
                        continue
                    if not detailRecord or detailRecord[:2] == 'D1':
                        break
                try:
                    preProcessResults = PreprocessRecord(transactionHandler)
                    for caData in transactionHandler.dataFromSource:
                        perform = ProcessRecord(caData[0])
                        if perform:
                            perform(log, caData[1], transactionHandler,
                                    overrideExisting, createNew, singleFile,
                                    preProcessResults, markitCAStatuses, markitImportUsers)

                    _GeneratePayoutForRequiredAction(transactionHandler)
                    with transactionHandler.Transaction():
                        transactionHandler.CommitCorporateActionEntities()

                except Exception as ex:
                    print(ex)
                    transactionHandler.CleanTransactionLists()


    log.listTopWarningMessages()
    log.listTopErrorMessages()
    CopySummary(log)


def _AddAdditionalInfo(ca, entity, addInfoName, value, transactionHandler):
    additionalInfo = FBDPCommon.SetAdditionalInfoValue(ca,
                                                        entity,
                                                        addInfoName,
                                                        value)
    transactionHandler.caAdditionalInfos.append(additionalInfo)
            

class _CreateOrUpdateBase(FBDPPerform.FBDPPerform):
    """
    """
    def __init__(self, log, markitImportUsers):
        FBDPPerform.FBDPPerform.__init__(self, log)
        self.markitImportUsers = markitImportUsers

    def _end(self):
        """
        """
        FBDPPerform.FBDPPerform._end(self)

    def FindIdentifyingSecurity(self, dictionary):
        sedol = self.IdentifySecurityID('03',dictionary)
        isin =  self.IdentifySecurityID('04',dictionary)
        if sedol:
            query = "type = {} and alias = '{}'".format(
                        acm.FInstrAliasType['SEDOL'].Oid(), sedol)
            insAlias = acm.FInstrumentAlias.Select01(query, None)
            if insAlias:
                stock = insAlias.Instrument()
                return stock

            self._logWarning('There is no alias for sedol {} in the database'.format(sedol))

        if isin:
            stock = acm.FStock.Select01("isin = '{}'".format(isin), None)
            if stock:
                return stock

            self._logWarning('There is no alias for isin {} in the database'.format(isin))

        return None

    def IdentifySecurityID(self, x, d):
        # This method should be redefined in each derived class.
        pass

    def CanUpdateRecord(self, record):
        return not (record.UpdateUser().Name().upper() not in self.markitImportUsers and
                acm.User().Name().upper() in self.markitImportUsers)

    def ValidateRecordInfo(self, d):
        return True


class _CreateOrUpdateFCorporateAction(_CreateOrUpdateBase):
    """
    """
    def __init__(self, log, caDefFileName, preProcessResults, markitImportUsers):
        _CreateOrUpdateBase.__init__(self, log, markitImportUsers)
        self.caDefFileName = caDefFileName
        self.preProcessResults = preProcessResults
        
    def end(self):
        _CreateOrUpdateBase._end(self)

    def IdentifySecurityID(self, x, d):
        return {
            d['Identifying Security ID Type']: d['Identifying Security ID'],
            d['Security ID Type']: d['Security ID'],
        }.get(x, None)

    def GetCaChoiceType(self, x):
        return {
            'M': 'Mandatory',
            'V': 'Voluntary',
        }.get(x, None)

    # Mapping Markit CA Type to
    # (acm's CA template object name, ael's CorpActionType enumeration type)
    def GetCaType(self, x):
        return {
            'RDN': ('RightsDistribution', 'Rights Distribution'),
            'BI': ('BonusIssue', 'Bonus Issue'),
            'BR': ('Bankruptcy', 'None'),
            'IN': ('GeneralInformation', 'None'),
            'TE': ('TenderOfferStock', 'Tender offer'),
            'SS': ('SplitStock', 'Stock Split'),
            'RS': ('ReverseStockSplit', 'Reverse Stock Split'),
            'SD': ('StockDividend', 'Stock Dividend'),
            'CD': ('CashDistribution', 'Cash Distribution'),
            'LQ': ('Liquidation', 'Liquidation'),
            'NC': ('NameChange', 'Name Change'),
            'DRI': ('DividendReinvestment', 'Dividend Reinvestment'),
            'MEM': ('MergerStock', 'Merger'),
            'MEV': ('MergerStock', 'Merger'),
            'RES': ('ExerciseRights', 'Exercise Rights'),
            'SC': ('ScripDividend', 'Scrip Dividend'),
            'SOM': ('SpinOffStock', 'Spin-off'),
            'SOV': ('SpinOffStock', 'Spin-off'),
            'SP': ('CashDistribution', 'Cash Distribution'),
            'SU': ('SubscriptionOffer', 'None'),
            'MT': ('Meeting', 'None'),
            'LS': ('Class Action Lawsuit', 'None'),
            'CN': ('Consent', 'None'),
            'CS': ('Change In Domicile', 'None'),
            'EXV': ('Exchange', 'None'),
            'RZM': ('Reorganization', 'None'),
            'CDCS': ('Coupon Dist. - Cash/Stock', 'None')
        }.get(x, (None, 'None'))

    def GetWorkflowStatus(self, x):
        return {
            'AP': 'Approved',
            'CN': 'Cancelled',
            'CT': 'In conflict',
            'IN': 'Incomplete',
            'PA': 'Pending approval',
            'PC': 'Pending cancelled',
            'CA': 'Conditionally approved',
            'PN': 'Pending conditionally approved',
            'DE': 'Deleted',
            'NS': 'Not Supported',
        }.get(x, None)

    def SetTemplate(self, ca, transactionHandler, template):
        if not template:
            return
        transactionHandler.caTemplatesToBeDeleted = ca.Templates()

        caTemplate = None
        if type(template) is type(''):
            caTemplate = acm.FCorpactTemplate()
            caTemplate.Name(template)
        elif type(template) is type([]):
            caTemplate = template[0]
        if caTemplate:
            caTemplate.CorporateAction(ca)
            transactionHandler.caTemplate = caTemplate

    def SetDividendPayDay(self, div, payDay):
        if payDay is '' or None:
            div.PayDay('9999-12-31')
        else:
            div.PayDay(payDay)

    def CreateFDividend(self, ca, transactionHandler):
        div = acm.FDividend()
        if ca.ExDate() is '' or None:
            div.ExDivDay('9999-12-31')
        else:
            div.ExDivDay(ca.ExDate())
        div.RecordDay(ca.RecordDate())
        self.SetDividendPayDay(div, ca.SettleDate())
        div.Description(ca.Name())
        div.Instrument(ca.Instrument())
        div.Currency(ca.Instrument().Currency())

        for p in self.preProcessResults['ca']['dividendsFields']:
            divCurrency = acm.FCurrency[p[0]]
            if ca.Instrument().Currency() == divCurrency:
                div.Amount(p[1])
                div.TaxFactor(1)
                div.Currency(divCurrency)
        
        transactionHandler.caDividend = div
        ca.Dividend(div)
        transactionHandler.summaryOks.append((div, 'CREATE'))

    
    def CreateFDividendStream(self, ca, transactionHandler):
        stream = acm.FDividendStream()
        stream.Instrument(ca.Instrument())
        stream.Name(ca.Instrument().Oid())
        transactionHandler.caDividendStream = stream
        transactionHandler.summaryOks.append((stream, 'CREATE'))

        divEstimate = acm.FDividendEstimate()
        divEstimate.DividendStream(stream)
        if ca.ExDate() is '' or None:
            divEstimate.ExDivDay('9999-12-31')
        else:
            divEstimate.ExDivDay(ca.ExDate())
        divEstimate.RecordDay(ca.RecordDate())
        self.SetDividendPayDay(divEstimate, ca.SettleDate())
        divEstimate.Description(ca.Name())
        divEstimate.Instrument(ca.Instrument())
        divEstimate.Currency(ca.Instrument().Currency())
        divEstimate.Amount(ca.Dividend().Amount())
        divEstimate.TaxFactor(ca.Dividend().TaxFactor())
        transactionHandler.caDividendEstimate = divEstimate
        transactionHandler.summaryOks.append((divEstimate, 'CREATE'))

        self.CreateDividendContextLink(str(ca.Instrument().Oid()),
                                ca.Instrument(), transactionHandler)

    def CreateDividendContextLink(self, name, inst, transactionHandler):
        myContext = GetContextParContextFunc()
        if not myContext:
            Logme()('No context mapped for the current user', 'ERROR')

        links = myContext.ContextLinks()
        for l in links:
            if l.Instrument() == inst and l.Type() == 'Dividend Stream':
                return 

        cl = acm.FContextLink()
        cl.Context(myContext)
        cl.Type('Dividend Stream')
        cl.Name(name)
        cl.MappingType('Instrument')
        cl.Instrument(inst)
        transactionHandler.dividendContextLink = cl
        transactionHandler.summaryOks.append((cl,'CREATE'))

    def UpdateFDividend(self, ca, div, transactionHandler):
        div_clone = div.Clone()
        if ca.ExDate() is '' or None:
            div_clone.ExDivDay('9999-12-31')
        else:
            div_clone.ExDivDay(ca.ExDate())
        div_clone.RecordDay(ca.RecordDate())
        self.SetDividendPayDay(div_clone, ca.SettleDate())
        div_clone.Description(ca.Name())
        div.Apply( div_clone )
        transactionHandler.caDividend = div
        ca.Dividend(div)
        transactionHandler.summaryOks.append((div, 'UPDATE'))

    def UpdateFDividendStream(self, ca, stream, transactionHandler):
        divStream = acm.FDividendStream[str(ca.Instrument().Oid())]
        if divStream:
            ds =  divStream.Dividends()
            for d in ds:
                if str(ca.Instrument().Oid()) in d.AsSymbol():
                    divEstimate_clone = d.Clone()
                    if ca.ExDate() is '' or None:
                        divEstimate_clone.ExDivDay('9999-12-31')
                    else:
                        divEstimate_clone.ExDivDay(ca.ExDate())
                    divEstimate_clone.RecordDay(ca.RecordDate())
                    self.SetDividendPayDay(divEstimate_clone, ca.SettleDate())
                    divEstimate_clone.Description(ca.Name())
                    divEstimate_clone.Currency(ca.Instrument().Currency())
                    divEstimate_clone.Amount(ca.Dividend().Amount())
                    d.Apply( divEstimate_clone )
                    transactionHandler.caDividendEstimate = d
                    transactionHandler.summaryOks.append((d, 'UPDATE'))
                    break
    
    def FindFDividend(self, ca):
        ins = ca.Instrument()
        if ins is None:
            return None
        div = ca.Dividend()
        if div:
            return div
        divs = ins.Dividends()
        desc = ca.Name()
        for div in divs:
            #markit import dividends have the markit ID
            #the description of the dividend
            if desc in div.Description():
                return div

    def CreateOrUpdateFDividend(self, ca, transactionHandler):
        div = self.FindFDividend(ca)
        # May not always be connected so try to search from the instrument
        if div:
            self.UpdateFDividend(ca, div, transactionHandler)
        else:
            self.CreateFDividend(ca, transactionHandler)
    
    def CreateOrUpdateFDividendStream(self, ca, transactionHandler):
        stream = acm.FDividendStream[str(ca.Instrument().Oid())]
        if stream:
            self.UpdateFDividendStream(ca, stream, transactionHandler)
        else:
            self.CreateFDividendStream(ca, transactionHandler)

    def _SetDate(self, date, dictionary):
        caTypeParams = self.GetCaType(dictionary['Corporate Action Type'])[0]
        dateHandlerDict = FBDPCommon.valueFromFParameter(caTypeParams, 'MarkitDateHandling')
        dateHandlerDict = ast.literal_eval(dateHandlerDict)
        desiredDates = dateHandlerDict[date]
        for d in desiredDates:
            if dictionary[d]:
                return dictionary[d].replace("/", "-")
        return ''

    def FillInCorporateAction(self, 
                            dictionary, 
                            transactionHandler, 
                            stock, 
                            ca, 
                            dbAction):
            transactionHandler.corporateAction = ca
            if dbAction == 'UPDATE_IGNORED':
                transactionHandler.ignore_ca_update = True
                return
            # "Issuer Description" is limited to 22 to avoid tranc of name during
            # commit in db. Field "Name" contains 39 chars in db,
            # max lenght of 'CA ID' is 16 and one char from "join"
            # function (39-16 - 1 = 22).
            ca.Name(' '.join([dictionary['Issuer Description'][:22], dictionary['CA ID']]).strip())
            ca.ExternalId(dictionary['CA ID'])
            ca.CaType(self.GetCaType(dictionary['Corporate Action Type'])[1]) 
            ca.Instrument(stock)
            ca.CaChoiceType(self.GetCaChoiceType(dictionary['Voluntary/Mandatory Code']))

            ca.ExDate(self._SetDate(date = 'Ex Date', dictionary = dictionary))    
            ca.RecordDate(self._SetDate(date = 'Record Date', dictionary = dictionary))    
            ca.SettleDate(self._SetDate(date = 'Payable Date', dictionary = dictionary))
            ca.EffectiveDate(self._SetDate(date = 'Effective Date', dictionary = dictionary))
            ca.ExpirationTime(self._SetDate(date = 'Expiration Date', dictionary = dictionary))
            ca.TradingBeginDate(self._SetDate(date = 'Trading Begin Date', dictionary = dictionary))
            ca.TradingEndDate(self._SetDate(date = 'Trading End Date', dictionary = dictionary))
            ca.WithdrawalDate(self._SetDate(date = 'Withdrawal Date', dictionary = dictionary))

            if 'NewQuantity' in self.preProcessResults['ca']:
                ca.OldQuantity(self.preProcessResults['ca']['OldQuantity'])
                ca.NewQuantity(self.preProcessResults['ca']['NewQuantity'])
            else:
                ca.OldQuantity(dictionary['Subscription Old Shares Qty'])
                ca.NewQuantity(dictionary['Subscription New Shares Qty'])
            
            if dictionary['Approved Date']:
                ca.Status('Active')
            if dictionary['Cancelled'] == 'Y':
                ca.Status('Inactive')
            if dictionary['Minimum Denomination']:
                ca.LotSize(dictionary['Minimum Denomination'])
            elif dictionary['Minimum Exercise Quantity']:
                ca.LotSize(dictionary['Minimum Exercise Quantity'])
            ca.CashAmount(dictionary['Event Cash Value'])
            ca.CashCurrency(acm.FCurrency[dictionary['Event Cash Value Currency']])

            recordDateCountries = FBDPCommon.valueFromFParameter(
                                    'FCAVariables', 'RecordDateMarkets')
            if dictionary['Country of Issue'] in recordDateCountries:        
                ca.Market(acm.FMarketPlace['RecordDate'])
            else:
                ca.Market(acm.FMarketPlace['ExDate'])
            
            textObject = ca.SourceRecord()
            if textObject:
                UpdateFPersistentTextObject(dictionary, textObject)
            else:
                textObjectName = 'corporate action: ' + ca.Name()
                textObject = acm.FCustomTextObject[textObjectName]
                if textObject:
                    ca.SourceRecord(textObject)
                    UpdateFPersistentTextObject(dictionary, textObject)
                else:
                    textObject = CreateFPersistentTextObject(dictionary, textObjectName)
                    ca.SourceRecord(textObject)
            transactionHandler.caTextObject = textObject
            if dictionary['Meeting Date']:
                ca.Text('Meeting Date: ' + dictionary['Meeting Date'])

            if dictionary['Corporate Action Type'] in ['CD','DRI','SC']:
                self.CreateOrUpdateFDividend(ca, transactionHandler)
                self.CreateOrUpdateFDividendStream(ca, transactionHandler)

            logMessage = '    {} Corporate Action for {}'.format(
                                        dbAction.capitalize()[:-1] + 'ed',
                                        ca.Name())
            transactionHandler.logOks.append((logMessage, dbAction))
            transactionHandler.summaryOks.append((ca, dbAction))

    def _AddConnectedObjects(self, ca, transactionHandler, dictionary):
        
        workflowStatus = self.GetWorkflowStatus(dictionary['Workflow Status'])
        _AddAdditionalInfo(ca, 'CorpAction', 'MarkitCAStatus', workflowStatus, transactionHandler)
        _AddAdditionalInfo(ca, 'CorpAction', 'CADefinitionFile', self.caDefFileName, transactionHandler)
        self.SetTemplate(ca, transactionHandler,
            self.GetCaType(dictionary['Corporate Action Type'])[0])

    def _perform(self, 
                dictionary,
                overrideExisting,
                createNew, 
                transactionHandler,
                markitStatuses):

        workflowStatus = self.GetWorkflowStatus(dictionary['Workflow Status'])
        if workflowStatus not in markitStatuses:
            caName = ' '.join([dictionary['Issuer Description'][:22], dictionary['CA ID']]).strip()
            logMessage = 'Ignored corp action {}, as its MarkitCAStatus \'{}\' '\
                        'is not selected as a valid status to import.'.format(
                        caName, workflowStatus)
            transactionHandler.logIgnores.append(logMessage)
            return

        stock = self.FindIdentifyingSecurity(dictionary)
        if stock:
            query = "externalId = '{}'".format(dictionary['CA ID'])
            ca = acm.FCorporateAction.Select01(query, None)
            dbAction = None
            if ca and overrideExisting:
                dbAction = 'UPDATE'
                if not self.CanUpdateRecord(ca):
                    dbAction = 'UPDATE_IGNORED'
                    caName = ' '.join([dictionary['Issuer Description'][:22], dictionary['CA ID']]).strip()
                    logMessage = 'Ignored corp action {}, as it has been manually updated by {}.'.format(caName, ca.UpdateUser().Name())
                    self._logWarning(logMessage)

            if not ca and createNew:
                dbAction = 'CREATE'
                ca = acm.FCorporateAction()

            if dbAction:
                self.FillInCorporateAction(dictionary, 
                                        transactionHandler, 
                                        stock, 
                                        ca, 
                                        dbAction)
                if dbAction != 'UPDATE_IGNORED':
                    self._AddConnectedObjects(ca, transactionHandler, dictionary)


class _CreateorUpdateFCorporateActionChoice(_CreateOrUpdateBase):
    """
    """
    def __init__(self, log, markitImportUsers):
        _CreateOrUpdateBase.__init__(self, log, markitImportUsers)

    def end(self):
        _CreateOrUpdateBase._end(self)

    def ValidateRecordInfo(self, dictionary):
        if dictionary['Option Status'] == 'DE':
            choiceName = ' '.join([dictionary['Option Number'], dictionary['Option Action'], dictionary['Option Text'][:25]])
            logMessage = 'Ignored corp action option{}, as its status is \'DE\'.'.format(choiceName)
            self._logWarning(logMessage)
            return False

        return True

    def FillInCaChoice(self, transactionHandler,dictionary, caChoice, ca, dbAction):

        choiceName = ' '.join([dictionary['Option Number'], 
                            dictionary['Option Action'], 
                            dictionary['Option Text'][:25]])[:39].strip()
        caChoice.ChoiceName(choiceName)
        caChoice.CorpAction(ca)
        caChoice.IsDefault({'Y': True, 'N': False}.get(dictionary['Default Option Indicator'], False))
        textObject = caChoice.ChoiceRecord()
        if textObject:
            UpdateFPersistentTextObject(dictionary, textObject)
        else:
            textObjectName = 'caChoice: ' + ca.Name() + ' ' + dictionary['Option Number']
            textObject = acm.FCustomTextObject[textObjectName]
            if textObject:
                caChoice.ChoiceRecord(textObject)
                UpdateFPersistentTextObject(dictionary, textObject)
            else:
                textObject = CreateFPersistentTextObject(dictionary, textObjectName)
                caChoice.ChoiceRecord(textObject)
            transactionHandler.caChoiceTextObjects.append(textObject)
        logMessage = ('    {} Corporate Action Choice {} '
                    'for Corporate Action {}'.format(
                        dbAction.capitalize()[:-1] + 'ed',
                        caChoice.Name().strip(), 
                        ca.Name()))
        transactionHandler.logOks.append((logMessage, dbAction))
        transactionHandler.summaryOks.append((caChoice, dbAction))


    def FindAndCorrectChoice(self, dictionary, ca, transactionHandler):

        ca_choice = None
        ca_choices = [choice for choice in ca.CaChoices()
                    if choice.ChoiceName()[0] == dictionary['Option Number']]
        if len(ca_choices) == 1:
            ca_choice = ca_choices[0]
        elif len(ca_choices) > 1:
            # There may be too many choices in the DB, due to incorrect imports.
            ca_choices.sort(key = lambda obj: obj.Oid())
            for choice in ca_choices[1:]:
                transactionHandler.caChoicesToBeDeleted.append(choice.Oid())
            ca_choice = ca_choices[0]
        return ca_choice


    def _perform(self,
                dictionary,
                overrideExisting,
                createNew,
                transactionHandler):
        ca = transactionHandler.corporateAction
        if not ca:
            return

        if not self.ValidateRecordInfo(dictionary):
            return

        caChoice = self.FindAndCorrectChoice(dictionary, ca, transactionHandler)

        dbAction = None
        if caChoice and overrideExisting:
            dbAction = 'UPDATE'
            if not self.CanUpdateRecord(caChoice):
                dbAction = 'UPDATE_IGNORED'
                choiceName = ' '.join([dictionary['Option Number'], 
                                    dictionary['Option Action'], 
                                    dictionary['Option Text'][:25]])[:39].strip()
                logMessage = 'Ignored corp action choice{}, as it has been manually updated by {}.'.format(choiceName, caChoice.UpdateUser().Name())
                self._logWarning(logMessage)

        if not caChoice and createNew:
            dbAction = 'CREATE'
            caChoice = acm.FCorporateActionChoice()

        if dbAction:
            update = False
            if dbAction != 'UPDATE_IGNORED':
                self.FillInCaChoice(transactionHandler,
                                    dictionary,
                                    caChoice,
                                    ca,
                                    dbAction)
                update = True
            transactionHandler.caChoices.append((caChoice, update))


class _CreateorUpdateFCorporateActionPayout(_CreateOrUpdateBase):
    """
    """
    def __init__(self, log, markitImportUsers):
        _CreateOrUpdateBase.__init__(self, log, markitImportUsers)

    def end(self):
        _CreateOrUpdateBase._end(self)

    def IdentifySecurityID(self,x,d):
        return {
            d['Payout Security ID Type']: d['Payout Security ID'],
            d['Payout Security Id Type']: d['Payout Security Id']
        }.get(x, None)

    def ValidateRecordInfo(self, dictionary):
        if dictionary['Payout Status'] == 'DE':
            payoutName = ' '.join([dictionary['Payout Number'], dictionary['Option Number'], dictionary['CA ID']])
            logMessage = 'Ignored corp action payout{}, as its status is \'DE\'.'.format(payoutName)
            self._logWarning(logMessage)
            return False

        return True


    def FillInCaPayout(self, dictionary, transactionHandler, caChoice, caPayout, dbAction):
        ca = transactionHandler.corporateAction
        div = transactionHandler.caDividend
        if div:
            divCurrency = acm.FCurrency[dictionary['Currency Code']]
            if ca.Instrument().Currency() == divCurrency:
                div.Amount(dictionary['Payout Gross Amount'])
                div.TaxFactor(1)
                div.Currency(divCurrency)
        caPayout.CaChoice(caChoice)
        caPayout.PayoutRate(dictionary['Payout Rate'])
        if isOverSubscription(caChoice) and ChoiceHasOnlyOnePayout(transactionHandler, dictionary['Option Number']):
            caPayout.PayoutRate(1.0)
        caPayout.PayoutAmount(dictionary['Payout Amount'])
        caPayout.PayoutNetAmount(dictionary['Payout Net Amount'])
        caPayout.PayoutGrossAmount(dictionary['Payout Gross Amount'])
        sec = self.FindIdentifyingSecurity(dictionary)
        caPayout.NewInstrument(sec)
        caPayout.Currency(acm.FCurrency[dictionary['Currency Code']])
        caPayout.Price(dictionary['Price'])
        if dictionary['Price Currency']:
            caPayout.PriceCurrency(dictionary['Price Currency'])

        caPayout.Fee(dictionary['Fee'])
        caPayout.FeeCurrency(acm.FCurrency[dictionary['Fee Currency']])
        payoutName = ' '.join([dictionary['Payout Number'], dictionary['Option Number'], dictionary['CA ID']])
        caPayout.Name(payoutName)
        textObjectName = 'caPayout: ' + ca.Name() + ' ' + dictionary['Payout Number'] + ' ' + dictionary['Option Number']
        textObject = acm.FCustomTextObject[textObjectName]
        if textObject:
            caPayout.SourceRecord(textObject)
            UpdateFPersistentTextObject(dictionary, textObject)
        else:
            textObject = CreateFPersistentTextObject(dictionary, textObjectName)
            caPayout.SourceRecord(textObject)
        transactionHandler.caPayoutTextObjects.append(textObject)
        logMessage = ('    {} Corporate Action Payout '
                    'for Corporate Action Choice {}, '
                    'Corporate Action {}'.format(
                        dbAction.capitalize()[:-1] + 'ed',
                        caChoice.Name().strip(), 
                        transactionHandler.corporateAction.Name()))

        transactionHandler.logOks.append((logMessage, dbAction))
        transactionHandler.summaryOks.append((caPayout, dbAction))


    def FindAndCorrectPayout(self, dictionary, caChoice, transactionHandler):

        ca_payout = None
        ca_payouts = [payout for payout in caChoice.CaPayouts()
                    if payout.Name()[0] == dictionary['Payout Number']]
        if len(ca_payouts) == 1:
            ca_payout = ca_payouts[0]
        elif len(ca_payouts) > 1:
            # There may be too many payouts in the DB, due to incorrect imports.
            ca_payouts.sort(key = lambda obj: obj.Oid())
            for payout in ca_payouts[1:]:
                transactionHandler.caPayoutsToBeDeleted.append(payout.Oid())
            ca_payout = ca_payouts[0]
        return ca_payout


    def _perform(self,
                dictionary,
                overrideExisting,
                createNew,
                transactionHandler):
        # CaChoices and CaPayouts are depended on coprorate action object
        # if there is on corporate action object,
        # processing of caChoices and caPayouts objecs is not possible
        if not transactionHandler.corporateAction:
            return

        if not self.ValidateRecordInfo(dictionary):
            return
        
        caChoice = transactionHandler.GetCaChoiceFromTransactonCache(
                                            dictionary['Option Number'])
        if not caChoice:
            payoutName = ' '.join([dictionary['Payout Number'], dictionary['Option Number'], dictionary['CA ID']])
            logMessage = 'Ignored corp action payout{}, as it has no choice.'.format(payoutName)
            self._logWarning(logMessage)
            return

        caPayout = self.FindAndCorrectPayout(dictionary, caChoice, transactionHandler)

        dbAction = None
        if not caPayout and createNew:
            dbAction = 'CREATE'
            caPayout = acm.FCorporateActionPayout()
        elif caPayout and overrideExisting:
            dbAction = 'UPDATE'
            if caPayout and not self.CanUpdateRecord(caPayout):
                dbAction = 'UPDATE_IGNORED'
                payoutName = ' '.join([dictionary['Payout Number'], dictionary['Option Number'], dictionary['CA ID']])
                logMessage = 'Ignored corp action payout{}, as it has been manually updated by {}.'.format(payoutName, caPayout.UpdateUser().Name())
                self._logWarning(logMessage)

        if dbAction:
            update = False
            if dbAction != 'UPDATE_IGNORED':
                self.FillInCaPayout(dictionary,
                                transactionHandler,
                                caChoice,
                                caPayout,
                                dbAction)
                update = True
            transactionHandler.caPayouts.append((caPayout, update))


#MarkitDataMapping
def CreateFPersistentTextObject(d, name):
    textObject = acm.FCustomTextObject()
    textObject.Name(name)
    textObject.SubType('Customizable')
    textObject.Text(str({k: v for k, v in d.items() if v.lstrip()}))
    return textObject


def UpdateFPersistentTextObject(d, textObject):
    textObject.Text(str({k: v for k, v in d.items() if v.lstrip()}))


def CopySummary(log):
    for key, value in Summary().tables.iteritems():
        if key == (' ', ' '):
            continue
 
        for fId in value.get('okIds', []):
            log.summaryAddOk\
            (
                recType = key[0], 
                oid = fId, 
                action = key[1].upper()
            )

        for fId, reasons in value.get('failed', []):
            log.summaryAddFail\
            (
                recType = key[0], 
                oid = fId, 
                action = key[1].upper(), 
                reasons = reasons
            )

