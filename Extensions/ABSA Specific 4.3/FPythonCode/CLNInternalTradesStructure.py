"""
MODULE
	CLNInternalTradesStructure

DESCRIPTION
	This module is used to create the trades for Credit Linked Note (CLN) deal structure

HISTORY
=======
2020-08-25 Snowy Mabilu ARR-74- Initial Code

"""

import acm
import at_addInfo
import FTradeCreator
from at_logging import getLogger

lOGGER = getLogger(__name__)


def populate_cds_leg(client_leg, new_leg, credit_ref):
    """
    This function creates the legs for the credit default swap trade by using information from an existing leg
    :param client_leg:
    :param new_leg:
    :param credit_ref:
    :return:
    """
    new_leg.Apply(client_leg)
    new_leg.FloatRateFactor(0)
    new_leg.FloatRateFactor2(0)
    new_leg.FloatRateReference(None)
    new_leg.NominalAtEnd('false')
    new_leg.ResetCalendar(None)
    new_leg.ResetDayMethod('Following')
    new_leg.ResetPeriodCount(0)
    new_leg.ResetDayOffset(-2)
    new_leg.ResetPeriodUnit('Days')
    new_leg.ResetType(0)
    new_leg.Spread(0)
    new_leg.CreditRef(acm.FBond[credit_ref])


def create_trade(instrument, params, client=None):
    """
    This fuction create a trade object using the parameters and a input trade
    :param instrument:
    :param params: FParameters with values that need to be set
    :param client:
    :return:
    """
    trade_data = {"Acquirer": client.Acquirer().Name() if params['acquirer'] is None else params['acquirer'].Text(),
                  "MirrorPortfolio": client.MirrorPortfolio() if params['mirror_portfolio'] is None else params[
                      'mirror_portfolio'].Text(),
                  "Counterparty": client.Counterparty().Name() if params['counterparty'] is None else params[
                      'counterparty'].Text(),
                  "Portfolio": client.Portfolio().Name() if params['portfolio'] is None else params['portfolio'].Text(),
                  "Instrument": instrument.Name()

                  }
    if client is None:
        trade = FTradeCreator.DecoratedTradeCreator(trade_data).CreateTrade()
    else:
        trade = client.StorageNew()
        trade.OptionalKey(None)
        FTradeCreator.TradeCreator.SetProperties(trade, trade_data)
    trade.Status('Simulated')
    trade.Trader(acm.User())
    trade.TradeTime(acm.Time.TimeNow())
    value_day = acm.FCalendar['ZAR Johannesburg'].AdjustBankingDays(acm.Time().DateToday(), 3)
    trade.ValueDay(value_day)
    trade.AcquireDay(value_day)
    trade.RegisterInStorage()
    return trade


def create_cds_trade(client, rate, credit_ref, params, deposit):
    """
    This function creates the Credit default swap trade and sets its transaction reference  to deposit trade
    :param client:
    :param rate:
    :param credit_ref:
    :param params: FParameters with values that need to be set
    :param deposit:
    :return:
    """
    cds = acm.FBusinessLogicDecorator.WrapObject(acm.FCreditDefaultSwap())

    frn_leg = client.Instrument().FirstEditLeg()
    frn_leg_clone = frn_leg.Clone()

    # Create the credit default leg
    pay_leg = cds.CreateLeg(8)
    populate_cds_leg(frn_leg_clone, pay_leg, credit_ref)
    pay_leg.LegType(8)
    pay_leg.PayLeg('true')
    pay_leg.RollingPeriodCount(0)

    # Create the fixed leg
    receive_leg = cds.CreateLeg(1)
    populate_cds_leg(frn_leg_clone, receive_leg, credit_ref)
    receive_leg.LegType(1)
    receive_leg.FixedRate(rate)
    receive_leg.ExtendedFinalCf('true')  
    cds.Commit()

    trade = create_trade(cds, params, client)
    trade.Price(0.0)
    if 'CLN_Client_Trade_Parameters' == params.Name().Text():
        trade.AddInfoValue('Approx. load', params['approx_load'].Text())
        trade.AddInfoValue('Approx. load ref', params['approx_load_ref'].Text())
        trade.AddInfoValue('InsOverride', params['ins_override'].Text())
    else:
        trade.AddInfoValue('Approx. load', None)
        trade.AddInfoValue('Approx. load ref', None)
        trade.AddInfoValue('InsOverride', None)
        trade.AddInfoValue('Companion_Spread', None)
        trade.AddInfoValue('RTG', None)
    at_addInfo.save_or_delete(trade, 'MM_Instype', '')
    trade.TrxTrade(deposit)
    trade.Premium(0.0)
    trade.Commit()
    lOGGER.info(
        "Successfully booked CDS trade {0} against Counterparty {1} ".format(trade.Name(), trade.Counterparty().Name()))
    return trade


def create_deposit(client, params):
    """
    Create the deposit trade using the input parameter
    :param client: The client trade which the deal structure is being created for
    :param params: FParameters with values that need to be set
    :return:
    """
    deposit = acm.FBusinessLogicDecorator.WrapObject(acm.FDeposit())
    deposit.RegisterInStorage()
    deposit.ValuationGrpChlItem(acm.FChoiceList[params['val_group'].Text()])
    deposit.Quotation(params['quotation'].Text())
    deposit.QuoteType(params['quotation'].Text())
    frn_leg = client.Instrument().FirstEditLeg()
    frn_leg_clone = frn_leg.Clone()
    new_leg = deposit.CreateLeg(2)
    new_leg.Apply(frn_leg_clone)
    new_leg.AmortDaycountMethod('Act/365')
    new_leg.FloatRateFactor2(0.0)
    new_leg.ResetPeriodCount(0)
    new_leg.ResetPeriodUnit('Days')
    new_leg.StrikeType('Absolute')
    deposit.Commit()
    trade = create_trade(deposit, params, None)
    trade.Price(client.Price())
    nominal = client.Nominal()
    premium = -1 * client.Nominal()
    trade.Premium(premium)
    trade.Nominal(nominal)
    trade.AdditionalInfo().Funding_Instype(params['funding_ins_type'].Text())
    trade.Commit()
    lOGGER.info("Successfully booked deposit trade {0} against counter-party {1} ".format(trade.Name(),
                                                                                          trade.Counterparty().Name()))
    return trade
