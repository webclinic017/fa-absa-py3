""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCACreateRight - Module used to create a Stock Right to be used by
    Corporate Actions New Issue, Buyback and Stock Dividend.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    A Macro variables window is displayed for the user to fill in relevant
    values. After pressing OK a new Right Instrument in the form of an Option
    is saved to the database.
----------------------------------------------------------------------------"""

import ael, time
from FCAGeneral import user, stock, save_deriv, right_list

Voluntary = 1
ca_user, ca_trader, ca_acquirer = user()

"""----------------------------------------------------------------------------
Main
----------------------------------------------------------------------------"""

stocks = stock()
rights = right_list()
if Voluntary != 1:
    typelist = ['Buyback', 'New Issue', 'Stock Dividend']
if Voluntary == 1:
    typelist = ['Call', 'Put']
    
ael_variables = [('ins', 'Stock', 'string', stocks, ''),
                ('name', 'Stock Right name', 'string', rights, ''),
        ('strike', 'Stock Right Strike Price', 'string', [], '0'),
        ('xd', "Stock Right Expiry Date", 'string', [],
                 str(ael.date_today())),
        ('startday', 'Trading start day', 'string', [], 
         str(ael.date_today())),
        ### Either old & new or cs:
        #('old', 'per Old Stock', 'string', [], ''),
        #('new', 'Number of New Stock', 'string', [], ''),
        ('cs', 'Contract Size', 'string', [], '1'),
        ('catype', 'Call or Put', 'string', typelist, 'Call'),
        ('sedol', 'External_ID (optional)', 'string', [], '', 0, 0)]

def ael_main(dict):
    ins = ael.Instrument[dict.get('ins')]
    name = dict.get('name')
    if ael.Instrument[name]:
        i = ael.Instrument[name]
    strike = dict.get('strike')
    xd = ael.date(dict.get('xd'))
    startday = ael.date(dict.get('startday'))
    #old = float(dict.get('old'))
    #new = float(dict.get('new'))
    #cs = (new/old)
    cs = float(dict.get('cs'))
    if Voluntary != 1:
        if dict.get('catype') == 'Buyback': catype = 0
        if dict.get('catype') == 'New Issue': catype = 1
        if dict.get('catype') == 'Stock Dividend': catype = 1
    if Voluntary == 1:
        if dict.get('catype') == 'Call': catype = 1
        if dict.get('catype') == 'Put': catype = 0


    sedol= dict.get('sedol')

    if not ael.Instrument[name]:
        print '\nCreated new Stock Right instrument.'
        r = save_deriv(1, ins, name, strike, xd, cs, catype, None, 'Option', startday, sedol)
    elif ael.Instrument[name]:
        print '\nInstrument has been updated.'
        r = save_deriv(1, ins, name, strike, xd, cs, catype, i, 'Option', startday, sedol)








