"""----------------------------------------------------------------------------------------------------
DESCRIPTION
    This module contains code to validate if NCD trade rate is in line with Absa JIBAR contributions

-------------------------------------------------------------------------------------------------------
HISTORY
=======================================================================================================
Date            JIRA no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-11-01      FAFO-44         Amit Kardile          Lucille Joseph          Initial Implementation
2019-11-11      FAFO-44         Amit Kardile          Lucille Joseph          Additional requirements
2020-04-07      FAFO-87         Amit Kardile          Lucille Joseph          Date range change
2021-04-08      FAFO-207        Amit Kardile          Lucille Joseph          Date range change and buyback check enablement
-------------------------------------------------------------------------------------------------------
"""

import acm

def popup(shell, message):
    return acm.UX.Dialogs().MessageBoxInformation(shell, message)
    

def get_jibar_index(ncd_instrument, trade):
    tenor_range_dict = {(27, 33):'NCD/JIBAR/CONTRIBUTION/1M', (58, 64):'NCD/JIBAR/CONTRIBUTION/2M',
                        (88, 94):'NCD/JIBAR/CONTRIBUTION/3M', (117, 123):'NCD/JIBAR/CONTRIBUTION/4M',
                        (148, 154):'NCD/JIBAR/CONTRIBUTION/5M', (179, 185):'NCD/JIBAR/CONTRIBUTION/6M',
                        (211, 221):'NCD/JIBAR/CONTRIBUTION/7M', (239, 249):'NCD/JIBAR/CONTRIBUTION/8M',
                        (270, 276):'NCD/JIBAR/CONTRIBUTION/9M', (298, 312):'NCD/JIBAR/CONTRIBUTION/10M',
                        (328, 342):'NCD/JIBAR/CONTRIBUTION/11M', (361, 367):'NCD/JIBAR/CONTRIBUTION/12M',
                        (540, 554):'NCD/JIBAR/CONTRIBUTION/18M', (723, 737):'NCD/JIBAR/CONTRIBUTION/24M',
                        (1089, 1103):'NCD/JIBAR/CONTRIBUTION/36M', (1453, 1467):'NCD/JIBAR/CONTRIBUTION/48M',
                        (1819, 1833):'NCD/JIBAR/CONTRIBUTION/60M'
                        }

    days = acm.Time.DateDifference(ncd_instrument.EndDate(), trade.ValueDay())
    for tenor_range in tenor_range_dict.keys():
        if days >= tenor_range[0] and days <= tenor_range[1]:
            jibar_index = tenor_range_dict[tenor_range]
            return jibar_index


def should_trade_be_blocked(jibar_index):
    return jibar_index in ['NCD/JIBAR/CONTRIBUTION/1M', 'NCD/JIBAR/CONTRIBUTION/3M', 'NCD/JIBAR/CONTRIBUTION/6M',
                            'NCD/JIBAR/CONTRIBUTION/9M', 'NCD/JIBAR/CONTRIBUTION/12M'
                            ]


def rate_validation_failed(shell, jibar_index, ncd_trade_rate, rate, direction):
    epsilon = 0.00000001
    if str(rate) == 'nan':
        message = '%s %s rate contribution not added. Please add it and retry.' %(jibar_index.Name(), direction)
        popup(shell, message)
        return True
    elif abs(ncd_trade_rate - rate) > epsilon:
        message = 'Trade price %f is not equal to Absa JIBAR contribution %s %s rate %f.'\
                    %(ncd_trade_rate, jibar_index.Name(), direction, rate)
        popup(shell, message)
        if should_trade_be_blocked(jibar_index.Name()):
            return True
    else:
        return False


def ncd_jibar_contribution_check_failed(shell, obj):
    if obj.IsKindOf('FTrade') and obj.Instrument().InsType() == 'CD' and obj.AdditionalInfo().Instype() == 'NCD'\
        and obj.Instrument().AdditionalInfo().Demat_Instrument() and obj.Status() == 'FO Confirmed'\
        and obj.Instrument().Issuer().Name() == 'ABSA BANK LTD':
        trade = obj
        ncd_instrument = trade.Instrument()
        jibar_index = get_jibar_index(ncd_instrument, trade)
        if not jibar_index:
            return False
        jibar_index = acm.FRateIndex[jibar_index]
        standard_calculation = jibar_index.Calculation()
        cs = acm.Calculations().CreateStandardCalculationsSpaceCollection("Standard")
        bid_rate = standard_calculation.BidPrice(cs).Number()
        ask_rate = standard_calculation.AskPrice(cs).Number()
        ncd_trade_rate = trade.Price()
        
        if trade.Direction() == 'Buy' and rate_validation_failed(shell, jibar_index, ncd_trade_rate, bid_rate, 'Bid'):
            return True
        elif trade.Direction() == 'Sell' and rate_validation_failed(shell, jibar_index, ncd_trade_rate, ask_rate, 'Ask'):
            return True
        trade.AdditionalInfo().JIBAR_Bid(bid_rate)
        trade.AdditionalInfo().JIBAR_Ask(ask_rate)
    return False
