""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/MarkitSecuritiesFinance/etc/FMarkitSecuritiesFinanceInstall.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FMarkitSecuritiesFinanceInstall - Installation script for Makit data Upload

    (c) Copyright 2012 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

    This module install Party, Choice List and Instrument alias type for Markit data upload.
    


-------------------------------------------------------------------------------------------------------"""

import acm


def create_alias_type():
    alias = acm.FInstrAliasType['CUSIP']
    if not alias:
        alias = acm.FInstrAliasType()
        alias.Name('CUSIP')
        alias.Commit()
    alias = acm.FInstrAliasType['SEDOL']
    if not alias:
        alias = acm.FInstrAliasType()
        alias.Name('SEDOL')
        alias.Commit()
    
def create_choice_list(list_name):
    ChoiceList = acm.FChoiceList[list_name]
    ChoiceList = acm.FChoiceList.Select('name='+list_name)
    if not ChoiceList:
        ChoiceList = acm.FChoiceList()
        ChoiceList.List(acm.FChoiceList["Product Type"])
        ChoiceList.Name(list_name)
        ChoiceList.Commit()
        return 1
    return 0

def SourceCreator(names=['Markit']):
    acm.BeginTransaction()
    try:
        for name in names:
            if not acm.FMarketPlace[name]:
                p = acm.FMarketPlace()
                p.Name(name)
                p.Commit()
        acm.CommitTransaction()
    except Exception:
        acm.AbortTransaction()
        print('Error inserting market places {}:{}'.format(names, traceback.format_exc()))



def Install(eii):
    SourceCreator()
    create_choice_list('Master Security Loan')
    create_alias_type()
    print('Sucesfully installed Markit data')