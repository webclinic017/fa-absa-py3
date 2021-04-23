'''-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer          Description
--------------------------------------------------------------------------------
2018-10-02                  Tibor Reiss        Initial implementation
2020-02-06 FAPE-205         Tibor Reiss        Fix format of addinfo PSSweepBaseDay
-----------------------------------------------------------------------------'''
import acm

from at_logging import getLogger
from PS_Names import (get_pswap_name,
                      get_portfolio_name,
                      get_rate_index_name,
                      get_pswap_portfolio_name)
from PS_AssetClasses import (CFD,
                             CORPBONDS,
                             GOVIBONDS)
from datetime import datetime


LOGGER = getLogger()


def add_engineering_trade(pswap, product_type, short_name, counterparty):
    trade = acm.FTrade()
    trade.Instrument(pswap)
    trade.Currency('ZAR')
    trade.Quantity(1)
    trade.Nominal(1)
    trade.TradeTime(pswap.StartDate())
    trade.ValueDay(pswap.StartDate())
    trade.AcquireDay(pswap.StartDate())
    trade.Counterparty(counterparty)
    trade.Acquirer(acm.FParty['PRIME SERVICES DESK'])
    if product_type == CFD:
        pfname = 'PB_CFD_' + short_name
    else:
        pfname = get_pswap_portfolio_name(short_name)
    portfolio = acm.FPhysicalPortfolio[pfname]
    trade.Portfolio(portfolio)
    trade.Status('Simulated')
    trade.Commit()
    return trade


def get_or_create_rate_index(product_type, short_name, fully_funded, bid, ask):
    rate_index_name = get_rate_index_name(product_type, short_name, fully_funded)
    rate_index = acm.FRateIndex[rate_index_name]
    if rate_index:
        # If rate index exists and it contains client name, then SPOT price must exist and will be updated
        if short_name in rate_index.Name():
            spot_price = None
            for price in rate_index.Prices():
                if price.Market().Name() == "SPOT":
                    spot_price = price
            if spot_price:
                LOGGER.info("Updating SPOT price for rate index {}".format(rate_index_name))
                p_clone = spot_price.Clone()
                p_clone.Bid(bid)
                p_clone.Ask(ask)
                p_clone.Day(acm.Time.DateToday())
                spot_price.Apply(p_clone)
                spot_price.Commit()
            else:
                msg = "Rate index exists, but could not find SPOT price"
                LOGGER.error(msg)
                raise RuntimeError(msg)
        return rate_index

    LOGGER.info("Creating rate index (and SPOT price) {}".format(rate_index_name))
    rate_index = acm.FRateIndex()
    rate_index.Name(rate_index_name)
    if product_type in (GOVIBONDS, CORPBONDS):
        rate_index.Underlying(acm.FRateIndex['ZAR-CFD-ZERO'])
    else:
        rate_index.Underlying(acm.FRateIndex['ZAR-CFD-SABOR'])
    rate_index.Currency('ZAR')

    leg = rate_index.CreateLeg(1)
    leg.StartPeriod('0d')
    leg.EndPeriod('1y')
    leg.Currency('ZAR')
    leg.PayCalendar('ZAR Johannesburg')
    leg.ResetCalendar('ZAR Johannesburg')
    rate_index.Commit()

    price = acm.FPrice()
    price.Bid(bid)
    price.Ask(ask)
    price.Currency('ZAR')
    price.Day(acm.Time.DateToday())
    price.Market('SPOT')
    price.Instrument(rate_index)
    price.Commit()

    return rate_index


def create_pswap(pswap_name, client_name, start_date, product_type,
                 fully_funded, cfd_number=None):
    if product_type == CFD and cfd_number is not None:
        stock_portfolio = acm.FPhysicalPortfolio[str(cfd_number)]
    else:
        stock_portfolio = get_portfolio_name(product_type,
                                             client_name,
                                             cr=True,
                                             fullyfunded=fully_funded)
        stock_portfolio = acm.FPhysicalPortfolio[stock_portfolio]
    LOGGER.info("Stock portfolio = {}".format(stock_portfolio.Name()))

    pswap = acm.FPortfolioSwap()
    pswap.Name(pswap_name)
    if product_type == CFD:
        valgroup = acm.FChoiceList.Select01("list='ValGroup' AND name='EQ_SAFEX'", None)
    else:
        valgroup = acm.FChoiceList.Select01("list='ValGroup' AND name='EQ_SAFEX_PB'", None)
    pswap.ValuationGrpChlItem(valgroup)
    pswap.FundPortfolio(stock_portfolio)
    pswap.StartDate(start_date)
    pswap.OpenEnd('Open End')
    pswap.NoticePeriod('50y')

    pswap.Commit()

    return pswap


def convert_from_ael_date(date_in_ael, date_format):
    try:
        (sd_year, sd_month, sd_day) = date_in_ael.to_ymd()
        sd_datetime = datetime(year=sd_year, month=sd_month, day=sd_day)
        return sd_datetime.strftime(date_format)
    except:
        msg = "Could not convert ael date!"
        LOGGER.exception(msg)
        raise RuntimeError(msg)


def update_pswap_add_infos(pswap_name, rate_index_name, start_date,
                           short_premium, fully_funded, product_type):
    create_or_update_add_info(pswap_name, 'PSONPremIndex', acm.FInstrument[rate_index_name])
    create_or_update_add_info(pswap_name, 'PSSweepBaseDay',
                              convert_from_ael_date(start_date, "%Y-%m-%d"))
    create_or_update_add_info(pswap_name, 'PSSweepFreq', '1')
    create_or_update_add_info(pswap_name, 'PSShortPremiumType', 'Fixed')
    create_or_update_add_info(pswap_name, 'PSShortPremRate', '%f' % short_premium, True)
    create_or_update_add_info(pswap_name, 'PB_PS_Fully_Funded', fully_funded)
    create_or_update_add_info(pswap_name, 'PB_Sweeping_Class', product_type.sweeping_class)


def create_or_update_add_info(pswap_name, ai_spec, ai_new_value, update = False):
    # Only update if explicitly requested
    pswap_oid = acm.FPortfolioSwap[pswap_name].Oid()
    add_infos = acm.FAdditionalInfo.Select("recaddr = %i" % pswap_oid)
    for ai in add_infos:
        if ai.AddInf().Name() == ai_spec:
            if update:
                ai.FieldValue(ai_new_value)
                ai.Commit()
            return
    ai = acm.FAdditionalInfo()
    ai.Recaddr(pswap_oid)
    ai.AddInf(acm.FAdditionalInfoSpec[ai_spec])
    ai.FieldValue(ai_new_value)
    ai.Commit()


def setup_pswaps(config, product_type):
    if config["dryRun"]:
        return
    pswap_names = {}
    if product_type.financed:
        ff_flag = False
        name = get_pswap_name(product_type,
                              config['shortName'],
                              ff_flag)
        pswap_names[name] = ff_flag
    if product_type.fullyfunded:
        ff_flag = True
        name = get_pswap_name(product_type,
                              config['shortName'],
                              ff_flag)
        pswap_names[name] = ff_flag
    if product_type.risk:
        ff_flag = False
        name = get_pswap_name(product_type,
                              config['shortName'],
                              ff_flag)
        pswap_names[name] = ff_flag
    for name, ff_flag in pswap_names.items():
        # Create the rate index first - it is needed for the addinfo
        # Doesn't work in the same transaction as the pswap
        acm.BeginTransaction()
        try:
            # Safex and yieldx don't have the rates specified.
            bid = config.get('%s_bid_rate' % product_type.key)
            ask = config.get('%s_ask_rate' % product_type.key)
            rate_index = get_or_create_rate_index(product_type,
                                                  config['shortName'],
                                                  ff_flag,
                                                  bid,
                                                  ask)
            rate_index_name = rate_index.Name()
            LOGGER.info('Rate index for pswap {}: {}'.format(name, rate_index_name))
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            LOGGER.exception("Could not create rate index for pswap {}".format(name))
            raise e
        
        if not acm.FPortfolioSwap[name]:
            acm.BeginTransaction()
            try:
                LOGGER.info('Creating Portfolio Swap: {}'.format(name))
                pswap_args = [
                    name,
                    config['shortName'],
                    config['startDate'],
                    product_type,
                    ff_flag,
                    config['cfdAccount'] if product_type == CFD else None
                ]
                pswap = create_pswap(*pswap_args)
            
                LOGGER.info('Creating engineering trade.')
                add_engineering_trade(pswap,
                                      product_type,
                                      config['shortName'],
                                      config['counterparty'])
            
                acm.CommitTransaction()
            except Exception as e:
                acm.AbortTransaction()
                LOGGER.exception('Could not create pswap {}'.format(name))
                raise e

        acm.BeginTransaction()
        try:
            premium = config['%s_premium' % product_type.key] if not ff_flag else 0.0
            update_pswap_add_infos(name, rate_index_name, config['startDate'],
                                   premium, ff_flag, product_type)
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise e
