""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/RandomMarkitFileCreation.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    RandomMarkitFileCreation - Function generates random Markit Rate data for all instruments which are underlying to Master Security Loan.

    (c) Copyright 2018 FIS FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""

import acm
import random
import csv
from FParameterSettings import ParameterSettingsCreator

def check_parameter(param):
    import acm
    aliases_types = [alias.Name() for alias in acm.FInstrAliasType.Select('')]
    addinfos_types = [addinfo.Name() for addinfo in acm.FAdditionalInfoSpec.Select("recType='Instrument'")]
    if param in aliases_types:
        return 'Alias'
    elif param in addinfos_types:
        return 'AdditionalInfo'
    elif isAttribute(acm.FInstrument, param):
        return 'Attribute'
    else:
        return None

    
def isAttribute(acmObj, attributes):
    if ":" not in attributes:#not alias and not addinfo
        attr = attributes.split(".", 1)
        if len(attr) == 2:
            try:
                return isAttribute(acmObj.GetMethod(attr[0], 0).ValueDomain(), attr[1])
            except Exception as e:
                return False
        else:
            return acmObj.GetMethod(attr[0], 0) is not None

def CreateRandomMarkitFile():

    parameter = ParameterSettingsCreator.FromRootParameter('MarkitSettings')
    isin = parameter.Isin()
    cusip = parameter.Cusip()
    sedol = parameter.Sedol()
    
    isinType = check_parameter(isin)
    cusipType = check_parameter(cusip)
    sedolType = check_parameter(sedol)
    
    sloans = acm.FSecurityLoan.Select("productTypeChlItem=Master Security Loan")
    len = sloans.Size()

    list = ('DXL Identifier', 'ISIN', 'SEDOL', 'CUSIP', 'Quick', 'Stock Description', 'Market Area', 'Record Type'\
    , 'Div Req', 'Lendable Value', 'Lendable Quantity', 'Balance Value vs Cash', 'Balance Value vs NonCash',\
    'Total Balance Value', 'Total Balance Quantity', 'Utilisation', 'SL Return to Lendable',\
    'Total Return to Lendable', 'SL Tenure', 'SL Fee High', 'SL Fee Low', 'VWAF 1 Day', 'VWAF 3 Day'\
    , 'VWAF 7 Day', 'VWAF All', 'VWAF 30 Day', 'Active Lendable Value', 'Active Lendable Quantity',\
    'Active Available Value', 'Active Available Quantity', 'Active Utilisation',\
    'Active Utilisation by Quantity', 'Balance Value 1 Day', 'Balance Value 3 Day', 'Balance Value 7 Day',\
    'Balance Value 30 Day', 'Number of Transactions 1 Day', 'Number of Transactions 3 Day',\
    'Number of Transactions 7 Day', 'Number of Transactions 30 Day', 'Number of Transactions',\
    'Tradable Fee', 'Tradable Rebate', 'Tradable Duration', 'All In Level')
    dict = {}
    for key in list:
        dict[key] = acm.FArray()
    for sl in sloans:
        dict['DXL Identifier'].Add(6)
        
        #isin definition
        if isinType == 'Alias':
            isn = sl.Underlying().Alias(isin)
        elif isinType == 'AdditionalInfo':
            isn = sl.Underlying().add_info(isin) 
        elif isinType == 'Attribute':
            isn = getattr(sl.Underlying(), isin)()         
        else:
            isn = ''
        if isn != None:
            dict['ISIN'].Add(isn)
        else:
            dict['ISIN'].Add('')            
        
        #sedol definition
        if sedolType == 'Alias':
            sdl = sl.Underlying().Alias(sedol)
        elif sedolType == 'AdditionalInfo':
            sdl = sl.Underlying().add_info(sedol) 
        elif sedolType == 'Attribute':
            sdl = getattr(sl.Underlying(), sedol)()         
        else:
            sdl =''         
        
        if sdl != None:
            dict['SEDOL'].Add(sdl)
        else:
            dict['SEDOL'].Add('')
            
        #cusip definition
        if cusipType == 'Alias':
            csp = sl.Underlying().Alias(cusip)
        elif cusipType == 'AdditionalInfo':
            csp = sl.Underlying().add_info(cusip)
        elif cusipType == 'Attribute':
            csp = getattr(sl.Underlying(), cusip)()           
        else:
            csp = ''
        if csp !=None:
            dict['CUSIP'].Add(csp)
        else:
            dict['CUSIP'].Add('')
            
        dict['Quick'].Add('')
        dict['Stock Description'].Add(sl.Underlying().Name())
        dict['Market Area'].Add('(others)')
        dict['Record Type'].Add(1)
        dict['Div Req'].Add('')
        dict['Lendable Value'].Add(round(max(random.gauss(60, 500), 0), 4))
        dict['Lendable Quantity'].Add(round(max(random.gauss(5550000, 100000), 0), 0))
        dict['Balance Value vs Cash'].Add(round(max(random.gauss(1.7, 45), 0), 4))
        dict['Balance Value vs NonCash'].Add(round(max(random.gauss(3, 55), 0), 4))
        dict['Total Balance Value'].Add(round(max(random.gauss(6, 100), 0), 4))
        dict['Total Balance Quantity'].Add(round(max(random.gauss(600000, 1000000), 0), 0))
        dict['Utilisation'].Add(round(max(random.gauss(10, 3), 0), 4))
        dict['SL Return to Lendable'].Add(round(max(random.gauss(45, 240), -4), 4))
        dict['Total Return to Lendable'].Add(round(max(random.gauss(70, 250), -30), 4))
        dict['SL Tenure'].Add(round(max(random.gauss(105, 120), 0), 0))
        dict['SL Fee High'].Add(round(max(random.gauss(380, 500), 0), 0))
        dict['SL Fee Low'].Add(round(max(random.gauss(150, 275), -210), 0))
        vwaf1d = round(max(random.gauss(150, 165), -33), 3)
        dict['VWAF 1 Day'].Add(vwaf1d)
        dict['VWAF 3 Day'].Add(round(vwaf1d + random.gauss(5, 1), 3))
        dict['VWAF 7 Day'].Add(round(vwaf1d + random.gauss(7, 1), 3))
        dict['VWAF All'].Add(round(vwaf1d + random.gauss(9, 1), 3))
        dict['VWAF 30 Day'].Add(round(vwaf1d + random.gauss(11, 1), 3))
        dict['Active Lendable Value'].Add(round(max(random.gauss(60, 600), 0), 4))
        dict['Active Lendable Quantity'].Add(round(max(random.gauss(4000000, 100000000), 0), 4))
        dict['Active Available Value'].Add(round(max(random.gauss(50, 900), 0), 0))
        dict['Active Available Quantity'].Add(round(max(random.gauss(3000000, 10000000), -10), 0))
        dict['Active Utilisation'].Add(round(max(random.gauss(25, 5), 0), 2))
        dict['Active Utilisation by Quantity'].Add(round(max(random.gauss(25, 5), 0), 2))
        dict['Balance Value 1 Day'].Add(round(max(random.gauss(0.005, 1.5), 0), 4))
        dict['Balance Value 3 Day'].Add(round(max(random.gauss(0.4, 10), 0), 4))
        dict['Balance Value 7 Day'].Add(round(max(random.gauss(0.7, 20), 0), 4))
        dict['Balance Value 30 Day'].Add(round(max(random.gauss(2.5, 50), 0), 4))
        nt1d = round(max(random.gauss(2, 1.5), 1), 0)
        dict['Number of Transactions 1 Day'].Add(nt1d)
        dict['Number of Transactions 3 Day'].Add(round(nt1d+random.gauss(4, 1), 0))
        dict['Number of Transactions 7 Day'].Add(round(nt1d+random.gauss(6, 1), 0))
        dict['Number of Transactions 30 Day'].Add(round(nt1d+random.gauss(8, 1), 0))
        dict['Number of Transactions'].Add(round(nt1d+random.gauss(12, 1), 0))
        dict['Tradable Fee'].Add(round(max(random.gauss(280, 400), 0), 3))
        dict['Tradable Rebate'].Add(round(max(random.gauss(-185, 800), -20000), 3))
        dict['Tradable Duration'].Add(round(max(random.gauss(45, 100), -20000), 3))
        r = round(max(random.gauss(90, 100), 0), 0)
        if r ==0:
            dict['All In Level'].Add('')
        else:
            dict['All In Level'].Add(r)
    return sloans, list, dict