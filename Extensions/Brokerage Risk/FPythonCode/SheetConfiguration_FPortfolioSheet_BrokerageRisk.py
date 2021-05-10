""" Compiled: 2020-09-18 10:38:55 """

#__src_file__ = "extensions/BrokerageRisk/etc/SheetConfiguration_FPortfolioSheet_BrokerageRisk.py"
"""--------------------------------------------------------------------------
MODULE
    Brokerage Risk

    (c) Copyright 2016 SunGard Front Arena AB. All rights reserved.

DESCRIPTION

-----------------------------------------------------------------------------"""

import acm

def ael_custom_dialog_show(shell, params):
    return acm.FDictionary()

def ael_custom_dialog_main( parameters, dictExtra ):
    eii = dictExtra['customData']
    extensionObject = eii.ExtensionObject()
    cna = eii.MenuExtension().GetString('ColumnNames', None)
    extensionObject.ColumnSetupExtensionAttribute( cna )
    extensionObject.Grouper( acm.Risk.GetGrouperFromName('Category') )
    return extensionObject


