""" Trade_Allocation:1.2.5 """

'''---------------------------------------------------------------------------------
 MODULE
     FTradeAllocation - Selects the portfolio that the trade shall be allocated to.
     
     (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.
 
 DESCRIPTION
     The Trade_Allocation function allows the user to define the section criteria for
     different portfolios in the ADS. The selection criteria is defined in the
     Assignment info field in the Portfolio definition. You can also in
     TradeAllocationRule define general allocation rules valid for several portfolios
     in the system. All fields support regular expressions.
     
     The acquirer party id will be set to the owner of the portfolio if the owner
     is of type 'Intern Dept', else the acquirer party id will be set to 'Default Dept'

     The following keys are used for defining trade allocation in the
     Portfolio Definition:

     -s : Sequence Number, to set the portfolios in a specific order. (Default -s0) 
     -c : Clearing Member (Default -c.*)
     -t : Trader (Default -t.*)
     -a : Account (Default -a.*)
     -b : Base ID (Default -b.*)
     -f : Free Text (Default -f.*)
     -m : Market Account (Default -m.*)
     -p : Market Party Id (Default -p.*)
     -r : Reference (Default -r.*)
     -i : Instrument Type (Default -i.*)
     -u : Underlying Instr Type (Default -u.*)
     -x : Extra Tag defined by the user. Can be any field in the
          Instrument Table (Default -x.*)
          Set the variable extra_tag below to the field of your choise.

     General rules are defined as follows:
     =====================================

     In the list general_alloc_table in module TradeAllocationGeneralRule
     you define your general rules.

     ************************|Assignment Info  |Match Record    |Match String   *****                
     general_alloc_table = [['-aP.*-bA.*',      'assinf',       "'F'+a+b"       ],
                             ['-f.*',           'prfid',        "f+'BAS'"       ]]

     The Assignment Info column defines what keys that are included in the portfolio
     allocation. Defined in the same way as the Assignment Info Field in each
     Portfolio. The Match Record column defines the Portfolio record to match
     against. The Match String defines how the Matching string shall be built up.
     No spaces allowed in the "Match String"
     
     The regular expression '.*' means "Any value". I.e the selection of the
     portfolio will only be based on message keys that you have included in your
     selection. Keys that you have left out will not be in your selection.

     DEFAULT_POOL needs no allocation Information. DEFAULT_POOL will be set if no
     other portfolio is found.

     
     Input parameters:
     
     m              The message broker message received.
     
 NOTE
     1. The first portfolio that fulfills the selection criteria in the list is
        selected.
     2. The selection is CASE SENSITIVE. Both the Keys and the Values must be spelled
         in the correct way.
     3. The object_tuplets also listed in the remove_key tuplet will be removed from
         the message sent to the AMBA.
     4. The assignment information supports regular expressions.
     5. Sequence number (-s) does not support regular expressions.
     
 DATA-PREP
     The assignment information shall be added to the Assigning Info in the portfolio
     definition. One parameter can be a sequence number defining in what order the
     portfolios shall be matched to the trade. The keys used for defining assignment
     info are -s -c -t -a -b -f -m -p -r -i -u -x and they are described above.
    
 REFERENCES
     Regular expressions in python:

     http://www.python.org/doc/current/lib/module-re.html
 
 ENDDESCRIPTION
---------------------------------------------------------------------------------'''
import ael
import string
import re
import TradeAllocationRule
import sys

#*************************************************************************************
object_tuplet = ('COMPANYID', 'TRADER_USRNBR.USERID', 'ACCOUNT', 'BASEID', 'FREE',\
                 'MARKETACCOUNT', 'MARKET_PTYNBR.PTYID', 'REFERENCE', 'INSADDR')
remove_key =    ('COMPANYID', 'ACCOUNT', 'BASEID', 'FREE', 'MARKETACCOUNT', 'REFERENCE')

try:
    overwrite = TradeAllocationRule.overwrite
except:
    overwrite = 0
    ael.log('WARNING: overwrite flag in TradeAllocationRule not defined')

try:
    extra_tag = TradeAllocationRule.extra_tag
except:
    extra_tag = None
    ael.log('WARNING: extra_tag (-x) in TradeAllocationRule not defined')

general_alloc_table = TradeAllocationRule.general_alloc_table

key_list = {'c':0,'t':1,'a':2,'b':3,'f':4,'m':5,'p':6,'r':7,'i':8,'u':9,'x':10}

default_portfolio = 'DEFAULT_POOL'

verbose = 1

trade_instrument = None

ob_dict = {}                #{name:insaddr...}
pf_dict = {}                #{PRFID:[Assinfo]...}  
pf_alloc_table = []         #[['-c','-t','-a','-b','-f'...,'PF_NAME',GAC_ROW],[...]]
pf_alloc_table_general = [] #[['-c','-t','-a','-b','-f'...,'PF_NAME',GAC_ROW],[...]]
c_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
t_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
a_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
b_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
f_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
m_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
p_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
r_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
i_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
u_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}
x_dict = {}             #{Message_value:[dict_length,{pf_alloc_table_index:None}]...}

c_sort = []     # Dict keys sorted in descending order
t_sort = []     # Dict keys sorted in descending order
a_sort = []     # Dict keys sorted in descending order
b_sort = []     # Dict keys sorted in descending order
f_sort = []     # Dict keys sorted in descending order
m_sort = []     # Dict keys sorted in descending order
p_sort = []     # Dict keys sorted in descending order
r_sort = []     # Dict keys sorted in descending order
i_sort = []     # Dict keys sorted in descending order
u_sort = []     # Dict keys sorted in descending order
x_sort = []     # Dict keys sorted in descending order

number_of_rows = 0
number_of_col = len(key_list.keys())


'''----------------------------------------------------------------------------------
 FUNCTION
     portfolio_subscription - Re-creates the allocation table (pf_alloc_table)
                               if necessary
     
 DESCRIPTION
     This function re-creates the allocation table (pf_alloc_table) if the
     assignment information is changed, or if a new portfolio is created of deleted.
     The function sets the global variable "number_of_rows" to 0 (zero) which will
     make the allocation table to be recreated when the next INSERT_TRADE message 
     is received.
     
 ARGUMENTS
     pf_table       ael_table   The portfolio table.
     pf             ael_entity  The "changed" portfolio.
     arg            any         None
     event          string      insert, update or delete
      
 RETURNS   
     None
         
----------------------------------------------------------------------------------'''
def portfolio_subscription(pf_table, pf, arg, event):
    global number_of_rows
    global pf_dict
    valid_ass_string = 0

    if sys.version[0] == '1':
        ai = string.split(pf.assinf, '-')
    else:
        ai = pf.assinf.split('-')
    for s in ai[1:]:
        if s[0] in key_list.keys():
            valid_ass_string = 1
    if event == 'delete' and pf.prfid in pf_dict.keys():
        # if the deleted portfolio is in our allocation table, recreate pf_alloc_table
        number_of_rows = 0      
    elif valid_ass_string:
        # if the assignment information or portfolio name has been changed,
        # recreate the pf_alloc_table
        number_of_rows = 0

'''----------------------------------------------------------------------------------
 FUNCTION
     rule_subscription - Re-creates the allocation table (pf_alloc_table)
                         if necessary
     
 DESCRIPTION
     This function re-creates the allocation table (pf_alloc_table) if the
     TradeAllocationRule file is updated.
     The function sets the global variable "number_of_rows" to 0 (zero) which will
     make the allocation table to be recreated when the next INSERT_TRADE message 
     is received.
     
 ARGUMENTS
     to_table       ael_table   The portfolio table.
     to             ael_entity  TradeAllocationRule module
     arg            any         None
     event          string      insert, update or delete
      
 RETURNS   
     None
         
----------------------------------------------------------------------------------'''
def rule_subscription(to_table, to, arg, event):
    global number_of_rows
    
    if to.name == 'TradeAllocationRule':
        number_of_rows = 0            
        
        return None

'''----------------------------------------------------------------------------------
 FUNCTION
     strip_spaces - Returns a string without spaces included, if not within quotation
     marks
     
 DESCRIPTION
     Removes unnecessary space characters.
     
 ARGUMENTS     
     strip_str      string      Sting to be stripped.
     
 RETURNS
     tmp_str        string      The stripped string.
          
----------------------------------------------------------------------------------'''
def strip_spaces(strip_str):
    wait_for_quote = 0
    tmp_str = ''
    for i in range(len(strip_str)):
        if strip_str[i] in ['"', "'"]:
            wait_for_quote = not wait_for_quote
        if wait_for_quote or strip_str[i] <> ' ':
            tmp_str = tmp_str + strip_str[i]
    return tmp_str
    
'''----------------------------------------------------------------------------------
 FUNCTION
     strip_quotes - Removes the quotes (single or double) from the beginning and
                    end of a string.
     
 DESCRIPTION
     Removes all quotation characters.
     
 ARGUMENTS     
     strip_str      string      Sting to be stripped.
     
 RETURNS
     tmp_str        string      The stripped string.
          
----------------------------------------------------------------------------------'''
def strip_quotes(strip_str):
    tmp_str = ''
    for i in range(len(strip_str)):
        if not strip_str[i] in ['"', "'"]:
            tmp_str = tmp_str + strip_str[i]
    return tmp_str

'''----------------------------------------------------------------------------------
 FUNCTION
     get_ob - returns a dictionary with all ob_names as keys and insaddr as values.
     
 DESCRIPTION
     Used to look up the instrument when allocating trades based on instrument
     type or underlying instrument type.
     
 ARGUMENTS     
     None
     
 RETURNS
     ob_dict        dict      A dictionary with all orderbook names as keys.
          
----------------------------------------------------------------------------------'''
def get_ob():
    global ob_dict
    
    obs = ael.OrderBook.select()
    for o in obs:
        if o.name != '':
            ob_dict[o.name] = o.oid
    return ob_dict

'''----------------------------------------------------------------------------------
 FUNCTION
     get_ass_list - Returns a list of allocation information for a specific portfolio
                    or for a row in the general 
     
 DESCRIPTION
     Returns a list of allocation information for a specific portfolio or for a row
     in the general allocation table. The list contains what ever keys that has been
     definied. If no keys are found the function returns None.
     
 ARGUMENTS     
     ass_info       String      The Assignment Info string.
     
 RETURNS
     ass_list    List   List containing the allocation rules.
          
----------------------------------------------------------------------------------'''
def get_ass_list(ai):
    ass_info_ok = None
    ass_list = ['0', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*']
    ass_info = []
    strip = 0
                
    if sys.version[0] == '1':
        tmp = string.split(ai, '-')
    else:
        tmp = ai.split('-')
    if tmp[0] != '': return None
    for i in range(1, len(tmp)):
        if tmp[i][0] in key_list.keys():
            strip = strip + 1

    if strip: ai = strip_spaces(ai) # If it is an allocation rule strip it.

    wait_for_quote = None
    get_key = None
    tmp_str = ''
    
    for i in range(len(ai)):
        if not wait_for_quote and ai[i] == '-':
            if tmp_str <> '': ass_info.append(tmp_str)
            tmp_str = ''
            get_key = 1
        elif get_key and ai[i] in key_list.keys():
            tmp_str = ai[i]
            get_key = 0
        elif ai[i] in ['"', "'"]:
            wait_for_quote = not wait_for_quote
        else:
            tmp_str = tmp_str + ai[i]
    if tmp_str: ass_info.append(tmp_str)
    
    for i in range(0, len(ass_info)):
        ass_info[i] = strip_quotes(ass_info[i])
        tag = ass_info[i][0]
        if tag in key_list.keys():
            ass_info_ok = 1
            ass_list[key_list[tag]+1] = ass_info[i][1:]
        elif ass_info[i][0] in ['s']:
            ass_info_ok = 1
            if sys.version[0] == '1':
                ass_list[0] = string.strip(ass_info[i][1:])
            else:
                ass_list[0] = ass_info[i][1:].strip()
    if ass_info_ok:
        return ass_list
    else:
        return None
'''----------------------------------------------------------------------------------
 FUNCTION
     create_alloc_table - Returns an allocation table based on assign_info
     information in the portfolios.
     
 DESCRIPTION
     This function scans all the portfolios in the ADS and generates an allocation
     table based on the information in the assign_info record of the portfolio table.
     
 ARGUMENTS     
     none
     
 RETURNS
     pf_alloc_table    List     List of lists containing the allocation rules.
          
----------------------------------------------------------------------------------'''
def create_alloc_table():
    global pf_dict
    global general_alloc_table
    pat = []
    ass_info = []
    r_len = number_of_col + 3
    
# Add Portfolio Assignment Info
    
    for pf in ael.Portfolio:
        
        ai = pf.assinf
        ass_list = get_ass_list(ai)
        if ass_list and pf.prfid <> default_portfolio and pf.compound == 0:
        # Only physical portfolios.
            ass_list.append(pf.prfid)
            ass_list.append(None)       # Index column for General Alloc Table
            if sys.version[0] == '1':
                pat.append([string.atoi(ass_list[0]), ass_list[1:r_len]])
            else:
                pat.append([int(ass_list[0]), ass_list[1:r_len]])
            pf_dict[pf.prfid] = ai

    # Add General Assignment Info
    for row in range(len(general_alloc_table)):
        if len(general_alloc_table[row]) != 3:
            ael.log("ERROR, rule %i in TradeAllocationRule does not contain three elements: %s" % \
                   (row + 1, general_alloc_table[row]))
        general_alloc_table[row][2] = strip_spaces(general_alloc_table[row][2])
        
        ai = general_alloc_table[row][0]
        ass_list = get_ass_list(ai)
        if ass_list:
            tmp_str = strip_quotes(general_alloc_table[row][2])
            if ael.Portfolio[tmp_str]:
                ass_list.append(tmp_str)
            else:
                ass_list.append('')
            ass_list.append(row)            
            if sys.version[0] == '1':
                pat.append([string.atoi(ass_list[0]), ass_list[1:r_len]])
            else:
                pat.append([int(ass_list[0]), ass_list[1:r_len]])

    pat.sort()
    for i in range(len(pat)):
        pat[i] = pat[i][1]
    pat.append(['.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', '.*', default_portfolio, None])
    return pat

'''----------------------------------------------------------------------------------
 FUNCTION
     get_alloc_list - Returns a list of all valid keys that the message fulfills.
     
 DESCRIPTION
     Generates an allocation list that fulfills the message received. E.g. If we
     get Base Id = ALV in the message, and we have the following keys in the
     b_dict: 'ALV', 'A.*' and '.*'. then we build a list defining all the portfolios
     that fulfills the selection criteria. I.e all portfolios with assigning info
     set to -bALV, -bA.* or -b left out.
     
 ARGUMENTS     
     tmp_dict       dictionary      g_dict, c_dict ....
     s          string          String received from message.
     index      
     
 RETURNS
     alloc_list   list  [Number of index,index_dictionary,message string, table col]
        
----------------------------------------------------------------------------------'''

def get_alloc_dict(tmp_dict, index):
    
    if tmp_dict.has_key('.*'):
        for k1 in tmp_dict.keys():
            tmp_dict[k1][1].update(tmp_dict['.*'][1])
            tmp_dict[k1][0] = len(tmp_dict[k1][1].keys())
    return tmp_dict

'''----------------------------------------------------------------------------------
 FUNCTION
     build_dict - Returns a dictionary with the values in each column in the
                   pf_alloc_table as keys.
     
 DESCRIPTION
     Builds a dictionary {Message_value:[dict_length,{pf_alloc_table_index:None}]...}
     for each column in the pf_alloc_table
     
 ARGUMENTS     
     pat        list            pf_alloc_table
     col       int              index of the column in pat to generate dict from.
     
 RETURNS
     tmp_dict    Dictionary          Allocation Dictionaries.
          
----------------------------------------------------------------------------------'''
def build_dict(pat, col, s_list):
    star_list = []
    tmp_dict = {}
    
    for i in range(number_of_rows):
        mval = pat[i][col]
        l = []
        if tmp_dict.has_key(mval):
            tmp_dict[mval][0] = tmp_dict[mval][0]+1
            tmp_dict[mval][1].update({i:None})
        else:
            try:
                pattern = re.compile(mval)
            except:
                continue
            d ={}
            l.append(1)
            d[i] = None
            l.append(d)
            l.append(pattern)
            tmp_dict[mval]= l
    
    tmp_dict = get_alloc_dict(tmp_dict, col)
    for (k, v) in tmp_dict.items():
        s_list.append([min(v[1].keys()), k])
    s_list.sort()
    for i in range(len(s_list)):
        s_list[i] = s_list[i][1]

    return tmp_dict, s_list        

'''----------------------------------------------------------------------------------
 FUNCTION
     create_alloc_dict - Creates the global dictionaries needed to enhance pf search.
     
 DESCRIPTION
     Builds all dictionaries for each column in the pf_alloc_table
     {Message_value:[dict_length,{pf_alloc_table_index:None}]...}
     
 ARGUMENTS
     
     pat        list            pf_alloc_table
      
 RETURNS
   
     None
          
----------------------------------------------------------------------------------'''
def create_alloc_dict(pat):
    global c_dict
    global t_dict    
    global a_dict
    global b_dict
    global f_dict
    global m_dict
    global p_dict
    global r_dict
    global i_dict
    global u_dict
    global x_dict
    
    global c_sort
    global t_sort
    global a_sort
    global b_sort
    global f_sort
    global m_sort
    global p_sort
    global r_sort
    global i_sort
    global u_sort
    global x_sort

    c_dict, c_sort = build_dict(pat, 0, c_sort)
    t_dict, t_sort = build_dict(pat, 1, t_sort)
    a_dict, a_sort = build_dict(pat, 2, a_sort)
    b_dict, b_sort = build_dict(pat, 3, b_sort)
    f_dict, f_sort = build_dict(pat, 4, f_sort)
    m_dict, m_sort = build_dict(pat, 5, m_sort)
    p_dict, p_sort = build_dict(pat, 6, p_sort)
    r_dict, r_sort = build_dict(pat, 7, r_sort)
    i_dict, i_sort = build_dict(pat, 8, i_sort)
    u_dict, u_sort = build_dict(pat, 9, u_sort)
    x_dict, x_sort = build_dict(pat, 10, x_sort)
   
    
    
'''----------------------------------------------------------------------------------
 FUNCTION
     check_message_type - Returns the name of the message type
     
 DESCRIPTION
     This function reads the received messages and extracts the message type and
     returns the value of the TYPE object in the message
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
      
 RETURNS
     message type  String  The message type name.
         
----------------------------------------------------------------------------------'''
def check_message_type(m):
    type = m.mbf_find_object('TYPE', 'MBFE_BEGINNING')
    return type.mbf_get_value()


'''----------------------------------------------------------------------------------
 FUNCTION
     get_instype - Gets the instrument type from the alias table
     
 DESCRIPTION
     Extracts the instrument address from the alias type and alias name in the
     trade message. If the OrderBooks are not found, we fetch the OrderBooks once more.
     This will happen if new instruments are inserted into the ADS without the
     AMBA being restarted.
     
 ARGUMENTS     
     ael_string  string  The INSADDR tag value in the trade message.
      
 RETURNS
     instrument type  String  The instrument type.
         
----------------------------------------------------------------------------------'''
def get_instrument_from_order_book_string(ael_string, do_log = 1):
    global ob_dict
    global trade_instrument
    
    if sys.version[0] == '1':
        if string.find(ael_string, 'ael.OrderBook.read') <= -1:
            return None
    else:
        if ael_string.find('ael.OrderBook.read') <= -1:
            return None

    if sys.version[0] == '1':
        s = string.split(ael_string, "'")
    else:
        s = ael_string.split("'")

    if ob_dict.has_key(s[1]):
        a = ael.OrderBook[ob_dict[s[1]]]
        if a:
            trade_instrument = a.insaddr
    else:
        # If the OrderBook was not found fetch the orderbooks again and try once
        # more. This may be caused by a new instrument upload.
        ob_dict = get_ob()
        try:
            a = ael.OrderBook[ob_dict[s[1]]]
            if a:
                trade_instrument = a.insaddr
        except:
            if do_log: ael.log('ERROR: OrderBook %s not found' % (s[1]))
            return None
        
    return trade_instrument

def get_instype(ael_string, und_ins_type, do_log = 1):
    ins = get_instrument_from_order_book_string(ael_string, do_log)
    if not ins:
        return 'None'
    if not und_ins_type:
        return ins.instype
    elif ins.und_insaddr:
        return ins.und_insaddr.instype
    else:
        return 'None'
        

'''----------------------------------------------------------------------------------
 FUNCTION
     find_allocation_objects - Extracts the information in the trade used for trade
                                allocation.
     
 DESCRIPTION
     This function extracts the objects listed in the global tuplet object_tuplet
     listed above. When the object value has been extracted the object in the message
     is deleted. The function then returns a list with all object values.
     
 ARGUMENTS     
     m  MBFE-object  The message object received.
     
 RETURNS
     alloc      list        List containing all object values, or None.
         
----------------------------------------------------------------------------------'''
def find_allocation_objects(m):
    global trade_instrument
    ins_addresses = ['INSADDR.INSID',     'INSADDR.ISIN',\
                     'INSADDR.EXTERN_ID1', 'INSADDR.EXTERN_ID2']
    obj_value_list = []
    tag_missing = None
    t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    for i in range(len(object_tuplet)):
        obj = object_tuplet[i]
        o = t.mbf_find_object(obj, 'MBFE_BEGINNING')
        if o == None :
            if obj == 'INSADDR':
            # If INSADDR was not found, check if any other INSADDR reference exists.
                insaddr_found = None
                for i in ins_addresses:
                    o = t.mbf_find_object(i, 'MBFE_BEGINNING')
                    if o:
                        insaddr_found = 1
                        if sys.version[0] == '1':
                            addr = string.split(i, '.')[1]+'='+o.mbf_get_value()
                        else:
                            addr = i.split('.')[1]+'='+o.mbf_get_value()
                        ins = ael.Instrument.read(addr)
                        trade_instrument = ins
                        if ins:
                            obj_value_list.append(ins.instype)
                            if ins.und_insaddr:
                                obj_value_list.append(ins.und_insaddr.instype)
                            else:
                                obj_value_list.append('None')
                            if extra_tag:
                                try:
                                    obj_value_list.append(str(eval('ins.'+extra_tag)))
                                except:
                                    ael.log('ERROR: extra_tag value "%s" in \
TradeAllocationRule does not exist in Instrument Table.' % (extra_tag))
                                    obj_value_list.append('None')
                            else:
                                obj_value_list.append('None')
                        else:
                            obj_value_list.append('None')
                        break
                if not insaddr_found: tag_missing = obj
            else:
                tag_missing = obj
            continue
        if obj == 'INSADDR':
            # instype
            if sys.version[0] == '1':
                obj_value_list.append(get_instype(string.strip(o.mbf_get_value()), 0, 0)) 
            else:
                obj_value_list.append(get_instype(o.mbf_get_value().strip(), 0, 0)) 

            # underlying instype
            if sys.version[0] == '1':
                obj_value_list.append(get_instype(string.strip(o.mbf_get_value()), 1, 0)) 
            else:
                obj_value_list.append(get_instype(o.mbf_get_value().strip(), 1, 0)) 

            if trade_instrument == None:
                try:
                    trade_instrument = ael.Instrument[int(o.mbf_get_value())]
                except:
                   ael.log("ERROR: Instrument not found INSADDR=%s" % (o.mbf_get_value()))
            # extra_tag
            if trade_instrument and extra_tag:
                try:
                    etv = eval('trade_instrument.'+extra_tag)
                    obj_value_list.append(str(eval('trade_instrument.'+extra_tag)))
                except:
                     ael.log('ERROR: extra_tag value "%s" in \
TradeAllocationRule does not exist in Instrument Table.' % (extra_tag))
                     obj_value_list.append('None')
            else:
                obj_value_list.append('None')
    
        else:
            if sys.version[0] == '1':
                obj_value_list.append(string.strip(o.mbf_get_value()))
            else:
                obj_value_list.append(o.mbf_get_value().strip())
        if obj in remove_key:
            t.mbf_remove_object()
    if not overwrite:
        n = t.mbf_find_object('PRFNBR.PRFID', 'MBFE_BEGINNING')
        a = t.mbf_find_object('PRFNBR.ASSINF', 'MBFE_BEGINNING')
        if n or a: return None
    if tag_missing :
        ael.log('The following tag is missing in the trade message: %s' % (tag_missing))
        return None
    else : return obj_value_list


'''----------------------------------------------------------------------------------
 FUNCTION
     get_alloc_list - Returns a list of all valid keys that the message fulfills.
     
 DESCRIPTION
     Generates an allocation list that fulfills the message received. E.g. If we
     get Base Id = ALV in the message, and we have the following keys in the
     b_dict: 'ALV', 'A.*' and '.*'. then we build a list defining all the portfolios
     that fulfills the selection criteria. I.e all portfolios with assigning info
     set to -bALV, -bA.* or -b left out.
     
 ARGUMENTS     
     tmp_dict       dictionary      g_dict, c_dict ....
     s          string          String received from message.
     index      
     
 RETURNS
     alloc_list   list  [Number of index,index_dictionary,message string, table col]
         
----------------------------------------------------------------------------------'''

def get_alloc_list(tmp_dict, s, index, s_list):
    d_temp = {}
    largest = 0
    key = None
    a_list = []
    if tmp_dict.has_key(s):
        return (tmp_dict[s][0], tmp_dict[s][1], s, index)

    # if key doesn't exist check for matches amongst the other keys.
    for k in s_list:
        if tmp_dict[k][2].search(s):
            if a_list == []:
                a_list = [tmp_dict[k][0], tmp_dict[k][1].copy(), s, index]
            else:
                for i in tmp_dict[k][1].keys():
                    if not a_list[1].has_key(i):
                        a_list[1][i] = None
                        a_list[0] = a_list[0] + 1
    return a_list


'''----------------------------------------------------------------------------------
 FUNCTION
     get_pf - Returns the name of the porfolio selected.
     
 DESCRIPTION
     This function extracts the name of the portfolio that the trade shall be
     allocated to. The selection is based on column dictionaries. The first row in 
     pf_alloc_table that matches the selection criteria defines the portfolio that
     shall be used for the trade allocation. The function always returns a valid
     portfolio. 
     
 ARGUMENTS     
     t  list    List with values used for allocation of the trades      
     
 RETURNS
     portfolio_name     string  The name of the portfolio used for allocation
         
----------------------------------------------------------------------------------'''
def get_pf(t):
    alloc_list = []
    k_list = []
    list_length = 0

    if len(c_dict.keys()) > 1: alloc_list.append(get_alloc_list(c_dict, t[0], 0, c_sort))
    if len(t_dict.keys()) > 1: alloc_list.append(get_alloc_list(t_dict, t[1], 1, t_sort))
    if len(a_dict.keys()) > 1: alloc_list.append(get_alloc_list(a_dict, t[2], 2, a_sort))
    if len(b_dict.keys()) > 1: alloc_list.append(get_alloc_list(b_dict, t[3], 3, b_sort))
    if len(f_dict.keys()) > 1: alloc_list.append(get_alloc_list(f_dict, t[4], 4, f_sort))
    if len(m_dict.keys()) > 1: alloc_list.append(get_alloc_list(m_dict, t[5], 5, m_sort))
    if len(p_dict.keys()) > 1: alloc_list.append(get_alloc_list(p_dict, t[6], 6, p_sort))
    if len(r_dict.keys()) > 1: alloc_list.append(get_alloc_list(r_dict, t[7], 7, r_sort))
    if len(i_dict.keys()) > 1: alloc_list.append(get_alloc_list(i_dict, t[8], 8, i_sort))
    if len(u_dict.keys()) > 1: alloc_list.append(get_alloc_list(u_dict, t[9], 9, u_sort))
    if len(x_dict.keys()) > 1: alloc_list.append(get_alloc_list(x_dict, t[10], 10, x_sort))
    
    # if no Assignment Info other than .* is defined
    if alloc_list == []:alloc_list.append(get_alloc_list(c_dict, t[0], 0, c_sort))
    alloc_list.sort()
    list_length = len(alloc_list)
    k_list = alloc_list[0][1].keys()
    k_list.sort()
    for k in k_list:
        match = 1
        ass_string = ''
        for i in range(1, list_length):
            if alloc_list[i][1].has_key(k):match = match + 1
            else: break
        if match == list_length:
            if pf_alloc_table[k][number_of_col] != '': # Portfolio name exists !!!
                return pf_alloc_table[k][number_of_col]
            else:
                row = pf_alloc_table[k][number_of_col+1]
                if sys.version[0] == '1':
                    s=string.split(general_alloc_table[row][2], '+')
                else:
                    s=general_alloc_table[row][2].split('+')
                for i in range(len(s)):
                    if s[i][0] == '"':
                        if sys.version[0] == '1':
                            ass_string = ass_string + string.strip\
                                     (string.split(s[i], '"')[1])
                        else:
                            ass_string = ass_string + s[i].split('"')[1].strip()
                    elif s[i][0] == "'":
                        if sys.version[0] == '1':
                            ass_string = ass_string + string.strip\
                                     (string.split(s[i], "'")[1])
                        else:
                            ass_string = ass_string + s[i].split("'")[1].strip()                                  
                    elif s[i][0] in key_list.keys():                        
                        if sys.version[0] == '1':
                            tmp_string = string.strip(t[key_list[s[i][0]]])
                        else:
                            tmp_string = t[key_list[s[i][0]]].strip()
                        if len(s[i]) > 1:
                            try:
                               ass_string = ass_string + eval("tmp_string"+s[i][1:]) 
                            except:
                                continue
                        else:
                            ass_string = ass_string + tmp_string
                rec = general_alloc_table[row][1]
                try:
                    pf = ael.Portfolio.read(rec+'="'+ass_string+'"')
                except:
                    pf = None
                if pf <> None and pf.compound == 0:
                    return pf.prfid
                else:
                    if verbose: 
                    	ael.log("Portfolio does not exist: %s"%(rec+"="+ass_string))
                    continue
    return default_portfolio

'''----------------------------------------------------------------------------------
 FUNCTION
     set_tag - Sets the tag to the string (s) in the message.
     
 DESCRIPTION
     This function sets the portfolio name (prfid) in the message. If the tag exists
     and the over_write flag is set, it will be updated with the string value in "s".
     If the tag exists but the over_write flag is NOT set, the tag will not be updated
     if it is a valid portfolio, if the portfolio does not exist in the ADS, the tag
     value will be set to DEFAULT_POOL.
     If the tag does not exist in the message it will be inserted last in the /TRADE
     section of the message.
     
 ARGUMENTS     
     m      MBFE-object         The message object received.
     s      string              Name to be set for the tag.
     tag    string              The message tag to be set.
     
 RETURNS
     m          MBFE-object  The message object received.
         
----------------------------------------------------------------------------------'''
def set_tag(m, s, tag, over_write):
    t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
    m_tag = t.mbf_find_object(tag, 'MBFE_BEGINNING')
    if m_tag:
        if over_write:
            t.mbf_replace_string(tag, s)
        else:
            m_prf = m_tag.mbf_get_value()
            if not ael.Portfolio[m_prf]:
                ael.log("Portfolio in trade message does not exist: %s" % (m_prf))
                t.mbf_replace_string(tag, default_portfolio)

    else: # Does not exist.
        t.mbf_last_object()
        t.mbf_add_string(tag, s)
    return m


#*************************************************************************************
#                                   Main
#*************************************************************************************

p = ael.Portfolio
p.subscribe(portfolio_subscription)
t = ael.TextObject
t.subscribe(rule_subscription)


def trade_allocation(m):
    global pf_alloc_table
    global number_of_rows
    
    if number_of_rows == 0:
        pf_alloc_table = create_alloc_table()
        number_of_rows = len(pf_alloc_table)
        create_alloc_dict(pf_alloc_table)
#       for i in range(number_of_rows):
#           print pf_alloc_table[i]
        if len(i_dict.keys()) > 1 or len(u_dict.keys()) > 1:
            ob_dict = get_ob()
        
    if check_message_type(m) in ('INSERT_TRADE',\
                                'ASSIGNMENT_TRADE',\
                                'EXERCISE_TRADE'):
        alloc = find_allocation_objects(m)
        if alloc:
            pf_name = get_pf(alloc)
            set_tag(m, pf_name, 'PRFNBR.PRFID', 1)
        else:
            t = m.mbf_find_object('TRADE', 'MBFE_BEGINNING')
            n = t.mbf_find_object('PRFNBR.PRFID', 'MBFE_BEGINNING')
            a = t.mbf_find_object('PRFNBR.ASSINF', 'MBFE_BEGINNING')
            if n:
                n_val = n.mbf_get_value()
                prf = ael.Portfolio[n_val]
            if a and (not prf):
                a_val = a.mbf_get_value()
                obj = ael.Portfolio.read('assinf='+a_val)
                if obj:
                    pf_name = obj.prfid
                    set_tag(m, pf_name, 'PRFNBR.PRFID', 1)
                    return m
                else:
                    ael.log('Portfolio with ASSINF=%s does not exist' % a_val)
            set_tag(m, default_portfolio, 'PRFNBR.PRFID', 0)
        return m
    return m
