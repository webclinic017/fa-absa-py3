""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCAMisc - Module including all misc functions common to Corporate Actions.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    This module stores functions common to several Corporate Actions.
----------------------------------------------------------------------------"""
import ael
try:
    import string
except ImportError:
    print('Failed to import the module string.')

def string_parse(s, tokens):
    """Find numbers in the CorpAction description field."""
    if tokens == None:
        tokens = ['Seqno.', '+', '-', 'DTC1:']
    exist = 0
    for token in tokens:
        try:
            exist = s.find(token) ### Find if s contains any tokens.
        except AttributeError:
            exist = string.find(s, token) # Old Python Version.
        if exist >= 0: ### Token exists.
            break
    if (exist == -1):
        return 'None'
    t = string.split(s, token)
    temp_str = t[len(t)-1]
    t2 = string.split(temp_str, ' ')
    if len(t2) > 1:
        temp_str = t2[0]
    if token == 'Seqno.': return temp_str
    elif token == 'NameChange:': return t[len(t)-1]
    elif token == ',': return string.replace(s, token, ' ')
    else: return token + temp_str

def scr_upd(scrupd):
    """Find which Corporate Actions have / have not been performed."""
    l = []
    for i in ael.CorpAction:
        if (i.ca_ins_status == scrupd or i.ca_trade_status == scrupd):
            s = 'Seqno.' + str(i.seqnbr) + ' ' + str(str(i.text) + ' ' +
                str(i.ca_type) + ' on ' + str(i.insaddr.insid) + '; ' +
                str(i.instype) + '; ' + 'ExDate: ' + str(i.ex_date))
            s_new = string_parse(s, ',')
            if s_new == 'None':
                l.append(s)
            else:
                l.append(s_new)
    return l

def asql_scr_upd(i, scrupd, *rest):
    """Find which Corporate Actions have / have not been performed."""
    if (i.ca_ins_status == scrupd or i.ca_trade_status == scrupd):
        s = 'Seqno.' + str(i.seqnbr) + ' ' + str(str(i.text) + ' ' +
            str(i.ca_type) + ' on ' + str(i.insaddr.insid) + '; ' +
            str(i.instype) + '; ' + 'ExDate: ' + str(i.ex_date))
        return s

def stock():
    """Create list with all stocks from the Instrument table."""
    stock = ael.Instrument.select('instype = "Stock"')
    i = []
    for s in stock:
        i.append(s.insid)
    return i
    
def right_list():
    """Create list with possible stock right names."""
    l = ['Option', 'Stock'] 
    d = []
    for type in l:
        t = ael.Instrument.select('instype = "%s"' % type)
        for i in t:
            d.append(i.insid)
    return d

def instr():
    """Create list of instruments."""
    ins = ael.Instrument
    instr = []
    for i in ins:
        instr.append(i.insid)
    return instr

def pf():
    """Create list of portfolios."""
    port = ael.Portfolio
    pf = []
    for p in port:
        pf.append(p.prfid)
    return pf

def script_update(seqnbr):
    corpact = ael.CorpAction[seqnbr]
    clone   = corpact.clone()
    if corpact.ca_ins_status == 'Script Update Done':
        clone.ca_ins_status = 'Script Update'
    if corpact.ca_trade_status == 'Script Update Done':
        clone.ca_trade_status = 'Script Update'
    clone.commit()

def renameOldInstrument(i, rb, exDate, commit = 1, debug = 1):
    oldInstrument = i.clone()
    for (nameType, size) in (('extern_id1', 29), ('insid', 39), 
                             ('extern_id2', 29), ('isin',  20)):
        s = 'oldInstrument.' + nameType
        if eval(s):
            if len(str(eval(s))) < size:
                exec s + ' = (' + s + '+ "_ca' + str(exDate) + '")[:size]'
            else:
                if nameType == 'insid':
                    exec s + ' = (' + s + '+ "_")[1:]'
                else:
                    exec s + ' = ""'
    alias_list = []
    for a in oldInstrument.aliases():
        alias_list.append(a)
    for a in alias_list:
        new_alias = a
        new_alias.delete()
    if debug:
        print('Old Instrumnent will be renamed to:')
        print(oldInstrument.insid)
    if commit:
        rb.add('Update', i, ['insid', 'extern_id1', 'extern_id2', 'isin'])
        oldInstrument.commit()
    return rb





