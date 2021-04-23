"""GenerateRegulatoryIdMapping - Task to generate the file with Party/Contact/Person
identifers to be read by the RegulatoryId service on the AIMS to map the
TNP Client and Account keys and identifiers, namely: 
exchangeID (TNP: RegulatoryId), CrmId, LEI, CustomerType and possibly an 
LSE ID (for a TRADEcho APA) or BATS ID (for a BATS/CBOE APA)
Version: 0.4"""

import acm
import FBDPGui
import FRegulatoryLogger
logger = 'GenerateRegulatoryMappingId'
#import FBDPCommon

# Menu parameters:
# IdFileName String
# GeneratePersonIds Bool
# CustomerTypeMandatory True/Warn/False
# ExchangeIdMandatory True/Warn/False
# CrmIdMandatory True/Warn/False
# PartyLeiMandatory True/Warn/False
# LSEIdAdd Bool
# BATSIdAdd Bool

def searchParties(eP, accTupList = [], searchString = ''):
    """search all parties within ADS and return their CrmId, ExchangeId and MiFIDCategory"""
    tupList = accTupList
    for p in acm.FParty.Select(searchString):
        lei = p.LEI()
        if not lei:
            if eP['PartyLeiMandatory'] == 'Warn': 
                FRegulatoryLogger.WARN(logger, 'Party "%s" is missing an LEI' %p.Name())
            elif eP['PartyLeiMandatory'] == 'True': 
                continue # Only take parties with LEI
        pr = p.RegulatoryInfo()
        clienttype = pr.MiFIDCategory()
        if not clienttype and eP['CustomerTypeMandatory'] in ['True', 'Warn']: 
            if eP['CustomerTypeMandatory'] == 'Warn': 
                FRegulatoryLogger.WARN(logger, 'Party "%s" (LEI:%s) missing MiFIDCategory' %(p.Name(), lei))#
            elif eP['CustomerTypeMandatory'] == 'True': 
                break
        exchid = pr.ExchangeId()
        if not exchid:
            exchid = 0 # Integer value
            if eP['ExchangeIdMandatory'] == 'Warn': 
                FRegulatoryLogger.WARN(logger, 'Party "%s" (LEI:%s) missing ExchangeId' %(p.Name(), lei))
            elif eP['ExchangeIdMandatory'] == 'True': 
                break
        crmid = pr.CrmId()
        if not crmid:
            if eP['CrmIdMandatory'] == 'Warn':
                FRegulatoryLogger.WARN(logger, 'Party "%s" (LEI:%s) missing CRM Id' %(p.Name(), lei))
            elif eP['CrmIdMandatory'] == 'True': 
                break
        if eP['LSEIdAdd']:
            lseid = p.PartyAlias().LSE()
        else: 
            lseid = ''
        if eP['BATSIdAdd']:
            batsid = p.PartyAlias().BATS()
        else: batsid = ''
        FRegulatoryLogger.INFO(logger, 'Appending %s'%p.Name())
        tupList.append((lei, clienttype, exchid, crmid, lseid, batsid))
    return tupList

def searchContacts(eP, accTupList = [], searchString = ''):
    """search all Contacts/Persons within ADS and return their CrmId and ExchangeId"""
    tupList = accTupList
    for c in acm.FContact.Select(searchString):
        cr = c.RegulatoryInfo()
        exchid = cr.ExchangeId()
        crmid = cr.CrmId()
        pers = c.Person()
        if pers:
            if pers.CrmId():
                crmid = pers.CrmId()
            if pers.ExchangeId():
                exchid = pers.ExchangeId()
        if not exchid:
            exchid = 0 # Integer value
            if eP['ExchangeIdMandatory'] == 'Warn':
                FRegulatoryLogger.WARN(logger, 'Contact "%s" (%s) missing ExchangeId' %(c.Name(), c.Party().Name()))
            elif eP['ExchangeIdMandatory'] == 'True': 
                break
        if not crmid:
            if eP['CrmIdMandatory'] == 'Warn':
                FRegulatoryLogger.WARN(logger, 'Contact "%s" (%s) missing CRM Id' %(c.Name(), c.Party().Name()))
            elif eP['CrmIdMandatory'] == 'True': 
                break
        if exchid and crmid:
            FRegulatoryLogger.INFO(logger, 'Appending %s' %c.Name())
            tupList.append(('', '', exchid, crmid, '', ''))
    return tupList


def writeFile(listOfTups, eP):
    """Write the party list of tuples like lei, clienttype, exchid, crmid) to the XML file""" 
    hdr = '''<?xml version="1.0"?>
<RegulatoryIdMapping xmlns:fn="http://www.w3.org/2005/xpath-functions" xmlns:fo="http://www.w3.org/1999/XSL/Format" xmlns:xs="http://www.w3.org/2001/XMLSchema">\n'''
    # LEI, MiFIDCustomerType, ExchangeID, LSEid, BATSid, CRMid
    """rowDefault = '''<RegulatoryId LEI="%s" customertype="%s" LSEMemberId="%s" BATSMemberId="%s" value="%d">
<BankInternalId value="%s"/>
</RegulatoryId>\n'''"""

    tail = '''</RegulatoryIdMapping>\n'''
    if not listOfTups:
        FRegulatoryLogger.INFO(logger, 'No LEIs or Contacts found')#
        return
    fd = open(eP['IdFileName'], 'w')
    fd.write(hdr)
    #for lei,clienttype,exchid,crmid,lseid,batsid in listOfTups:
    for tup in listOfTups:
        FRegulatoryLogger.DEBUG(logger, 'Writing tuple %s'%str(tup))
        row = '''<RegulatoryId LEI="%s" customertype="%s"'''%(tup[0], tup[1])
        if eP['LSEIdAdd'] and tup[4]:
            row += ''' LSEMemberId="%s"'''%tup[4]
        if eP['BATSIdAdd'] and tup[5]:
            row += ''' BATSMemberId="%s"'''%tup[5]
        row += ''' value="%d">
<BankInternalId value="%s"/>
</RegulatoryId>\n''' % (tup[2], tup[3])
        fd.write(row)
    fd.write(tail)
    fd.close()
    FRegulatoryLogger.INFO(logger, "Wrote to file %s"%eP['IdFileName'])

warnBool = ['True', 'Warn', 'False']
boolVal = [True, False]
ttIdFileName = 'Path and file name of resulting Id mapping file'
ttGeneratePersonIds = "Should IDs be generated for Persons and Contacts, or only for Parties?"
ttPartyLeiMandatory = "Must the Party have a LEI, or also collect IDs for parties without, like Client and Depot"
ttCustomerTypeMandatory = "Must the MiFIDCustomerType of Party have been set (Retail/Professional/Equal)"
ttExchangeIdMandatory = "Must the ExchangeId have been set on all parties? Should we warn if it isn't?"
ttCrmIdMandatory = "Must the CRM Id have been set on all parties? Should we warn if it isn't?"
ttLSEIdAdd = "Should an LSE Member ID be added to file (only necessary for TRADEcho APAs)"
ttBATSIdAdd = "Should a BATS Member ID be added to file (only necessary for BATS APAs)"

ael_variables = FBDPGui.TestVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        # TODO: Filename callback should be a File locator
        ['IdFileName',
                'File path',
                'string', None, 'c:/tmp/RegulatoryMapping.xml',
                1, 0, ttIdFileName, None, None], 
        ['PartyLeiMandatory',
                'Is a LEI mandatory on a Party',
                'string', warnBool, 'True',
                0, 0, ttPartyLeiMandatory, None, None],
        ['ExchangeIdMandatory',
                'ExchangeId mandatory',
                'string', warnBool, 'Warn',
                0, 0, ttExchangeIdMandatory, None, None],
        ['CrmIdMandatory',
                'CRM Id mandatory',
                'string', warnBool, 'Warn',
                0, 0, ttCrmIdMandatory, None, None],
        ['CustomerTypeMandatory',
                'CustomerType mandatory',
                'string', warnBool, 'Warn',
                0, 0, ttCustomerTypeMandatory, None, None],
        ['GeneratePersonIds',
                "Generate Contact/Person Ids",
                'bool', boolVal, True,
                0, 0, ttGeneratePersonIds, None, None],
        ['LSEIdAdd',
                'Add LSE Member ID',
                'bool', boolVal, False,
                0, 0, ttLSEIdAdd, None, None],
        ['BATSIdAdd',
                'Add BATS Member ID',
                'bool', boolVal, False,
                0, 0, ttBATSIdAdd, None, None]
        )


def ael_main(execParam):
    if execParam['Testmode']:
        FRegulatoryLogger.INFO(logger, "Testing only, no file produced")
        for k in execParam.keys():
            FRegulatoryLogger.DEBUG(logger, k, str(execParam[k]))

    try:
        if execParam['LSEIdAdd'] and not acm.FPartyAliasType['LSE']:
            FRegulatoryLogger.ERROR(logger, 'Error. No PartyAliasType "LSE" defined.')
            execParam['LSEIdAdd'] = False
    except: 
        FRegulatoryLogger.ERROR(logger, 'Error! No PartyAliasType "LSE" defined.')
    try:
        if execParam['BATSIdAdd'] and not acm.FPartyAliasType['BATS']:
            FRegulatoryLogger.ERROR(logger, 'Error. No PartyAliasType "BATS" defined.')
            execParam['BATSIdAdd'] = False
    except:
        FRegulatoryLogger.ERROR(logger, 'Error! No PartyAliasType "BATS" defined.')
    tupList = searchParties(execParam)
    tupList = searchContacts(execParam, tupList)
    if not execParam['Testmode']:
        writeFile(tupList, execParam)
    else:
        FRegulatoryLogger.INFO(logger, str(tupList))
