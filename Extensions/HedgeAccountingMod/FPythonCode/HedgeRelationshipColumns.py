# grouping: sheet columns/dealpackagesheet
# grouping: sheet columns/tradesheet

'''
===================================================================================================
PURPOSE: The purpose of this module is to contain functions that retrieve and calculate values
            used in the Hedge Effectiveness Testing trading manager columns.
HISTORY:
---------------------------------------------------------------------------------------------------
XX-XX-2016 FIS Team            Initial implementation
29-08-2018 FIS Team            Addition of closing trade columns for dedesignation
===================================================================================================
'''

import acm
import FLogger
import HedgeRelation
import HedgeConstants
import HedgeUtils

logger = FLogger.FLogger(HedgeConstants.STR_HEDGE_TITLE)

denominatedvalue = acm.GetFunction('denominatedvalue', 4)

# Column Names
CLEAN_PRICE = 'Portfolio Clean PnL'
TOTAL_PROFIT_AND_LOSS = 'Portfolio Total Profit and Loss'
REALISED_DEPREC = 'Portfolio Realized Deprec Profit and Loss'
UNREALISED_DEPREC = 'UnRealized Deprec'
TOTAL_DEPREC = 'Total Deprec'
VAL_END = 'Total Val End'
PORTFOLIO_VAL = 'Portfolio Value'
VAL = 'Portfolio Value End'
INTEREST = 'Portfolio Interest'
ACCRUED_INTEREST = 'Portfolio Accrued Interest'
TRADED_INTEREST = 'Portfolio Traded Interest'
ACCRUED_INTEREST_ADJ = 'Accrued Interest Adjustment'
HYPO_PL_ADJ = 'Hypo PL Adjustment'
NOMINAL = 'Current Nominal'

PNLSTARTDATE = "Portfolio Profit Loss Start Date"
PNLSTARTDATECUSTOM = "Portfolio Profit Loss Start Date Custom"
PNLENDDATE = "Portfolio Profit Loss End Date"
PNLENDDATECUSTOM = "Portfolio Profit Loss End Date Custom"

calc_space = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FTradeSheet')


def custom_method_HR_status(trade):
    hedge_relationship_status = ''
    try:
        deal_package = trade.DealPackage()
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None
        else:
            hedge_relationship_status += hedge_relationship.get_status()
    except:
        hedge_relationships = HedgeRelation.find_relation_for_trade(trade)
        for hedge_relationship_name in hedge_relationships:
            hedge_relationship = HedgeRelation.HedgeRelation(hedge_relationship_name)
            hedge_relationship.read()
            hedge_relationship_status += hedge_relationship.get_status()
    return hedge_relationship_status


def custom_method_ref_HR(trade):
    hedge_relationship_ref_HR = ''
    try:
        deal_package = trade.DealPackage()
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None
        else:
            hedge_relationship_ref_HR += hedge_relationship.get_HR_reference()
    except:
        hedge_relationships = HedgeRelation.find_relation_for_trade(trade)
        for hedge_relationship_name in hedge_relationships:
            hedge_relationship = HedgeRelation.HedgeRelation(hedge_relationship_name)
            hedge_relationship.read()
            hedge_relationship_ref_HR += hedge_relationship.get_HR_reference()
    return hedge_relationship_ref_HR


def get_hedge_start_date(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_start_date()


def get_hedge_end_date(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_end_date()


def get_hedge_status(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_status()


def get_hedge_name(deal_package, trade):
    if deal_package:
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None
        else:
            hedge_relationship_name = hedge_relationship.get_file_name()
    else:
        hedge_relationships = HedgeRelation.find_relation_for_trade(trade)
        hedge_relationship_name = ', '.join(hedge_relationships)

    return hedge_relationship_name


def get_hedge_dedesignation_reason(deal_package, trade):
    if deal_package:
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None

        return hedge_relationship.get_termination()

    return None


def get_hedge_dedesignation_date(deal_package, trade):
    if deal_package:
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None

        return hedge_relationship.get_termination_date()

    return None


def get_hedge_ref_HR(deal_package, trade):
    if deal_package:
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if not hedge_relationship:
            return None
        else:
            hedge_relationship_ref_HR = hedge_relationship.get_HR_reference()
    else:
        hedge_relationship_ref_HR = ''
        hedge_relationships = HedgeRelation.find_relation_for_trade(trade)
        for hedge_relationship_name in hedge_relationships:
            hedge_relationship = HedgeRelation.HedgeRelation(hedge_relationship_name)
            hedge_relationship.read()
            hedge_relationship_ref_HR += hedge_relationship.get_HR_reference()

    return hedge_relationship_ref_HR


def get_hedge_number(deal_package, trade):
    '''Assumes that the deal package name includes the hr text object oid
    '''
    hedge_relationship_names = get_hedge_name(deal_package, trade)
    hr_names = ''
    count = 0
    if hedge_relationship_names:
        hr_name_list = hedge_relationship_names.split(',')
        for hr_name in hr_name_list:
            if count > 0:
                hr_names += ', '
            hr_names += hr_name.split('/')[1]
            count += 1

    return hr_names


def get_hedge_traded_spread(deal_package):
    if not deal_package:
        return
    else:
        attr_curve_name = HedgeConstants.STR_SPREAD_ATTR_CURVE
        attr_curve = acm.FYieldCurve[attr_curve_name]
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if hedge_relationship:
            start_date = hedge_relationship.get_start_date()
            if start_date != acm.Time().DateNow():
                attr_curve = acm.GetHistoricalEntity(attr_curve, start_date)
            yc_attribute = acm.FYCAttribute.Select('curve = "%s"' % attr_curve.Name())[0]

            for spread in yc_attribute.Spreads():
                if spread.Point().Name() == '1d':
                    return spread.Spread() * 100
        else:
            return
    logger.ELOG('The 1d spread for the curve %s could not be found on %s. '
                'Returned none.' % (attr_curve_name, start_date))
    return


def get_hedge_current_spread(deal_package, pnl_start_date):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    attr_curve_name = HedgeConstants.STR_SPREAD_ATTR_CURVE
    attr_curve = acm.FYieldCurve[attr_curve_name]
    if pnl_start_date != acm.Time().DateNow():
        attr_curve = acm.GetHistoricalEntity(attr_curve, pnl_start_date)
    yc_attribute = acm.FYCAttribute.Select('curve = "%s"' % attr_curve.Name())[0]

    for spread in yc_attribute.Spreads():
        if spread.Point().Name() == '1d':
            return spread.Spread() * 100
    logger.ELOG('The 1d spread for the curve %s could not be found on %s. '
                'Returned none.' % (attr_curve_name, pnl_start_date))
    return


def get_trade_hedge_type(trade, deal_package):
    result_hedge_type = None

    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if hedge_relationship:
        hedge_trades = hedge_relationship.get_trades()

        if str(trade.Oid()) in list(hedge_trades.keys()):
            hedge_type, _, _ = hedge_trades['%s' % trade.Oid()]
            result_hedge_type = hedge_type
        elif trade.TrxTrade():
            if str(trade.TrxTrade().Oid()) in list(hedge_trades.keys()):
                hedge_type, _, _ = hedge_trades['%s' % trade.TrxTrade().Oid()]
                result_hedge_type = hedge_type
        else:
            result_hedge_type = None

    else:
        result_hedge_type = None

    return result_hedge_type


def get_trade_hedge_percent(trade, deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    hedge_trades = hedge_relationship.get_trades()
    if str(trade.Oid()) in list(hedge_trades.keys()):
        _, percent, _ = hedge_trades['%s' % trade.Oid()]
    elif str(trade.TrxTrade().Oid()) in list(hedge_trades.keys()):
        _, percent, _ = hedge_trades['%s' % trade.TrxTrade().Oid()]
    else:
        return None
    return percent


def get_oid_for_type(deal_package, in_type):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    hedge_trades = hedge_relationship.get_trades()
    for oid in hedge_trades:
        hedge_type, _, _ = hedge_trades[oid]
        if hedge_type == in_type:
            return int(oid)
    return None


def get_hedge_relationship_category(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_type()


def get_hedge_relationship_sub_category(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_sub_type()


def remove_simulations():
    calc_space.RemoveGlobalSimulation(PNLSTARTDATE)
    calc_space.RemoveGlobalSimulation(PNLSTARTDATECUSTOM)
    calc_space.RemoveGlobalSimulation(PNLENDDATE)
    calc_space.RemoveGlobalSimulation(PNLENDDATECUSTOM)


def get_simulated_calc_space(pnl_start_date, pnl_end_date):
    # Simulate PnL start and end dates
    calc_space.SimulateGlobalValue(PNLSTARTDATE, 'Custom Date')
    calc_space.SimulateGlobalValue(PNLSTARTDATECUSTOM, pnl_start_date)
    calc_space.SimulateGlobalValue(PNLENDDATE, 'Custom Date')
    calc_space.SimulateGlobalValue(PNLENDDATECUSTOM, pnl_end_date)
    return calc_space


def get_required_trades(hedge_trades):
    bond_list = []
    bond_child_list = []
    hypo_list = []
    zero_list = []
    external_list = []
    for oid in list(hedge_trades.keys()):
        hedge_type, _, child_oid = hedge_trades[oid]
        if hedge_type == 'Hypo':
            hypo_list.append(acm.FTrade[oid])
        if hedge_type == 'External':
            external_list.append(acm.FTrade[oid])
        if hedge_type == 'Original':
            bond_list.append(acm.FTrade[oid])
            bond_child_list.append(acm.FTrade[child_oid])
        if hedge_type == 'Zero Bond':
            zero_list.append(acm.FTrade[oid])
    return bond_list, bond_child_list, external_list, hypo_list, zero_list


def get_closed_trades(hedge_trades):
    bond_child_close_list = []
    hypo_close_list = []
    zero_close_list = []
    external_close_list = []
    for oid in list(hedge_trades.keys()):
        trade = acm.FTrade[oid]
        hedge_type, _, child_oid = hedge_trades[oid]
        if hedge_type == 'Hypo Close':
            hypo_close_list.append(acm.FTrade[oid])
        if hedge_type == 'External' and trade.Type() == 'Closing':
            external_close_list.append(acm.FTrade[oid])
        if hedge_type == 'Original Close':
            bond_child_close_list.append(acm.FTrade[oid])
        if hedge_type == 'Zero Bond' and trade.Type() == 'Closing':
            zero_close_list.append(acm.FTrade[oid])
    return bond_child_close_list, external_close_list, hypo_close_list, zero_close_list


def get_bond_child_ai(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, bond_child_list, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not (bond_list and bond_child_list):
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_ai = 0

    for bond_child in bond_child_list:
        ai = HedgeUtils.get_value_for_calculation(calc_space, bond_child, ACCRUED_INTEREST)
        ti = HedgeUtils.get_value_for_calculation(calc_space, bond_child, TRADED_INTEREST)
        bond_child_ai += ai - ti

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_ai, currency, '', '')


def get_bond_child_close_ai(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_child_close_list, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not bond_child_close_list:
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_close_ai = 0

    for bond_child_close in bond_child_close_list:
        ai = HedgeUtils.get_value_for_calculation(calc_space, bond_child_close, ACCRUED_INTEREST)
        ti = HedgeUtils.get_value_for_calculation(calc_space, bond_child_close, TRADED_INTEREST)
        bond_child_close_ai += ai - ti

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_close_ai, currency, '', '')


def get_bond_child_nom(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, bond_child_list, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not (bond_list and bond_child_list):
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_nom = 0
    for bond_child in bond_child_list:
        bond_child_nom += HedgeUtils.get_value_for_calculation(calc_space, bond_child, NOMINAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_nom, currency, '', '')


def get_bond_child_close_nom(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_child_close_list, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not bond_child_close_list:
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_close_nom = 0
    for bond_child_close in bond_child_close_list:
        bond_child_close_nom += HedgeUtils.get_value_for_calculation(calc_space, bond_child_close, NOMINAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_close_nom, currency, '', '')


def get_bond_child_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    currency = ''
    bond_child_unrealised_deprec = 0
    for trade in deal_package.Trades():
        hedge_type = calc_space.CreateCalculation(trade, 'Trade Hedge Type')
        if currency == '' and hedge_type.Value() == HedgeConstants.Hedge_Trade_Types.Hypo:
            currency = HedgeUtils.get_value_for_calculation(calc_space, trade, 'Portfolio Currency')
        if hedge_type.Value() == HedgeConstants.Hedge_Trade_Types.Original:
            bond_child_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space, trade, UNREALISED_DEPREC)
    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_unrealised_deprec, currency, '', '')


def get_bond_child_close_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    currency = ''
    bond_child_close_unrealised_deprec = 0
    for trade in deal_package.Trades():
        hedge_type = calc_space.CreateCalculation(trade, 'Trade Hedge Type')
        if currency == '' and hedge_type.Value() == 'Hypo Close':
            currency = HedgeUtils.get_value_for_calculation(calc_space, trade, 'Portfolio Currency')
        if hedge_type.Value() == HedgeConstants.Hedge_Trade_Types.Original:
            bond_child_close_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space, trade,
                                                                                       UNREALISED_DEPREC)
    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(-1 * bond_child_close_unrealised_deprec, currency, '', '')


def get_bond_child_val(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, bond_child_list, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not (bond_list and bond_child_list):
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_val = 0
    for bond_child in bond_child_list:
        bond_child_val += HedgeUtils.get_value_for_calculation(calc_space,
                                                               bond_child,
                                                               PORTFOLIO_VAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_val, currency, '', '')


def get_bond_child_close_val(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_child_close_list, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not bond_child_close_list:
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_child_close_val = 0
    for bond_child_close in bond_child_close_list:
        bond_child_close_val += HedgeUtils.get_value_for_calculation(calc_space,
                                                                     bond_child_close,
                                                                     PORTFOLIO_VAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_child_close_val, currency, '', '')


def get_bond_from_trade(trade):
    deal_package = trade.DealPackage()
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, _, _, _, _ = get_required_trades(hedge_trades)
    if not bond_list:
        return None
    sorted_bond_list = sorted(bond_list, key=lambda x: x.TradeTime())
    first_bond_oid = sorted_bond_list[0].Oid()  # Get oldest original trade from DP
    first_bond_child_oid = hedge_trades[str(first_bond_oid)][2]
    return acm.FTrade[first_bond_child_oid]


def get_bond_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, bond_child_list, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not (bond_list and bond_child_list):
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    bond_unrealised_deprec = 0
    for bond in bond_list:
        bond_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space,
                                                                       bond,
                                                                       UNREALISED_DEPREC)
    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(bond_unrealised_deprec, currency, '', '')


def get_hypo_ai(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not hypo_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_ai = 0
    for hypo in hypo_list:
        ai = HedgeUtils.get_value_for_calculation(calc_space, hypo, ACCRUED_INTEREST)
        ti = HedgeUtils.get_value_for_calculation(calc_space, hypo, TRADED_INTEREST)
        hypo_ai += ai - ti

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_ai, currency, '', '')


def get_hypo_close_ai(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not hypo_close_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_close_ai = 0
    for hypo_close in hypo_close_list:
        ai = HedgeUtils.get_value_for_calculation(calc_space, hypo_close, ACCRUED_INTEREST)
        ti = HedgeUtils.get_value_for_calculation(calc_space, hypo_close, TRADED_INTEREST)
        hypo_close_ai += ai - ti

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_close_ai, currency, '', '')


def get_hypo_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not hypo_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_unrealised_deprec = 0
    for hypo in hypo_list:
        hypo_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space,
                                                                       hypo,
                                                                       UNREALISED_DEPREC)
    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_unrealised_deprec, currency, '', '')


def get_hypo_close_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_close_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not hypo_close_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_close_unrealised_deprec = 0
    for hypo_close in hypo_close_list:
        hypo_close_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space, hypo_close, UNREALISED_DEPREC)
    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(-1 * hypo_close_unrealised_deprec, currency, '', '')


def get_hypo_val(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not hypo_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_val = 0
    for hypo in hypo_list:
        hypo_val += HedgeUtils.get_value_for_calculation(calc_space, hypo, PORTFOLIO_VAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_val, currency, '', '')


def get_hypo_close_val(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not hypo_close_list:
        remove_simulations()
        return denominatedvalue(0.0, None, '', '')

    hypo_close_val = 0
    for hypo_close in hypo_close_list:
        hypo_close_val += HedgeUtils.get_value_for_calculation(calc_space, hypo_close, PORTFOLIO_VAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_close_val, currency, '', '')


def get_hypo_nom(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_list, bond_child_list, _, hypo_list, _ = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    if not (bond_list and bond_child_list):
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    hypo_nom = 0
    for hypo in hypo_list:
        hypo_nom += HedgeUtils.get_value_for_calculation(calc_space, hypo, NOMINAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_nom, currency, '', '')


def get_hypo_close_nom(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    bond_child_close_list, _, hypo_close_list, _ = get_closed_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    if not bond_child_close_list:
        remove_simulations()
        return denominatedvalue(0.0, currency, '', '')

    # Calculate required values
    hypo_close_nom = 0
    for hypo_close in hypo_close_list:
        hypo_close_nom += HedgeUtils.get_value_for_calculation(calc_space, hypo_close, NOMINAL)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(hypo_close_nom, currency, '', '')


def get_zero_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_list, zero_list = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    zero_unrealised_deprec = 0
    for zero in zero_list:
        zero_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space,
                                                                       zero,
                                                                       UNREALISED_DEPREC)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(zero_unrealised_deprec, currency, '', '')


def get_zero_close_unrealised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_close_list, zero_close_list = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_close_list[0], 'Portfolio Currency')
    zero_close_unrealised_deprec = 0
    for zero_close in zero_close_list:
        zero_close_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space, zero_close, UNREALISED_DEPREC)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(-1 * zero_close_unrealised_deprec, currency, '', '')


def get_zero_realised_deprec(deal_package, pnl_start_date, pnl_end_date):
    # Get hedge relation from deal package
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return denominatedvalue(0.0, None, '', '')

    calc_space = get_simulated_calc_space(pnl_start_date, pnl_end_date)

    # Get required trades
    hedge_trades = hedge_relationship.get_trades()
    _, _, _, hypo_list, zero_list = get_required_trades(hedge_trades)

    currency = HedgeUtils.get_value_for_calculation(calc_space, hypo_list[0], 'Portfolio Currency')
    zero_unrealised_deprec = 0
    for zero in zero_list:
        zero_unrealised_deprec += HedgeUtils.get_value_for_calculation(calc_space,
                                                                       zero,
                                                                       REALISED_DEPREC)

    # Unsimulate PnL start and end dates
    remove_simulations()

    return denominatedvalue(zero_unrealised_deprec, currency, '', '')


def get_used_in_hedge(trade):
    if trade.DealPackage():
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(trade.DealPackage())
        if not hedge_relationship:
            return False
        return True
    if HedgeRelation.find_relation_for_trade(trade):
        return True
    return False


def get_child_used_in_hedge(trade):
    if not trade:
        return False
    query = "portfolio = '%s' and trxTrade = %d" \
            % (HedgeConstants.STR_CHILD_TRADE_PORTFOLIO, trade.Oid())
    child_trades = acm.FTrade.Select(query)
    if not child_trades:
        return False
    for child_trade in child_trades:
        deal_package = child_trade.DealPackage()
        if not deal_package:
            return False
        hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
        if hedge_relationship:
            return True
    return False


def get_pro_reg_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_pro_reg_enabled()


def get_pro_do_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_pro_do_enabled()


def get_pro_cv_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_pro_cv_enabled()


def get_ret_do_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_ret_do_enabled()


def get_pro_vrm_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_pro_vrm_enabled()


def get_ret_vrm_enabled(deal_package):
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)
    if not hedge_relationship:
        return None
    return hedge_relationship.get_ret_vrm_enabled()


def get_dedesignation_payment(trade):
    payment_value = 0
    if trade and trade.IsKindOf(acm.FTrade):
        if trade.Payments():
            for payment in trade.Payments():
                if payment.Type() == 'Termination Fee':
                    payment_value = payment.Amount()

    return payment_value


def get_closing_trade_total(deal_package):
    closingTradePaymentTotal = 0
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)

    trade_list = hedge_relationship.get_trades()

    for tradeOid in trade_list:
        m_type, _, _ = trade_list[tradeOid]

        if m_type in ['Closing', 'Close Zero']:
            trade = acm.FTrade[tradeOid]
            closingTradePaymentTotal += get_dedesignation_payment(trade)

    return closingTradePaymentTotal


def has_closing_trade(deal_package):
    closingTradeFound = False
    hedge_relationship = HedgeUtils.get_hedge_from_dealpackage(deal_package)

    trade_list = hedge_relationship.get_trades()

    for tradeOid in trade_list:
        m_type, _, _ = trade_list[tradeOid]

        if m_type in ['Closing', 'Close Zero']:
            closingTradeFound = True

    return closingTradeFound
