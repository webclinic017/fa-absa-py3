""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/archive_trades/FCashAggregation.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FCashAggregation - Perform aggregation of cash values

DESCRIPTION

NOTE

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import acm

import FBDPGui
import importlib
importlib.reload(FBDPGui)

ScriptName = "FCashAggregation"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters',
        'FCashAggregation')

ttDeaggregate = "Open up the positions after the aggregation date."
ttDate = ('Specify the aggregation horizon date. Aggregation will be done up '
        'until and not including this date. If the date is today, '
        'aggregation will be done for all historical days.')
ttPreserveYTDPnL  = ('Preserve YTD PnL.  This will result in additional payment records.')
ttFilter = 'Specify the tradefilters that you want to process.'
ttGrouper = ('Specify a grouper template. If no grouper is selected, a '
        'default grouping of per portfolio will be used.')
ttCPInstrument = 'Instrument used for cash posting trades.'
ttPortfolio = ('Select positions using Portfolios.')
ttGrouper = ('Specify a grouper template. This will be used to calculate cash values.')
ttGrouperPositions = ('Specify a grouper template. This will be used to validate zero positions.')

def archiveDearchive_cb(index, fieldValues):
    return fieldValues

agg_days = [acm.Time.DateToday(),
            'Today',
            'First of Month',
            'First of Quarter',
            'First of Year']

cashAggregationGroupingAttributes = [
    'Trade.Instrument',
    'Trade.Acquirer',
    'Trade.Counterparty',
    'Trade.Market',
    'Trade.Trader',
    'Trade.Broker',
    'Trade.Currency',
    'Trade.OptKey1',
    'Trade.OptKey2',
    'Trade.OptKey3',
    'Trade.OptKey4'
    
]
groupingCriteriaGroupers = dict([(acm.FAttributeGrouper(caga).StringKey(), caga) for caga in cashAggregationGroupingAttributes])

allPaymentTypes = acm.GetDomain('enum(PaymentType)').Enumerators()

class FCashAggregationPositionVariables(FBDPGui.FxPositionVariablesBase):

    def __init__(self, *ael_variables):

        onlyOne = ('Only one of these alternatives - Stored Folders, Trade '
                'Filters or Portfolios - should be used.')
        ttStoredFolder = ('Select positions using Stored Folders. '
                '{0}'.format(onlyOne))
        ttTradeFilter = ('Select positions using Trade Filters. '
                '{0}'.format(onlyOne))
        ttPortfolio = ('Select positions using Portfolios. '
                '{0}'.format(onlyOne))
        ttGrouper = ('Specify trade grouping attributes. If no attributes are selected, '
                'the default behaviour is to group by portfolio.')
        ttConsolidateCash = ('If NOT selected, one cash posting trade per instrument position will be created.')
        ttPaymentTypes = ('Preserve payments matching the the selected payment types')              
        
        self.createVariable(
                # [VariableName,
                #       DisplayName,
                #       Type, CandidateValues, Default,
                #       Mandatory, Multiple, Description, InputHook, Enabled]
                ['TradeQuery',
                        'Stored Folder_Positions',
                        'FStoredASQLQuery', None, FBDPGui.insertStoredFolder(),
                        0, 1, ttStoredFolder, self.object_cb])
        self.createVariable(
                ['TradeFilter',
                        'Trade Filter_Positions',
                        'FTradeSelection', None, None,
                        0, 1, ttTradeFilter, self.object_cb])
        self.createVariable(
                ['TradingPortfolios',
                        'Portfolio_Positions',
                        'FPhysicalPortfolio', None, None,
                        0, 1, ttPortfolio, self.object_cb])
        self.createVariable(
                ['PortfolioGrouperAttributes',
                        'Portfolio Grouper_Positions',
                        'string', groupingCriteriaGroupers.keys(), None,
                        0, 1, ttGrouper, self.grouper_cb])
        self.createVariable(
                ['ConsolidateCash',
                        'Consolidate Cash Postings_Positions',
                        'int', [0, 1], 1, 0, 0, ttConsolidateCash, None])
        self.createVariable(
                ['PreservePaymentTypes',
                        'Preserve payments_Positions',
                        'string', allPaymentTypes, None, 
                        0, 1, ttPaymentTypes, None])
        FBDPGui.FxPositionVariablesBase.__init__(self, *ael_variables)


ael_variables = FCashAggregationPositionVariables(#FxAggregationVariables
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['deaggregate',
                'Deaggregate',
                'int', [0, 1], 0,
                0, 0, ttDeaggregate, archiveDearchive_cb],
        ['date',
                'Aggregation Date',
                'string', agg_days, 'Today',
                1, 0, ttDate],)


def ael_main(dictionary):
    #Import Front modules
    import FBDPString
    importlib.reload(FBDPString)
    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FCashAggregationPerform
    importlib.reload(FCashAggregationPerform)
    import FBDPCurrentContext

    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    dictionary['PortfolioGrouperNativeAttributes'] = [groupingCriteriaGroupers[pg_attr] for pg_attr in dictionary['PortfolioGrouperAttributes']]

    FBDPCommon.execute_script(FCashAggregationPerform.perform,
                              dictionary)

