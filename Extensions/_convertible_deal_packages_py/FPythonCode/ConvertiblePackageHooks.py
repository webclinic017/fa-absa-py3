""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/ConvertibleDealPackages/etc/ConvertiblePackageHooks.py"
"""-------------------------------------------------------------------------------------------------------
MODULE
    ConvertiblePackageHooks

    (c) Copyright 2016 SunGard FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""


def CustomDefaultInstrumentProperties(instrument, dealPackageType):
    return


def CustomDefaultTradeProperties(trade, dealPackageType):
    return


def PortfolioChanged(convertiblePackage):
#    if convertiblePackage.portfolio:
#        if convertiblePackage.portfolio == 'Portfolio 1':
#            convertiblePackage.b2bPrf = 'B2B Portfolio'
#            convertiblePackage.b2bAcq = 'B2B Acquirer'
    return

def SuggestName(dealPackage):
#    dealPackage.Name = 'NewName' #If the deal package name is set, it must be unique
#    return 'NewInsPkgName' #This is the name of the instrument package. Unique identifier will be added automatically
    return
     
def TradeForPayments(dealPackage):
    #if dealPackage.DefinitionName() == "CBOption":
    #    return dealPackage.TradeAt('ascot')
    return