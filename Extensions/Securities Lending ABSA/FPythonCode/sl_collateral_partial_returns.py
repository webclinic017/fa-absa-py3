"""--------------------------------------------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Generates a partial return for a collateral trade entry instrument.
                           This script will terminate the existing trade and
                           open both a new trade representing the remaining quantity and the returned quantity.
DEPATMENT AND DESK      :  Collateral
REQUESTER               :  Shaun Du Plessis
DEVELOPER               :  Sihle Gaxa
CR NUMBER               :  

History:

Date            Who                             What
    
2020-02-21      Sihle Gaxa                      Initial Implementation
2020-10-27      Sihle Gaxa                      PCGDEV-608 Updated available collateral
                                                validation to check against selected tra3des only
2021-02-19      Sihle Gaxa                      PCGDEV-663_Added original trade ID in text2 for bulk full returns
-----------------------------------------------------------------------------------------------------------------"""
import acm
from at_logging import getLogger
import sbl_booking_utils as sbl_utils
import sbl_booking_validator as sbl_validator

LOGGER = getLogger(__name__)
BALANCE_TRADE_INDICATOR = "Collateral balance trade"

def partial_return(trades, return_date, return_quantity, trade_time=None, swift_flag=None):

    custody_list = []
    return_trade = None
    sl_validator = None
    custody_trade = None
    remaining_collateral = None

    for trade in trades:

        sl_validator = sbl_validator.ReturnValidator(trade, return_date, return_quantity)

        if (sl_validator.is_valid_collateral_return(trades) or
            sbl_validator.different_client(trades, trade.Counterparty()) or
            sbl_validator.different_instrument(trades, trade.Instrument())):
            raise Exception("{trade} is not valid for collateral return".format(trade=trade.Oid()))
        
        custody_trades = [trade for trade in acm.FTrade.Select("contractTrdnbr = {contract} and oid <> {parent}".format(
                                                             contract=trade.ContractTrdnbr(), parent=trade.Oid()))]
        if custody_trades:
            custody_list.append(custody_trades[0])

    if custody_list:
    
        for custody_trade in custody_list:
            sl_validator = sbl_validator.ReturnValidator(custody_trade, return_date, -1*return_quantity)

            if (sl_validator.is_valid_collateral_return(custody_list) or
                sbl_validator.different_client(custody_list, custody_trade.Counterparty()) or
                sbl_validator.different_instrument(custody_list, custody_trade.Instrument())):
                raise Exception("{trade} is not valid for collateral return".format(trade=custody_trade.Oid()))
        

    return_trade = sbl_utils.generate_partial_return(trades, return_date, return_quantity,
                                                     trade_time, swift_flag)

    custody_trade = [trade for trade in acm.FTrade.Select("contractTrdnbr = {contract} and oid <> {parent}".format(
                                                          contract=return_trade.ContractTrdnbr(), parent=return_trade.Oid()))]

    if not sl_validator.is_collateral_full_return(trades):
        new_custody_trade = None
        remaining_collateral = sbl_utils.get_remaining_collateral(trades, return_quantity,
                                                                  return_trade)
                                                             
        if remaining_collateral:
            new_trade = sbl_utils.create_trade(trades, trades[0].Instrument(), remaining_collateral,
                                                return_date, trade_time, swift_flag)
            new_trade.Text1("")
            new_trade.TradeTime(return_trade.TradeTime())
            new_trade.ValueDay(sbl_utils.TODAY)
            new_trade.AcquireDay(sbl_utils.TODAY)
            new_trade.OptKey1(BALANCE_TRADE_INDICATOR)
            new_trade.ConnectedTrade(return_trade)
            new_trade.Status("Simulated")
            new_trade.Commit()
            LOGGER.info("New balance trade {bal_trade}".format(bal_trade=new_trade.Oid()))
            
            custody_trades_list = sbl_utils.get_custody_trades_list(trades)
            
            if custody_trades_list:
                custody_parent_trade = custody_trades_list[0]
                new_custody_trade = sbl_utils.create_trade(custody_trades_list, custody_parent_trade.Instrument(),
                                                           -1*remaining_collateral, return_date,
                                                           trade_time, swift_flag)
                new_custody_trade.Text1("")
                new_custody_trade.TradeTime(return_trade.TradeTime())
                new_custody_trade.ValueDay(sbl_utils.TODAY)
                new_custody_trade.AcquireDay(sbl_utils.TODAY)
                new_custody_trade.OptKey1(BALANCE_TRADE_INDICATOR)
                if custody_trade:
                    new_custody_trade.ConnectedTrade(custody_trade)
                new_custody_trade.Status("Simulated")
                new_custody_trade.Commit()
                LOGGER.info("New custody balance trade {cus_bal_trade}".format(cus_bal_trade=new_custody_trade.Oid()))
                sbl_utils.connect_trades(new_trade, new_custody_trade)
            new_trade.Status("FO Confirmed")
            new_trade.Commit()
            if new_custody_trade and new_custody_trade.Status() == "Simulated":
                new_custody_trade.Status("FO Confirmed")
                new_custody_trade.Commit()

    else:
        return_trade.Text1("FULL_RETURN")
        if trades and len(trades) > 1:
            return_trade.Text2(return_trade.Oid())
        return_trade.Commit()

        if custody_trade:
            custody_trade[0].Text1("FULL_RETURN")
            if len(custody_list) > 1:
                custody_trade[0].Text2(custody_trade[0].Oid())
            custody_trade[0].Commit()

    return return_trade


ael_variables = sbl_utils.get_ael_variables()


def get_trades(additional_data):

    trades = None
    object = additional_data.At('customData')
    if object.ExtensionObject().IsKindOf(acm.FUiTrdMgrFrame):
        try:
            trades = object.ExtensionObject().ActiveSheet().Selection().SelectedTrades()
        except Exception as e:
            raise Exception('Could not retrieve trades to return against because %s' % str(e))
    else:
        trades = object.ExtensionObject().OriginalTrade()

    return trades

# Menu call defined in FMenuExtension
def run_partial_return(extensionInvokationInfo):
    acm.RunModuleWithParametersAndData('sl_collateral_partial_returns', 'Standard', extensionInvokationInfo)


def ael_main_ex(dictionary, additional_data):

    return_trade = None
    trades = get_trades(additional_data)
    swift_flag = dictionary["swift_flag"]
    trade_time = dictionary['return_tradetime']
    return_quantity = float(dictionary['return_quantity'].replace(',', ''))
    return_date = sbl_utils.CALENDAR.AdjustBankingDays(dictionary['return_date'], 0)

    return_trade = partial_return(trades, return_date, return_quantity, trade_time, swift_flag)

    if return_trade:
        acm.StartApplication('Instrument Definition', return_trade)
