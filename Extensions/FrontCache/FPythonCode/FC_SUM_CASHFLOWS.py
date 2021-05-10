'''Developer    : Paseka Motsoeneng, Bhavik Mistry 
    Jira        : FXFA-1250 
'''
import acm
import os
from FxPricingUtils import CalculateTradeValueDayPnL
from penguin_feed import calc_value
from at_logging import getLogger

LOGGER = getLogger(__name__)

CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()
FX_FORWARD = 'FX Forward'
FX_SPOT = 'FX Spot'
FX_SWAP = 'FX Swap'
SWAP_NEAR_LEG = 'Swap Near Leg'
SWAP_FAR_LEG = 'Swap Far Leg'
FX_SALES_PORTS = acm.FCompoundPortfolio['FX_SALES'].SubPortfolios()
ZAR_CURR = acm.FCurrency['ZAR']
TODAY = acm.Time.DateToday()
FILE_PATH = r'D:\DATA\LogFiles\Flogger\customerPnL-{}.txt'.format(str(os.getpid()))


def loop_cashflows(constellation, main_trade):
    """
    Method to add all ZAR cashflows from each trade in the constellation,
    belonging to the FX_SALES portfolio.
    :param constellation: All trades that form part of the constellation.
    :param main_trade: User defined trade to be worked on.
    :return: Total ZAR cashflow amount
    """
    group_total = 0
    proj_values = []

    for member_trade in constellation:
        money_flows = member_trade.MoneyFlows()
        for money_flow in money_flows:
            if money_flow.Currency().Name() == 'ZAR' and \
               money_flow.PayDate() == main_trade.ValueDay() and \
               member_trade.Portfolio() in FX_SALES_PORTS:
                    proj_values.append(float(money_flow.Calculation().Projected(CALC_SPACE).Number()))
                    group_total += float(money_flow.Calculation().Projected(CALC_SPACE).Number())
    LOGGER.info("PNL is {}".format(group_total))
    LOGGER.info("Saving PNL (%s) to file: '%s'", group_total, FILE_PATH)

    try:
        with open(FILE_PATH, 'a') as myfile:
            myfile.write('Input trade: ' + str(main_trade.Oid()) + '\n')
            myfile.write('Return type: ' + str(type(group_total)) + '\n' )
            myfile.write('Return Value: ' + str(float(group_total)) + '\n')
            myfile.write('Proj Values: ' + str(group_total) + '\n')
            myfile.write('---------------------------------\n')
    except:
        LOGGER.exception("Saving of file '%s' failed", FILE_PATH)

    # always return a value if exception occurred only during saving file
    return float(group_total)


def get_sum_cashflows(object):
    """
    Method to separate calculation based on trade type in order to get the
    correct trade constellation
    :param object:
    :return: Total ZAR cashflow amount
    """
    try:
        trade = object.Trade()
        LOGGER.info('Calculating customer PNL for trade {}'.format(trade.Name()))
        if trade.Currency().Name() != 'ZAR' and trade.Instrument().Name() != 'ZAR':
            fx_rate = trade.Currency().Calculation().FXRate(CALC_SPACE, ZAR_CURR, TODAY).Number()
            LOGGER.info('FX rate of currency pair {}/{} is {}'.format(trade.Currency().Name(),
                                                                      trade.Instrument().Name(),
                                                                      fx_rate))
            try:
                if trade.IsFxSwap():
                    return float(CalculateTradeValueDayPnL(trade)*fx_rate)
                else:
                    return float(CalculateTradeValueDayPnL(trade)*fx_rate)
            except:
                return float(calc_value(trade, 'Portfolio Total Profit and Loss')*fx_rate)

        else:
            trade_process = trade.TradeProcessesToString()

            if FX_SPOT in trade_process or FX_FORWARD in trade_process:

                constellation = acm.FTrade.Select('groupTrdnbr = %i' % trade.Oid())

                return loop_cashflows(constellation, trade)

            elif SWAP_NEAR_LEG in trade_process:
                '''Included Spot component in near leg calculation - 2016-04-13'''
                constellation = [x for x in acm.FTrade.Select('groupTrdnbr = %i'
                                 % trade.Oid()) if x.IsFxSwapNearLeg() or x.IsFxSpot() or x.IsFxSwapFarLeg()]

                return loop_cashflows(constellation, trade)

            elif SWAP_FAR_LEG in trade_process:

                connected_trd = trade.ConnectedTrdnbr()

                constellation = [x for x in acm.FTrade.Select('groupTrdnbr = %i'
                                 % connected_trd) if x.IsFxSwapNearLeg() or x.IsFxSpot() or x.IsFxSwapFarLeg()]

                return loop_cashflows(constellation, trade)

        return 0.0
    except:
        LOGGER.exception("Failed to calculate total ZAR cashflow amount")
