'''---------------------------------------------------------------------------------
 MODULE
    FAMBA_Bridge - Hook in AMBA to modify passing messages.
     
    (c) Copyright 2007 by SunGard FrontArena. All rights reserved.
 
 DESCRIPTION    
 
        This script is a part of the 'AMBA bridge' project.
        
        The aim of the project is to provide a way to upgrade a FrontArena
        system in a step-by-step manner. This is achieved by setting up a
        completely new system in parallel with an existing one in production
        and as a first step letting the trades and instruments updates 'flow' 
        over from the older system into the new one, rendering it possible
        to monitor activity of the old system from both systems. 
        
        As a second step the new system is put into production and the flow is 
        reversed. However it may not work for all records due to the differences
        between the old and new ADMs. These scripts have not been tested for
        such use and may require substantial revision.
    
        Prices should always be filtered as the AMB cannot handle the large amount
        of data sent. This means that filtering must be done on the sending AMBA to 
        avoid sending prices over the AMB.

    CHANGES
         2009-10-30 .. fixes for FxOutrights and update FX swaps and trades
    
         2009-10-29 .. fixes for erroneous LINKS
    
         2009-10-28 .. fixes for FxOutrights
    
         2009-10-26 .. fixes for FxSwaps and FxOutrights
    
         2009-07-09 .. fixes for yield curves, removing some obsolete code
                         moving some code not needed by everyone
                         added custom processing option
    
         2009-05-08 ... many small additions
    
         2009-03-03 ... adding support for more complex criterias for filtering
            
         2008-01-25 Added support for FX Swap, FX Forward, FX Spot
  
         2007-12-06 Added support for upstream direction
  
         2007-12-03 Changed filter calculation.
  
         2007-10-09 Added better trace functionality for the AMBA Bridge
         
         2007-09-20 Added more text objects, fixed a few problems. Moved prefs
                    into another module
  
         2007-08-28 Fixing the AMBA Bridge to send task over the AMBA Bridge
                    Will try using configuration archived = 1
  
         2007-08-22 Cleaning up and correcting the settings of text_object filtering
                    The setup of the AMBA Bridge still looks more difficult than
                    it should be considering how easy it is to destroy data by 
                    configuring something incorrectly.
  
         2007-08-21 Changing handling of text_object to be more reliable
                    and secure.
  
         2007-08-16 Adding textObjects to the elements sent over the bridge
                    These are limited AEL Module, SQL Query, SQL Report  
                    
         2007-06-13 This version removes all the primary keys from the messages.
                    This is in order to avoid some additional confusion.
                    

TECHNICAL SPECIFICATION:



    There are several different pipelines

     3.X.X --> Out
     4.1.X --> In
     3.X.X <-- In  (Reverse direction)
     4.1.X <-- Out (Reverse direction)

    Every stage will be structured as indicated below.

    Every message will go through the filter stage and will then possible be changed by
    the Processing stage.


    Filter Stage: (Implemented sooner or later)
    
    MBF Message In ---> Agent Filters    ----> (True | False , integer, String)
                            A
                            |
                            |
                            |
                            V
                        Agents (Filters)
            

    Processing (mutation) stage: (partially implemented)

    MBF Message In ---> Agent Processing ----> MBF Message Out
                            A
                            |
                            |
                            |
                            V
                         Agents (Mutators)


Agent protocol

    Filter agents: 
    MBF Input -----> (Bool,Priority:Int,ErrorMessage:String)
    
    Mutation agents:
    MBF Input -----> MBF Input


Algortihmm for filters is

filter(MBF Message):
    filterIdeas = {agent.filter(MBF Message) }
    sort filterIdeas by priority descending and then Bool value
    return MBF Messsage
    
mutation(MBF Message):
    x = MBF Message
    for each agent:
        x = agent.mutate(x)
        
        

The file has not been split into multiple smaller files because
of install requirements.

The bridge must use event conversion to be able to handle "child"
entities correctly during insert.


---------------------------------------------------------------------------------'''
import FAMBA_BridgeLib


VERSION='1.15.7'

########### for cmake ########
__version__ = '1.15.7'
VERSION_S = __version__
#if(__version__ == '1.15.7'):
#    VERSION_S = "1.7."+ str(VERSION) # using major, minor, micro numbering

def dReply():
    return "Running FAMBA_Bridge from python File "+VERSION_S

# there have been reports ael, acm can import two different dlls
import acm, ael, amb, re, time


import AMBA_Bridge_pref
from AMBA_Bridge_pref import isTransferableDefault, \
    isInDebugMode, \
    bridgeTables, \
    notBridgeTables, \
    allowedTablesInDest, \
    allowedTablesInSource, \
    AMBA_pref 

""" The choice which messages are transferable via the AMBA_Bridge is stored in 
    dictionaries notBridgeTables and bridgeTables and parameter isTransferableDefault. 
    The script checks what is the record type of a message. If it is not among the keys 
    of the dictionaries, the message is transferable when isTransferableDefault is nonzero. 
    
    notBridgeTables says which messages are not transferable. If the dictionary maps a 
    table name to an empty subdictionary, no message with such table will go through. 
    If the subdictionary is not empty, only messages with attributes from the subdictionary 
    are not transferable, while all the other are transferable.
    
    bridgeTables says which messages are transferable: only messages with attributes 
    from the subdictionary are transferable, while all the other are not transferable.
    A table name with empty subdictionary means that any message with this table is
    transferable.
    
    Correspondingly, FValidation in DEST system then prohibits any changes in 
    transferable tables. FValidation in SOURCE system prohibits changes in 
    non-transferable tables. In case it is too prohibitive, we can allow some tables 
    to be changed by adding them to the lists allowedTablesInSource and 
    allowedTablesInDest. 
    """

# -----------------------------------------------------------------------------------------
# -----------------------------------------------------------------------------------------


""" Since the bridge sends through AEL modules, we have a list of modules which cannot
    be sent under any circumstances. """
specialRecords =    { 'TextObject':{'name':['FValidation'
                                            
                                            # a list of modules that 
                                            # cannot be sent over the bridge
                                            # because the code differs from 
                                            # different versions                                            
                                            
                                            ]}}


mainTablesWithoutUniqueKey = ['Trade']
referenceDic = {'Trade':{'AGGREGATE_TRDNBR':'Trade',
                         'CONNECTED_TRDNBR':'Trade',
                         'CORRECTION_TRDNBR':'Trade',
                         'MIRROR_TRDNBR':'Trade',
                         'CONTRACT_TRDNBR':'Trade',
                         'TRX_TRDNBR':'Trade',
                         'BO_TRDNBR':'Trade',
                         'HEDGE_TRDNBR':'Trade',
                         'OPENING_BO_TRDNBR':'Trade'}
                }

# prefixes, reverse and forward
addinfo_prefix = 'zzAB_'
reverse_addinfo_prefix = 'zzBR_'

RE_TABLE = re.compile('(INSERT|UPDATE|DELETE)_(?P<table>.*$)')
RE_OP = re.compile('(INSERT|UPDATE|DELETE)')
addinfoDic = {}


# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------
#
    
pref = AMBA_pref()

# --------------------------------------------------------------------------------------------
# Reverse version of below functions
# --------------------------------------------------------------------------------------------

#
#This code is obsolete since reversing has been discontinued
#
def reverse_receiver_modify(m):
    """ Recieve from 4 to 2 ADS """
    out = agentProcessLine(m, defaultReverseFilterAgents(), defaultReverseMutators())
    #reportMB("output",out)
    return out


def reverse_sender_modify(m, s):
    """ Send from 4 to 2 ADS """
    #pref.dMsg("")
    return agentProcessLine(m, defaultReverseSendFilterAgents(),
                                defaultReverseSendMutators(), s)

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

# -----------------------------------------------------------
# Utility functions..
# -----------------------------------------------------------


def getSQLVal(query):
    """ Convenience function to reterieve values from the database. 
    Useful to retrieve elemnts by attributes
    """
    pref.dMsg("="*40)
    pref.dMsg(query)
    pref.dMsg("="*40)
    res = ael.asql(query)
    resList = res[1][0]
    #val = res[1][0][0][0]
    if len(resList)>0:
        return resList[0][0]
    else:
        return None


def reportMB(comment, out):
    #pref.dMsg("The output is "+str(out))
    pref.dMsg( "-"*8 +" " + comment +" "+ "-"*8)
    pref.dMsg( out )
    try:
        if isInDebugMode:
            pref.dMsg(out.mbf_object_to_string())
    except Exception, e:
        pass        
    pref.dMsg( "-"*(18+len(comment)))



# -----------------------------------------------------------
# SENDER_MODIFY and RECEIVER_MODIFY 
# -----------------------------------------------------------

class FAMBAFilter:
    """
    Filter class
    """
    def filter(self, m):
        # out message style
        return (True, 0, '')
    
    def getBest(self, res):
        resP = 0
        resC = True
        resM = ''
        for (B, P, M) in res:
            if P > resP or (P == resP and  B == True):
                resP = P
                resC = B
                resM = M
        return (resP, resC, resM)
    
    
    def getAgentResults(self, m, agents):
        """
        Use other classes to as agents
        """
        list = [X.filter(m) for X in agents]
        (R, P, M) = self.getBest(list)
        return R


        


def agentProcessLine(m,filterAg,mutatorAg,s="DUMMY_TOKEN"):
    reportMB("Input", m)
    res = [f.filter(m) for f in filterAg]
    pref.dMsg("filters returned ")
    pref.dMsg(filterAg)
    pref.dMsg(res)
    resP = 0
    resC = True
    resM = ''
    for (B, P, M) in res:
        if P > resP or (P == resP and  B == True):
            resP = P
            resC = B
            resM = M
    
    if not resC:

        reportMB("Filtered Message", m)
        ael.log(resM)
        if(FAMBA_BridgeM.xfilter):
                FAMBA_BridgeM.xfilter.filterMessage(m, resP, resM)
        else:
                pref.dMsg("No FAMBA_BridgeM.xfilter to log against")
        return None

    pref.dMsg("Processing using")
    pref.dMsg(mutatorAg)
    for a in mutatorAg:
        m = a.mutate(m)
        
    reportMB("Output", m)
    if s == "DUMMY_TOKEN":
        return m
    else:
        return (m, s)


            

def agentFilterLine(m, filterAg):
    """True if message should be filtered false if not"""
    global filterLogger
    res = [f.filter(m) for f in filterAg]
    resP = 0
    resC = True
    resM = ''
    for (B, P, M) in res:
        if P > resP or (P == resP and  B == True):
            resP = P
            resC = B
            resM = M
    
    if not resC:
        return False
    else:
        return True


def agentSecondSweep(m, mutatorAg, exceptionClasses):
        """Second sweep of mutators without using exceptions"""
        d = dict([(N, True) for N in exceptionClasses])
        for a in mutatorAg:
                if not a.__class__ in d:
                        m = a.mutate(m)
        return m

        
    
def defaultFilterAgents():
    """Defines standard interpretation of the parameters"""
    global pref
    if hasattr(pref, "useANDSettings") and pref.useANDSettings():
        return [MultiTableMutator(),
            DefaultFilter(),
            ANDNotBridgeTableFilter(),
            PathMessageFilter(),
            SpecialRecordsFilter(),
            ANDBridgeTableFilter(),
            SwapFX()
             ]
    else:
        return [MultiTableMutator(),
            DefaultFilter(),
            NotBridgeTableFilter(),
            PathMessageFilter(),
            SpecialRecordsFilter(),
            BridgeTableFilter()
             ]

def defaultSendFilterAgents():
    """Defines standard interpretation of the parameters"""
    global pref
    if hasattr(pref, "useANDSettings") and pref.useANDSettings():
            return [DefaultFilter(),
                    ANDNotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    ANDBridgeTableFilter()
                    ]
    else:
            return [DefaultFilter(),
                    NotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    BridgeTableFilter()
                    ]

def defaultReverseFilterAgents():
    global pref
    if hasattr(pref, "useANDSettings") and pref.useANDSettings():
            return [ReverseMultiTableMutator(),
                    DefaultFilter(),
                    ANDNotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    ANDBridgeTableFilter()
                     ]
    else:
            return [ReverseMultiTableMutator(),
                    DefaultFilter(),
                    NotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    BridgeTableFilter()
                     ]

def defaultReverseSendFilterAgents():
    global pref
    if hasattr(pref, "useANDSettings") and pref.useANDSettings():
            return [DefaultFilter(),
                    ANDNotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    ANDBridgeTableFilter(),
                    SwapFXInvSender()
                     ]
    else:
            return [DefaultFilter(),
                    NotBridgeTableFilter(),
                    PathMessageFilter(),
                    SpecialRecordsFilter(),
                    BridgeTableFilter(),
                    SwapFXInvSender()
                     ]



def getExtraMutators(fname):
        """
        Add name specified extensions to message mutations
        This
        
        """
        if(hasattr(pref, fname)):
                names = getattr(pref, fname)()
                #For now all additional elements will be in 
                # FAMBA_BridgeM
                extra = []
                for name in names:
                        if(hasattr(FAMBA_BridgeM, name)):
                           O = getattr(FAMBA_BridgeM, name)()
                           extra.append(O) 
                return extra
        else:
                return []

def defaultMutators():
    """
    Default mutators

    """
    list =  [MultiTableMutator(),
     ContextLink_processor(), TaskHistoryFilter(),
     PatchReceiveMessage(), KillFilter(), PriceDefinition(),
     TradeFilterFixReceive(), TaskFixReceive(), InstrumentFix(),
     SwapFX(), SwapFXInstrument(), fixLegnbr(),
     fixYieldCurves(), removeOldieLinks()]
    list.extend(getExtraMutators("extraMessageProcessing"))
    return list

def defaultReverseMutators():
    """
    Default mutators

    """
    return [ReverseMultiTableMutator(),
     ContextLink_processor(), TaskHistoryFilter(),
     PatchReceiveMessage(), KillFilter(), PriceDefinition(),
     TradeFilterFixReceive(), TaskFixReceive(), SwapFXInv(), ForwardFXInv()]

def defaultSendMutators():
     return [PrimaryKeyAdjuster(), TextObjectFix(), TaskFix(),
             YieldCurveFix(), TradeFilterFix(), addFieldObject(), SwapFXSender()]

def defaultReverseSendMutators():
    """ These should be further adjusted """
    return [ReversePrimaryKeyAdjuster(), TextObjectFix(), TaskFix(),
             YieldCurveFix(), TradeFilterFix(), SwapFXInvSender()]


def receiver_modify_agent(m):
    """
    New agent styled receiver modify, that splits processing in two stages 
    """
    out = agentProcessLine(m, defaultFilterAgents(), defaultMutators())
    #reportMB("output",out)
    return out

def sender_modify_agent(m, s):
    return agentProcessLine(m, defaultSendFilterAgents(), defaultSendMutators(), s)

# -----------------------------------------------------------
# SENDER_MODIFY and RECEIVER_MODIFY entry points.
# -----------------------------------------------------------

def receiver_modify(m):

    if(not FAMBA_BridgeM.xfilter and hasattr(pref, "filterMessageFile")):
            filef = pref.filterMessageFile()
            pref.dMsg("receiver_modify Output file "+str(filef))
            if(filef):
                    FAMBA_BridgeM.xfilter = FAMBA_BridgeM.filteredMessageLogger(filef)
    return receiver_modify_agent(m)

def sender_modify(m, s):
    return sender_modify_agent(m, s)


# ------------------------------------------------------------
# Replacement classes for the old style changes
# ------------------------------------------------------------


class DefaultFilter(FAMBAFilter):
    # pri 1
    def filter(self, m):
        # 'tableName' isn't from any of the dictionaries, hence isTransferableDefault needed
        if isTransferableDefault == 0:
            return (False, 1, '')
        return (True, 1, '')
    
#Example query of retreiveing the name of one orderbook
#
#select oid from orderbook o, instrument i, instrument c, party p
#    where o.insaddr = i.insaddr and i.insid = 'DAIM 7.0 21/03/11'
#        and o.curr = c.insaddr and c.insid = 'EUR' 
#        and p.ptynbr = o.market_ptynbr and p.ptyid = 'AIMS'
#
#mutate has been changed to dispatch to other member methods to simplify the code
#
class FAMBA_mutator:
    """ A class that may change messages if it desires 
        Takes Message broker messages
        
        IMPORTANT!! the sender may operate in show_change mode. In this mode
            all objects have all object names prefixed to the object names.
            This must be handled by subclasses to this class. 
        
    """ 
    def mutate(self, msg):
        type = getMessageType(msg)
        
        #
        #This may be a security hazard
        #as the type itself is used in the call
        # 
        # security reasons
        type.upper() 
        # how fast is this ?
        if type in dir(self):
            return (getattr(self, type)(msg))
        else:
            return msg
        #return msg
   

    def tnorm(self, str):
        """
        Normalize any string of type (+|-|!){1,1}.* to be .*
        """
        if(str[0] == "+" or str[0] == "-" or str[0] == "!" ):
            return str[1:] # skip the first character if update styled 
        return str
        

   

    def replace(self,obj,search,replace,prev=None,isfirst=True):
        """
        Search and replace a pattern of [object,object,...,fieldname] where replace
        is (oldValue,NewValue) or newValue
        WARNING: Does not automatically handle show_change = 1
        """
        if(search == []):
            pref.dMsg("Found object "+obj.mbf_get_name()+" value is "+obj.mbf_get_value())

            if(replace == None):
                   # not removed since later version could return lists
                   val = obj.mbf_get_value()
                   return val
            elif(type(replace)!=type(())):
                   name = str(obj.mbf_get_name())
                   val = replace
                   pref.dMsg("Replacing "+str(name) + " with " + str(val))
                   prev.mbf_replace_string(str(name), str(val))

            else:
                if(obj.mbf_get_value() == replace[0]):
                    name = str(obj.mbf_get_name())
                    val = replace[1]
                    pref.dMsg("Replacing "+name + " with " + val)
                    prev.mbf_replace_string(str(name), str(val))
                
                else:
                    pref.dMsg("Found object with value not == " + replace[1])
        else:
            isearch = list(search)
            item = isearch.pop(0)
            
            obj2 = None
            if(isfirst):
                obj2 = obj.mbf_find_object(item)
            else:
                obj2 = obj.mbf_find_object(item, "current")
                
            if(obj2 == None):
                pref.dMsg("Could not find object "+item)
                return None# breaks out of recursion
            else:
                pref.dMsg("Found obj2 "+item)    
                self.replace(obj2, isearch, replace, obj, True)            
                # search for additional objects of the similar types
                obj.mbf_next_object() # go to next object
                self.replace(obj, search, replace, prev, False)
 

    def deleteS(self,obj,search,prev=None,isfirst=True):
        """
        Search and delete a pattern of [object,object,...,fieldname] w
        WARNING: Does not automatically handle show_change = 1
        """
        if(search == []):
            pref.dMsg("Found object to delete "+obj.mbf_get_name()+" value is "+obj.mbf_get_value())

            prev.mbf_remove_object()    
            pref.dMsg("Object is after delete "+obj.mbf_get_name())

        else:
            isearch = list(search)
            item = isearch.pop(0)
            
            obj2 = None
            if(isfirst):
                obj2 = obj.mbf_find_object(item)
            else:
                obj2 = obj.mbf_find_object(item, "current")
                
            if(obj2 == None):
                pref.dMsg("Could not find object "+item)
                return None# breaks out of recursion
            else:
                pref.dMsg("Found obj2 "+item)    
                self.deleteS(obj2, isearch, obj, True)            
                # search for additional objects of the similar types
                obj.mbf_next_object() # go to next object
                self.deleteS(obj, search, prev, False)

    def delete(self, obj, search):
        """
        Search and delete a pattern of [object,object,...,fieldname] w
        Allows use of * to process all links
        """
        groups = fetchSmartPathI(search)
        for i in groups:
            pref.dMsg("Delete "+str(i))
            self.deleteS(obj, i)


    def copy(self, wc, targ):
        """
        Copy wc to targ
        """
        o = wc.mbf_first_object()
        while o !=None:
            
            if o.mbf_is_list():
                l = targ.mbf_start_list(o.mbf_get_name())
                self.copy(o, l)
                targ.mbf_end_list()
            else:
                l = targ.mbf_add_string(o.mbf_get_name(), o.mbf_get_value())
            o = wc.mbf_next_object()


    def fetchVal(self,obj,search, oldVal = None):
        return fetchPath(obj, search, oldVal)

    # example skeleton methods
           
    def UPDATE_CONTEXT(self, msg):
        return msg
    
    def INSERT_CONTEXT(self, msg):
        return msg

    def UPDATE_INSTRUMENT(self, msg):
        return msg
    
    def INSERT_INSTRUMENT(self, msg):
        return msg
    
    def UPDATE_TASK(self, msg):
        return msg
    
    def INSERT_TASK(self, msg):
        return msg

    def INSERT_TEXTOBJECT(self, msg):
        return msg

    def UPDATE_TEXTOBJECT(self, msg):
        return msg

    def UPDATE_YIELDCURVE(self, msg):
        return msg
    
    def INSERT_YIELDCURVE(self, msg):
        return msg
    
    def INSERT_PRICEDEFINITION(self, msg):
        return msg
    
    def UPDATE_PRICEDEFINITION(self, msg):
        return msg

    def UPDATE_TRADEFILTER(self, msg):
        return msg

    def INSERT_TRADEFILTER(self, msg):
        return msg
    
    def INSERT_TRADE(self, msg):
        return msg
    
    def DELETE_TRADE(self, msg):
        return msg
    
    #etc etc ..
    
    
    #
    #convert an MBF message to a python message
    # list = entry list |
    # entry = (key,elem) | list
    # key - the key
    # elem - the value
    # input is always a list
    def mbf2py(self, m):
        """
        convert an MBF message to a python message
        list = entry list |
        entry = (key,elem) | list
        key - the key
        elem - the value
        input is always a list        
        
        values are transformed to [(K,V),..,(KN,[...])]
        this allows easy editing by python
        """
        list = []
        obj = m.mbf_first_object()
        
        while obj != None:
            if obj.mbf_is_list():
                name = obj.mbf_get_name()
                ll = self.mbf2py(obj)
                list.append((name, ll))
            else:
                name = obj.mbf_get_name()
                val  = obj.mbf_get_value()
                list.append((name, val))
            obj = m.mbf_next_object()
        return list
    
    def clear(self, m):
        """
        Deletes all object except the first element in an mbf message
        deleting all objects crashes the AMBA.
        """
        obj = m.mbf_last_object()
        while not obj.mbf_get_name() == "TYPE": 
            obj = m.mbf_remove_object()
            
    def pyreplace2mbf(self, m, pyd):
        self.clear(m)
        self.py2mbf(m, pyd)
        # patch the fact that the header should not be removed
        m.mbf_first_object()
        m.mbf_remove_object()
        

    
    def py2mbf(self,m,pyd,level=0):
        """
        convert a python message to an  MBF message
        list = entry list |
        entry = (key,elem) | list
        key - the key
        elem - the value
        input is always a list        
        
        values are transformed from [(K,V),..,(KN,[...])]
        to MBF messages
        """
        for x in pyd:
            (k, v) = x
            if type(v) == type(list()):
                # create list
                ml = m.mbf_start_list(k)
                self.py2mbf(ml, v, level+1)
            elif type(v) == type(int()):
                m.mbf_add_int(k, v)
            elif type(v) == type(float()):
                m.mbf_add_double(k, v)
            elif type(v) == type(str()):
                m.mbf_add_string(k, v)
            else:
                m.mbf_add_string(k, str(v))

#here for now should be moved somewhere else
swapFXcache = "UNINIT"
        
#
#Swap FX
#
class SwapFX(FAMBA_mutator, FAMBAFilter):
    """
    This class will split a single 
    SwapFX mbf message into two
    Both message parts will still be part of the same message
    
    FX Spot is currently managed inside MultiTableMutator class
    """
    
    def getAddInfoSpec(self, ins):
            global swapFXcache
            key = "zzFX_SWAPT"            
            ais = ael.AdditionalInfoSpec[key]
            if not ais:
                ais = ael.AdditionalInfoSpec.new()
                ais.rec_type = "Trade"
                ais.field_name = key
                ais.mandatory = 0
                setattr(ais, 'data_type.grp', 'Standard')
                setattr(ais, 'data_type.type',
                        ael.enum_from_string('B92StandardType', 'String'))
                ais.description = 'FX AMBA Bridge reference key.'
                ais.commit() 
                #fetch the real recaddress
                ais = ael.AdditionalInfoSpec[key]
            
            if(swapFXcache=="UNINIT"):   
                    swapFXcache = {}
                            
            return ais
    
    def fetchTradesByInstrument(self, ins):
            """Using insid to fetch trades"""
            global swapFXcache
            #assume no trades are ever added to an cached instrument
            #logical true if passed in by AMBA Bridge
            if(swapFXcache!="UNINIT" and ins.insid in swapFXcache):
                    elems = swapFXcache[ins.insid]
            else:
                    ais = self.getAddInfoSpec(ins)
                    
                    q = "select recaddr from additionalinfo where addinf_specnbr='%d' and value = '%s'" \
                        % (ais.specnbr, ins.insid)
                    pref.dMsg("Searching for SwapFX trades by additional info zzFX_SWAPT")
                    pref.dMsg(q)

                    elems = [int(V[0]) for V in ael.asql(q)[1][0]]
                    swapFXcache[ins.insid] = elems

            #load each trade and ensure its not deleted
            if(len(elems)>2):
                return []
            tlist = []
            #return none deleted
            for i in elems:
                    try:
                            trade = ael.Trade[i]
                            tlist.append(trade)
                    except Exception, e:
                            pass
            #update cache with deletes
            swapFXcache[ins.insid] = [L.trdnbr for L in tlist]
            return tlist
            
            
            
    
    def setInsAddInfo(self, ins):
        global swapFXcache
        """connect the FX trades to the instruments"""
        if(swapFXcache=="UNINIT"):
                self.getAddInfoSpec(ins)
                swapFXcache = {}
        return [("ADDINF_SPECNBR.FIELD_NAME", "zzFX_SWAPT"), ("VALUE", ins.insid)]
    

    def collect(self, m):
        """
        collect info from current SwapFX
        """
        self.msg = self.mbf2py(m)
        #to adjust some entries
        #self.mtime = [v for (k,v) in self.msg if k =="TIME"][0]
        self.nmsg = [(k, v) for (k, v) in self.msg if type(v) != type(list())]
        self.swap = [v for (k, v) in self.msg if type(v) == type(list())][0]
        # keys are unique except additional infos
        #self.lista = [(k,v) for (k,v) in self.swap if type(v) == type(list())]
        self.att  = dict([(k, v) for (k, v) in self.swap if type(v) != type(list())])
        # missing is handling all of the list function with fields
        # names that are identical
        self.trans = []
        # insert type
        self.type = [k for (k, v) in self.msg if type(v) == type(list())][0]

    def mType(self):
        return self.type

        
    def getInstr(self):
        #if we are in an instrument update the latest setting have not been commited
        #hence use a proxy instead
        if(hasattr(self, "insproxy")):
           return self.insproxy
            
        insid = self.att["INSADDR.INSID"]
        #using ael as in the conversion code
        ins = ael.Instrument[insid]        
        return ins
        
    def getPayleg(self):    
        """
        returns Payleg
        """
        legs = self.getInstr().legs()
        if legs[0].payleg == 1:
            payleg = 0
        else:
            payleg = 1
        return legs[payleg]
    
    def getRecleg(self):
        legs = self.getInstr().legs()
        if legs[0].payleg == 1:
            recleg = 1
        else:
            recleg = 0
        return legs[recleg]
        
        
    
    def getPaylegCurr(self):
        """
        returns currency
        """
        return self.getPayleg().curr
        
    def getReclegCurr(self):
        return self.getRecleg().curr
        
    def getFarPrice(self):
        
        pay_endfactor = self.getPayleg().nominal_factor \
            * (1.0 + self.getPayleg().fixed_rate)
        rec_endfactor = self.getRecleg().nominal_factor \
            * (1.0 + self.getRecleg().fixed_rate) 
            
        #self.pay_endfactor = pay_endfactor
        #self.rec_endfactor = rec_endfactor
        #self.getrecleg_nominal_factor = self.getRecleg().nominal_factor
        #self.one_plus_fixed_rate = 1.0 + self.getRecleg().fixed_rate
        return pay_endfactor / rec_endfactor

    def appendMisc(self, list):
        """
        Copy all entries that have not been set as is to both trades
        """
        d = dict(list)
        some = [(k, v) for (k, v) in self.swap if not k in d
                    and k != "TRDNBR"
                    and k != "CONTRACT_TRDNBR"
                    and k != "CONNECTED_TRDNBR"]
        
        # for testing purposes
        list.extend(some)
        #and k != "TRDNBR"

            
    def makeOptionalKey(self):
        """
        This will grab the additional info and use its ID
        as optionalKey value
        NOTE that one of the swap sides needs to modify the name
        """
        #if an update on an instrument occurs the following will be found in the message
        #        
        if("_TRUERECEIVERTRDNBR" in self.att):
                return self.att["_TRUERECEIVERTRDNBR"]

        res = None
        nlist = [b for (a, b) in self.swap if type(b) == type(list())
                    and a == "ADDITIONALINFO"]
        for ent in nlist:
            d = dict(ent)    
            if "ADDINF_SPECNBR.FIELD_NAME" in d and \
                d["ADDINF_SPECNBR.FIELD_NAME"] == "zzAB_Trade" :
                res = "zzAB"+str(d["Value"])
        if res == None:
            raise Exception("Could not convert FX Swap because addinfo was missing")
            
        return res
        
        
    def znorm(self, arg, zval):
        """
        default values for things that are not transmitted
        """
        if not arg in self.att:
            return zval
        else:
            return self.att[arg]

    def far(self):
        """
        build far side
        """
        # append a swap
        # should handle updates as well (later)
        list = []
        if("PRFNBR.RPFID" in self.att):
                list.append(("PRFNBR.PRFID", self.att["PRFNBR.PRFID"]))
        if("ACQUIRER_PTYNBR.PTYID" in self.att):
                list.append(("ACQUIRER_PTYNBR.PTYID", self.att["ACQUIRER_PTYNBR.PTYID"]))        
        if("COUNTERPARTY_PTYNBR.PTYID" in self.att):                
                list.append(("COUNTERPARTY_PTYNBR.PTYID", self.att["COUNTERPARTY_PTYNBR.PTYID"]))
        list.append(("CURR.INSID", self.getPaylegCurr().insid))
        # added stuff for correct instrument handling
        
        # 
        #if not self.outright():
        # unknown how to handle outrights ...
        list.append(("INSADDR.INSID", self.getReclegCurr().insid))
        list.append(("INSADDR.INSTYPE", "INS_CURR"))
        list.append(("ADDITIONALINFO", self.setInsAddInfo(self.getInstr())))
        
        list.append(("ACQUIRE_DAY", str(self.getInstr().exp_day)))
        list.append(("VALUE_DAY", self.getInstr().exp_day))        
        list.append(("PRICE", self.getFarPrice()))        
                
        if(self.getRecleg().is_locked):
            pref.dMsg("getRecleg locked")
            quant = self.getInstr().contr_size*self.getRecleg().nominal_factor
            list.append(("QUANTITY", quant))
            list.append(("PREMIUM", -quant*self.getFarPrice()))
            list.append(("QUANTITY_IS_DERIVED", "No"))
            

                        
        else:
            pref.dMsg("getRecleg unlocked")
            premium = -self.getInstr().contr_size*self.getPayleg().nominal_factor
            list.append(("PREMIUM", premium ))
            list.append(("QUANTITY", -premium / self.getFarPrice()))
            list.append(("QUANTITY_IS_DERIVED", "Yes"))
        list.append(("STATUS", self.att["STATUS"]))
        list.append(("TYPE", self.att["TYPE"]))
        list.append(("REFERENCE_PRICE", 1.0 / self.getRecleg().nominal_factor))
        
        if self.outright():
            
            list.append(("SALES_MARGIN", self.znorm("SALES_MARGIN", 0.0)))
            list.append(("TRADE_PROCESS", 1 << 13))
            list.append(("OPTIONAL_KEY", self.makeOptionalKey()+"_1"))
        else:
            list.append(("TRADE_PROCESS", 1 << 15))
            #list.append(("OPTIONAL_KEY","OPTKEY#401_1"))
            list.append(("OPTIONAL_KEY", self.makeOptionalKey()+"_1"))
            
            #list.append(("CONNECTED_TRDNBR.OPTIONAL_KEY","OPTKEY#401"))
            list.append(("CONNECTED_TRDNBR.OPTIONAL_KEY", self.makeOptionalKey()))

        self.appendMisc(list) # add misc stuff to MBF
        item = (self.mType(), list)        
        self.far = item
        self.trans.append(item)


    def isUpdateInstrument(self):
            return hasattr(self, "insproxy")
               
    
    def compareDates(self, aval, bval):
            at =  time.mktime(time.strptime(aval, "%Y-%m-%d"))
            bt =  time.mktime(time.strptime(bval, "%Y-%m-%d"))
            return aval < bval
    
    def nearDate(self):
            """grab the cashflows and acquire days. The cashflows are grabbed using 
            asql to ensure only a single ADS query is used to retrieve data
            """
            
            #start with end day and then use other days
            val = self.getPayleg().end_day            
            if(self.isUpdateInstrument()):
                    ret = val
                    for cf in self.getRecleg().cash_flows():
                            if self.compareDates(cf.pay_day, ret):
                                    ret = cf.pay_day
                    pref.dMsg("nearDate using legs "+ret)
                    return ret
            else:
            
                    query = """select min(f.pay_day < '%s' ? f.pay_day : '%s')
                            from instrument i,leg l,cashflow f where 
                            i.insaddr = l.insaddr and f.legnbr = l.legnbr
                                and i.insid ='%s' """
                    v = ael.asql(query % (val, val, self.att["INSADDR.INSID"]))
                    ret = v[1][0][0][0]
                    pref.dMsg("nearDate asql answer "+ret)
                    return ret
    
    
    def near(self):
            """ 
            build near side
            """        
            #if not self.outright():
            list = []
            if("PRFNBR.PRFID" in self.att):
                    list.append(("PRFNBR.PRFID", self.att["PRFNBR.PRFID"]))
            if("ACQUIRER_PTYNBR.PTYID" in self.att):
                    list.append(("ACQUIRER_PTYNBR.PTYID", self.att["ACQUIRER_PTYNBR.PTYID"]))
            if("COUNTERPARTY_PTYNBR.PTYID" in self.att):        
                    list.append(("COUNTERPARTY_PTYNBR.PTYID", self.att["COUNTERPARTY_PTYNBR.PTYID"]))
            list.append(("CURR.INSID", self.getPaylegCurr().insid))
            
            # added stuff for correct instrument handling
            
            list.append(("INSADDR.INSID", self.getReclegCurr().insid))
            list.append(("INSADDR.INSTYPE", "INS_CURR"))
            list.append(("ADDITIONALINFO", self.setInsAddInfo(self.getInstr())))

            nearD = self.nearDate()
            list.append(("ACQUIRE_DAY", nearD))
            list.append(("VALUE_DAY", nearD))
                
            #list.append(("ACQUIRE_DAY",str(self.getRecleg().start_day)))
            #list.append(("VALUE_DAY",str(self.getRecleg().start_day)))
            
            price = self.getPayleg().nominal_factor / \
                        self.getRecleg().nominal_factor
            list.append(("PRICE", price)) 
        
            if(self.getRecleg().is_locked):
                quant = -self.getInstr().contr_size * self.getRecleg().nominal_factor
                list.append(("QUANTITY", quant))
                #near_trade_price = self.getPayleg().nominal_factor * \
                #    self.getRecleg().nominal_factor
                list.append(("PREMIUM", -quant*price))
                list.append(("QUANTITY_IS_DERIVED", "No"))
            else:
                premium = -self.getInstr().contr_size*self.getPayleg().nominal_factor
                list.append(("PREMIUM", premium))
                list.append(("QUANTITY", premium / price ))   
        
            list.append(("STATUS", self.att["STATUS"]))
            list.append(("TYPE", self.att["TYPE"]))
            list.append(("REFERENCE_PRICE", price))
            sales_margin = 0;
            if "SALES_MARGIN" in self.att:
                sales_margin = self.att["SALES_MARGIN"]
            list.append(("SALES_MARGIN", sales_margin))
            if(self.outright()):
                    list.append(("TRADE_PROCESS", 1 << 13))                    
            else:
                    list.append(("TRADE_PROCESS", 1 << 14))
            list.append(("OPTIONAL_KEY", self.makeOptionalKey()))
        
            self.appendMisc(list) # add misc stuff to MBF
            item = (self.mType(), list)
            self.trans.append(item)
    
    def connect(self):
        pass

    #def adjustedLegBySpotDay(self,rec_leg):
    #    pass
    #    
    #    today = ael.date_from_string(self.mtime[0:10],"%Y-%m-%d")
    #    legd = ael.date_from_string(self.getRecleg().start_day,"%Y-%m-%d")
    #    offset =0
    #    if("OFFSET" in self.att):
    #            offset = self.att["OFFSET"]
    #    spot = today.add_banking_day(self.getReclegCurr(),int(offset))
    #    pref.dMsg("LegversusSpotDay Spot "+spot+" legd "+legd)
    #    if(legd < spot):
    #            return 1
    #    else:
    #            return 2
        

    def outright(self,insid = None):
        """Return 1 if outright on nominal_at_start (near leg)
           Returns 2 if outright on nominal_at_end (far leg)
           Returns 0 if Swap
           
           Takes insid as argument in case self.att has not been built
        """
        #use override element if available
        #cause is that the F4 is not storing these values correctly
        if(hasattr(self, "att") and "_SWAPFXS_OUTRIGHT" in self.att):
                pref.dMsg("Found outright marker in message!")
                return self.att["_SWAPFXS_OUTRIGHT"] == "1" \
                        or self.att["_SWAPFXS_OUTRIGHT"] == "2"
            
        # assumes that collect has setup data of the swap
        # check if
        if(insid==None):
                insid = self.att["INSADDR.INSID"]
        #using ael as in the conversion code
        ins = ael.Instrument[insid]        
        legs = ins.legs()
        if legs[0].payleg == 1: 
            nonpayleg = 1
        else:
            nonpayleg = 0
        rec_leg = legs[nonpayleg]
        
        
        if rec_leg.nominal_at_start == 0 \
                or rec_leg.nominal_at_end == 0:
            #this also determines direction of trade
            if(rec_leg.nominal_at_start):
                    out = 1 # self.adjustedLegBySpotDay(rec_leg)
            else:
                    #out =  2
                    out = 2
        else:
            out = 0
        
        pref.dMsg("SwapFX.outright("+insid+") = "+str(out)
                        +" rec_leg.nominal_at_start "+str(rec_leg.nominal_at_start) 
                        +" rec_leg.nominal_at_end " + str(rec_leg.nominal_at_end))
        return out
        
    def swap(self, m):
        return hasPath(m, ["*Trade", "INSADDR.INSTYPE", "INS_FX_SWAP"]) \
                or hasPath(m, ["*Trade", "INSADDR.INSTYPE", "FxSwap"])

    def swapIns(self, m):
        """is instrument a swap, (placed here for simplifying inheritance"""
        return hasPath(m, ["*INSTRUMENT", "INSTYPE", "INS_FX_SWAP"]) \
                        or hasPath(m, ["*INSTRUMENT", "INSTYPE", "FxSwap"])


    #def outrightBeforeSpot(self):
    #        #check the start day versus the expiry of the instrument
    #        #if this the case the meanings are reversed
    #        #val = str( self.getInstr().exp_day)
    #        createT = long(self.getInstr().creat_time)
    #        val = str(self.att["VALUE_DAY"])
    #        valD  = time.mktime(time.strptime(val,"%Y-%m-%d"))
    #        startD  = time.mktime(time.strptime(str(self.getRecleg().start_day),"%Y-%m-%d"))
    #        res = not (startD < valD)
    #        #(l.start_day < i.creat_time) and not (l.start_day < t.value_day)
    #        res = (startD < createT) and not(startD < valD)
    #        pref.dMsg("Is outright before spot? "+str(res))
    #        return res

    def outrightBeforeSpot(self):
            if("_SWAPFXS_OUTRIGHT" in self.att):                    
                    res =  self.att["_SWAPFXS_OUTRIGHT"] == "1"
                    pref.dMsg("outright before spot!" + str(res))
                    return res
            return False
        
        
    def changeMessage(self):
        #
        #Should be run in a transaction (which currently is available
        # from 4.4p something ..

        if self.outright():
                #the its incorrect to always assume far is the outright
                #at times the near leg should be used
                if(self.outrightBeforeSpot()):
                        self.near()
                else:
                        self.far()
        else:
                self.near()
                self.connect()
                self.far()

        # add the transaction
        self.nmsg.append(("TRANSACTION", self.trans))
            
    def changeCommit(self, m, pmsg):
        """ convert message from python back to mbf
        """
        #self.py2mbf(pmsg)
        self.clear(m)
        self.py2mbf(m, pmsg)
        # patch the fact that the header should not be removed
        m.mbf_first_object()
        m.mbf_remove_object()

    def fixMessage(self, m):
        if not self.swap(m):
            pref.dMsg("Ignoring trade because this is not a Swap!")
            return m
        pref.dMsg("Fixing the Swap trade (outright/swap)...!!!")
        self.collect(m)
        self.changeMessage()
        self.changeCommit(m, self.nmsg)
        return m

    def INSERT_TRADE(self, m):
        return self.fixMessage(m)
        
    def UPDATE_TRADE(self, m):
        #store type of pdate
        return self.fixMessage(m)


    def filter(self, m):
        #need to stop FXtrades getting filtered because there are no additional infos
        if(self.swap(m)):
                return (True, 10002, 'found swap trade')
        else:
                # do nothing
                return (True, 0, '')


class SwapFXSender(SwapFX):
        """Add instrument information from F2 to trade message
           Required as the data on F4 is unreliable
           also used for instrument to help out update for trades
        """

        def changeMessage(self):
                """Change the message"""
                # self.nmsg   <- this is the message without swap
                # self.swap   <- the swap itself
               
                #if self.outright():
                #       self.swap.append(("_SWAPFXS_OUTRIGHT","1"))
                #else:
                #        self.swap.append(("_SWAPFXS_OUTRIGHT","0"))
                self.swap.append(("_SWAPFXS_OUTRIGHT", self.outright()))        
                self.nmsg.append(("TRADE", self.swap))
 
        def inscollect(self, m):
                self.msg = self.mbf2py(m)
                self.nmsg = [(k, v) for (k, v) in self.msg if type(v) != type(list())]
                self.ins = [v for (k, v) in self.msg if type(v) == type(list())][0]
                self.insatt  = dict([(k, v) for (k, v) in self.ins if type(v) != type(list())])
                
        def changeInsMessage(self):
                """Add the reference to the instrument definition"""
                self.ins.append(("_SWAPFXS_OUTRIGHT", self.outright(self.insatt["INSID"])))
                self.nmsg.append(("INSTRUMENT", self.ins))
                
        def UPDATE_INSTRUMENT(self, m):
                if(not self.swapIns(m)):
                        return m
                pref.dMsg("Adding outrigh data to instrument (outright/swap)...!!!")
                self.inscollect(m)

                self.changeInsMessage()
                self.changeCommit(m, self.nmsg)
                return m


                
class legproxy:

        def __init__(self, leglist):
                self.nominal_at_end = 0
                self.nominal_at_start = 0
                self.payleg = 0
                self.fixed_rate = 0
                self.cwf = [cashflowproxy(v) for k, v in leglist 
                                if k=="CASHFLOW" or k=="+CASHFLOW" or k=="!CASHFLOW"]
                self.attach(leglist)

        def attach(self, inlist):                
                elems = [(k, v) for (k, v) in inlist if type(v) != type(list())]
                for k, v in elems:
                        #sometimes conversion will be needed below

                        kl = k.lower()
                        fv = v
                        try:
                                fv = int(v)
                        except Exception:
                                try:
                                        fv = float(v)
                                except Exception:
                                        pass
                        #more auto conversion
                        if(fv=="Yes"):
                                fv = 1
                        if(fv=="No"):
                                fv = 0
                                
                        setattr(self, kl, fv)

                        if(k=="CURR.INSID"):
                                setattr(self, "curr", ael.Instrument[v])
                                
        def cash_flows(self):
                return self.cwf


class insproxy(legproxy):

        def __init__(self, inslist, ins):
                pass
                self.exp_day = ins.exp_day
                
                self.build(inslist)

        def build(self, inslist):
                #pass may create itself kif needed
                self.attach(inslist)
                #build the legs (always two)
                legs = [v for k, v in inslist if k=="LEG" or k=="+LEG" or k=="!LEG"]
                legs = legs[:2]
                self.leg = []
                self.leg.append(legproxy(legs[0]))
                self.leg.append(legproxy(legs[1]))                
                
        def legs(self):
                return self.leg

class cashflowproxy(legproxy):
        
        def __init__(self, cflist):
                self.attach(cflist)


class SwapFXInstrument(SwapFX):
        """This class is to process instruments and send updates to FX trades
        
        Requires additional request to the ADS server.
        
        genereate something like the following
        
        [MESSAGE]
          TYPE=INSERT_TRADE
          VERSION=1.0
          TIME=2009-10-30 13:05:43
          SOURCE=AMBA_oldNew2
          [TRADE]
            TRDNBR=17442
            [ADDITIONALINFO]
              ADDINF_SPECNBR.FIELD_NAME=zzAB_Trade
              Value=17442
            [/ADDITIONALINFO]
            INSADDR.INSID=USD-ZAR/FXS/090921-091103
            INSADDR.INSTYPE=FxSwap
            INSADDR.EXOTIC_TYPE=None
            INSADDR.INSTYPE=INS_FX_SWAP
            ACQUIRE_DAY=2009-09-22
            ACQUIRER_PTYNBR.PTYID=Legal Entity 2
            CURR.INSID=ZAR
            VALUE_DAY=2009-09-22
            TIME=2009-09-20 00:00:00
            QUANTITY=1
            STATUS=TRADE_STATUS_FO_CONF
            COUNTERPARTY_PTYNBR.PTYID=Abbey Natl plc
            COUNTERPARTY_PTYNBR.PTYID2=002BB2
            TRADER_USRNBR.USERID=ROLF.STENHOLM
            OPTKEY1_CHLNBR.ENTRY=10. ARC KNKCLR
            OPTKEY1_CHLNBR.LIST=Strategy
            TYPE=TRADE_NORMAL
            CONTRACT_TRDNBR=17442
            EXECUTION_TIME=2009-10-30 14:05:43
            CONNECTED_TRDNBR=17442
            [+ADDITIONALINFO]
              ADDINF_SPECNBR.FIELD_NAME=Option Hedge
              VALUE=No
            [/+ADDITIONALINFO]
            _SWAPFXS_OUTRIGHT=1
          [/TRADE]
        [/MESSAGE]

        
        """        



        def collectOld(self, m):
                self.msg = self.mbf2py(m)
                #to adjust some entries
                #self.mtime = [v for (k,v) in self.msg if k =="TIME"][0]
                self.nmsg = [(k, v) for (k, v) in self.msg if type(v) != type(list())]
                self.swap = [v for (k, v) in self.msg if type(v) == type(list())][0]
                # keys are unique except additional infos
                #self.lista = [(k,v) for (k,v) in self.swap if type(v) == type(list())]
                self.att  = dict([(k, v) for (k, v) in self.swap if type(v) != type(list())])
                # missing is handling all of the list function with fields
                # names that are identical
                self.trans = []
                # insert type
                self.type = [k for (k, v) in self.msg if type(v) == type(list())][0]


        def reverseEngineerOptKey(self, tradeA):
                """May need to adjust key depending on which side grabbed the key!"""
                val = str(tradeA.optional_key)
                if(val[-2:]=='_1'):
                        val= val[:-2]
                return val

        def collectSwap(self, m):
                """Collect information from Swap and process as if MBF message"""
                insid = self.insatt["INSID"]                        
                ins = ael.Instrument[insid]
                swapt = self.fetchTradesByInstrument(ins)

                tradeA = swapt[0]
                # build all the swaps elements needed for update
                swapl = []
                swapl.append(("TRDNBR", str(tradeA.trdnbr)))
                #need to fetch the addinfo value of the trade
                
                
                #addinfl = [("ADDINF_SPECNBR.FIELD_NAME","zzAB_TRADE"),("VALUE",ins.insid)]
                swapl.append(("_TRUERECEIVERTRDNBR", self.reverseEngineerOptKey(tradeA)))
                swapl.append(("INSADDR.INSID", self.insatt["INSID"]))
                swapl.append(("INSADDR.INSTYPE", self.insatt["INSTYPE"]))
                swapl.append(("PRFNBR.PRFID", str(tradeA.prfnbr.prfid)))
                swapl.append(("ACQUIRER_PTYNBR.PTYID", str(tradeA.acquirer_ptynbr.ptyid)))
                swapl.append(("COUNTERPARTY_PTYNBR.PTYID", str(tradeA.counterparty_ptynbr.ptyid)))
                
                swapl.append(("STATUS", str(tradeA.status)))
                swapl.append(("TYPE", str(tradeA.type)))
                
                swapl.append(("SALES_MARGIN", str(tradeA.sales_margin)))
                swapl.append(("ACQUIRE_DAY", str(tradeA.acquire_day)))


                if("_SWAPFXS_OUTRIGHT" in self.insatt):
                        swapl.append(("_SWAPFXS_OUTRIGHT", self.insatt["_SWAPFXS_OUTRIGHT"]))

                
                #finally we have generated all information used in the previous instance                
                self.swap = swapl
                

        def collect(self, m):
                self.msg = self.mbf2py(m)
                #to adjust some entries
                #self.mtime = [v for (k,v) in self.msg if k =="TIME"][0]
                self.nmsg = [(k, v) for (k, v) in self.msg if type(v) != type(list())]
                self.ins = [v for (k, v) in self.msg if type(v) == type(list())][0]
                self.insatt  = dict([(k, v) for (k, v) in self.ins if type(v) != type(list())])
                
                self.trans = []
                self.trans.append(("INSTRUMENT", self.ins)) #pass through an FXinstrument
                #get the trades that should be processed (one of them)
                #remove before release
                self.collectSwap(m)
                self.type = "!TRADE"

                pref.dMsg("THE SWAP "+ str(self.swap))
                self.att  = dict([(k, v) for (k, v) in self.swap if type(v) != type(list())])

                #build a proxy instrument
                insid = self.insatt["INSID"]                        
                ins = ael.Instrument[insid]
                self.insproxy = insproxy(self.ins, ins)
                pref.dMsg("insproxy looks like "+str(dir(self.insproxy)))


        def UPDATE_INSTRUMENT(self, m):
                if(not self.swapIns(m)):
                        return m
                pref.dMsg("FX swap instrument update, sending updates to trades!!!")
                self.swap = None
                self.collect(m)
                if(self.swap == None):
                        return m
                else:
                        self.changeMessage()
                        #display result
                        #pref.dMsg("Message passed to change commit "+str(self.nmsg))
                        self.changeCommit(m, self.nmsg)
                        return m

    
class SwapFXInv(FAMBA_mutator):
    """
    Convert swaps from 4.X to 2.X 
    
    This solution will use information added by another mutator as such
    
    sender adds trade information from the connected trade to the swap
    (because of bugs in the AMBA information of the near trade might not
    be available on the target side)
    
    """

    """
[MESSAGE]
  TYPE=INSERT_INSTRUMENT
  VERSION=1.0
  TIME=2008-01-30 12:05:34
  SOURCE=AMBA_oldBlank
  [+INSTRUMENT]
    UPDAT_TIME=2008-01-30 13:05:30
    !UPDAT_TIME=2008-01-24 11:02:30
    VERSION_ID=201
    !VERSION_ID=200
    INSID=ROLF_SWAP_FX
    INSTYPE=INS_FX_SWAP
    CURR.INSID=TWD
    QUOTE_TYPE=QUOTE_PCT_OF_NOM
    OTC=Yes
    SPOT_BANKING_DAYS_OFFSET=2
    PRODUCT_CHLNBR.ENTRY=CCS
    PRODUCT_CHLNBR.LIST=ValGroup
    CONTR_SIZE=33527500
    PAY_OFFSET_METHOD=DATEPERIOD_BUSINESS_DAYS
    [LEG]
      LEGNBR=12093
      TYPE=LEG_FIXED
      PAYLEG=Yes
      DAYCOUNT_METHOD=DAYCOUNT_ACT_360
      CURR.INSID=TWD
      NOMINAL_FACTOR=1
      START_DAY=2008-01-16
      END_DAY=2008-01-29
      ROLLING_BASE_DAY=2008-01-29
      PAY_DAY_METHOD=BUSINESS_DAY_FOLLOWING
      PAY_CALNBR.CALID=Taipei
      PAY2_CALNBR.CALID=New York
      FIXED_RATE=-9.69353514124E-008
      NOMINAL_AT_END=Yes
      NOMINAL_AT_START=Yes
      [CASHFLOW]
        PAY_DAY=2008-01-29
        CFWNBR=79359
        TYPE=CASH_FLOW_FIXED_AMOUNT
        FIXED_AMOUNT=1
        NOMINAL_FACTOR=0.999999903065
      [/CASHFLOW]
      [CASHFLOW]
        PAY_DAY=2008-01-16
        CFWNBR=79362
        TYPE=CASH_FLOW_FIXED_AMOUNT
        FIXED_AMOUNT=-1
        NOMINAL_FACTOR=1
      [/CASHFLOW]
    [/LEG]
    [LEG]
      LEGNBR=12094
      TYPE=LEG_FIXED
      PAYLEG=No
      DAYCOUNT_METHOD=DAYCOUNT_ACT_360
      CURR.INSID=USD
      NOMINAL_FACTOR=0.0298262620237
      START_DAY=2008-01-16
      END_DAY=2008-01-29
      ROLLING_BASE_DAY=2008-01-29
      PAY_DAY_METHOD=BUSINESS_DAY_FOLLOWING
      PAY_CALNBR.CALID=New York
      PAY2_CALNBR.CALID=Taipei
      NOMINAL_AT_END=Yes
      NOMINAL_AT_START=Yes
      IS_LOCKED=Yes
      [CASHFLOW]
        PAY_DAY=2008-01-29
        CFWNBR=79363
        TYPE=CASH_FLOW_FIXED_AMOUNT
        FIXED_AMOUNT=1
        NOMINAL_FACTOR=1
      [/CASHFLOW]
      [CASHFLOW]
        PAY_DAY=2008-01-16
        CFWNBR=79366
        TYPE=CASH_FLOW_FIXED_AMOUNT
        FIXED_AMOUNT=-1
        NOMINAL_FACTOR=1
      [/CASHFLOW]
    [/LEG]
  [/+INSTRUMENT]
[/MESSAGE]
    """
    


    def isSwap(self, m):
        return (hasPath(m, ["*Trade", "INSADDR.INSTYPE", "INS_CURR"]) or
                        hasPath(m, ["*Trade", "INSADDR.INSTYPE", "Curr"])) \
            and hasPath(m, ["*Trade", "TRADE_PROCESS", str(1<<15)])
        
    
    def isVoid(self, m):
        return (hasPath(m, ["*Trade", "INSADDR.INSTYPE", "INS_CURR"]) or
                        hasPath(m, ["*Trade", "INSADDR.INSTYPE", "Curr"])) \
            and hasPath(m, ["*Trade", "TRADE_PROCESS", str(1<<14)])
        
    
    def insExists(self, unqid):
        return ael.Instrument[unqid] != None
    
    
    def getPayRecLeg(self, ins):
        # the legs are set upon creation of the instrument
        leg = ins.legs()
        if leg[0].payleg == 1:
            payleg = 0
            nonpayleg = 1
        else:
            payleg = 1
            nonpayleg = 0
        return (payleg, nonpayleg)


    def setPayLeg(self, pay_leg, ins, att, near_trade):
        # should do different things depending on fixed legs or not
        
        # locked rec_lec
        pay_leg.nominal_factor = 1.0 
        pay_leg.curr           = ael.Instrument[att["CURR.INSID"]]
        
        pay_leg.fixed_rate = -1 * float(att["PREMIUM"]) /float(near_trade["premium"]) -1
        
        # change the time of expiry
        pay_leg.start_day = ael.date_from_string(near_trade["acquire_day"])
        pay_leg.end_day = ael.date_from_string(att["ACQUIRE_DAY"])
        
        pref.dMsg("PAY_LEG.FIXED_RATE="+str(pay_leg.fixed_rate))
        pref.dMsg("PAY_LEG.NOMINAL_FACTOR="+str(pay_leg.nominal_factor))
        
        
    
    def setRecLeg(self, rec_leg, ins, att, near_trade, pay_leg):
        
        # should do different things depending on fixed legs or not

        #locked rec_leg
        # assume that we can do all of this
        rec_leg.nominal_factor = -1 *float(near_trade["quantity"]) / float(near_trade["premium"])
        rec_leg.curr           = ael.Instrument[att["INSADDR.INSID"]]        
        #rec_leg.fixed_rate     = 1
        
        # change the time of expiry
        rec_leg.start_day = ael.date_from_string(near_trade["acquire_day"])
        rec_leg.end_day = ael.date_from_string(att["ACQUIRE_DAY"])
        
 
        rec_leg.fixed_rate = -float(att["QUANTITY"]) / float(near_trade["quantity"]) -1

        pref.dMsg("REC_LEG.FIXED_RATE="+str(rec_leg.fixed_rate))
        pref.dMsg("REC_LEG.NOMINAL_FACTOR="+str(rec_leg.nominal_factor))
        pref.dMsg("REFERENCE_PRICE="+str(att["REFERENCE_PRICE"]))
        
        

    def voidTrade(self, trade):
        tc = trade.clone()
        tc.status = "Void"
        tc.commit()

    def editInstrument(self, unqid, att, ins):
        near_t = dict(att["near_trade"]) # the near trade 
        
        ins.insid = unqid
        
        (payleg, nonpayleg) = self.getPayRecLeg(ins)
                
        leg = ins.legs()
        pay_leg = leg[payleg]
        rec_leg = leg[nonpayleg]

        # will have to add elements to handle floating swaps

        #far_trade_att = att
        # we have the legs now set some of the info
        
        ins.exp_day = ael.date_from_string(att["VALUE_DAY"])
        #ins.start_day = 
        self.setPayLeg(pay_leg, ins, att, near_t)
        # must be called after
        self.setRecLeg(rec_leg, ins, att, near_t, pay_leg)
        
        #these don't look ok
        #far_trade.quantity = orig_instr.contr_size * rec_leg.nominal_factor
        #created problems with nominal 
        
        #Appears to cause issues, however setting the contr_size = 1.0
        #may also break the application ?? because premiums and other cash will be wrong?
        ins.contr_size =  float(near_t["premium"]) #float(att["QUANTITY"]) / rec_leg.nominal_factor
        #makes the values such as premium look good but other values become bad
        #should if possible values so that we can make contr_size = 1
        #ins.contr_size = 1.0
        #it appears that quantity is wrong and should be replaced in the trade
        pref.dMsg("INS.CONTR_SIZE="+str(ins.contr_size))
        
        #commit new or update changes
        ins.commit()
        
    def createInstrument(self, unqid, att):
        ins = ael.Instrument.new("FxSwap")
        self.editInstrument(unqid, att, ins)
        
    def updateInstrument(self, unqid, att):
        ins = ael.Instrument[unqid]
        self.editInstrument(unqid, att, ins.clone())
        
    
    
    def linkMessage2Instrument(self, trade, ins):        
        """ linking by changing the list in place """
        for i in range(len(trade)):
            (n, v) = trade[i]
            if n == "INSADDR.INSID":
                trade[i] = ("INSADDR.INSID", ins.insid)
            elif n == "INSADDR.INSTYPE":
                trade[i] = ("INSADDR.INSTYPE", ins.instype)
            elif n == "QUANTITY":
                # revise quantity to ensure values are proper
                # the meaning is something different
                trade[i] = ("QUANTITY", 1.0)
            elif n == "PREMIUM":
                    trade[i] = ("SENT_PREMIUM", v)
            elif n == "TARGET_PREMIUM":
                    trade[i] = ("PREMIUM", v)
    
    def getUnqINSID(self, unqid):
        # should it be possible to swap this ?
        return "abFX_"+unqid
    
    def messageM(self, pyl):
        """
        change the message
                
        """
        # assuming single trade in message
        tr = [l for (n, l) in pyl if type(l) == type(list())][0]
        d = dict(tr)
        
        # fetch the instrument belonging to the SWAP
        unqid = None
        for (n, l) in tr:
            if n == "ADDITIONALINFO":
                dx = dict(l)
                if dx["ADDINF_SPECNBR.FIELD_NAME"] == "zzBR_Trade":
                    unqid = dx["Value"]
        if unqid == None:
            raise Exception("Message should have contained a unique identifier named zzBR_Trade")
        
        #create or update instrument
        insid = self.getUnqINSID(unqid)
        if not self.insExists(insid):
            self.createInstrument(insid, d)
        else:
            self.updateInstrument(insid, d)
        #do we need this?
        ael.poll()

        ins = ael.Instrument[insid]
        # using the fact that lists are changed in place
        self.linkMessage2Instrument(tr, ins)
        
        #we need to edit the trade quantity
        #it appears that the quntity should be set to one
        #otherwise most parameters will be wrong (found out by creating the same trade
        # manually in the tradong manager)
        
        # uses the modified tr
        return pyl
    
 
    
    def messageVoid(self, pyl):
        """ void first part of FX Swap trades """
        tr = [l for (n, l) in pyl if type(l) == type(list())][0]
        for i in range(len(tr)):
            (n, v) = tr[i]
            if n == "STATUS":
                tr[i] = ("STATUS", "TRADE_STATUS_VOID")
        return pyl

    def __init__(self):
        self.count = 0
    
       
    
    def fixMessage(self, m):
                        
            if self.isSwap(m):
                reportMB("FxSWapInv sees message", m)
                pyd = self.mbf2py(m)               
                pyd = self.messageM(pyd)                
                self.pyreplace2mbf(m, pyd)
                
            # void these trades, if sent
            elif self.isVoid(m):
                pyd = self.mbf2py(m)               
                pyd = self.messageVoid(pyd)                
                self.pyreplace2mbf(m, pyd)
            
            return m
        
    def INSERT_TRADE(self, m):
        return self.fixMessage(m)
    
    def UPDATE_TRADE(self, m):
        return self.fixMessage(m)
        
    ## aditional methods for inheritance ###
    def isFXForward(self, m):
        """
        there are a few different trade_process numbers below
        """
        return hasPath(m, ["*Trade", "INSADDR.INSTYPE", "INS_CURR"]) \
            and (hasPath(m, ["*Trade", "TRADE_PROCESS", str(1<<12)])
                 or hasPath(m, ["*Trade", "TRADE_PROCESS", str(1<<13)]))



class SwapFXInvSender(SwapFXInv, FAMBAFilter):
    """
    Add additional data for the trade that goes to the target side.
    This is to retrieve information about related entites on the source 
    side to send the rest of the information to the target side.
    """
     
    def addAttrib(self, dict, name, trd):
        dict[name] = getattr(trd, name)
     

    def get_cash(self, trade):
        """Help function to calculate cash value of a trade.
        Premium of the trade is set to the cash value of both trades.
        
        The functions has problems due to weaknesses in the AMBA implementation
        hence should not be used.
        """
        context = acm.GetDefaultContext()
        sheetT = "FTradeSheet"
        trd = acm.FTrade[trade]
        calc_space = acm.Calculations().CreateCalculationSpace(context, sheetT) 
        value = calc_space.CalculateValue(trd, "Portfolio Accumulated Cash")
        pref.dMsg("Trade"+str(trade)+"value="+str(value))
        return value.Value().Number()
     
    def handleMessage(self, pyd):
        # find the trade
        trade = [l for (n, l) in pyd if type(l) == type(list())][0]
        att = dict(trade)
        con = int(att["CONNECTED_TRDNBR"])
        otr = ael.Trade[con]        
        # build list from pp() ?? no need could simply add those
     
        ainfo = {}
        self.addAttrib(ainfo, "price", otr)
        self.addAttrib(ainfo, "acquire_day", otr)
        self.addAttrib(ainfo, "value_day", otr)
        self.addAttrib(ainfo, "quantity", otr)
        self.addAttrib(ainfo, "premium", otr)
        # using in place editing of lists
        trade.append(("near_trade", ainfo.items()))
     
        #change at point
        acmContrd = int(att["CONNECTED_TRDNBR"])
        acmCurtrd = int(att["TRDNBR"])
        #ncash = self.get_cash(acmContrd)+self.get_cash(acmCurtrd)
        ncash = ael.Trade[acmContrd].premium + ael.Trade[acmCurtrd].premium
        pref.dMsg("acmContrd nbr "+str(acmContrd))
        pref.dMsg("acmContrd.premium"+str(ael.Trade[acmContrd].premium))
        pref.dMsg("acmCurtrd nbr "+str(acmCurtrd))
        pref.dMsg("acmCurtrd.premium "+str(ael.Trade[acmCurtrd].premium))
        pref.dMsg("ncash:"+str(ncash))
        trade.append(("TARGET_PREMIUM", ncash))
     
        return pyd
     
    def addTradeData(self, m):
        
         pyd = self.mbf2py(m)
         pyd = self.handleMessage(pyd)                
         self.pyreplace2mbf(m, pyd)
         return m
     
    def messageVoid(self, m):
            """Produce a message for the opposite trade and process it as if it was
            a proper trade, otherwise some updates do not go through"""
            pyd = self.mbf2py(m)               
            pyd = self.handleMessage(pyd)
            trade = [V for (N, V) in pyd if N == "TRADE" or N =="!TRADE"][0]
            conntrade = int([V for (N, V) in trade if N == "TRDNBR" 
                         or N == "!TRDNBR"][0])
            #assume that next trade is the connected trade
            atrade = ael.Trade[conntrade+1]
            if atrade==None or atrade.connected_trdnbr.trdnbr != conntrade:
                    pref.dMsg("No connected trade found returning nothing ("+str(conntrade)
                                +"),ael="+str(atrade)+" connected="+str(atrade.connected_trdnbr.trdnbr)
                                )
                    return None
            pref.dMsg("Found connected trade!!")
            proxy = ambProxy(atrade)
            pref.dMsg("Is proxy a swap? "+str(self.isSwap(proxy)))
            # send it through transformation,
            pref.dMsg("*"*40)
            pref.dMsg("Running second sweep")
            pref.dMsg("*"*40)
            proxyr = agentSecondSweep(proxy, defaultReverseSendMutators(), [])
            pref.dMsg("*"*40)
            self.pyreplace2mbf(m, proxyr.pyStruct())
            return m           
            
     
    def fixMessage(self, m):
            pref.dMsg("Running FXinvSender")
            if self.isSwap(m):
                pref.dMsg("isSwap proceeding")
                return self.addTradeData(m)
            elif self.isVoid(m):
                return self.messageVoid(m)
            return m

    def filter(self, m):
        # dont send insert, but if updates send the message anyway
        if self.isVoid(m) and (not hasPath(m, ["TYPE", "UPDATE_TRADE"])):
                # dont send the message
                return (False, 2000, 'Second trade part of an FXSwap trade')
        else:
                return (False, 0, '')

#
#Using the SwapFX to handle operations
#
#
#
class ForwardFXInv(SwapFXInv):
    """
    ...
    """

        
    def setRecLeg(self, rec_leg, ins, att, near_t, pay_leg):
        """
        ...
        """
        rec_leg.start_day = ael.date_from_string(att["VALUE_DAY"])
        rec_leg.nominal_factor = -1 *float(att["QUANTITY"]) / float(att["PREMIUM"])
        rec_leg.fixed_rate = 1.0
        # use default
        #rec_leg.end_day = ael.date_from_string(..)

        pref.dMsg("REC_LEG.FIXED_RATE="+str(rec_leg.fixed_rate))
        pref.dMsg("REC_LEG.NOMINAL_FACTOR="+str(rec_leg.nominal_factor))        


        
    def setPayLeg(self, pay_leg, ins, att, near_trade):
        """
        ....
        """      

        pay_leg.start_day = ael.date_from_string(att["VALUE_DAY"])
        pay_leg.nominal_factor = 1.0
        pay_leg.fixed_rate = 1.0
           


    def setRecLegFuture(self, rec_leg, ins, att, near_t, pay_leg):
        """
        ...
        """
        rec_leg.end_day = ael.date_from_string(att["VALUE_DAY"])
        
        points = (float(att["PRICE"]) - float(att["REFERENCE_PRICE"])) *10**4
        
        D = float(att["PREMIUM"])
        C = (0.01*D - points) / 0.01
 
        ins.contr_size =  C
 
        # there is an error with D or C or this value
        pay_leg.fixed_rate = -1*D/C+1     
 
        
        rec_leg.nominal_factor = float(att["QUANTITY"])/ C    
        rec_leg.fixed_rate = 0.0
        # changed to -1
        pay_leg.nominal_factor = 1.0 

        # use default
        #rec_leg.end_day = ael.date_from_string(..)
        pref.dMsg("PAY_LEG,REC_LEG===> future..")
        pref.dMsg("REC_LEG.FIXED_RATE="+str(rec_leg.fixed_rate))
        pref.dMsg("REC_LEG.NOMINAL_FACTOR="+str(rec_leg.nominal_factor))        
        pref.dMsg("PAY_LEG.FIXED_RATE="+str(pay_leg.fixed_rate))
        pref.dMsg("PAY_LEG.NOMINAL_FACTOR="+str(pay_leg.nominal_factor))        
        pref.dMsg("POINTS="+str(points))
        pref.dMsg("D="+str(D))
        pref.dMsg("C="+str(C))
        pref.dMsg("PRICE="+str(float(att["PRICE"])))
        pref.dMsg("REFERENCE_PRICE="+str(float(att["REFERENCE_PRICE"])))
        



    def setPayLegFuture(self, pay_leg, ins, att, near_trade):
        """
        ....
        """      
        pay_leg.end_day = ael.date_from_string(att["VALUE_DAY"])
     

    def getCurrencyPair(self, leftC, rightC):
        item = "%s/%s" % (leftC, rightC)
        pref.dMsg("Using %s as val direction" % item)
        q = "select seqnbr from CurrencyPair where name = '%s' " % item
        pref.dMsg("Using query %s " % q)
        val = getSQLVal(q)
        # dont try to find alternative paths for this
        if val == None:
            item = "%s/%s" % (rightC, leftC)
            q = "select seqnbr from CurrencyPair where name = '%s' " % item
            val = getSQLVal(q)
            if val == None:
                raise "No currency pair for translating %s " % item
        cnp = ael.CurrencyPair[int(val)]
        pref.dMsg("CNP getCurrencyPair "+ str(cnp))
        return cnp

    def getValDayDirection(self, att):
        """
        Determine if value day is before or after spot day..
        """
        # estimated approach is the following
        now = ael.date_from_string(att["VALUE_DAY"])
        
        leftC  = att["INSADDR.INSID"]
        rightC = att["CURR.INSID"]
        # this could also be reversed order ?
        
        cnp = self.getCurrencyPair(leftC, rightC)
        spot = cnp.spot_date(ael.date_today())
                    
        res = -2
        if now == spot:
            res = 0
        elif now < spot:
            res =-1
        else:
            res =  1
        return res

        
    def createInstrument(self, unqid, att):
        #
        #Create instrument as needed
        #called from changeForward by messageM
        #
        pref.dMsg("CreateInstrument!!")
        
  
        # supposedly has two legs and data from the previous trade
        ins = ael.Instrument.new("FxSwap")
        ins.insid = unqid
        (payleg, nonpayleg) = self.getPayRecLeg(ins)
        leg = ins.legs()
        pay_leg = leg[payleg]
        rec_leg = leg[nonpayleg]
        #far_trade_att = att        
        ins.exp_day = ael.date_from_string(att["VALUE_DAY"])
        
        #the leg that is changed needs to be different depending on these
        # values
        dir =  self.getValDayDirection(att)
        if dir == -1:
            rec_leg.nominal_at_start = 1
            pay_leg.nominal_at_start = 1
            rec_leg.nominal_at_end   = 0
            pay_leg.nominal_at_end   = 0
            self.setPayLeg(pay_leg, ins, att, dict())
            self.setRecLeg(rec_leg, ins, att, dict(), pay_leg)
            ins.contr_size =  float(att["PREMIUM"])
            
        elif dir == 0:
            rec_leg.nominal_at_start = 1
            pay_leg.nominal_at_start = 1
            rec_leg.nominal_at_end   = 0
            pay_leg.nominal_at_end   = 0
            self.setPayLeg(pay_leg, ins, att, dict())
            self.setRecLeg(rec_leg, ins, att, dict(), pay_leg)
            ins.contr_size =  float(att["PREMIUM"])

        else: 
            rec_leg.nominal_at_start = 0
            pay_leg.nominal_at_start = 0
            rec_leg.nominal_at_end   = 1
            pay_leg.nominal_at_end   = 1
            # reversed leg order
            self.setPayLegFuture(pay_leg, ins, att, dict())
            self.setRecLegFuture(rec_leg, ins, att, dict(), pay_leg)

 
        # must be called after
        #is not supposed to             
        pref.dMsg("INS.CONTR_SIZE="+str(ins.contr_size))                
        ins.commit()
 
    
    
    def changeForward(self, m):
        pass
        reportMB("ForwardFXInv sees message", m)
        pyd = self.mbf2py(m)               
        pyd = self.messageM(pyd)                
        self.pyreplace2mbf(m, pyd)
        return m
    
    def fixMessage(self, m):
        """
        fix message
        """
        if self.isFXForward(m):
            return self.changeForward(m)            
        else:
            return m



class InstrumentFix(FAMBA_mutator):
    """
    This class is to add external IDs to legs on the instrument.
    This is in turn a fix to prevent th wrong leg to be updated on
    instrument update and insert
    
    The fixed rate also seems to be a problem as it converts itself
    to 1.0 ? both features fixed.
    
    check when this diffiers in FAMBA_BridgeM fixLegnbr
    Appears that fetchPath is problematic below
    TODO: test that this can be saffely removed
    TODO: check the influence of this on FX
    """
    def fixMessage(self, m):
        # pass
        if fetchPath(m, ["*INSTRUMENT", "LEG", "LEGNBR"]):
            # get all legs
            # get python form
            message = self.mbf2py(m)
            # get instrumenut            
            ins = [I for (N, I) in message if N =="!INSTRUMENT"
                       or N == "+INSTRUMENT" or N=="INSTRUMENT"][0]
            legs = [l for (n, l) in ins if n == "LEG"]
            # using  the fact that are not copied when doing list co
            for leg in legs:
                elem = ""
                fixed_rate = ""
                for i in leg:
                    (N, B) = i
                    if N == "LEGNBR":
                        elem = B
                    elif N == "FIXED_RATE":
                        fixed_rate = B
                # patches problems with leg order
                leg.append(("EXTERN_ID", "L"+str(elem))) 
                # patches rate problems
                if fixed_rate == "":
                    leg.append(("FIXED_RATE", "0"))
                    
            
            #changing the message
            self.pyreplace2mbf(m, message)
        return m
    
    def INSERT_INSTRUMENT(self, m):
        return self.fixMessage(m)
    
    def UPDATE_INSTRUMENT(self, m):
        pref.dMsg("INSTRUMENTFIX INSERT_INSTRUMENT")
        return self.fixMessage(m)
    

class PrimaryKeyAdjuster(FAMBA_mutator):

    def isReverseDirection(self):
        return False

    def mutate(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        table = getCamelCaseTableName(tableName)
        if table in mainTablesWithoutUniqueKey:
            m = sender_modify_table(m, getCamelCaseTableName(tableName),
                                    self.isReverseDirection()) 
        return m

class ReversePrimaryKeyAdjuster(PrimaryKeyAdjuster):
    
    def isReverseDirection(self):
        return True
    
    
#------------------------------------------------------------------------------------
#The oldie or style of parameter settings, needed for old customers and old setups
#
#------------------------------------------------------------------------------------

class NotBridgeTableFilter(FAMBAFilter):
    
    def filter(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        if notBridgeTables.has_key( tableNameCC ):
              # if message has the attributes from notBridgeTables then it is not transferable
             return self.isMessageIncludedInDict( m, notBridgeTables, tableNameCC)
        return (True, 0, '')
         
    def isMessageIncludedInDict(self, m, dict, tableNameCC):
        """
        Check whether the message has the attributes from dict.
        """      
        if not dict[tableNameCC].keys():
            # no subdictionary => all 'tableName' messages are in dict
            return (False, 1020, '')
        for key in dict[tableNameCC].keys():
            filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
            if filterValue in dict[tableNameCC][key]:
                # only 'tableName' messages with certain attributes are in dict
                return (False, 1030, '')
        # other 'tableName' messages are not in dict
        return (True, 0, '')

class BridgeTableFilter(FAMBAFilter):

    def filter(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        #using dictonary in old style
        if bridgeTables.has_key( tableNameCC ):
           # if message has the attributes from bridgeTables then it is transferable 
           return self.isMessageIncludedInDict( m, bridgeTables, tableNameCC)
        return (True, 0, '')

    def isMessageIncludedInDict(self, m, dict, tableNameCC):
        """
        Check whether the message has the attributes from dict.
        """      
        if not (tableNameCC in dict):
            return (True, 0, '')
        
        if not dict[tableNameCC].keys():
            # no subdictionary => all 'tableName' messages are in dict
            return (True, 1025, '')
        for key in dict[tableNameCC].keys():
            filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
            if filterValue in dict[tableNameCC][key]:
                # only 'tableName' messages with certain attributes are in dict
                return (True, 1035, '')
        # other 'tableName' messages are not in dict
        return (True, 0, '')

#------------------------------------------------------------------------------------
#The AND style of parameter settings, more powrful and better?
#Imported if settings are porperly done in AMBA_Bridge_pref
#New features should not destroy old settings
#------------------------------------------------------------------------------------

#notBridgeTables
class ANDNotBridgeTableFilter(FAMBAFilter):

    def bestMatch(self, X, F, V, D):
            NF, NV, ND = X
            if NV > V:
                    return (NF, NV, ND)
            else:
                    return (F, V, D)

    def filter(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        F = True;
        V = 0
        D = ''
        pref.dMsg("ANDNotBridgeTableFilter "+tableNameCC)
        for i in notBridgeTables:
           if (i[0].upper()) == (tableNameCC.upper()):
                   # if message has the attributes from bridgeTables then it is transferable 
                   RES = self.isMessageInDict( m, i[1], tableNameCC)
                   #pref.dMsg("ANDNotBridgeTableFilter line "+str(i)+" res="+str(RES))
                   F, V, D =  self.bestMatch(RES, F, V, D)
                   pref.dMsg("Matching (%s,%s,%s) pattern %s " % (F, V, D, i))

        return (F, V, D)

    def isMessageInDict(self, m, wattrib, tableNameCC):
        """
        Check whether the message has the attributes from dict.
        """      
        if wattrib == {}:
            return (False, 1025, '')
        V = 1030
        for key in wattrib.keys():
            filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
            pref.dMsg("isMessageInDict (%s,%s,%s) " % 
                        (filterValue, key, wattrib[key]))
            if filterValue and filterValue == wattrib[key]:
                # only 'tableName' messages with certain attributes are in dict
                V = V + 0.01
            else:
                V = 0
                break; # skip processing
        # other 'tableName' messages are not in dict
        return (False, V, '')

class ANDBridgeTableFilter(FAMBAFilter):

    def bestMatch(self, X, F, V, D):
            NF, NV, ND = X
            if NV > V:
                    return (NF, NV, ND)
            else:
                    return (F, V, D)

    def filter(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        F = True;
        V = 0
        D = ''
        for i in bridgeTables:
           if i[0] == tableNameCC:
                   # if message has the attributes from bridgeTables then it is transferable 
                   RES = self.isMessageInDict( m, i[1], tableNameCC)
                   #pref.dMsg("ANDBridgeTableFilter line "+str(i)+" res="+str(RES))
                   F, V, D =  self.bestMatch(RES, F, V, D)
        #return (True,0,'')
        return (F, V, D)

    def isMessageInDict(self, m, wattrib, tableNameCC):
        """
        Check whether the message has the attributes from dict.
        """      
        if wattrib == {}:
            return (True, 1025, '')
        V = 1030
        for key in wattrib.keys():
            filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
            if filterValue and filterValue == wattrib[key]:
                # only 'tableName' messages with certain attributes are in dict
                V = V + 0.01
            else:
                V = 0
                break; # skip processing
        # other 'tableName' messages are not in dict
        return (True, V, '')

#------------------------------------------------------------------------------------


class PathMessageFilter(FAMBAFilter):
    """
    Needs improvment to be useful
    """
    def filter(self, m):
        # filtered by message path
        if isMessageInPathStruct(m):
            return (False, 1100, '')
        return (True, 0, '')
    
    
class Update2Insert(FAMBA_mutator):
    
    
    def getOperation(self, m):
        op = RE_OP.match(getMessageType(m)).group(0)
        return op
    
    def getTableName(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        return tableName
    
    def name(self):
        return "u2i"
    
    def operation(self):
        return "UPDATE"

    def synop(self):
        return "!"
    
    def outOperator(self):
        return "INSERT_"
    
    def outSymbol(self):
        return "+"
    
    def mutate(self, m):
        #reportMB(self.name()+" before processing",m) 
        op = self.getOperation(m)
        pref.dMsg("op is "+str(op))
        tableName = self.getTableName(m)
        if op == self.operation():
            self.replace(m, ["TYPE"], str(self.outOperator()+tableName))
            m.mbf_last_object() # attach last
            nlist = m.mbf_start_list(self.outSymbol()+tableName)            
            o = m.mbf_find_object(self.synop()+tableName)
            self.copy(o, nlist)
            self.delete(m, [self.synop()+tableName])
            
            pass
        #reportMB(self.name()+" after processing",m)
        return  m

class Delete2Insert(Update2Insert):
    """ using the behaviour of Update2Insert"""
    def name(self):
        return "d2i"
    
    def operation(self):
        return "DELETE"
    
    def synop(self):
        return "-"
    
class Update2Delete(Update2Insert):
    
    def name(self):
        return "u2d"
    
    def operation(self):
        return "UPDATE"
    
    def synop(self):
        return "!"
    
    def outOperator(self):
        return "DELETE_"
    
    def outSymbol(self):
        return "-"

class Insert2Delete(Update2Delete):
    
    def name(self):
        return "i2d"
    
    def operation(self):
        return "INSERT"
    
    def synop(self):
        return "+" 
    
    

    
class SpecialRecordsFilter(FAMBAFilter):
    """ used to return something illegal at times """
    def filter(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        if specialRecords.has_key( tableNameCC ):
             return self.isMessageIncludedInDict( m, specialRecords, tableNameCC)
             # special records which we don't want to send through
        return (True, 0, '')

    def isMessageIncludedInDict(self, m, dict, tableNameCC):
        """
        Check whether the message has the attributes from dict.
        """      
        if not dict[tableNameCC].keys():
            # no subdictionary => all 'tableName' messages are in dict
            return (False, 150001, '')
        for key in dict[tableNameCC].keys():
            filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
            if filterValue in dict[tableNameCC][key]:
                # only 'tableName' messages with certain attributes are in dict
                return (False, 150002, '')
        # other 'tableName' messages are not in dict
        return (True, 0, '')

        

class MultiTableMutator(FAMBA_mutator, FAMBAFilter):
    """
    Fixes references insid messages    
    
    """
    
    def getTranslatedPrimaryKey(self, A, B):
        # forward direction
        return getTranslatedPrimaryKey(A, B, False)
            
    
    def verboseError(self, m):
            mess = self.mbf2py(m)
            xtrainfo = ""
            l = [V for K, V in mess if(K == "TRADE" or K== "!TRADE"
                                        or K == "+TRADE")]
            if(len(l)==1):
                    v = [V for K, V in l[0] if K == "INSADDR.INSID"
                         or K == "+INSADDR.INSID"
                         or K == "!INSADDR.INSID"]
                    if(len(v)>0):
                            xtrainfo = " Instrument is '%s'. " % v[0]
            return xtrainfo
                    
    def filter(self, m):
        """
        We should check if this message is connected to anything like below in 
        receiver_modify_table and and return pretty negative reaction to it.
        
        This allows us to write a proper override later on
        
        Needed is a better check for messages
        
        Should probably be removed as this it not useful to
        have anymore.
        
        """
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        tableNameCC = getCamelCaseTableName(tableName)
        obj = find_mbf_object(m, tableName)
        if not obj:
            return (False, 10000, 'Message not complete')                    

        op = RE_OP.match(getMessageType(m)).group() 
        if op == "INSERT":
                return (True, 0, '')
    
        if tableNameCC in mainTablesWithoutUniqueKey:
            primaryKey = getKeyName(tableNameCC)
            ref = obj.mbf_find_object(primaryKey)
            
            if ref:
                ref_value = ref.mbf_get_value()
                translated_nbr = self.getTranslatedPrimaryKey(tableNameCC, ref_value)
                pref.dMsg("translated_nbr is "+str(translated_nbr))
                if not translated_nbr:
                    if op == "INSERT":
                        return (True, 0, '')
                    else:
                        # This exception means there is no mapping for a key that should have
                        # mapping. Resolve manually before starting AMBA bridge again.
                        xtrainfo = self.verboseError(m)
                        val = "E404 Could not find key for '%s' in table %s. %s" % (str(ref_value), tableNameCC, xtrainfo)
                        return (False, 10001, val)
        return (True, 0, '')
    
    
    def mutate(self, m):
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
        op = RE_OP.match(getMessageType(m))         
        out =  self.receiver_modify_table(m, getCamelCaseTableName(tableName), op.group()) 
        reportMB("-- answer from mutate of MultiTableMutator --", out)
        return out
    
    
    def correct_FXSPOT(self, tableName, obj):
        """ Fix for FX Spot trade: adds refence_price, with its value equal to price. """
        # this stuff should idealy be moved to its own mutator class 
        if tableName == 'Trade':   
            return corrections_FxSpot(obj)
        else:
            return obj
    
    
    def adjustMainTabkesWithoutUniqueKey(self, obj, tableName, op):
        """ Find and change/remove primary key for tables without unique key since this 
            could otherwise cause unwanted updates/overwrites in the receiving system. """
            
        if tableName in mainTablesWithoutUniqueKey:
            primaryKey = getKeyName(tableName)
                
            if op == "INSERT":
                obj = remove(obj, primaryKey)
            else:
                    try:
                        obj = self.replace_reference(obj, tableName, primaryKey)
                    except Exception, e:
                        # Could not find mapping to this primary key. OK if insert operation. Not otherwise.
                        if op == "INSERT":
                            obj = remove(obj, primaryKey)
                            # need to re add the information using additional keys
                        else:
                            #this may now be overidden on th target side
                            pref.dMsg("Mapping to primary key not found but it should be there. Resolve manually. No updates will occur.")
                            pref.dMsg("Reason:"+str(e))
                            #pref.dMsg(m.mbf_object_to_string())
        return obj

    def adjustOtherReferenceKeys(self, obj, tableName, op):
        """ Find and change other reference keys in this message if needed. """
        if referenceDic.has_key(tableName):
            for key in referenceDic[tableName].keys():
                pref.dMsg("referenceDic replacing "+str(key))
                
                #CREATE HIDDEN FIELDS
                ref = obj.mbf_find_object(key)
                if ref:
                    pref.dMsg("adding hidden field")
                    ref_value = ref.mbf_get_value()
                    # add hidden value for future reference (needed by Swap func)
                    pref.dMsg("_HIDDEN adding (%s,%s)" % ("_"+key, str(ref_value)))
                    obj.mbf_add_string("_"+key, str(ref_value))
                else:
                    pref.dMsg("not add _HIDDEN "+str(key))
                #
                
                if(op!="INSERT"):
                        try:                    
                            obj = self.replace_reference(obj, referenceDic[tableName][key], key)
                        except Exception, e:
                            pref.dMsg("removing and replacing reference "+key)
                            obj = remove(obj, key)                    
                            # report any errors
                            pref.dMsg("Warning "+str(e))
                            #e.printStackTrace()
                else:
                        pref.dMsg("Will not resiolve "+key+" on insert")
                        obj = remove(obj, key)
        return obj
    
    def receiver_modify_table(self, m, tableName, op):
        """
        Change parts of a message
        """
        obj = find_mbf_object(m, tableName)
        if not obj:
            return m
     
        """ Find and change/remove primary key for tables without unique key since this 
            could otherwise cause unwanted updates/overwrites in the receiving system. """
        obj = self.adjustMainTabkesWithoutUniqueKey(obj, tableName, op)
              
        #
        #This has been added to remove all keys that could cause problems for the AMBA
        # and synchronization. If seqnbr are similar in both simulator environments
        # keeping primary keys (auto count numbers) could possible hide obvious errors
        # that will be created in the customer database.
        # Hence remove anything that may cause errors below
        #
        """ Remove useless primary auto number keys which are not the same accross different
        systems. But dont change primary keys that use additional advice"""
        if not (tableName in mainTablesWithoutUniqueKey):
            pref.dMsg("Deleting junk keys!!")
            primaryKey = getKeyName(tableName)
            obj = remove(obj, primaryKey)
    
        """ Find and change other reference keys in this message if needed. """
        obj = self.adjustOtherReferenceKeys(obj, tableName, op)
        
        """ Several small correction scripts for known problems in AMBA bridge """
        """ PortfolioLink with uknown portfolio, SPR 276209 """
        if tableName == 'Portfolio':
            obj = corrections_CheckForMissingPortfolio(obj)
       
        obj = self.correct_FXSPOT(tableName, obj)

        
        # for internal use for handling references
        obj.mbf_add_string('AMBA_BRIDGE_REF_RES', "1")
                        
        #remove indirect illegal references
        self.removeIllegalLinkFields(obj, tableName)
        
        return m


    def removeIllegalLinkFields(self, obj, tableName):
            if not tableName in referenceDic:
                    return
            bl = referenceDic[tableName]
            # we need to scan the object for indirect illegal references
            elems = self.mbf2py(obj)
            pref.dMsg("removeIllegalLinkFields E="+str(elems))
            for (k, v) in elems:
                    pref.dMsg("removeIllegalLinkFields "+str((k, v)))
                    if len(k.split("."))>1 and ((k.split("."))[-1]) in bl:
                            #remove illegal indirect reference
                            pref.dMsg("removing "+k)
                            remove(obj, k)
                            


    def replace_reference(self, m, table, key):
        """ Replaces the field key, which should be a primary key reference,
            with the corresponding key in the destination system. """
        pref.dMsg("replace_reference call "+str(m)+" "+str(table)+" "+str(key))
        ref = m.mbf_find_object(key)
        if ref:
            ref_value = ref.mbf_get_value()
            pref.dMsg("replace_reference ref="+str(ref_value))
            translated_nbr = self.getTranslatedPrimaryKey(table, ref_value)
            pref.dMsg("self.replace_reference nbr="+str(translated_nbr))
            if translated_nbr!=None:
                ref = m.mbf_find_object(key)
                m.mbf_replace_string(key, str(translated_nbr))
            else:
                # This exception means there is no mapping for a key that should have
                # mapping. Resolve manually before starting AMBA bridge again.
                val = "Could not find key for '%s' in replace_reference." % str(ref_value)
                pref.dMsg(val) 
                raise Exception, val
        return m
    
    

class ReverseMultiTableMutator(MultiTableMutator):

    def getTranslatedPrimaryKey(self, A, B):
        # forward direction
        return getTranslatedPrimaryKey(A, B, True)
         
                  
    def correct_FXSPOT(self, tableName, obj):
        """ in upstream direction we should not try to do anythin """
        return obj
         
# -----------------------------------------------------------
# Helper functions. 
# -----------------------------------------------------------  

# should be converted into an agent
# and removed from the change mess
def corrections_CheckForMissingPortfolio(obj):
    """ Checks if there is PortfolioLink in the portfolio message and if the
        related portfolio exists in the database of the receiving system.
        If the related portfolio doesn't exist, portfoliolink is removed.
        Implemented to avoid AMBA crashing (SPR 276209) """
    portLink = find_mbf_object(obj, 'PortfolioLink')
    while portLink:
        if portLink.mbf_get_name() in ['PORTFOLIOLINK', '!PORTFOLIOLINK', '+PORTFOLIOLINK']:
            portId = getMBFMessageValueInObject(portLink, 'MEMBER_PRFNBR.PRFID')
            if not ael.Portfolio[portId]:
                ael.log('Portfolio %s not found. Related PortfolioLink is removed' %portId)
                obj.mbf_remove_object()
        portLink = obj.mbf_next_object()
        
    return obj

# should be corrected
#
#Looks old should be replaced or removed
#TODO check if still in use
#
def corrections_FxSpot(obj):
    """ Fix for FX Spot trade: add refence_price (with its value equal to price) 
        and trade_process (=4096). 
        Implemented to bridge a difference in ADM 2.2 and 4.0."""
    tradeInstype = getMBFMessageValueInObject(obj, 'INSADDR.INSTYPE')
    if tradeInstype in ['INS_CURR', 'Curr']:
        try:
            price = getMBFMessageValueInObject(obj, 'PRICE')
            obj.mbf_add_string('REFERENCE_PRICE', price)
            obj.mbf_add_string('TRADE_PROCESS', '4096')
        except:
            ael.log("Failed fix of FX Spot")
    return obj


def find_mbf_object(m, key):
    """ Returns an mbf-object with defined key contained in the 
        mbf-object m. If the key is not found directly the function 
        will try to look for key '!key' and '+key' as well. """
    obj = m.mbf_find_object(key)
    if not obj:
        obj = m.mbf_find_object('!' + key)
    if not obj:
        obj = m.mbf_find_object('+' + key)
    if not obj:
        obj = m.mbf_find_object('-' + key) 
    if not obj:
        return None
    return obj


def getCamelCaseTableName(table):
    """ Matches entered table name of any casing to camel case table
        name. Returns this name if found. Returns None otherwise. """
    tabLower=table.lower()
    for name in dir(ael):
        if name.lower() == tabLower and type(eval('ael.'+name)) == ael.ael_table:
            return name
    return None


def getKeyName(recType): 
    """ Returns the name of the primary key of this record. """
    
    for k in eval('ael.' + recType + '.keys()'):
        if k[1] == 'primary': 
            primary = k[0]
    if primary:
        pref.dMsg("Primary key for recType " + recType + " is " + primary.upper())
        return primary.upper() 
    else: 
        pref.eMsg("Error: Failed finding primary key for %s" % (recType))
        raise Exception('Missing primary key')


def getMBFMessageValue(m, tableName, key):
    """ Finds first tableName object in m, then key in it and finaly the value 
        for the key. """
    obj = find_mbf_object(m, tableName)
    if not obj:
        raise RuntimeError, "%s message is not complete." %tableName
    return getMBFMessageValueInObject(obj, key)

def getMBFMessageValueInObject(obj, key):
    """ Finds key in object obj and returns its value. """
    tag = obj.mbf_find_object(key, 'MBFE_BEGINNING')
    if tag:
        return tag.mbf_get_value()
    return None

def getMessageType(m):
    """ Returns a string with the message type of the mbf-object m. """
    type = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    return type.mbf_get_value()


def getTranslatedPrimaryKey(table, key,reverse=False):
    """ Returns destination system primary key given source system primary key 
        and table. Updates dictionary if needed. """
    #
    #lookups could be done in a better way
    #
    global addinfoDic
    initAddinfoDic(reverse) # Initialize dictionary with old-new trdnbr mapping.
    
    if addinfoDic[table].has_key(key):
        return str(addinfoDic[table][key])
    else:
        #poll first as ael cache is inaccurate at times!!=??
        #ael.poll()
        #was addinf_specnbr
        ais = ael.AdditionalInfoSpec[(directionalPrefix(reverse) + table)]
        for ai in ael.AdditionalInfo.select('addinf_specnbr=%d' % ais.specnbr):
            if ai.value == key:
                addinfoDic[table][ai.value] = ai.recaddr # Add value to dictionary.
                return str(ai.recaddr)
        #failing that try to extract the value from the table
        try:
                #issues with new trades being produced
                #problem two partially identical databases
                #if a trade is created on old side it may be equal to old
                #side trade, and update that erroneously
                #hence creation time on old side should be used to verify
                #match by cloning
                #hence creation time must be fetched from message
                #this should only happen in partially synchronized 
                #simulator enviroments
                pref.dMsg("Trying to retrieve element from table "+str(table)+" key "+str(key))
                elem = getattr(ael, table)[int(key)]
                if (int(elem.creat_time) < pref.databaseCloneTime()):
                        addinfoDic[table][key] = str(key)
                        pref.dMsg("Found element by original OID "+str(key))
                        return str(key)
                else:
                        pref.dMsg("Unable to locate element created before database cloning")
        except Exception, e:
              pref.dMsg("Unable to find item reason "+str(e))  
    return None

def initAddinfoDic(reverse=False):
    """ Init dictionary with primary key and addinfo field (primary key in other system)."""
    global addinfoDic
    if addinfoDic: return # Already initialized.
    for table in mainTablesWithoutUniqueKey:
        tempDic = {} 
        aiPrefix = directionalPrefix(reverse)
        ais = FAMBA_BridgeLib.addInfoSpecRdOrNew(table, reverse)        
        addinfoDic[table] = tempDic


def isBridgeMessage(m, extTableName = None):
    """
    Check whether the message is transferable according to dictionaries 
    notBridgeTables and bridgeTables.
    Child records are handled by the extTableName var and
    return indicates only if the child record is allowed inside
    the message.
    
     """
    if extTableName == None:       
        tableName = RE_TABLE.search(getMessageType(m)).group('table')
    else:
        #to support filtering child records
        tableName = extTableName
    tableNameCC = getCamelCaseTableName(tableName)
    if specialRecords.has_key( tableNameCC ):
        if isMessageIncludedInDict( m, specialRecords, tableNameCC):
            # special records which we don't want to send through
            return 0

    # filtered by message path
    if isMessageInPathStruct(m):
            return 0
        
    if bridgeTables.has_key( tableNameCC ):
        # if message has the attributes from bridgeTables then it is transferable 
        return isMessageIncludedInDict( m, bridgeTables, tableNameCC)
    if notBridgeTables.has_key( tableNameCC ):
        # if message has the attributes from notBridgeTables then it is not transferable
        indict = not isMessageIncludedInDict( m, notBridgeTables, tableNameCC)
        return indict
    # 'tableName' isn't from any of the dictionaries, hence isTransferableDefault needed
    if isTransferableDefault == 0:
        return 0
    return 1
    

def isBridgeRecord(e):
    """ Check whether the record is transferable according to
        notBridgeTables and bridgeTables """
    #TODO replace this with something that actualy works i.e. parse the message into an MBF look alike
    recordType=e.record_type
    if bridgeTables.has_key(recordType):
        return isRecordIncludedInDict(e, bridgeTables, recordType)
    if notBridgeTables.has_key(recordType):
        return not isRecordIncludedInDict(e, notBridgeTables, recordType)
    if isTransferableDefault == 0:
        return 0
    return 1

def isMessageIncludedInDict(m, dict, tableNameCC):
    """
    Check whether the message has the attributes from dict.
    """       
    if not dict[tableNameCC].keys():
        # no subdictionary => all 'tableName' messages are in dict
        return 1
    for key in dict[tableNameCC].keys():
        filterValue = getMBFMessageValue(m, tableNameCC.upper(), key)
        if filterValue in dict[tableNameCC][key]:
            # only 'tableName' messages with certain attributes are in dict
            return 1
    # other 'tableName' messages are not in dict
    return 0

def isMessageInPathStruct(m):
    """
    Examine if there are matching filter packages
    """
    if(hasattr(pref, "filterPaths")):
       list = pref.filterPaths()
    else:
       list = []
    #pref.dMsg("Using filters "+str(list))
    for package in list:
        filter = True
        for entry in package:
            pref.dMsg("Testing message against "+str(entry) )
            if not hasPath(m, entry):
                filter = False
        if filter == True:
            pref.dMsg("Message matching "+str(package)+" removing string")
            return True
    return False

def isRecordIncludedInDict(e, dict, tableNameCC):
    """
    Check whether record 'e' has the attributes from dict.
    """       
    if not dict[tableNameCC].keys():
        # no subdictionary => all 'tableName' records are in dict
        return 1
    for key in dict[tableNameCC].keys():
        filterValue = eval('e.'+ key)
        if filterValue in dict[tableNameCC][key]:
            # only 'tableName' records with certain attributes are in dict
            return 1
    # other 'tableName' records are not in dict
    return 0

def receiver_modify_table(m, tableName, op):
    """ Update primary key and other references with keys of new system. 
        Will also remove keys that yet have no corresponding reference. 
        
    
        Should perhaps be split into several parts ?
        The raise checks, will be moved outside this script,
        They not be part of this processing
    """
    obj = find_mbf_object(m, tableName)
    if not obj:
        raise RuntimeError, "Message %s is not complete." %tableName
     
    """ Find and change/remove primary key for tables without unique key since this 
        could otherwise cause unwanted updates/overwrites in the receiving system. """
    if tableName in mainTablesWithoutUniqueKey:
        primaryKey = getKeyName(tableName)
        try:
            obj = replace_reference(obj, tableName, primaryKey)
        except Exception, e:
            # Could not find mapping to this primary key. OK if insert operation. Not otherwise.
            if op == "INSERT":
                obj = remove(obj, primaryKey)
            else:
                pref.eMsg("Mapping to primary key not found but it should be there. Resolve manually. No updates will occur.")
                pref.eMsg("Reason:"+str(e))
                pref.eMsg(m.mbf_object_to_string())
                #ael.log("Mapping to primary key not found but it should be there. Resolve manually. No updates will occur.")
                return None
                
    #
    #This has been added to remove all keys that could cause problems for the AMBA
    # and synchronization. If seqnbr are similar in both simulator environments
    # keeping primary keys (auto count numbers) could possible hide obvious errors
    # that will be created in the customer database.
    # Hence remove anything that may cause errors below
    #
    """ Remove useless primary auto number keys which are not the same accross different
    systems. But dont change primary keys that use additional advice"""
    if not (tableName in mainTablesWithoutUniqueKey):
        pref.dMsg("Deleting junk keys!!")
        primaryKey = getKeyName(tableName)
        obj = remove(obj, primaryKey)
    
    
    """ Find and change other reference keys in this message if needed. """
    if referenceDic.has_key(tableName):
        for key in referenceDic[tableName].keys():
            try:
                obj = replace_reference(obj, referenceDic[tableName][key], key)
            except:
                obj = remove(obj, key)
                
    """ Several small correction scripts for known problems in AMBA bridge """
    """ PortfolioLink with uknown portfolio, SPR 276209 """
    if tableName == 'Portfolio':
        obj = corrections_CheckForMissingPortfolio(obj)
    """ Fix for FX Spot trade: adds refence_price, with its value equal to price. """
    if tableName == 'Trade':   
        obj = corrections_FxSpot(obj)
                
    return m
    
#
#This looks buggy
#
def remove(m, key):
    """ Removes an mbf_object with key 'key' within the given mbf_object 'm'. """
    obj = m.mbf_find_object(key)
    if obj:
        m.mbf_remove_object()
    return m


def replace(m, key, val):
    """ If there exists a key 'key' in the mbf_object 'm' the value of it 
        is replaced with value 'val'. """
    item = m.mbf_find_object(key)
    if item:
        m.mbf_replace_string(key, str(val))        
    return m

#
#Likely to be obsolete and replaced by replace_reference in MultiTableMutator
#There are still a few replace_reference pointing at this, most of those should no 
# longer be used
#
def replace_reference(m, table, key):
    """ Replaces the field key, which should be a primary key reference,
        with the corresponding key in the destination system. """
        
    raise "obsolete function called"
        
    pref.dMsg("replace_reference call "+str(m)+" "+str(table)+" "+str(key))
    ref = m.mbf_find_object(key)
    if ref:
        ref_value = ref.mbf_get_value()
        pref.dMsg("replace_reference ref="+str(ref_value))
        translated_nbr = getTranslatedPrimaryKey(table, ref_value)
        if type(translated_nbr) == type(list()):
            pref.dMsg("Could not resolve %s multiple options!!" % str(key))
            return
        pref.dMsg("replace_reference X nbr="+str(translated_nbr))
        if translated_nbr!=None:
            pref.dMsg("translated_nbr true") 
            ref = m.mbf_find_object(key)
            pref.dMsg("replace_reference changing "+ref.mbf_get_name())
            m.mbf_replace_string(key, str(translated_nbr))
        else:
            pref.dMsg("translated_nbr false")
            # This exception means there is no mapping for a key that should have
            # mapping. Resolve manually before starting AMBA bridge again.
            val = "Could not find key for '%s' in replace_reference." % str(ref_value)
            pref.dMsg(val) 
            raise Exception, val
        pref.dMsg("end of replace reference")
    else:
        pref.dMsg("replace_reference no reference found!!")
    return m
    

def sender_modify_table(m, tableName,reverse=False):
    """ Makes sure that the message gets its primary key in an addinfo field. 
        This is later used for lookup in the receiving system. """
    
    obj = find_mbf_object(m, tableName)
    if not obj:
        raise RuntimeError, "Message %s is not complete." %tableName

    aiPrefix = directionalPrefix(reverse)
    pref.dMsg("sender_modify_table prefix "+aiPrefix+" reverse "+str(reverse))
    primaryKey = getKeyName(tableName)
    key = obj.mbf_find_object(primaryKey)
    if key:
        value = key.mbf_get_value()
    if value:
        ai = obj.mbf_start_list('ADDITIONALINFO')
        ai.mbf_add_string('ADDINF_SPECNBR.FIELD_NAME', (aiPrefix + tableName))
        ai.mbf_add_string('Value', value)
    else:
        pref.eMsg("Trying to send message without primary key.")    
                
    return m


def directionalPrefix(reverse=False):
    if reverse:
        return reverse_addinfo_prefix
    else:
        return addinfo_prefix

# -----------------------------------------------------------
# Validation functions.
# -----------------------------------------------------------  
#
#
#These functions do no follow the new style of filtering.
#This means that functions below are inaccurate.
#
#
#
def amba_bridge_validate_entity_dest(e, op):
    """ validation function in the receiving system """
    try:
        theUser = ael.user().userid
        if theUser != 'AMBA' and e.record_type in allowedTablesInDest:
            return 1
        if theUser != 'AMBA' and not isBridgeRecord(e):
            return 1
        elif theUser == 'AMBA' and isBridgeRecord(e):
            return 1
        else:
            return 0
    except:
        ael.log('Validation amba_bridge_validate in destination system failed.')
        return 1

def amba_bridge_validate_entity_source(e, op):
    """ validation function in the sending system """
    try: 
        if e.record_type in allowedTablesInSource:
            return 1
        if isBridgeRecord(e):
            return 1
        else:
            return 0
    except:
        ael.log('Validation amba_bridge_validate in source system failed.')
        return 1

## helpful function that makes it simple to get single
## only usable to get single value from multiple values
def getSQLList(query):
    res = ael.asql(query)
    val = res[1][0]
    list = []
    [list.append(v[0]) for v in val]
    return list




#
#
#
#
"""Replacing CONTEXT_FUNDING_RATES with CONTEXT_FUNDING_PARAMETERS
      in context objects containing contextlinks
   
"""
class ContextLink_processor(FAMBA_mutator):
   
     
    def UPDATE_CONTEXT(self, msg):
        pref.dMsg("/\\UDATE_CONTEXT/\\")
        pref.dMsg("UDATE_CONTEXT")
        self.replace(msg, ["CONTEXT", "CONTEXTLINK", "TYPE"], ("CONTEXT_FUNDING_RATES", "CONTEXT_FUNDING_PARAMETER"))
        self.replace(msg, ["!CONTEXT", "+CONTEXTLINK", "TYPE"], ("CONTEXT_FUNDING_RATES", "CONTEXT_FUNDING_PARAMETER"))
        self.replace(msg, ["!CONTEXT", "!CONTEXTLINK", "TYPE"], ("CONTEXT_FUNDING_RATES", "CONTEXT_FUNDING_PARAMETER"))
        
        return msg
    
    def INSERT_CONTEXT(self, msg):
        pref.dMsg("/\\INSERT_CONTEXT/\\")
        pref.dMsg("INSERT_CONTEXT")
        self.replace(msg, ["CONTEXT", "CONTEXTLINK", "TYPE"], ("CONTEXT_FUNDING_RATES", "CONTEXT_FUNDING_PARAMETER"))
        self.replace(msg, ["+CONTEXT", "+CONTEXTLINK", "TYPE"], ("CONTEXT_FUNDING_RATES", "CONTEXT_FUNDING_PARAMETER"))

        return msg


        

class TaskHistoryFilter(FAMBA_mutator):
    """
    Filter to remove taskhistories from being sent over the bridge,
    There are no parameters that can block children of an object
    """
         
    def UPDATE_TASK(self, msg):
        # search for task, assume only one task can be sent by every message 
        task = find_mbf_object(msg, "TASK")
        # remove all task histories
        t2 = find_mbf_object(task, "TASKHISTORY")
        while t2:
            task.mbf_remove_object() 
            t2 = find_mbf_object(task, "TASKHISTORY")
        return msg


class DATAFix(FAMBA_mutator):

############# Generic functions ###########
    
    def fixText(self, msg, what, tmsg):
        if(tmsg!=None):
            pref.dMsg("TheTEXT-\n["+str(tmsg)+"]\n")
            
            self.replace(msg, what, tmsg)
            what[0] = "+" + what[0] # ["+...","...",...]
            self.replace(msg, what, tmsg) 
            what[0] = "!" +what[0][1:] # ["+...","...",...]
            self.replace(msg, what, tmsg)
        else:
            pref.dMsg(self.TaskFix()+" Nothing found")
            raise(self.TaskFix()+" Nothing found")

    def refBuildBySQL(self, msg, sql, chg):
        pref.dMsg("SQL query for fetching vals")  
        pref.dMsg(sql) 
        val = getSQLVal(sql)
        # patch null values sent through the AMB
        val = self.fixZero(val)
        data = self.getTextData(val)
        self.fixText(msg, chg, data)

            
    def fixZero(self, val):
        """
        Method to patch errors in the AMBA
        """
        if val == "" or val == None:
            return "N"
        else:
            return val    
    
class TextObjectFix(DATAFix): # used to be from FAMBA_mutatir
    """
    Add the text in the textobject to the textobject.
    """

    # is there a lookup table for this ?
    # if so replace this ..
    def remapType(self, item):
        elems = {"TEXT_OBJECT_AEL":"AEL Module",
                 "TEXT_OBJECT_SQL":"SQL Query",
                 
                 "TEXT_OBJECT_AGENT_PARAMETER" :"Agent Parameter" ,
                 "TEXT_OBJECT_AGENT_TRACE" : "Agent Trace"  ,
                 "TEXT_OBJECT_SHEET_AGENT" : "Agent sheet"  ,
                 "TEXT_OBJECT_SHEET_CALLPUT_OB" : "Call/put order book sheet" ,
                 "TEXT_OBJECT_SHEET_CALLPUT_O" :"Call/put quote sheet"  ,
                 "TEXT_OBJECT_CUSTOM_LAYOUT" : "Custom Layout"  ,
                 "TEXT_OBJECT_EXT_CONTEXT" :"Extension Context"  ,
                 "TEXT_OBJECT_EXT_MODULE" : "Extension Module" ,
                 "TEXT_OBJECT_FASQL_QUERY" : "FASQL Query" ,
                 "TEXT_OBJECT_NEXT" : "Next"  ,
                 "TEXT_OBJECT_NONE" : "None",
                 "TEXT_OBJECT_SHEET_TRADE_DEFINITION" : "OTC Deal Sheet"  ,
                 "TEXT_OBJECT_SHEET_ORDER_BOOK" : "Order book sheet",
                 "TEXT_OBJECT_SHEET_ORDER_MANAGER" : "Order manager sheet" ,
                 "TEXT_OBJECT_FILTER_OWN_ORDER" : "Own order filter"  ,
                 "TEXT_OBJECT_SHEET_PORTFOLIO": "Portfolio sheet"  ,
                 "TEXT_OBJECT_PREFERENCES" : "Preferences"  ,
                 "TEXT_OBJECT_SHEET_QUOTE" : "Quote sheet"  ,
                 "TEXT_OBJECT_RISK_MATRIX_PARAM" : "Risk Matrix Parameter"  ,
                 "TEXT_OBJECT_SQL_REPORT" : "SQL Report"  ,
                 "TEXT_OBJECT_STORED_GROUPER" : "Stored Grouper"  ,
                 "TEXT_OBJECT_TRADING_SHEET_TEMPLATE" : "Trade Sheet Templates"  ,
                 "TEXT_OBJECT_FILTER_TRADE" : "Trade filter"   ,
                 "TEXT_OBJECT_SHEET_TRADE" : "Trade sheet"  ,
                 "TEXT_OBJECT_SHEET_UTILITY_OB" : "Utility order book sheet" ,
                 "TEXT_OBJECT_WORKBOOK" : "Workbook" ,
                 "TEXT_OBJECT_WORKSPACE" : "Workspace" 

                 }
        return elems[item]
    
    def adjust(self, msg):
        """
        Adjust the msg to include the text data
        """
        
        Ltype = self.fetchVal(msg, ["TEXTOBJECT", "TYPE"])
        Ltype = self.fetchVal(msg, ["+TEXTOBJECT", "TYPE"], Ltype)
        Ltype = self.fetchVal(msg, ["!TEXTOBJECT", "TYPE"], Ltype)
        Lname = self.fetchVal(msg, ["TEXTOBJECT", "NAME"])
        Lname = self.fetchVal(msg, ["+TEXTOBJECT", "NAME"], Lname)
        Lname = self.fetchVal(msg, ["!TEXTOBJECT", "NAME"], Lname)

        Ltype = self.remapType(Ltype) # the names differ on the AMB and in the database
        pref.dMsg("Ltype = "+str(Ltype)+" Lname="+str(Lname))
        search = "name='%s' and type='%s'" % (Lname, Ltype)
        pref.dMsg("Search "+search)
        # this is broken for certain textObjects
        #o = ael.TextObject.read(search)
        
        # works for anything unlike read
        val = getSQLVal("select seqnbr from textObject"
                  +" where name = '"+Lname+"' " 
                  +"and type = '"+Ltype+"'")
        o = ael.TextObject[val]
        
        
        if(o!=None):
            pref.dMsg("TheTEXT-\n["+o.get_text()+"]\n")
            tmsg = o.get_text()
            tmsg = self.fixZero(tmsg)
            self.replace(msg, ["TEXTOBJECT", "DATA"], tmsg)
            self.replace(msg, ["!TEXTOBJECT", "DATA"], tmsg)
            self.replace(msg, ["+TEXTOBJECT", "DATA"], tmsg)
                
        else:
            pref.dMsg("TextObjectFix Nothing found")
            # ensure that a false value is not sent over the line
            # has to be tested..
            raise("TextObjectFix Nothing found")


        
        
    def UPDATE_TEXTOBJECT(self, msg):
        self.adjust(msg)
        return msg
    
    def INSERT_TEXTOBJECT(self, msg):
        self.adjust(msg)
        return msg


class TaskFix(DATAFix):
    '''
    Fix the task object, also designed as template for additional 
    textobject objects
    '''

    def name(self):
        return "TaskFix"

    def getTextData(self, entry):
        # the info is only available in ACM
        t2 = acm.FAelTask[entry]
        if t2 == None:
            raise("Failing lookup of Task!")
        return t2.ParametersText()

    def adjust(self, msg):
        '''
        retrieve the message information
        '''
        Lname = self.fetchVal(msg, ["TASK", "NAME"])
        Lname = self.fetchVal(msg, ["+TASK", "NAME"], Lname)
        Lname = self.fetchVal(msg, ["!TASK", "NAME"], Lname)
        sql = "select tasknbr from task where name = '"+str(Lname)+"'"
        self.refBuildBySQL(msg, sql, ["TASK", "PARAMETER"])

        
    def UPDATE_TASK(self, msg):       
        self.adjust(msg)
        return msg
    
    def INSERT_TASK(self, msg):   
        self.adjust(msg)
        return msg          


class TaskFixReceive(TaskFix):
        
    def __init__(self):
            pass
            self.tnumber = 0
    
    
    def addTask(self, seq, msg):
        self.tnumber += 1
        pref.dMsg("Adding addTask!!"+str(self.tnumber))
        #return
        obj = ael.TaskSchedule[seq]
    
        #
        #We will write and MBF here
        #
        
        # happens if someone updates a task
        # while tasks are transfered over the bridge
        #
        if obj != None:
            task = find_mbf_object(msg, "TASK")
            #task = msg.mbf_find_object("TASK")
            # assumes task exists
                        
            tasks = task.mbf_start_list("TASKSCHEDULE")
            
            enabled = "Yes"
            if not obj.enabled :
                enabled = "No"

            schedule = obj.schedule
            
            tasks.mbf_add_string("ENABLED", enabled)
            tasks.mbf_add_string("SCHEDULE", schedule)
            
            task.mbf_end_list()
        

    
    def adjust(self, msg):
        
        # remove the old taskschedules
        self.removeTaskSchedule(msg)        



        # fetch 4.0 task schedules and patch them into the message
        taskName = self.fetchVal(msg, ["*TASK", "NAME"])
        seqList = getSQLList("select seqnbr from Task t, TaskSchedule s where t.tasknbr = s.tasknbr and t.name = '%s'" % (taskName))
        
        # creating data from 4.0 system
        for i in seqList:
            self.addTask(int(i), msg)
            
        
    def removeTaskSchedule(self, msg):
        self.delete(msg, ["!TASK", "*TASKSCHEDULE"])
        
        
    def simpleForward(self, msg):
        # check if this is a legal table, i.e. the child is included in the processing
        return isBridgeMessage(msg, "TASKSCHEDULE")
        
        
    def UPDATE_TASK(self, msg):
        #if not self.simpleForward(msg):       
        #    self.adjust(msg)
        return msg
    
    def INSERT_TASK(self, msg):
        #if not self.simpleForward(msg):            
        #    self.removeTaskSchedule(msg)
        return msg
        
            
class YieldCurveFix(DATAFix):
            
    def name(self):
        return "YieldCurveFix"
    
    def getTextData(self, entry):
        t2 = acm.FYieldCurve[entry]
        if t2 == None:
            raise("Failing lookup of task")
        return t2.TextData()

    def adjust(self, msg):
        pref.dMsg("ADJUSTING BY YieldCurveFix")
        Lname = fetchPath(msg, ["*YIELDCURVE", "YIELD_CURVE_NAME"])
        pref.dMsg("CurveName is " + str(Lname))
        sql = "select seqnbr from yieldcurve where yield_curve_name = '"+str(Lname) \
            +"'"
            
        self.refBuildBySQL(msg, sql, ["YIELDCURVE", "DATA"])

    def INSERT_YIELDCURVE(self, msg):
        pref.dMsg("yieldcurve")
        self.adjust(msg)
        return msg
    
    def UPDATE_YIELDCURVE(self, msg):
        pref.dMsg("yieldcurve")
        self.adjust(msg)
        return msg


class PatchReceiveMessage(DATAFix):

    def edit(self, msg):
        pref.dMsg("editing message!")
        size = self.fetchVal(msg, ["*TEXTOBJECT", "SIZE"])
        data = self.fetchVal(msg, ["*TEXTOBJECT", "DATA"])

        
        pref.dMsg("PathReceiveMessage size = "+str(size)+" data = "+str(data))
        # replace if this is value that can crash the AMBA
        if size == "1" and (data == "" or data == None):
            self.fixText(msg, ["TEXTOBJECT", "DATA"], "N")
            pref.dMsg("Changing empty data object!")
        
        data = self.fetchVal(msg, ["*TEXTOBJECT", "DATA"])        
        pref.dMsg("Data was changed by patch to "+str(data))
        
        return msg

    def INSERT_TEXTOBJECT(self, msg):
        return self.edit(msg)
        
        
    def UPDATE_TEXTOBJECT(self, msg):
        return self.edit(msg)

class KillFilter(DATAFix):

    def __init__(self):
        global pref
        if(hasattr(pref, "killPaths")):
           self.vals = pref.killPaths()
        else:
           self.vals = []

    def mutate(self, msg):
        for i in self.vals:
            pref.dMsg("Processing "+str(i))
            if hasPath(msg, i[0]):
                pref.dMsg("Match will try to delete !!"+str(i))
                self.delete(msg, i[1])
                
        return msg
    

class PriceDefinition(DATAFix):
    """
    Empty the version field
    
    This has been incorrectly done correct version 
    should VERSION_ID inside the message
    
    It appears that PriceDefiniton does not use version
    """
  
    def changeVersion(self, msg):
        self.replace(msg, ["VERSION"], "")
        return msg
    
    def INSERT_PRICEDEFINITION(self, msg):
        return self.changeVersion(msg)
    
    def UPDATE_PRICEDEFINITION(self, msg):
        return self.changeVersion(msg)

class TradeFilterFix(DATAFix):
    """
    Fix the binary field,
    This object is intended to operate on the send part
    """
    def name(self):
        return "TradeFilterFix"
    
    def getTextData(self, entry):
        t2 = ael.TradeFilter[entry]
        if t2 == None:
            raise("Failing lookup of task")
        return t2.get_query()

    def adjust(self, msg):
        pref.dMsg("ADJUSTING BY TradeFilterFix")
        Lname = fetchPath(msg, ["*TRADEFILTER", "FLTID"])
        pref.dMsg("TradeFilter is " + str(Lname))
        sql = "select fltnbr from tradefilter where fltid = '"+Lname+"'"
            
        self.refBuildBySQL(msg, sql, ["TRADEFILTER", "QUERY"])

        
    
   

    def INSERT_TRADEFILTER(self, msg):
        self.adjust(msg)
        return msg
    
    def UPDATE_TRADEFILTER(self, msg):
        self.adjust(msg)
        return msg

class TradeFilterFixReceive(TradeFilterFix):


    def __init__(self):
        self.query = None

    def addTradeFilter(self, msg):
        '''
        Change insert to update and add a tradfilter
        '''
        self.replace(msg, ["TYPE"], "UPDATE_PRICEDEFINITION")
        
        Lname = fetchPath(msg, ["*TRADEFILTER", "FLTID"])
        # check that this realy is a new Filter
        if not ael.TradeFilter[Lname]:
                
                ftf = ael.TradeFilter.new()
                ftf.fltid = Lname
        
                self.setQuery(ftf, msg)
                ftf.commit()
                pref.dMsg("Created a new tradeFilter!!!")
        
        
        #
        #Get the message 
        #
    def setQuery(self, obj, msg):
        if self.query == None:
            self.query = fetchPath(msg, ["*TRADEFILTER", "QUERY"])                            
        pref.dMsg("Query is " + str(self.query))
        obj.set_query(eval(self.query))
        

    def adjust(self, msg):
        pref.dMsg("ADJUSTING receive by TradeFilterFixReceive ")
        # get the data
        key   = fetchPath(msg, ["*TRADEFILTER", "FLTID"])
        self.query = fetchPath(msg, ["*TRADEFILTER", "QUERY"]) 
        self.delete(msg, ["*TRADEFILTER", "QUERY"])
        pref.dMsg("FLTID is "+str(key))
        atf  = ael.TradeFilter[key]
        #pref.dMsg("ATF tradefilter "+str(atf.pp()))
        atfc = atf.clone()
        # is this ok ?
        # eval is potentially a problem ..
        self.setQuery(atfc, msg)
        atfc.commit()
        atfc.apply()
        
    def INSERT_TRADEFILTER(self, msg):
        self.addTradeFilter(msg)
        self.adjust(msg)
        return msg
        
    def UPDATE_TRADEFILTER(self, msg):
        self.adjust(msg)
        return msg




#=====================================================================
#
#These are path request lines that can fetch one values such as
#
# ["<objectnam>","<another node>",..,"<value>"]
#
#=====================================================================


#
#Differs from replace by the fact that only one value is retrieved
#
#
def fetchPathI(obj,search,prev=None,isfirst=True):
        """
        Search for a pattern of [object,object,...,fieldname] and return first 
        WARNING: Does not automatically handle show_change = 1
        """
        if(search == []):

            val = obj.mbf_get_value()
            return val
        else:
            isearch = list(search)
            item = isearch.pop(0)
            
            obj2 = None
            if(isfirst):
                obj2 = obj.mbf_find_object(item)
            else:
                obj2 = obj.mbf_find_object(item, "current")
                
            if(obj2 == None):
                return None# breaks out of recursion
            else:  
                val = fetchPathI(obj2, isearch, obj, True)            
                
                if val !=None:
                    return val
                else:
                    # search for additional objects of the similar types
                    obj.mbf_next_object() # go to next object
                    return fetchPathI(obj, search, prev, False)



def fetchSmartPathI(list):
        """
        iterator for the other stuff
        Creates a list of options to delete in the message
        """
        if list == []:
            return []
        
        head = list[0]
        tail = list[1:]
        ans = fetchSmartPathI(tail)
        
        if head[0] == "*":
            # expand
            headE = head[1:]
            a1 = [head]
            
            heads = [headE, "+"+headE, "!"+headE]
            
        else:
            # return single element
            heads = [head]
            
    
        # add the tails
        if ans == []:
            if(len(heads)>1):
                completes = [[x] for x in heads]
            else:
                completes = [heads] # list of lists
        else:
            #completes = [ [i for i in y] for x in heads for y in ans]
            completes = []
            for x in heads:
                for y in ans:
                    head = [x]
                    head.extend(y)
                    completes.append(head)
                    
        return completes

def fetchSmartPath(obj, search):
    """
    Internal for processing [+!]{0,1}<word> with one arg *<word>
    This will be done by text expansion, we can do it by other means if
    its not fast enough
    """
    group = fetchSmartPathI(search)
    for i in group:
        v = fetchPathI(obj, i)
        if v != None:
            return v

# uses above function to access data
def fetchPath(obj,search, oldVal=None):
        """
        Search for a value, and return oldVal if not found
        """
        aval =  fetchSmartPath(obj, search)
        res = oldVal
        if aval!=None:
            res = aval
        return res

def hasPath(obj, search):
    """
    Check if the path exists and the result is found in the object
    """
    if(type(search) == type([]) and len(search)!=0):
        list = search[:-1]
        item = search[-1:][0]
        res = fetchPath(obj, list)
        return item == res
    else:
        # dont blame me if you send in junk!!
        raise "Error hasPath got invalid search path "+str(search)
    

    
def update2insert_sender(ex):
    pref.dMsg("Using converstion of message")
    ex = (Update2Insert()).mutate(ex)
    ex = (Delete2Insert()).mutate(ex)
    return ex

def update2delete_sender(ex):
    """
    convert see example message
    """
    """
[MESSAGE]
  TYPE=DELETE_INSTRUMENT
  VERSION=1.0
  TIME=2008-02-07 07:47:37
  SOURCE=AMBA_oldBlank
  [-INSTRUMENT]
    INSID=ZZ
    INSTYPE=INS_STOCK
    CURR.INSID=EUR
    QUOTE_TYPE=QUOTE_PER_UNIT
    MTM_FROM_FEED=Yes
    SPOT_BANKING_DAYS_OFFSET=2
    PRODUCT_CHLNBR.ENTRY=Equity
    PRODUCT_CHLNBR.LIST=ValGroup
    ISSUER_PTYNBR.PTYID=AB Electrolux
    ISSUER_PTYNBR.PTYID2=0B11AH
    CONTR_SIZE=1
    PAY_OFFSET_METHOD=DATEPERIOD_BUSINESS_DAYS
    DIVIDEND_FACTOR=1
  [/-INSTRUMENT]
[/MESSAGE]
    """
    pref.dMsg("Using delete2insert filter")    
    ex = (Update2Delete()).mutate(ex)
    ex = (Insert2Delete()).mutate(ex)
    return ex


#=====================================================================
#
#AMB message repplicator and alternative validation code
#amb pretense methods
#
#=====================================================================

class ambPointer:
    def __init__(self, message):
        (n, m) = message
        self.message = m
        self.name    = n
        #the index
        self.ptr = 0
        
    def mbf_find_object(self,what,where="MBFE_BEGINNING"):
        what = what.upper()
        if where == "MBFE_BEGINNING":
            self.ptr = 0
        #search
        for i in range(self.ptr, len(self.message)):
            self.ptr = i
            (n, v) = self.message[i]
            if n == what:
                return ambPointer(self.message[i])
                
    def mbf_get_value(self):
        return self.message
        
        
    def mbf_is_list(self):
        return type([]) == self.message
        
    def mbf_get_name(self):
        return self.name

    def mbf_first_object(self):
        self.ptr = 1
        return ambPointer(self.message[0])

    def mbf_next_object(self):
        ptr = self.ptr
        self.ptr = self.ptr+1
        if len(self.message) > ptr:
                return ambPointer(self.message[ptr])
        else:
                return None

    def mbf_add_int(self, k, v):
        self.message.append((k, v))
        
    def mbf_add_double(self, k, v):
        self.message.append((k, v))
        
    def mbf_add_string(self, k, v):
        self.message.append((k, v))
        
    def mbf_start_list(self, k):
        """Start list, using the fact that changes to l will make changes to  t"""
        l = []
        t = (k, l)
        self.message.append(t)
        return ambPointer(t)

    def mbf_last_object(self):
        l = len(self.message)-1
        self.ptr = l
        return ambPointer(self.message[l])

    def mbf_remove_object(self):
        #removes the item that ptr points at
        del self.message[self.ptr]
        self.ptr = self.ptr-1
        if self.ptr < 0:
                self.ptr = 0
        return ambPointer(self.message[self.ptr])


 
 
    
"""
Simulates AMB messages useful in ceratin instances
where AMB messages cannot be used
    
#        obj = m.mbf_last_object()
#        while not obj.mbf_get_name() == "TYPE": 
#            obj = m.mbf_remove_object()
"""
class ambProxy(ambPointer):
        
    def getVal(self, ent, coln):
            a = getattr(ent, coln)
            if coln == "connected_trdnbr":
                #reference by trdnbr
                return [("CONNECTED_TRDNBR", str(a.trdnbr))]
            elif hasattr(a, "record_type"):
                unql = [N for (N, T, D) in getattr(ael, a.record_type).keys()
                    if T == 'unique' or (T =='optional unique' 
                                         and getattr(a, N)!=None and getattr(a, N)!="")
                        or N == "instype"]
                #unique is never a reference
                L = [(coln.upper()+"."+C.upper(), getattr(a, C))
                         for C in unql]
                XL = []
                for (k, v) in L:
                        if k == "INSADDR.INSTYPE" and v == "Curr":
                                XL.append((k, "INS_CURR"))
                        elif k == "INSADDR.INSTYPE" and v == "FxSwap":
                                XL.append((k, "INS_FX_SWAP"))
                        else:
                                XL.append((k, v))
                return XL
            else:
                return [(coln.upper(), str(a))]
        
    #pretend to be amb
    def __init__(self,ent,operation="UPDATE"):
        self.ent = ent
        self.name = "MESSAGE"
        message = []
        message.append(("TYPE", operation+"_"+ent.record_type.upper()))
        message.append(("VERSION", "1.0"))
        message.append(("TIME", "1900-01-01"))
        message.append(("SOURCE", "AMBA BRIDGE src"))
        entm = []
        # create trade
        for i in ent.columns():
            #entm.append((i.upper(),getattr(ent,i)))
            res = self.getVal(ent, i)
            if res:
                    entm.extend(res)
        message.append((ent.record_type.upper(), entm))
        self.message = message
        
        #replicate pointer
        self.npointer = ambPointer(("MESSAGE", self.message))
        
        
    def output(self):
        """Print data to output"""
        print self.xml(("MESSAGE", self.message))
        
    def xml(self,message,tab=0):
        (n, v) = message
        if type(v) == type([]):
            a = "\t"*tab+"<"+n+">\n"
            for i in v:
                a = a  + self.xml(i, tab+1)
            a = a  + "\t"*tab+"</"+n+">\n"
            return a
        else:
            return "\t"*tab+"<"+n+">"+str(v)+"<"+n+">\n"


    def pyStruct(self):
            # return the message
            return self.message


def exampleValidateFilter(message):
    """Example use to validate entites on a side of the AMBA"""
    #use something like this to validate messages
    ag = defaultReverseSendFilterAgents()
    return agentFilterLine(message, ag)



############ 
#lib files with class definitions
#from FAMBA_BridgeM import MirrorTranslation, MirrorTranslationSend
from FAMBA_BridgeM import fixLegnbr, fixYieldCurves, fixRemoveResets, addFieldObject, removeOldieLinks
import FAMBA_BridgeM


