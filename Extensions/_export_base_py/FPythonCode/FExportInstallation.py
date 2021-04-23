""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/export/./etc/FExportInstallation.py"
from __future__ import print_function
"""-------------------------------------------------------------------------------------------------------
MODULE
    FExportInstallation - 
    This module provides methods to perform basic checks that an export integration
    is correctly set up 

    (c) Copyright 2014 SunGard FRONT ARENA. All rights reserved.

-------------------------------------------------------------------------------------------------------"""
import acm

import FExportUtils
import FTransactionHistoryReader

# Required additional info specifications
ADDITIONAL_INFO_SPECS = (
        ('FTP Hostname', 'Contact', 'String'),
        ('FTP Port', 'Contact', 'Integer'),
        ('FTP Username', 'Contact', 'String'),
        ('FTP Password', 'Contact', 'String'),
        ('FTP Path', 'Contact', 'String'),
    )

def CreateAdditionalInfos(additionalInfoSpecs=ADDITIONAL_INFO_SPECS):
     # Create required additional infos
    for spec in additionalInfoSpecs:
        ai = FExportUtils.FileTransferAddInfoSpecCreator(spec)
        ai.Create()

def CheckTradeStatus():
    # Trade status 'FO Amend' must exist to monitor corrected trades
    customTradeStatus = 'FO Amend'
    try:
        if not acm.FEnumeration['enum(TradeStatus)'].Enumeration(customTradeStatus):
            raise RuntimeError('No enum!')
    except Exception as e:
        assert(False),  "Trade status '%s' does not exist: %s" % (customTradeStatus, e)

def CheckExportStateChart(exportStateChartName):
    # Create the export state chart, if required
    FExportUtils.CreateStandardExportStateChart(exportStateChartName)
    assert(acm.FStateChart[exportStateChartName]), \
        "State chart (%s) for export does not exist" % exportStateChartName
      
def CheckTransactionHistory(integrationId):
    # Check transaction history and subscription functionality is available.
    # This is not strictly required, so only log a warning on failure.
    try:
        subscriber = FTransactionHistoryReader.FTransactionHistorySubscriber(integrationId)
        subscription = subscriber.TransHistSubscription()
        if not subscription:
            print("WARNING: Subscription to transaction history does not exist")
    except Exception as e:
        print("WARNING: Failed to get transaction history subscription:", str(e))
        
def CheckTradeACMQuery(tradeACMQueryPrefix):
    # ACM queries should be setup to select trades to be exported
    queries = FExportUtils.TradeFilterQueriesForIntegration(tradeACMQueryPrefix) 
    assert(len(queries) > 0), \
        "No ACM queries have been defined for '%s', selecting exportable trades." % tradeACMQueryPrefix

def CheckTradingSheetTemplate(tradingSheetName):
    # Check if a trading sheet template has been created
    tradingSheet = acm.FTradingSheetTemplate[tradingSheetName]
    assert(tradingSheet), "Trading sheet template '%s' does not exist" % tradingSheetName

def CheckTradingSheetTemplatePerQuery(tradeACMQueryPrefix):
    # Each query must have a corresponding trading sheet template
    queries = FExportUtils.TradeFilterQueriesForIntegration(tradeACMQueryPrefix)
    for query in queries:
        tradingSheetName = acm.FTradingSheetTemplate[query.Name()]
        assert(tradingSheetName), "Couldn't find sheet template name for ACM query '%s'" % query.Name()
        tradingSheet = acm.FTradingSheetTemplate[tradingSheetName.Name()]
        assert(tradingSheet), "Trading sheet template '%s' (for ACM query '%s') does not exist" \
            % (tradingSheet, query.Name())
    
    # There should be at least one contact defining the FTP details for export file transfer
def CheckContactSetup(ftpContactName, createAdditionalInfos, additionalInfoSpecs=ADDITIONAL_INFO_SPECS):
    #pylint: disable-msg=W0612,
    contacts = acm.FContact.Select('fullname=' + ftpContactName)
    if not contacts:
        print('WARNING: No contacts named "%s" could be found.' % ftpContactName)
    
    # Check the contact additional info specification setup
    if createAdditionalInfos:
        CreateAdditionalInfos()
    has_additional_info_setup = True
    data_type_enums = acm.FEnumeration['enum(B92StandardType)']
    for ai_name, ai_object, ai_data_type in additionalInfoSpecs:
        spec = acm.FAdditionalInfoSpec[ai_name]
        if not spec:
            print('WARNING: Additional info specification %s (%s) was not found.' % (ai_name, ai_data_type))
            has_additional_info_setup = False
        elif spec.RecType() not in ('Contact', 'Party'):
            print('WARNING: Additional info specification', ai_name, 'is not defined for Contact or Party.')
            has_additional_info_setup = False
        elif spec.DataTypeType() != data_type_enums.Enumeration(ai_data_type):
            print('WARNING: Additional info specification %s has unexpected data type (%s, expected %s)' % \
                (ai_name, data_type_enums.Enumerator(spec.DataTypeType()), ai_data_type))
            has_additional_info_setup = False

    # Check that the contacts have the minimum required FTP information, provided that we have the
    # correct additional info setup as previously checked:
    if has_additional_info_setup:
        for contact in contacts:
            ai = contact.AdditionalInfo()
            try:
                if not ai.FTP_Hostname():
                    print('WARNING: No FTP hostname has been defined for contact %s on party %s.' % \
                        (contact.Fullname(), contact.Party().Name()))
                if not ai.FTP_Port():
                    print('WARNING: No FTP port has been defined for contact %s on party %s.' % \
                        (contact.Fullname(), contact.Party().Name()))
            except Exception:
                print('WARNING: Failed to check FTP details for contact %s on party %s.' % \
                        (contact.Fullname(), contact.Party().Name()))



