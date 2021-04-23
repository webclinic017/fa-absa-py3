import acm
import ael
'''ccpSetup: Setup of all values needed for the Central CounterParty clearing
  and Arena MarkitWire Integration solution. First ChoiceLists are defined,
  then the AdditionalInfoSpecs.
  Source for the data is the table in section ADM Changes from the AMWI System
  description document.
'''
disableMWWireStatus = False
def getACMVersion():
    version = acm.Version()    
    indexPos = version.find(',')
    if indexPos != -1:
        versionNumber = version[0:indexPos]
        indexPos = versionNumber.find('.')
        indexPos1 = versionNumber.find('.', indexPos + 1)
        if indexPos1 > -1:
            versionNumber = versionNumber[0: indexPos1]
        return float(versionNumber)
    else:
        return float(version)
        
        
if getACMVersion() < 2009.2:    
    import AMWI2_2

import FLogger
log = FLogger.FLogger.GetLogger('CCPSetup')

def ccpName(aName):
    'Name can only be 19 characters, so cut after 16'
    name = aName
    if aName not in ['UTI_1part', 'UTI_2part', 'priorUTI_1part', 'priorUTI_2part', 'prior_middleware', 'mwire_sideid', 'prior_mwire_side', 'regClearingTime', 'regConfirmationTime']:
	'Add CCP as a prefix.'
	name = aName[:16]
        name = 'CCP'+aName[:16]
    return name
    
def parseTable(tableName):
    '''Split excelTable. Only returns AdditionalInfo lines. Return is list of
    tuples: (Name, Description, grpS, part, xxx).
    '''
    attrList = []
    excelTable = ''
    if tableName == 'Trade':

        excelTable = """
clearing_process	Trade.AdditionalInfo	Categorization of clearing process, or workflow. Can control e.g. TradeStatus paths and other status transitions.	Ref(ChoiceList):CCPWorkFlow. Bilateral, LCH.Clearnet, CME	Could be a link to a workflow control table
middleware_ptynbr	Trade.AdditionalInfo	Reference to Party with information for the Middleware that the trade will be sent through	Ref(Party)
middleware_id	Trade.AdditionalInfo	Reference key in middleware system	String
middleware_version	Trade.AdditionalInfo	Version number of Instrument + Trade, as set by and stored in the Middleware	String
clearing_status	Trade.AdditionalInfo	Common status for all middleware (MW, ICE, etc).	Ref(ChoiceList):CCPClearingStatus. Pending, Alleged, Affirmed, Confirmed, Disputed, Rejected,  LockedUs, LockedThem, Affirming, Pulling, Releasing, Submitting, Withdrawing, Initiated, Ready, PickedUp, Affirmed, CptyAffirmed, Recalled, PrimaryAgreed, Agreed, Released, CHSubmitted, CHAcknowledged, Registered, Cleared, Received, Accepted, Rejected, Withdrawn, Error,
mwire_contract_status	Trade.AdditionalInfo	Status to capture MarkitWire API status "Contract Status"	String
mwire_process_status	Trade.AdditionalInfo	Status to capture MarkitWire API status "Process Status"	String
mwire_booking_status	Trade.AdditionalInfo	Status to capture MarkitWire API status "Post Release Status"	String
mwire_message_status	Trade.AdditionalInfo	Status to capture MarkitWire API status "Message Status"	String
mwire_new_status 	Trade.AdditionalInfo	Status to capture MarkitWire API status "New Status"	String
clr_broker_ptynbr	Trade.AdditionalInfo	Reference to clearing broker	Ref(Party)	SPR324832
clr_broker_id	Trade.AdditionalInfo	Reference key in broker system. This might not be received or used	String	Might not be needed
clr_broker_status	Trade.AdditionalInfo	Trade status to reflect clearing broker's acceptance of  the trade.	Ref(ChoiceList):CCPcbStatus. Pending, Accepted, Rejected
original_counterparty	Trade.AdditionalInfo	Reference to orginal party, once this trade has cleared to CCP	Ref(Party)
ccp_ptynbr	Trade.AdditionalInfo	Reference to clearing house	Ref(Party)	SPR324832
ccp_id	Trade.AdditionalInfo	ID at clearing house	String
ccp_status	Trade.AdditionalInfo	Trade status to reflect the clearing house's acceptance of  the trade.	Ref(ChoiceList):CCPstatus. Pending, Matched, Cleared, Rejected
tdr_ptynbr	Trade.AdditionalInfo	Reference to trade document repository	Ref(Party)
tdr_id	Trade.AdditionalInfo	ID at repository	string
tdr_status	Trade.AdditionalInfo	Trade status to reflect the repository's acceptance of the trade	Ref(ChoiceList):CCPtdrStatus. Pending, Accepted, Rejected
mwire_user_msg	Trade.AdditionalInfo	User Message on deal	String
priorUTI_1part	Trade.AdditionalInfo	Prior Unique Trade Identifier first 39 char	String
priorUTI_2part	Trade.AdditionalInfo	Prior Unique Trade Identifier last 13 char	String
prior_middleware	Trade.AdditionalInfo	Reference key in prior middleware system	String
mwire_sideid	Trade.AdditionalInfo	Reference to the side id	String
prior_mwire_side	Trade.AdditionalInfo	Reference to the side id	String
regConfirmationTime	Trade.AdditionalInfo	Time when trade was confirmed, if Confirmation records are not used	Time
regClearingTime	Trade.AdditionalInfo	Time when trade was cleared, if Settlement records are not used	Time
"""
        if getACMVersion() < 2015.3:
            UTIAddInfos = """
UTI_1part	Trade.AdditionalInfo	Unique Trade Identifier first 39 char	String
UTI_2part	Trade.AdditionalInfo	Unique Trade Identifier last 13 char	String
"""
            excelTable = excelTable + UTIAddInfos
    elif tableName == 'Party':        
        if getACMVersion() >= 2012.1:
            excelTable = """
is_tdr	Party.AdditionalInfo	Is the Party a Trade Documentation Repository	Boolean
"""
        else:
            excelTable = """
is_clearing_broker	Party.AdditionalInfo	Is the Party a Clearing Broker	Boolean
is_tdr	Party.AdditionalInfo	Is the Party a Trade Documentation Repository	Boolean
is_ccp	Party.AdditionalInfo	Is the Party a Central Counterparty clearing house	Boolean
is_middleware	Party.AdditionalInfo	Is the Party a middleware, like MarkitWire	Boolean
"""
    elif tableName == 'StateChart':
        if getACMVersion() >= 2012.1:
            excelTable = """
perspective	StateChart.AdditionalInfo	Clearing perspective	Ref(ChoiceList):CCPPerspective. T2ExecutionBroker, T2Client, T2ClearingBroker, DirectDeal, AmendOrCancelDirectDeal, DirectDealNovationStepOut, DirectDealNovationRemaining
"""
    else:
        print 'No definition for table', tableName
        excelTable = ''

    for line in excelTable.split('\n'):
        if line == '': continue
        array = line.split('\t')
        if 0: #Set to debug
            for i in range(5):
                print i, array[i]
                pass
        name = ccpName(array[0])                
        if disableMWWireStatus and name.startswith('CCPmwire'): 
            continue        
        try:
            tab, aiString = array[1].split('.')            
            if aiString != 'AdditionalInfo': 
                print name, 'not an AddInfo'
                continue
        except:
            print 'Error in', array[1]
            continue

        ais = acm.FAdditionalInfoSpec[name]        
        if not ais:
            print "Creating additional info spec <%s>"%(name)
            ais = acm.FAdditionalInfoSpec()
            ais.FieldName = name
            description = array[2]            
            excType = array[3]
            if excType.capitalize() in ['String', 'Boolean', 'Time']:
                grpS = 'Standard'
                typ = acm.FEnumeration['enum(B92StandardType)'].Enumeration(excType.capitalize())
            elif excType[:4].capitalize() == 'Ref(':
                grpS = 'RecordRef'
                part = excType[4:]
                refType = part[:part.find(')')]
                if refType == 'ChoiceList':
                    # Format of Excel description is like "Ref(ChoiceList):Colours. For example Blue, Red, Green"
                    # For ChoiceList references, write reference table in "Description"
                    description = part[part.find(':')+1 : part.find('.')]
                typ = acm.FEnumeration['enum(B92RecordType)'].Enumeration(refType)
            else:
                print 'Nope:', excType
                continue
            ais.DataTypeGroup(acm.FEnumeration['enum(B92DataGroup)'].Enumeration(grpS))
            ais.DataTypeType(typ)
            ais.Description = description
            ais.RecType(tab)
            ais.Commit()            
        description = array[2]
        excType = array[3]
        excType = excType.strip()
        part, typ, clName, values, refType = None, None, None, None, None # Defaults
        if excType.capitalize() in ['String', 'Boolean', 'Time']:
            grpS = 'Standard'
            typ = acm.FEnumeration['enum(B92StandardType)'].Enumeration(excType.capitalize())
        elif excType[:4].capitalize() == 'Ref(':
            grpS = 'RecordRef'
            part = excType[4:]
            refType = part[:part.find(')')]
            if refType == 'ChoiceList':
                # Format of Excel description is like "Ref(ChoiceList):Colours. For example Blue, Red, Green"
                # For ChoiceList references, write reference table in "Description"
                description = part[part.find(':')+1 : part.find('.')]
                values = part[part.find('.')+1:].lstrip()                
            typ = acm.FEnumeration['enum(B92RecordType)'].Enumeration(refType)
        else:
            print 'Nope:', excType
            continue
        attrList.append((tab, name, description, excType, grpS, typ, refType, values))
    return attrList


def translateChoiceListEntry(chlName, list):
    'Front Arena 2.2 allows only 19 char ChoiceList.Entry. Substitute below'
    substDict = AMWI2_2.getLookUpForStatus()
    ret = 'None'
    if chlName[:19] == chlName:
        ret = chlName        
    elif list in substDict.keys():        
        if chlName in substDict[list].keys():
            ret = substDict[list][chlName]            
        else:
            log.ELOG('Unknown ChoiceList (%s:%s)' % (list, chlName))
            print 'Too long', chlName, len(chlName)    
    return ret

def addChoiceListValue(key,val,descr='',sortO=0):
    'Add a new ChoiceList entry. But cut off and translate for 2.2'
    changedName = val.strip()
    if getACMVersion() < 2009.1: # TODO: Test for Front Arena 2.2
        changedName = translateChoiceListEntry(val, key)        
    query = "list = '%s' and name = '%s'" %(key, changedName)    
    clval = acm.FChoiceList.Select(query)    
    if not clval:
        try:
            print "Adding <%s> in <%s> ChoiceList"%(changedName, key)            
            newcl = acm.FChoiceList()
            newcl.List = key    
            newcl.Name = changedName        
            if descr: newcl.Description(descr)
            if sortO: newcl.SortOrder(sortO)            
            newcl.Commit()    
        except Exception, e:
            print "in addChoiceListValue for ", val
            print e
   
def AddChoiceListWithTranslations():
    print 40*'-'
    tableArr = ['Trade', 'Party', 'StateChart']
    for table in tableArr:
        for c in parseTable(table):
            if c[6] == 'ChoiceList':
                for e in c[7].split(", "):                
                    addChoiceListValue(c[2], e)
                
def AddDocumentationChoiceList():
    key = 'Standard Document'
    choiceListName = ['AFB/FBF|ISDA2000', 'AFB/FBF|ISDA2006', 'DERV|ISDA2000', 'DERV|ISDA2006', 'ISDA|ISDA2000', 'ISDA|ISDA2006', 'ISDA|ISDA2003Credit', 'EquitySwapGlobalPrivate|2007-01-01', 'EquitySwapAEJPrivate|2007-01-01', 'ISDA2009EquityEuropeanInterdealer|2007-01-01', 'ISDA2009EquitySwapPanAsia|2007-01-01', '2003CreditIndex', '2004EquityEuropeanInterdealer', '2005VarianceSwapEuropeanInterdealer', '2006DividendSwapEuropean', '2006DividendSwapEuropeanInterdealer', 'DJ.CDX.EM', 'DJ.CDX.EM.DIV', 'DJ.CDX.NA', 'DJ.iTraxx.Europe', 'EquityAmericas', 'EquityAsia', 'EquityEuropean', 'ISDA1999Credit', 'ISDA2003CreditAsia', 'ISDA2003CreditAustraliaNewZealand', 'ISDA2003CreditEuropean', 'ISDA2003CreditJapan', 'ISDA2003CreditNorthAmerican', 'ISDA2003CreditSingapore', 'ISDA2003CreditSovereignAsia', 'ISDA2003CreditSovereignCentralAndEasternEurope', 'ISDA2003CreditSovereignJapan', 'ISDA2003CreditSovereignLatinAmerica', 'ISDA2003CreditSovereignMiddleEast', 'ISDA2003CreditSovereignWesternEurope', 'ISDA2003StandardCreditAsia', 'ISDA2003StandardCreditAustraliaNewZealand', 'ISDA2003StandardCreditEuropean', 'ISDA2003StandardCreditJapan', 'ISDA2003StandardCreditNorthAmerican', 'ISDA2003StandardCreditSingapore', 'ISDA2004CreditSovereignAsia', 'ISDA2004CreditSovereignEmergingEuropeanAndMiddleEastern', 'ISDA2004CreditSovereignJapan', 'ISDA2004CreditSovereignLatinAmerican', 'ISDA2004CreditSovereignWesternEuropean', 'ISDA2004EquityAmericasInterdealer', 'ISDA2004EquityAmericasInterdealerRev1', 'ISDA2004StandardCreditSovereignAsia', 'ISDA2004StandardCreditSovereignEmergingEuropeanAndMiddleEastern', 'ISDA2004StandardCreditSovereignJapan', 'ISDA2004StandardCreditSovereignLatinAmerican', 'ISDA2004StandardCreditSovereignWesternEuropean', 'ISDA2005EquityAsiaExcludingJapanInterdealer', 'ISDA2005EquityAsiaExcludingJapanInterdealerRev2', 'ISDA2005EquityJapaneseInterdealer', 'ISDA2006VarianceSwapJapanese', 'ISDA2006VarianceSwapJapaneseInterdealer', 'ISDA2007EquityEuropean', 'ISDA2007VarianceSwapAmericas', 'ISDA2007VarianceSwapAsiaExcludingJapan', 'ISDA2007VarianceSwapAsiaExcludingJapanRev1', 'ISDA2007VarianceSwapAsiaExcludingJapanRev2', 'ISDA2007VarianceSwapEuropean', 'ISDA2007VarianceSwapEuropeanRev1', 'ISDA2008DividendSwapJapan', 'ISDA2008DividendSwapJapaneseRev1', 'ISDA2008EquityAmericas', 'ISDA2008EquityAsiaExcludingJapan', 'ISDA2008EquityAsiaExcludingJapanRev1', 'ISDA2008EquityJapan', 'ISDA2009EquityAmericas', 'ISDA2009EquityEuropeanInterdealer', 'ISDA2009EquityPanAsia', 'ISDA2010EquityEMEAInterdealer']
    for eachName in choiceListName:
        query = "list = '%s' and name ='%s'" %(key, eachName[0:39])        
        clval = acm.FChoiceList.Select(query)
        if not clval:
            print "Adding <%s> in <%s> ChoiceList"%(eachName, key)
            try:
                newcl = acm.FChoiceList()
                newcl.List = key
                newcl.Name = eachName
                newcl.Commit()
            except Exception, e:
                print e
'''
def renameInChoiceList(choiceList, OldValue, ReplaceValue):
    oldQry = "list = '%s' and name = '%s'" %(choiceList, OldValue)
    newQry = "list = '%s' and name = '%s'" %(choiceList, ReplaceValue)
    newChoiceExists = acm.FChoiceList.Select(newQry)
    Oldchoices = acm.FChoiceList.Select(oldQry)
    if not newChoiceExists:
        if Oldchoices:
            for oldChoice in Oldchoices:
                clonedObj = oldChoice.Clone()
                clonedObj.Name(ReplaceValue)
                oldChoice.Apply(clonedObj)
                oldChoice.Commit()
    else:
        for oldChoice in Oldchoices:
            oldChoice.Delete()

def renameParamInChoiceList():
    renameInChoiceList('CCPMidWstatus', 'UsLocked', 'LockedUs')
    renameInChoiceList('CCPMidWstatus', 'ThemLocked', 'LockedThem')
    renameInChoiceList('MASTER', 'CCPMidWstatus', 'CCPClearingStatus')

def removeRedundantChoiceList(choicelist):
    clval = acm.FChoiceList.Select("list = '%s'" %choicelist)
    if clval:
        clval.Delete()
    clval = acm.FChoiceList.Select("list = 'MASTER' and name = '%s'" %choicelist)
    if clval:
        clval.Delete()

def removeParametersInChoiceList(clDict):
    for key in clDict.keys():        
        master = acm.FChoiceList.Select("list='MASTER' and name='%s'" % key)        
        if master:
            for val in clDict[key].split(", "):
                clval = acm.FChoiceList.Select("list='%s' and name='%s'" % (key,val))            
                if clval:                    
                    clval.Delete()                

def removeParamInChoiceList():
    clDict = {'MWstatus':  """Exercised-Cash/Exercised-Physical, Pending""", 
               'MWprocessStatus': """Affirm, CptyAffirm, PickedUp, Pulled, RegisteredForClearing, Sent, SentForClearing""" } 
    removeParametersInChoiceList(clDict)
    removeRedundantChoiceList('MWpostreleaseStatus')

'''
def renameRedundantAdditionalInfoSpec(oldValue, newValue, description):
    ais = acm.FAdditionalInfoSpec[oldValue]
    ais_booking = acm.FAdditionalInfoSpec[newValue]
    if ais_booking and ais:
        ais.Delete()
    else:
        if ais:
            cloned_ais = ais.Clone()
            cloned_ais.FieldName(newValue)
            cloned_ais.Description(description)
            ais.Apply(cloned_ais)
            ais.Commit()
'''
def renameAdditionalInfoSpec():
    renameRedundantAdditionalInfoSpec('CCPmwire_postreleas', 'CCPmwire_booking_st', 'MWbookingStatus')
    renameRedundantAdditionalInfoSpec('CCPmiddleware_statu', 'CCPclearing_status', 'CCPClearingStatus')

def renameChoiceList():
    renameList = {}
    renameList['CCPMidWstatus'] = 'CCPClearingStatus'
    for renameObj in renameList:        
        qry = "list = '%s'"%renameList[renameObj]
        existChoices = acm.FChoiceList.Select(qry)        
        query = "list = '%s'"%renameObj
        choices = acm.FChoiceList.Select(query)
        if not existChoices:        
            for choice in list(choices):
                clonedObj = choice.Clone()
                clonedObj.List('CCPClearingStatus')
                choice.Apply(clonedObj)
                choice.Commit()
        else:
            for choice in list(choices):
                choice.Delete()
'''
def renameBussinessCenter():
    oldValue = 'CCPBusinessCentre'
    newValue = 'CCPBusinessCenter'
    description = '''4 character description of calendar constructed from ISO country code + city name. 
                Used in FpML and SWIFT. N.B. Calendar AddInfo do not have access through GUI    
                String    SPR324685, calendar attribute''' 
    
    ais_new = acm.FAdditionalInfoSpec[newValue]
    
    if ais_new:
        return
    
    ais = acm.FAdditionalInfoSpec[oldValue]
        
    if ais:
        cloned_ais = ais.Clone()
        cloned_ais.FieldName(newValue)
        cloned_ais.Description(description)
        ais.Apply(cloned_ais)
        ais.Commit()

def setChoiceList(clDict):
    for key in clDict.keys():        
        master = acm.FChoiceList.Select("list='MASTER' and name='%s'" % key)
        if not master:
            addChoiceListValue('MASTER', key)            
        added = []
        for val in clDict[key].split(", "):
            clval = acm.FChoiceList.Select("list='%s' and name='%s'" % (key, val))
            if not clval:
                addChoiceListValue(key, val)
                added.append(val)
        if added:            
            added = []

def setChoiceLists():
    clDict = {} 
    tableArr = ['Trade', 'Party', 'StateChart']
    for table in tableArr:
        for tab, name, clName, e, g, t, refType, values in parseTable(table):
            if refType == 'ChoiceList':
                clDict[clName] = values
        setChoiceList(clDict)
    '''
    clDict = {    
    'MWbookingStatus':"""Pending, Withdrawn, Done, Released, Received, Validated, Cleared, Error, Expired, Novated""",
    }    
    setChoiceList(clDict) 
    '''
'''
def AddValuesToChoiceList():

    clDict = {'CCPClearingStatus':  """Initiated, Ready, PickedUp, Affirmed, CptyAffirmed, Recalled, PrimaryAgreed, Agreed, Released, CHSubmitted, CHAcknowledged, Registered, Cleared, Received, Accepted, Rejected, Withdrawn, Error,""",
               'MWnewStatus': """RequestRevision""" } 
    setChoiceList(clDict)
'''
'''    
def correctChoiceLists():
    'Correct the odd ChoiceList values which were erroneously defined originally'
    clDict = {'MWstatus': { 'New_PrimeBrokered': 'New-PrimeBrokered','New_Novated':'New-Novated'}}
    for cList in clDict.keys():
        cDict = clDict[cList]
        for wrongName in cDict.keys():
            clvalList = acm.FChoiceList.Select("list='%s' and name='%s'" % (cList,wrongName))
            if clvalList: #List has 0 or 1 entries
                clval = clvalList[0]
                clval.Name(cDict[wrongName])
                print 'For',cList,'changed',wrongName,'to',cDict[wrongName]
'''
def correctAddInfo():
    'Correct AddInfo names which were changed'
    changed = False
    aiDict = {'is_tiw': 'is_tdr', 'tiw_ptynbr':'tdr_ptynbr',
        'tiw_status':'tdr_status', 'tiw_id':'tdr_id' }
    for name in aiDict.keys():
        cName = ccpName(name)
        ais = acm.FAdditionalInfoSpec[cName]
        if ais:
            ais.Name(ccpName(aiDict[name]))            

def deleteObsoleteAdditionalInfos():
    addinfos = ['CCPtdr_SWMLStatus', 'CCPpartyContact']
    for addInfo in addinfos:
        ais = acm.FAdditionalInfoSpec[addInfo]
        if ais:
            ais.Delete()

def createPartyAliasType(aliasTypeName):
    aliasType = acm.FPartyAliasType[aliasTypeName]
    if not aliasType:
        aliasType = acm.FPartyAliasType()
        aliasType.AliasTypeName(aliasTypeName)
        aliasType.Name(aliasTypeName)
        aliasType.Type('Party')
        aliasType.Commit()

def renameInstrumentAliasSpec(oldName, newName):
    ais = acm.FInstrAliasType[oldName]
    if ais:
        cloned_ais = ais.Clone()
        cloned_ais.Name(newName)
        ais.Apply(cloned_ais)
        ais.Commit()
        
def createInsAliasType(oldName, newName):
    ais = acm.FInstrAliasType[oldName]
    if ais:
        renameInstrumentAliasSpec(oldName, newName)
    else:
        ais = acm.FInstrAliasType[newName]
        if not ais:
            ais = acm.FInstrAliasType()
            ais.Name(newName)
            ais.Commit()

def changeAddInfoSpec():
    addInfoSpecs = ['CCPclearing_process', 'CCPclearing_status', 'CCPmwire_booking_st', 'CCPmwire_contract_s', 'CCPmwire_message_st', 'CCPmwire_new_status', 'CCPmwire_process_st']
    for addInfoSpecName in addInfoSpecs:
        addInfoSpec = acm.FAdditionalInfoSpec[addInfoSpecName]
        addInfoSpec.DataTypeGroup(acm.FEnumeration['enum(B92DataGroup)'].Enumeration('Standard'))
        addInfoSpec.DataTypeType(acm.FEnumeration['enum(B92StandardType)'].Enumeration('String'))
        addInfoSpec.Commit()        
'''
def removeChoiceLists():
    choiceListsToDelete = ['MWbookingStatus', 'MWmessageStatus', 'MWnewStatus', 'MWprocessStatus', 'MWstatus', ]
    for choicelistToDelete in choiceListsToDelete:
        choicelist = list(acm.FChoiceList.Select("list=%s"%choicelistToDelete))
        for choiceEntry in choicelist:
            choiceEntry.Delete()    
        acmChoiceList = acm.FChoiceList[choicelistToDelete]
        if acmChoiceList:
            acmChoiceList.Delete()
'''
def addUSIAddInfos():
    if getACMVersion() < 2013.1: 
        names = ['USI_Issuer', 'USI_Identifier']
        for name in names:
            ais = acm.FAdditionalInfoSpec[name]        
            if not ais:
                print "Creating additional info spec <%s>"%(name)
                ais = acm.FAdditionalInfoSpec()
                ais.FieldName = name
                ais.DataTypeGroup(acm.FEnumeration['enum(B92DataGroup)'].Enumeration('Standard'))
                ais.DataTypeType(acm.FEnumeration['enum(B92StandardType)'].Enumeration('STRING'))
                ais.Description = name
                ais.RecType('Trade')
                ais.Commit()

def createTradeAliasType():
    if getACMVersion() >= 2013.1:
        aliasName = 'USI'
        aliasType = acm.FTradeAliasType[aliasName]
        if not aliasType:
            aliasType = acm.FTradeAliasType()
            aliasType.AliasTypeName(aliasName)
            aliasType.AliasTypeDescription('USI Details on a trade')
            aliasType.Commit()

def migrateUTIAddInfoToAttribute():
    if getACMVersion() >= 2015.3:
        ais_uti1 = acm.FAdditionalInfoSpec['UTI_1part']
        ais_uti2 = acm.FAdditionalInfoSpec['UTI_2part']
        if ais_uti1:
            aiSels = acm.FAdditionalInfo.Select('addInf=%d'%ais_uti1.Oid())
            while aiSels:
                for aiSel in list(aiSels):
                    if aiSel.RecType() == 'Trade':
                        print aiSel.FieldValue()
                    trd = acm.FTrade[aiSel.Recaddr()]
                    if trd:
                        uti_2part = trd.AdditionalInfo().UTI_2part()
                        if not trd.UniqueTradeIdentifier():
                            if uti_2part:
                                trd.UniqueTradeIdentifier(aiSel.FieldValue() + uti_2part)
                            else:
                                trd.UniqueTradeIdentifier(aiSel.FieldValue())
                            trd.Commit()
                        uti_2partAddInfo = acm.FAdditionalInfo.Select('addInf=%d and recaddr=%d'%(ais_uti2.Oid(), aiSel.Recaddr()))
                        if uti_2partAddInfo:
                            uti_2partAddInfo[0].Delete()
                    aiSel.Delete()
                try:
                    ais_uti1.Delete()
                    ais_uti2.Delete()
                except Exception, e:
                    aiSels = acm.FAdditionalInfo.Select('addInf=%d'%ais_uti1.Oid())
            ais_uti1.Delete()
            ais_uti2.Delete()


def rename_statecharts():
    """ Rename StateCharts and update CCPWorkflow ChoiceList to new StateChart names"""
    
    sc_names = [('LCH.Clearnet_T2_CB', 'LCH_Clearnet_T2_CB'), ('LCH.Clearnet_T2_Client', 'LCH_Clearnet_T2_Client'), ('LCH.Clearnet_T2_EB', 'LCH_Clearnet_T2_EB'), ('Amend/CancelDirectDeal', 'AmendOrCancelDirectDeal')]

    for name in sc_names:
        sc = acm.FStateChart[name[0]]
        if sc:
            sc.Name(name[1])
            sc.Commit()
    
    # Change the CCPWorkFlow ChoiceList entry to new SC name
    for name in sc_names:
        query = "list = '%s' and name = '%s'" %('CCPWorkFlow', name[0])
        Choice_list_entry = acm.FChoiceList.Select01(query, '')

        new_choice_query = "list = '%s' and name = '%s'" %('CCPWorkFlow', name[1])
        New_list_entry = acm.FChoiceList.Select01(new_choice_query, '')

        if Choice_list_entry and not New_list_entry:
            Choice_list_entry.Name(name[1])
            Choice_list_entry.Commit()
        


print "Execution of ccpSetup script started..."
renameBussinessCenter()
AddChoiceListWithTranslations()
setChoiceLists()
#correctChoiceLists()
correctAddInfo()
#renameAdditionalInfoSpec()
#renameChoiceList()
#renameParamInChoiceList()
#removeParamInChoiceList()
AddDocumentationChoiceList()
#AddValuesToChoiceList()
#deleteObsoleteAdditionalInfos()
createPartyAliasType('MarkitWireID')
createInsAliasType('MarkitWire', 'ISDAIndexTenor')
createTradeAliasType()
changeAddInfoSpec()
#removeChoiceLists()
addUSIAddInfos()
migrateUTIAddInfoToAttribute()
rename_statecharts()
print "Execution of ccpSetup script complete!"





