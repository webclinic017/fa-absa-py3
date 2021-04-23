#####################################################################################################################
'''
Purpose                 :Generic function to amend/add Additional Info Field Values. This will
                         be used via the SAGEN_SM_Automated_Payments script.
Department and Desk     :IT
Requester:              :Heinrich Cronje
Developer               :Heinrich Cronje
CR Number               :243563

Purpose                 :Added functions: get_Port_Struct, get_Port_Struct_from_Port, get_lowest_settlement
                         get_Port_Struct: Checks if the portfolio links roll up to a specified Portfolio.
                         get_Port_Struct_from_Port: Checks if the portfolio roll up to a specified Portfolio.
                         get_lowest_settlement: Gets the lowest level of children for a specified Settlement.
Department and Desk     :Ops Money Market Settlements
Requester:              :Martie Waite
Developer               :Heinrich Cronje/Anwar Banoo/Bhavnisha Sarawan
CR Number               :

Purpose                 :Added Function set_AdditionalInfoValue_ACM
Department and Desk     :CFD Project
Requester:              :CFD Project
Developer               :Heinrich Cronje
CR Number               :429426

Purpose                 :Created a seperate function for Amendments. If the new sections is excecuted
                         and the additional info gets populated while busy excecuting, then call the
                         amendment function. FA-TLM Affirmations.
Department and Desk     :Operations
Requester:              :FA-TLM - IRD implementation
Developer               :Heinrich Cronje
CR Number               :478334

Purpose:                Nominal taken from Face Value
Department and Desk:    OPS DERIVATIVES
Requester:              Sipho Ndlalane
Developer:              Ickin Vural
CR Number:              C000000548269

Purpose:                Created function to return the Enum of a field
Department and Desk:    Middle Office
Requester:              Khunal Ramesar
Developer:              Heinrich Cronje
CR Number:              581033

Purpose:                Amended set_AdditionalInfoValue_ACM to handle Additional Info names containing spaces.
Department and Desk:    Ops
Requester:              Lititia Roux
Developer:              Heinrich Cronje
CR Number:              XXXXXX
Date:                   2012-07-05

Purpose:                Added the function toUpper to change the characters of a text to upper case.
Department and Desk:    PACE MM
Requester:              Linton Behari-Ram
Developer:              Heinrich Cronje
CR Number:              603220
Date:                   2012-10-16

Purpose:                Added the function startFile which replaces os.startfile(), due to a bug in Win7 windows 64bit causing Front Arena Session to freeze.
Department and Desk:    Operations
Requester:              Sipho Ndlalane
Developer:              Sanele Macanda
CR Number:              CHNG0001662676
Date:                   2013-01-23

Purpose:                Added GetLeastNetTrade, IsNet and get_trd_from_possible_nettsettle
Department and Desk:    Operations
Requester:              Linda Breytenbach
Developer:              Willie van der Bank
CR Number:              CHNG0003898744
Date:                   2016-08-23

Purpose:                Amended function get_lowest_settlement to get rid of mutable type argument error
Department and Desk:    Operations
Requester:              Eleine Visagie
Developer:              Willie van der Bank
CR Number:              CHNG0004052977
Date:                   2016-10-25

Purpose:                Added caching decorator to increase performance of SAOPS_CA_Bond_Settlement ASQL query.
Department and Desk:    Operations
Requester:              Seven
Developer:              Hugo
CR Number:              FAOPS-391
Date:                   2019-03-29

'''
#####################################################################################################################
import ael, acm

import FBDPCommon as bdp
import at_logging

from functools import wraps
import functools


LOGGER = at_logging.getLogger()


# Caching mechanism
def cacheFunction(func):
    cache = func.cache = {}
    @functools.wraps(func)
    def memoized_func(*args, **kwargs):
        key = str(args) + str(kwargs)
        if key not in cache:
            cache[key] = func(*args, **kwargs)
        return cache[key]
    return memoized_func
    
    
# Generic function to add and amend Additional Info fields on any entity
def set_AdditionalInfoValue(entity, primary_key, AddInfoName, AddInfoValue, *rest):
    aisp = ael.AdditionalInfoSpec[AddInfoName]
    if aisp:
        aiList = ael.AdditionalInfo.select('addinf_specnbr = %i' % aisp.specnbr)
        recaddrList = []
        for ai in aiList:
            recaddrList.append(ai.recaddr)

        if recaddrList.__contains__(primary_key):
            # Amend
            amend_Add_Info(entity, primary_key, AddInfoName, AddInfoValue, aisp)
        else:
            # New
            entity_clone = entity.clone()
            ai = ael.AdditionalInfo.new(entity_clone)
            ai.addinf_specnbr = aisp
            ai.value = AddInfoValue
            try:
                entity_clone.commit()
                LOGGER.info("%s %s :Additional info %s created with value %s",
                            entity.record_type, primary_key, AddInfoName, AddInfoValue)
            except:
                LOGGER.exception("%s %s :Additional info %s was not created with value %s",
                                 entity.record_type, primary_key, AddInfoName, AddInfoValue)
                amend_Add_Info(entity, primary_key, AddInfoName, AddInfoValue, aisp)
    else:
        LOGGER.error("Additional Info Spec %s does not exist.", AddInfoName)
        
# Generic function to add and amend Additional Info fields on any entity through ACM
def set_AdditionalInfoValue_ACM(entity, addInfoName, value):
    acmAddInfoName = addInfoName.replace(' ', '_')
    
    if entity.AdditionalInfo().GetProperty(acmAddInfoName) == None:
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(entity.Oid())
        addInfo.AddInf(acm.FAdditionalInfoSpec[addInfoName])
        addInfo.FieldValue(value)
        try:
            addInfo.Commit()
        except Exception:
            LOGGER.exception('Commit failed')
    else:
        addInfo = acm.FAdditionalInfo.Select('recaddr = %i' % entity.Oid())
        for i in addInfo:
            LOGGER.info("%s %s %s", i.AddInf().Name() == addInfoName, i.AddInf().Name(), addInfoName)
            if i.AddInf().Name() == addInfoName:
                i.FieldValue(value)
                try:
                    i.Commit()
                except Exception:
                    LOGGER.exception('Commit failed')
                break

# Function to retrieve the ACM choicelist from a Choice List
def get_ChoiceList_ACM(choiceList, value):
    for i in choiceList:
        if i.Name() == value:
            return i
    return None

def amend_Add_Info(entity, primary_key, AddInfoName, AddInfoValue, aisp, *rest):
    if entity.add_info(AddInfoName) != AddInfoValue:
        entity_clone = entity.clone()
        ais = entity_clone.additional_infos()
        for ai in ais:
            if ai.addinf_specnbr.specnbr == aisp.specnbr:
                ai.value = AddInfoValue
        try:
            entity_clone.commit()
            LOGGER.info("%s %s :Additional info %s updated to %s",
                        entity.record_type, primary_key, AddInfoName, AddInfoValue)
        except:
            LOGGER.exception("%s %s :Additional info %s was not updated to %s",
                             entity.record_type, primary_key, AddInfoName, AddInfoValue)
    else:
        LOGGER.error("%s %s :Additional info %s was already set to %s",
                             entity.record_type, primary_key, AddInfoName, AddInfoValue)
        
# Recursive function to check if a portfolio is in a specified portfolio in the portfolio tree.
def get_Port_Struct(portLinkLst, checkPort, match=0):
    if match != 1:
        for portLink in portLinkLst:
            if portLink.member_prfnbr.prfid != checkPort:
                if portLink.owner_prfnbr:
                    if portLink.owner_prfnbr.prfid == checkPort:
                        match = 1
                    else:
                        match = get_Port_Struct(ael.PortfolioLink.select('member_prfnbr=%i' % portLink.owner_prfnbr.prfnbr), checkPort, match)
            else:
                match = 1

    return match

# Function that calls the recursive portfolio tree climber function
def get_Port_Struct_from_Port(port, checkPort, *rest):
    """
    try:        
        portLink = ael.PortfolioLink.select('member_prfnbr=%i' % port.prfnbr)
        match = get_Port_Struct(portLink, checkPort)
    except:
        match = 0
        
    return match
    """    
    return get_Port_Struct_from_Port_v2(port.prfnbr, checkPort)
    

# Function that calls the recursive portfolio tree climber function
def get_Port_Struct_from_Port_Cached(port, checkPort, *rest):
    return get_Port_Struct_from_Port_v2(port.prfnbr, checkPort)
    
    
@cacheFunction
def get_Port_Struct_from_Port_v2(prfnbr, checkPort):
    """
    This method uses the cacheFunc decorator to increase report performance.  
    """
    try:        
        portLink = ael.PortfolioLink.select('member_prfnbr=%i' % prfnbr)
        match = get_Port_Struct(portLink, checkPort)
    except:
        match = 0
    return match

    
# Function that calls the recursive portfolio tree climber function
def get_Port_Struct_from_Port_list(port, flag, checkPort, *rest):
    p_list = ['GROUP TREASURY', 'PRIMARY MARKETS BANKING', 'PRIMARY MARKETS TRADING', 'PM Portfolio Management', 'ALCH', 'SECURITIES LENDING', '7268_Prime Services']
    if flag == 2:
        for p in p_list:
            try:        
                portLink = ael.PortfolioLink.select('member_prfnbr=%i' % port.prfnbr)
                match = get_Port_Struct(portLink, checkPort)
            except:
                match = 0

            if match == 0:
                return 0
        return 1
    else:
        try:        
            portLink = ael.PortfolioLink.select('member_prfnbr=%i' % port.prfnbr)
            match = get_Port_Struct(portLink, checkPort)
            # print match
        except:
            match = 0
        return match    
    
def GetLeastNetTrade(settlement):
    children = get_lowest_settlement(settlement)
    children = [acm.FSettlement[child] for child in children if acm.FSettlement[child].Trade() != None]    
    if len(children) == 0:
        return None

    return min(children, key=lambda child:child.Trade().Oid())
    
def IsNet(settlement):
    if settlement.RelationType() in ('Ad Hoc Net', 'Net'):
        return True
    return False
   
# Function to get the children settlements from any settlement.
def get_lowest_settlement(settlement, low_set=None, *rest):
    if not bdp.is_acm_object(settlement):
        settl = bdp.ael_to_acm(settlement)
    else:
        settl = settlement

    if low_set is None:
        low_set = []
    if settl.Children():
        for child in settl.Children():
            get_lowest_settlement(child, low_set)
    else:
        low_set.append(settl.Oid())
    
    return low_set

def get_trd_from_possible_nettsettle(settlement):
    if IsNet(settlement):
        trade = GetLeastNetTrade(settlement).Trade()
    else:
        trade = settlement.Trade()
    return trade
    
def getFaceValue(temp, t, *rest):
    trade = acm.FTrade[t]
    quantity = trade.FaceValue()
    
    return quantity

# Function to return the enum of a field
def GetEnum(enumType, enumValue):
    ''' Example usage::
        GetEnum('InsType', 'Bond')
        returns the numeric representation of the enum. '''
    enumDict = {}
    enum = -1
    foundInCache = False
    enumDictKey = str(enumType) + '.' + str(enumValue)
    if (enumDictKey in enumDict):
        foundInCache = True
        enum = enumDict[enumDictKey]  # Get it from the cache dict
    
    if not foundInCache:
        enums = acm.FEnumeration['enum(%s)' % enumType]
        assert enums != None, 'The enum-type could not be found in ACM.'
        enum = enums.Enumeration(enumValue)
        enumDict[enumDictKey] = enum  # Cache the enum value
    return enum

# Function to return the input in upper case.
def toUpper(object, text, *rest):
    try:
        return text.upper()
    except:
        return text


# Replaces os.startfile(), due to a bug in Win7 windows 64bit causing Front Arena Session to freeze.
def startFile(Path):
    import subprocess
    
    try:
# Calls the subprocess to execute the command prompt with a given path using the application that is associated with file suffix.
        retcode = subprocess.call(('cmd', '/C', 'start', '', Path))
        if retcode < 0:
            LOGGER.info("Child process was terminated by signal %s", -retcode)
        else:
            LOGGER.info("Child process returned %s", retcode)
    except OSError:
        LOGGER.exception("Execution failed")
