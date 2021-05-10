'''----------------------------------------------------------------------
Department: Prime Services

History:
Date       CR Number     Who                    What
2019-03-28 CHG1001247290 Tibor Reiss            Initial implementation: after aggregation,
                                                move funding and TPL to cash instrument
2019-04-12 CHG1001622197 Tibor Reiss            Include instrument type so that it can be scheduled
                                                at the end of the aggregation batches
2019-04-17 CHG1001639975 Tibor Reiss            Cosmetics only
2019-10-02 FAU-452       Tibor Reiss            FA2018: automatic generation of cfs, resets -> correct these
----------------------------------------------------------------------'''
from time import time
from functools import wraps

import acm
import ael

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from PS_FundingSweeper import (GetLeg, GetFloatCashFlow,
                               CreateLeg, CreateCashFlow,
                               FundingSweeper_transaction,
                               GetReturnCashFlow)
from PS_FundingCalculations import GetReset


LOGGER = getLogger()
NON_ACTIVE_TRADE_STATUS = ["Void", "Simulated"]
TODAY = acm.Time().DateToday()
PREV_BUS_DAY = acm.FCalendar["ZAR Johannesburg"].AdjustBankingDays(acm.Time().DateToday(), -1)
AGGREGATION_USRNBR = acm.FUser["AGGREGATION"].Oid()

LEG_TYPE_FUNDING = "Float"
CF_TYPE_FUNDING = "Funding"
RESET_TYPE_FUNDING = "Return"
LEG_TYPE_TPL = "Total Return"
CF_TYPE_TPL = "TPL"
RESET_TYPE_TPL = "Return"

SQL_GET_INSTRUMENTS = """ 
    SELECT DISTINCT(i.insid)
    FROM trade t, portfolio p, instrument i
    WHERE 1 = 1
          AND t.prfnbr = p.prfnbr
          AND t.insaddr = i.insaddr
          AND t.archive_status = 1
          AND t.aggregate_trdnbr = {trade_number} 
          AND i.insid NOT LIKE 'CASH_PAYMENT%'
    """
SQL_ACTIVE_TRADES = """
    SELECT t.trdnbr
    FROM trade t, portfolio p, instrument i, ds_enums de
    WHERE 1 = 1
          AND t.prfnbr = p.prfnbr
          AND t.insaddr = i.insaddr
          AND de.name = 'TradeStatus'
          AND de.value = t.status
          AND de.tag NOT IN ('Void', 'Simulated')
          AND p.prfid = '{portfolio_name}'
          AND i.insid = '{instrument_name}'
    """
SQL_ARCHIVE_LEG = """
    UPDATE leg
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = 1
    WHERE legnbr = {legnbr}
    """
SQL_ARCHIVE_CASH_FLOW = """
    UPDATE cash_flow
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = 1
    WHERE legnbr = {legnbr}
    """
SQL_ARCHIVE_RESET = """
    UPDATE reset
    SET updat_usrnbr = {usrnbr}
        , updat_time = GETDATE()
        , archive_status = 1
    WHERE cfwnbr = {cfwnbr}
    """


def measure_time(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time()
        result = func(*args, **kwargs)
        end = time()
        LOGGER.info("Time taken for {} = {}".format(func.__name__, end-start))
        return result
    return wrapper


def select_aggregate_trades_today(portfolio_list, ins_types):
    query = acm.CreateFASQLQuery('FTrade', 'AND')
    or_node = query.AddOpNode('OR')
    for it in ins_types:
        or_node.AddAttrNode('Instrument.InsType', 'EQUAL', it)
    query.AddAttrNode('CreateTime', 'GREATER_EQUAL', TODAY)
    for pf in portfolio_list:
        if pf.Compound():
            or_node = query.AddOpNode('OR')
            for pf_phys in pf.AllPhysicalPortfolios():
                or_node.AddAttrNode('Portfolio.Name', 'EQUAL', pf_phys.Name())
        else:
            query.AddAttrNode('Portfolio.Name', 'EQUAL', pf.Name())
    query.AddAttrNode('Aggregate', 'EQUAL', 2)
    return query.Select()


def check_no_active_trades(instrument_name, portfolio_name, only_non_archived=True):
    # If the Void and Terminated (or expired) trades are aggregated
    # at the same time, and the aggregate void trade is processed
    # first in this script, the leg on the pswap can't be archived.
    sql = SQL_ACTIVE_TRADES.format(instrument_name=instrument_name, portfolio_name=portfolio_name)
    if only_non_archived:
        sql += " AND t.archive_status = 0"
    trades = ael.dbsql(sql)
    return trades


def get_cash_ins_leg(pswap, leg_type, cash_ins, funding_index):
    leg = GetLeg(pswap, leg_type, cash_ins)
    is_new_leg = False
    if not leg:
        LOGGER.info("\tCreating leg for {}...".format(cash_ins.Name()))
        leg = CreateLeg(pswap, leg_type, cash_ins, pswap.StartDate(), PREV_BUS_DAY, funding_index)
        is_new_leg = True
    return leg, is_new_leg


def get_cash_flow(leg, cf_type):
    cf_to_migrate = None
    if cf_type == CF_TYPE_TPL:
        cf_to_migrate = GetReturnCashFlow(leg, CF_TYPE_TPL)
    elif cf_type == CF_TYPE_FUNDING:
        cf_to_migrate = GetFloatCashFlow(leg, CF_TYPE_FUNDING)
    return cf_to_migrate


def get_cash_ins_cash_flow(trans, pswap, leg, cf_type):
    cash_flow = get_cash_flow(leg, cf_type)
    if not cash_flow:
        LOGGER.info("\tCreating cash flow for leg {}..".format(leg.Oid()))
        if cf_type == CF_TYPE_FUNDING:
            cash_flow = CreateCashFlow(leg, "Float Rate", pswap.StartDate(),
                                       PREV_BUS_DAY, None, None, CF_TYPE_FUNDING)
        elif cf_type == CF_TYPE_TPL:
            cash_flow = CreateCashFlow(leg, "Position Total Return", pswap.StartDate(),
                                       PREV_BUS_DAY, None, None, CF_TYPE_TPL)
        else:
            LOGGER.error("\tInvalid cash flow type {}".format(cf_type))
            return
    trans.ExtendLeg(leg, PREV_BUS_DAY)
    trans.ExtendCashFlow(cash_flow, PREV_BUS_DAY)
    return cash_flow


def calc_resets(resets_to_migrate, leg, cf_type):
    ins_name = leg.IndexRef().Name()
    if cf_type not in [CF_TYPE_TPL, CF_TYPE_FUNDING]:
        LOGGER.error("\tNot supported cf_type {} for instrument {}".format(cf_type, ins_name))
        return
    cf_to_migrate = get_cash_flow(leg, cf_type)
    if not cf_to_migrate:
        LOGGER.warning("\tNo {} cash flow found for {}.".format(cf_type, ins_name))
        return
    LOGGER.info("\tCalculating {} for {}...".format(cf_type, ins_name))
    last_reset_day = None
    last_reset = None
    for reset in cf_to_migrate.Resets():
        reset_type = reset.ResetType()
        invalid_reset_msg = ("\t\tInvalid reset type {} for instrument "
                             "{}, leg oid = {}, cf oid = {}".format(
                                reset_type, ins_name, leg.Oid(), cf_to_migrate.Oid()))
        if cf_type == CF_TYPE_FUNDING and reset_type != RESET_TYPE_FUNDING:
            LOGGER.error(invalid_reset_msg)
            return
        if cf_type == CF_TYPE_TPL and reset_type != RESET_TYPE_TPL:
            LOGGER.warning(invalid_reset_msg)
            LOGGER.warning("\t\tSkipping this reset")
            continue
        reset_day = reset.Day()
        if not last_reset_day or reset_day > last_reset_day:
            last_reset_day = reset_day
            last_reset = reset
        if reset_day in resets_to_migrate:
            resets_to_migrate[reset_day]["fixing_value"] += reset.FixingValue()
        else:
            resets_to_migrate[reset_day] = {}
            resets_to_migrate[reset_day]["fixing_value"] = reset.FixingValue()
            resets_to_migrate[reset_day]["start_date"] = reset.StartDate()
            resets_to_migrate[reset_day]["end_date"] = reset.EndDate()
    LOGGER.info("\t\tTotal {} contribution = {}".format(cf_type, last_reset.FixingValue()))


def create_cash_ins_resets(trans, cash_flow, resets_to_migrate, reset_type):
    for reset_day in resets_to_migrate:
        reset = GetReset(cash_flow, reset_type, reset_day, True)
        new_reset_value = resets_to_migrate[reset_day]["fixing_value"]
        if reset:
            new_reset_value += reset.FixingValue()
            trans.UpdateResetFixingValue(reset, new_reset_value)
        else:
            reset = resets_to_migrate[reset_day]
            trans.CreateReset(cash_flow, reset_type,
                              reset_day, reset["start_date"],
                              reset["end_date"], new_reset_value)


@measure_time
def archive_legs(legs_to_archive):
    for leg_oid in legs_to_archive:
        leg = acm.FLeg[leg_oid]
        cf_oids = [cf.Oid() for cf in leg.CashFlows()]
        for cf_oid in cf_oids:
            try:
                sql = SQL_ARCHIVE_RESET.format(cfwnbr=cf_oid, usrnbr=AGGREGATION_USRNBR)
                ael.dbsql(sql)
                sql = SQL_ARCHIVE_CASH_FLOW.format(legnbr=leg_oid, usrnbr=AGGREGATION_USRNBR)
                ael.dbsql(sql)
            except:
                LOGGER.exception("\tCould not archive cashflow/reset with cfwnbr {}.".format(cf_oid))
        try:
            sql = SQL_ARCHIVE_LEG.format(legnbr=leg_oid, usrnbr=AGGREGATION_USRNBR)
            ael.dbsql(sql)
        except:
            LOGGER.exception("\tCould not archive leg with legnbr {}".format(leg_oid))
        LOGGER.info("Archiving leg {} successful.".format(leg_oid))


@measure_time
def migrate_resets(trans, pswap, leg_type, cf_type, reset_type, resets, cash_ins, funding_index):
    (leg, is_new_leg) = get_cash_ins_leg(pswap, leg_type, cash_ins, funding_index)
    cash_flow = get_cash_ins_cash_flow(trans, pswap, leg, cf_type)
    create_cash_ins_resets(trans, cash_flow, resets, reset_type)
    if is_new_leg:
        return leg
    return None


def clean_up_new_legs(leg_funding, leg_tpl):
    """ In 2018 version, cashflows and resets are automatically created
        when creating a new leg, thus need to be corrected if necessary
    """
    acm.PollDbEvents()
    if leg_funding is not None:
        leg_oid = leg_funding.Oid()
        cash_flow = GetFloatCashFlow(leg_funding, 'Funding')
        if not cash_flow:
            LOGGER.error("Did not find funding cash flow for leg {}".format(leg_oid))
        else:
            cash_flow.AddInfoValue('PS_FundWarehouse', "Funding")
            cash_flow.Commit()
            for reset in cash_flow.Resets()[:]:
                if reset.ResetType() in ("Nominal Scaling", "Simple Overnight"):
                    reset.Delete()
            LOGGER.info("\tUpdated funding leg {}".format(leg_oid))
    if leg_tpl is not None:
        leg_oid = leg_tpl.Oid()
        cash_flow = GetReturnCashFlow(leg_tpl, 'TPL')
        if not cash_flow:
            LOGGER.error("Did not find return cash flow for leg {}".format(leg_oid))
        else:
            cash_flow.CashFlowType("Position Total Return")
            cash_flow.AddInfoValue('PS_FundWarehouse', "TPL")
            cash_flow.Commit()
            LOGGER.info("\tUpdated tpl leg {}".format(leg_oid))


ael_variables = AelVariableHandler()
ael_variables.add("pf_list",
                  label="Portfolio Name",
                  cls="FCompoundPortfolio",
                  mandatory=True,
                  multiple=True,
                  collection=acm.FCompoundPortfolio.Select('')
                  )
ael_variables.add("ins_types",
                  label="Instrument types",
                  cls="string",
                  mandatory=True,
                  multiple=True,
                  collection=acm.FEnumeration['enum(InsType)'].Values()
                  )


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    acm.PollDbEvents()
    legs_to_archive = []
    aggregate_trades_list = select_aggregate_trades_today(ael_dict["pf_list"], ael_dict["ins_types"])
    for aggregate_trade in aggregate_trades_list:
        aggregate_trade_status = aggregate_trade.Status()
        aggregate_trade_oid = aggregate_trade.Oid()
        portfolio = aggregate_trade.Portfolio()
        portfolio_name = portfolio.Name()
        pswap = portfolio.AdditionalInfo().PS_FundingIns()
        funding_index = acm.FInstrument[pswap.add_info('PSONPremIndex')]
        LOGGER.info("Processing trade {}: status={} pf={} pswap={}...".format(aggregate_trade_oid, aggregate_trade_status, portfolio_name, pswap.Name()))
        # Get archived trades which are part of the aggregated trade
        sql = SQL_GET_INSTRUMENTS.format(trade_number=aggregate_trade_oid)
        instrument_names_of_archived_trades = ael.dbsql(sql)
        ins_names_to_archive = []
        only_non_archived_trades_flag = True
        if aggregate_trade_status in NON_ACTIVE_TRADE_STATUS:
            only_non_archived_trades_flag = False
        for row in instrument_names_of_archived_trades[0]:
            archived_ins_name = row[0]
            active_trades = check_no_active_trades(archived_ins_name, portfolio_name, only_non_archived_trades_flag)
            if active_trades[0]:
                msg = ("\tThere are active trades on instrument {} "
                       "in portfolio {}.".format(archived_ins_name, portfolio_name))
                if aggregate_trade_status in NON_ACTIVE_TRADE_STATUS:
                    LOGGER.warning(msg)
                else:
                    LOGGER.error(msg)
            else:
                ins_names_to_archive.append(archived_ins_name)
        # Calculate funding/tpl resets
        resets_funding = {}
        resets_tpl = {}
        for leg in pswap.Legs():
            index_ref_name = leg.IndexRef().Name()
            if index_ref_name in ins_names_to_archive:
                leg_oid = leg.Oid()
                LOGGER.info("\tMarking {} oid={} for archiving".format(index_ref_name, leg_oid))
                legs_to_archive.append(leg_oid)
                if aggregate_trade_status not in NON_ACTIVE_TRADE_STATUS:
                    if leg.LegType() == LEG_TYPE_FUNDING:
                        calc_resets(resets_funding, leg, CF_TYPE_FUNDING)
                    if leg.LegType() == LEG_TYPE_TPL:
                        calc_resets(resets_tpl, leg, CF_TYPE_TPL)
        # Write funding/tpl resets to cash payment instrument
        trans = FundingSweeper_transaction(pswap)
        cash_ins = aggregate_trade.Instrument()
        leg_funding = migrate_resets(trans, pswap,
                                     LEG_TYPE_FUNDING, CF_TYPE_FUNDING, RESET_TYPE_FUNDING,
                                     resets_funding, cash_ins, funding_index)
        leg_tpl = migrate_resets(trans, pswap,
                                 LEG_TYPE_TPL, CF_TYPE_TPL, RESET_TYPE_TPL,
                                 resets_tpl, cash_ins, funding_index)
        trans.Commit()
        clean_up_new_legs(leg_funding, leg_tpl)
        LOGGER.info("\tCash instrument updated on pswap.")

    # Archive legs on pswap
    archive_legs(legs_to_archive)
    
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    
    LOGGER.info('Completed successfully.')
