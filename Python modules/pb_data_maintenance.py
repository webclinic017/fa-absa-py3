'''
Created on 16 Mar 2016

@author: conicova
'''

import acm
import os
from at_log import log
from at_ael_variables import AelVariableHandler
from PS_FormUtils import DateField
from at_report import CSVReportCreator
from at_time import acm_date

from PS_Functions import (get_pb_fund_counterparties,
                          get_pb_fund_shortname,
                          get_pb_reporting_portfolio,
                          get_trades)

from _collections import defaultdict

from at_logging import getLogger, bp_start

LOGGER = getLogger()

VERSION = "1.0"

# set to true to turn on debugging information
DEBUG = False
# generated report only for the specified clients
DEBUG_CLIENTS = ['MROC']  # 'MAP290', 'COGITO', 'NITROGEN', 'ABAXFIT', 'KAISOPT', 'NITROGEN', 'SEFI', 'ARI',
DEBUG_INSTRUMENTS = []  # 'ZAR/IRS/F-JI/130828-180828/7.6800#1'

def calc_value(calc_space, entity, column_name):    
    value = calc_space.CalculateValue(entity, column_name)
        
    if value == None:
        LOGGER.info("Column '%s' returned a None value", column_name)
        value = 0
    if hasattr(value, "Number"):
        value = value.Number() 
    
    return value
    
class ACheck(CSVReportCreator):
    
    def __init__(self, report_date, calc_space_type='FTradeSheet', full_file_path="C:\\tmp\\sett_control\\CHECK\\default.csv"):
        self.full_file_path = full_file_path
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)
        
        super(ACheck, self).__init__(file_name_only,
                                          file_suffix,
                                          file_path)
        self.t0_report_date = report_date
        self.t1_report_date = acm.Time().DateAddDelta(self.t0_report_date, 0, 0, -1)
        self.t2_report_date = acm.Time().DateAddDelta(self.t0_report_date, 0, 0, -2)
        
        context = acm.GetDefaultContext()
        self.calc_space_t0 = acm.Calculations().CreateCalculationSpace(context, calc_space_type)
        self.calc_space_t1 = acm.Calculations().CreateCalculationSpace(context, calc_space_type)
        self.calc_space_t2 = acm.Calculations().CreateCalculationSpace(context, calc_space_type)

        ACheck._setup_calc_space(self.calc_space_t0, self.t0_report_date)
        ACheck._setup_calc_space(self.calc_space_t1, self.t1_report_date)
        ACheck._setup_calc_space(self.calc_space_t2, self.t2_report_date)
        
        self.all_data_rows = []
        LOGGER.info("Report date: %s", report_date)
        
    @staticmethod
    def _setup_calc_space(calc_space, report_date):
        calc_space.Clear()
        calc_space.Refresh()
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', report_date)
    
    def is_trade_alive(self, trade):
        """Returns True if the trade is alive, else returns False"""
        if trade.Status() in ["Void", "Simulated", "Terminated"]:
            return False
        
        return True
    
    def is_instrument_expired(self, ins):
        if ins.ExpiryDate() >= self.t0_report_date:
            return False
        
        return True
    
    def has_live_trades(self, ins):
        
        for t in ins.Trades():
            if self.is_trade_alive(t):
                return True
        
        return False
    
    def get_live_trades(self, ins):
        result = []
        for t in ins.Trades():
            if self.is_trade_alive(t):
                result.append(t)
        
        return result
    
    def ignore_instrument(self, ins):
        
        if self.is_instrument_expired(ins) or not self.has_live_trades(ins):
            return True
        
        return False

    def append_msg(self, data=[]):
        self.all_data_rows.append(data)  
    
    def print_data(self):
        print "-"*40, "DATA", "-"*40
        print ";".join(self.get_header())
        for row in  self.all_data_rows:
            print ";".join(map(lambda i: str(i), row))
    
    def get_header(self):
        return []
    
    def _collect_data(self):
        for row in self.all_data_rows:
            self.content.append(row)
    
    def _header(self):
        return self.get_header()
    
class CheckStalePrice(ACheck):
    
    def __init__(self, report_date, full_file_path):
        super(CheckStalePrice, self).__init__(report_date, "FDealSheet", full_file_path)
          
    def get_header(self):
        return ["Instrument", "Status", "Price T-1", "Price T0", "Live Trades"]
    
    def _instruments_with_stale_prices(self, portfolio=acm.FPhysicalPortfolio['PB_CR_LIVE'], market='SPOT'):
        """Identify all instruments on the specified tree
        which have prices that are the same as the  prior day"""
        all_portfolios = portfolio.AllPhysicalPortfolios()
        instruments = []
        for p in all_portfolios:
            instruments.extend(p.Instruments())
        
        instruments = set(instruments)
        LOGGER.info("Checking the prices for %s instruments", len(instruments))
        ignore_instruments = 0
        ok_instruments = 0
        for ins in instruments:
            if DEBUG and ins.Name() not in DEBUG_INSTRUMENTS:
                continue 
            if self.ignore_instrument(ins):
                ignore_instruments += 1
                continue
            
            price_t0 = calc_value(self.calc_space_t0, ins, "Portfolio Profit Loss Price End Date")
            price_t1 = calc_value(self.calc_space_t1, ins, "Portfolio Profit Loss Price End Date")
            
            live_trades = len(self.get_live_trades(ins))
            if price_t0 == price_t1:
                LOGGER.warning("Instrument '%s' on '%s' has the same price '%s' as on '%s'",
                               ins.Name(), self.t0_report_date, price_t0, self.t1_report_date)
                self.append_msg([ins.Name(), 'Warning', price_t1, price_t0, live_trades])
            else:
                LOGGER.info("Instrument '%s', price t0: '%s', t1: '%s'", ins.Name(), price_t0, price_t1)
                self.append_msg([ins.Name(), 'Info', price_t1, price_t0, live_trades])
                ok_instruments += 1
        
        LOGGER.info("Ignored %s instruments, which are expired or with no live trades.", ignore_instruments)
        LOGGER.info("%s ok instruments.", ok_instruments)
    
    def _trades_with_suspicious_prices(self, portfolio=acm.FPhysicalPortfolio['PB_CR_LIVE']):
        all_portfolios = portfolio.AllPhysicalPortfolios()
        trades = []
        for p in all_portfolios:
            trades.extend(p.Trades())
            
        LOGGER.info("Checking the prices for %s trades", len(trades))
        dead_trades = 0
        ok_trade = 0
        for t in trades:
            warning = False;
            if not self.is_trade_alive(t):
                dead_trades += 1
                continue
            
            if t.Price() == None or t.Price() == 0:
                LOGGER.warning("Trade '%s' has a suspicious price '%s'", t.Oid(), t.Price())
                self.append_msg([t.Oid(), t.Price()])
                warning = True
            
            price_t0 = calc_value(self.calc_space_t0, t, "Trade Price")
            price_t1 = calc_value(self.calc_space_t1, t, "Trade Price")
            
            if price_t0 == price_t1:
                LOGGER.warning("Trade '%s' on '%s' has the same price '%s' as on '%s'",
                               t.Oid(), self.t0_report_date, price_t0, self.t1_report_date)
                self.append_msg([t.Oid(), self.t0_report_date, price_t0, self.t1_report_date])
                warning = True
            
            if not warning:
                ok_trade += 1
        
        LOGGER.info("Ignored %s not live trades.", dead_trades)
        LOGGER.info("%s ok trades.", ok_trade)
        
    def run(self):
        self._instruments_with_stale_prices(acm.FPhysicalPortfolio['PB_CR_LIVE'])
        # self._trades_with_suspicious_prices(acm.FPhysicalPortfolio['PB_CR_LIVE'])
        
class CheckNAV(ACheck):
    
    def __init__(self, report_date, threshold, full_file_path):
        super(CheckNAV, self).__init__(report_date, "FPortfolioSheet", full_file_path)
        
        self.threshold = threshold
    
    def get_header(self):
        return ["Client", "Status", "NAV Fair Value T0", "NAV Fair Value T1", "NAV Change", "NAV Change %"]
    
    def run(self):
        cps = get_pb_fund_counterparties()
        for cp in cps:
            short_name = get_pb_fund_shortname(cp)
            if DEBUG and short_name not in DEBUG_CLIENTS:
                continue
            try:
                nav_t0, nav_t1, nav_change, nav_pr_change = self._get_nav(cp)
                msg = "NAV for '{0}' has change by '{1:.5f}%'".format(cp.Name(), nav_pr_change * 100.0)
                if abs(nav_pr_change) >= self.threshold: 
                    LOGGER.warning(msg)
                    self.append_msg([short_name, "Warning", nav_t0, nav_t1, nav_change, nav_pr_change * 100])
                else:
                    LOGGER.info(msg)
                    self.append_msg([short_name, 'Info', nav_t0, nav_t1, nav_change, nav_pr_change * 100])
            except Exception:
                LOGGER.exception("Client '%s'", short_name)
    
    def _get_portfolio_references(self, cp):
        result = []
        margin_pf = "PB_CALL_MARGIN_{0}".format(get_pb_fund_shortname(cp))
        callaccnt_pf = "PB_CALLACCNT_{0}".format(get_pb_fund_shortname(cp))
        
        if acm.FPhysicalPortfolio[margin_pf]:
            result.append(acm.FPhysicalPortfolio[margin_pf])
        if acm.FPhysicalPortfolio[callaccnt_pf]:
            result.append(acm.FPhysicalPortfolio[callaccnt_pf])
        
        return result 
    
    def _get_ff_trades(self, cp):
        result = []
        
        pf = get_pb_reporting_portfolio(cp)  # PB_client_CR
        print pf.Name()
        if not pf:
            raise Exception("Could not find the portfolio for counterparty '{0}'".format(cp.Name()))
        
        pfs = filter(lambda p: "_FF_" in p.Name(), pf.AllPhysicalPortfolios())

        for p in pfs:
            for t in p.Trades():
                if self.is_trade_alive(t):
                    result.append(t)
        
        return result
    
    def _get_nav(self, cp):  
        pfs = self._get_portfolio_references(cp)        
        ps_nav_t0 = ps_nav_t1 = 0
        for pf in pfs:
            ps_nav_t0 += calc_value(self.calc_space_t0, pf, "PS Fair Value NAV")
            ps_nav_t1 += calc_value(self.calc_space_t1, pf, "PS Fair Value NAV")
        
        nav_pr_change = 1
        if ps_nav_t1 != 0:
            nav_pr_change = (ps_nav_t0 - ps_nav_t1) / ps_nav_t1
        else:
            if ps_nav_t1 == ps_nav_t0:
                nav_pr_change = 0
        
        return (ps_nav_t0, ps_nav_t1, ps_nav_t0 - ps_nav_t1, nav_pr_change)

class CheckShortEndProvision(ACheck):
    
    def __init__(self, report_date, full_file_path):
        super(CheckShortEndProvision, self).__init__(report_date, "FPortfolioSheet", full_file_path)
    
    def get_header(self):
        return ['Client', 'Instrument', 'Trade', 'Provision T-1', 'Provision T-2', 'Provision Movement']
            
    def run(self):
        cps = get_pb_fund_counterparties()
        for cp in cps:
            if DEBUG and get_pb_fund_shortname(cp) not in DEBUG_CLIENTS:
                continue
            try:
                self._get_short_end_provision(cp)
            except Exception:
                LOGGER.exception("Client '%s'", cp.Name())
    
    def _get_trades(self, cp):
        result = []
        
        pf = get_pb_reporting_portfolio(cp)  # PB_client_CR
        if not pf:
            raise Exception("Could not find the portfolio for counterparty '{0}'".format(cp.Name()))
        
        pfs = filter(lambda p: "_IRS_" in p.Name() or "_FRA_" in p.Name(), pf.AllPhysicalPortfolios())

        for p in pfs:
            for t in p.Trades():
                if self.is_trade_alive(t):
                    result.append(t)
        
        return result
    
    def _get_short_end_provision(self, cp):
        trades = self._get_trades(cp)
        LOGGER.info("Got %s IRS and FRA trades. Client: '%s'", len(trades), cp.Name())
        
        daily_provision_t1 = daily_provision_t2 = 0
        for t in trades:
            daily_provision_t1 = calc_value(self.calc_space_t1, t, "Daily Provision")
            daily_provision_t2 = calc_value(self.calc_space_t2, t, "Daily Provision") 
            LOGGER.info("%s, %s, %s, %s, %s, %s",
                        cp.Name(), t.Instrument().Name(), t.Oid(),
                        daily_provision_t1, daily_provision_t2, daily_provision_t2 - daily_provision_t1)
            self.append_msg([cp.Name(),
                             t.Instrument().Name(),
                             t.Oid(),
                             daily_provision_t1,
                             daily_provision_t2,
                             daily_provision_t2 - daily_provision_t1])

class CheckOnOffTreePosition(ACheck):
    
    _asql_template = """ 
    SELECT 
        t.trdnbr 
    FROM 
        trade t,
        instrument i,
        portfolio p
    WHERE
        i.insaddr=t.insaddr
    and t.prfnbr=p.prfnbr
    and t.status not in ('Simulated', 'Void', 'Terminated')
    and i.insid='{0}'
    and p.prfid='{1}'
    """
    
    TO_CHECK = ['FRA', 'IRS', 'repobond', 'govibond', 'corpbond']
    def __init__(self, report_date, full_file_path):
        super(CheckOnOffTreePosition, self).__init__(report_date, "FPortfolioSheet", full_file_path)
    
    def get_header(self):
        return ["Client", "Status", "Instrument", "Instrument CR", "Instrument PSWAP", "Portfolio", "Portfolio CR", "Position End", "Position End CR", "Position Pswap", "Trades", "Trades CR"]
        
    def run(self):
        cps = get_pb_fund_counterparties()
        for cp in cps:
            if DEBUG and get_pb_fund_shortname(cp) not in DEBUG_CLIENTS:
                continue
            try:
                self._check(cp)
                self._check2(cp)
            except Exception:
                LOGGER.exception("Client '%s'", cp.Name())
    
    def _get_cfd_cr_portfolio(self, cp):
        
        pf = get_pb_reporting_portfolio(cp)
        print pf.Name()
        if not pf:
            raise Exception("Could not find the portfolio for counterparty '{0}'".format(cp.Name()))
        
        return filter(lambda p: "PB_CFD_" in p.Name() and p.Name().endswith("_CR"), pf.AllPhysicalPortfolios())
        
    def _get_cfd_trades(self, cp):
        
        result = []
        pf = acm.FPhysicalPortfolio["PB_RISK_FV_{0}".format(get_pb_fund_shortname(cp))]

        if not pf:
            raise Exception("Could not find the portfolio for counterparty '{0}'".format(cp.Name()))
        
        pfs = filter(lambda p: "PB_CFD_" in p.Name() and not p.Name().endswith("_CR"), pf.AllPhysicalPortfolios())
        
        for pf in pfs:
            for t in pf.Trades():
                if self.is_trade_alive(t) and t.Instrument().InsType() in ["Portfolio Swap"]:
                    result.append(t)
        
        return result
    
    def _get_pf_pair(self, cp):
        result = []
        pf = get_pb_reporting_portfolio(cp)
        # print pf.Name()
        for p_cr in pf.AllPhysicalPortfolios():
            if p_cr.AdditionalInfo().PS_PortfolioType() != "CFD":
                continue
            pswap = p_cr.AdditionalInfo().PS_FundingIns()
            if not pswap:
                LOGGER.error("Portfolio '%s' is missing the PS_FundingIns additional info.", p_cr.Name())
            else:
                if not hasattr(pswap, "FundPortfolio"):
                    LOGGER.error("There is something wrong with the portfolio '%s' PS_FundingIns '%s'.", p_cr.Name(), pswap.Name())
                if len(pswap.Trades()) == 0:
                    LOGGER.warning("Portfolio SWAP '%s' has no trades.", pswap.Name())
                else:
                    result.append((p_cr, pswap.FundPortfolio()))
            
        return result    
   
    def _get_pf_pair2(self, cp):
        result = []
        pf_cr = get_pb_reporting_portfolio(cp)
        for p_cr in pf_cr.AllPhysicalPortfolios():
            pf = None
            p_name = p_cr.Name()[0:-3]
            for pf_type in CheckOnOffTreePosition.TO_CHECK:
                if pf_type in p_cr.Name():
                    pf = acm.FPhysicalPortfolio[p_name]
                    if pf:
                        result.append((p_cr, pf)) 
                    else:
                        LOGGER.error("There is something wrong with the portfolio '%s'. '%s' not found.", p_cr.Name(), p_name)    
                       
        return result
                
    def _check(self, cp):
        pf_pairs = self._get_pf_pair(cp)
        
        for (pf_cr, pf) in pf_pairs:
            inss_pf_cr = pf_cr.Instruments()
            inss_pf = pf.Instruments()
            ins_pswap = pf.AdditionalInfo().PS_FundingIns()
            
            pswap_values = self._get_values_from_mtm_legs(ins_pswap.Trades()[0], 'Portfolio Profit Loss Period Position')  # Position
            trades_pf = pf.Trades()
            trades_pf_cr = pf_cr.Trades()
            LOGGER.info("%s (Instruments: %s)(Trades: %s)->%s (Instruments: %s)(Trades: %s)",
                        pf.Name(), len(inss_pf), len(trades_pf),
                        pf_cr.Name(), len(inss_pf_cr), len(trades_pf_cr))
            for ins_pf in inss_pf:
                if ins_pf.InsType() not in ['Stock']:
                    if not ins_pf.Name().startswith("PROFIT_REMIT"):
                        LOGGER.error("Ignoring instrument: '%s' of unexpected type '%s'",
                                     ins_pf.Name(), ins_pf.InsType())
                        self.append_msg([cp.Name(), "Error: ins type {0}".format(ins_pf.InsType()), ins_pf.Name(), "", "", pf.Name(), pf_cr.Name(),
                                        '', '', '', '', '' ])
                    continue

                ins_pf_cr_name = ins_pf.Name() + "/CFD"
                ins_pf_cr = filter(lambda i: ins_pf_cr_name == i.Name(), inss_pf_cr)
                if not ins_pf_cr:
                    LOGGER.warning("Instrument '%s' missing in the off tree portfolio '%s'",
                                   ins_pf.Name(), pf_cr.Name())
                    trades = filter(lambda t: self.is_trade_alive(t), ins_pf.Trades())
                    self.append_msg([cp.Name(), "Warning", ins_pf.Name(), 'NOT FOUND {0}'.format(ins_pf_cr), ins_pswap, pf.Name(), pf_cr.Name(),
                                      '', '', '', len(trades), ''])
                    continue
#                 if len(ins_pf_cr) != 0:
#                     raise Exception("Unexpected number of instruments {0}".format(ins_pf_cr_name))
                ins_pf_cr = ins_pf_cr[0]
                
                pos_end = pos_end_cr = 0

                pos_end = calc_value(self.calc_space_t0, self._get_asql_query(ins_pf, pf), "Portfolio Profit Loss Position End")  # Position End
                pos_end_cr = calc_value(self.calc_space_t0, self._get_asql_query(ins_pf_cr, pf_cr), "Portfolio Profit Loss Position End")
                pos_end_pswap = ''
                ins_pswap = ''
                if ins_pf.Name() in pswap_values.keys():
                    pos_end_pswap = pswap_values[ins_pf.Name()]
                    ins_pswap = ins_pf.Name()
                    
                if pos_end != pos_end_cr or (pos_end_pswap != '' and pos_end_pswap != pos_end):
                    trades = filter(lambda t: self.is_trade_alive(t), ins_pf.Trades())
                    trades_cr = filter(lambda t: self.is_trade_alive(t), ins_pf_cr.Trades())
                    LOGGER.warning("%s: (Position end:) %s != %s, (Nr Trades:) (%s vs %s)",
                                   ins_pf.Name(), pos_end, pos_end_cr,
                                   len(trades), len(trades_cr))
                    self.append_msg([cp.Name(), "Warning", ins_pf.Name(), ins_pf_cr.Name(), ins_pswap, pf.Name(), pf_cr.Name(),
                                     pos_end, pos_end_cr, pos_end_pswap, len(trades), len(trades_cr)])
                else:
                    LOGGER.info("%s: (Position end:) %s == %s", ins_pf.Name(), pos_end, pos_end_cr)
                    self.append_msg([cp.Name(), "Info", ins_pf.Name(), ins_pf_cr.Name(), ins_pswap, pf.Name(), pf_cr.Name(),
                                     pos_end, pos_end_cr, pos_end_pswap, '', ''])
                    
    def _check2(self, cp):
        pf_pairs = self._get_pf_pair2(cp)
        
        for (pf_cr, pf) in pf_pairs:
            inss_pf_cr = pf_cr.Instruments()
            inss_pf = pf.Instruments()
            
            trades_pf = pf.Trades()
            trades_pf_cr = pf_cr.Trades()
            LOGGER.info("%s (Instruments: %s)(Trades: %s)->%s (Instruments: %s)(Trades: %s)",
                        pf.Name(), len(trades_pf), len(inss_pf),
                        pf_cr.Name(), len(inss_pf_cr), len(trades_pf_cr))
            for ins_pf in inss_pf:
                if DEBUG and ins_pf.Name() not in DEBUG_INSTRUMENTS:
                    continue
                if ins_pf.Name().startswith("PROFIT_REMIT"):
                    continue
                if self.ignore_instrument(ins_pf):
                    LOGGER.info("Ignoring instrument: '%s'.", ins_pf.Name())
                    continue
                # Check if the counterparty is a PB client (the same client)
                trades = filter(lambda t: self.is_trade_alive(t) and t.Counterparty() == cp, ins_pf.Trades())
                if len(trades) == 0:
                    LOGGER.info("Ignoring instrument: '%s'. No trades with a PB client counterparty.", ins_pf.Name())
                    continue
                    
                pos_end_pswap = ''
                ins_pswap = ''
                
                ins_pf_cr = filter(lambda i: ins_pf.Name() == i.Name(), inss_pf_cr)
                if not ins_pf_cr:
                    LOGGER.warning("Instrument '%s' missing in the off tree portfolio '%s'", ins_pf.Name(), pf_cr.Name())
                    self.append_msg([cp.Name(), "Warning", ins_pf.Name(), 'NOT FOUND {0}'.format(ins_pf_cr), ins_pswap, pf.Name(), pf_cr.Name(),
                                     '', '', pos_end_pswap, len(trades), ''])
                    continue
                ins_pf_cr = ins_pf_cr[0]
                
                pos_end = pos_end_cr = 0

                pos_end = calc_value(self.calc_space_t0, self._get_asql_query(ins_pf, pf, cp), "Portfolio Profit Loss Position End")  # Position End
                pos_end_cr = calc_value(self.calc_space_t0, self._get_asql_query(ins_pf_cr, pf_cr, None), "Portfolio Profit Loss Position End")
                
                    
                if pos_end + pos_end_cr != 0:
                    trades = filter(lambda t: self.is_trade_alive(t) and t.Counterparty() == cp, ins_pf.Trades())
                    trades_cr = filter(lambda t: self.is_trade_alive(t) and t.Counterparty() == cp, ins_pf_cr.Trades())
                    LOGGER.warning("%s: %s != %s, (%s vs %s)",
                                   ins_pf.Name(), pos_end, pos_end_cr,
                                   len(trades), len(trades_cr))
                    self.append_msg([cp.Name(), "Warning", ins_pf.Name(), ins_pf_cr.Name(), ins_pswap, pf.Name(), pf_cr.Name(),
                                     pos_end, pos_end_cr, pos_end_pswap, len(trades), len(trades_cr)])
                else:
                    LOGGER.info("%s: %s == %s", ins_pf.Name(), pos_end, pos_end_cr)
                    self.append_msg([cp.Name(), "Info", ins_pf.Name(), ins_pf_cr.Name(), ins_pswap, pf.Name(), pf_cr.Name(),
                                     pos_end, pos_end_cr, pos_end_pswap, '', ''])
                    
    def _get_asql_query(self, instrument, portfolio, cp=None):
        query = acm.CreateFASQLQuery('FTrade', 'AND')
        query.AddAttrNode('Portfolio.Name', 'EQUAL', portfolio.Name())
        query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Simulated'))
        query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Void'))
        query.AddAttrNode('Status', 'NOT_EQUAL', acm.EnumFromString('TradeStatus', 'Terminated'))
        query.AddAttrNode('Instrument.Name', 'EQUAL', instrument.Name())
        if cp:
            query.AddAttrNode('Counterparty.Name', 'EQUAL', cp.Name())
        return query
    
    def _get_values_from_mtm_legs(self, entity, column_name):
        acm.FACMServer().GetUserPreferences().ShowLegsInSheet(True)
        calc_space = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', self.t1_report_date)
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom')
        calc_space.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', self.t0_report_date)
        
        top_node = calc_space.InsertItem(entity)
        calc_space.Refresh()
        # top_node = calc_space.RowTreeIterator().FirstChild()
        ins_node = top_node.Iterator().FirstChild()
        ins_node.Tree().Expand(True)
        leg_node = ins_node.Clone().FirstChild()
        result = {}
        while leg_node:
            leg_desc = calc_space.CalculateValue(leg_node.Tree(), "Leg Description")
            if leg_desc == "Mtm":
                index_ref = calc_space.CalculateValue(leg_node.Tree(), "Leg Index Ref").Value().Name()
                value = calc_space.CalculateValue(leg_node.Tree(), column_name)
                if value == None:
                    value = 0
                if hasattr(value, "Number"):
                    value = value.Number() 
                result[index_ref] = value
            leg_node = leg_node.NextSibling()
        
        return result

class CheckExternalId(ACheck):
    
    def __init__(self, report_date, full_file_path):
        super(CheckExternalId, self).__init__(report_date, "FPortfolioSheet", full_file_path)
        self.min_expiry_date = acm.Time().DateAddDelta(self.t0_report_date, 0, 0, -30)
    
    def get_header(self):
        return ['Client', 'Status', 'Portfolio', 'Instrument', 'Trade', 'External Id', 'Expiry date', 'Trades']
            
    def run(self):
        cps = get_pb_fund_counterparties()
        for cp in cps:
            if DEBUG and get_pb_fund_shortname(cp) not in DEBUG_CLIENTS:
                continue
            try:
                self._check_external_id(cp)
            except Exception:
                LOGGER.exception("Client '%s'", cp.Name())
        
        LOGGER.info("Min expiry date")        
        self.append_msg(["Min expiry date", self.min_expiry_date, '', '', '', '', ''])
    
    def _check_external_id(self, cp):
        portfolio = get_pb_reporting_portfolio(cp)
        trades_checked = 0
        safex_trades = get_trades("SAFEX exchange", portfolio.Name())
        for trade in safex_trades:
            trades_checked += 1
            if not self._is_trade_valid(trade):
                LOGGER.warning("Missing the external Id for trade %s", trade.Oid())
                self.append_msg([cp.Name(), 'Warning', portfolio.Name(), trade.Instrument().Name(),
                                 trade.Oid(), trade.OptionalKey(),
                                 trade.Instrument().ExpiryDate(), 1])
        yieldx_trades = get_trades("YieldX exchange", portfolio.Name())
        for trade in yieldx_trades:
            trades_checked += 1
            if not self._is_trade_valid(trade):
                LOGGER.warning("Missing the external Id for trade %s", trade.Oid())
                self.append_msg([cp.Name(), 'Warning', portfolio.Name(), trade.Instrument().Name(),
                                 trade.Oid(), trade.OptionalKey(),
                                 trade.Instrument().ExpiryDate(), 1])

        LOGGER.info("Finished processing the portfolio %s (%s trades)", portfolio.Name(), trades_checked)
        self.append_msg([cp.Name(), 'Info', portfolio.Name(), '', '', '', '', trades_checked])
        
    def _is_trade_valid(self, trade):
        """ Return true if the trade is ok. """
        if trade.OptionalKey() != '':
            return True
        if trade.Instrument().ExpiryDate() < self.min_expiry_date:
            return True
        
        return False

START_DATES = DateField.get_captions([
    'Inception',
    'First Of Year',
    'First Of Month',
    'Last of Previous Month',
    'TwoBusinessDaysAgo',
    'PrevBusDay',
    'Now',
    'Custom Date'])

def custom_start_date_hook(selected_variable):
    """Enable/Disable Custom Start Date base on Start Date value."""
    start_date = ael_variables.get('start_date')
    start_date_custom = ael_variables.get('start_date_custom')

    if start_date.value == 'Custom Date':
        start_date_custom.enabled = True
    else:
        start_date_custom.enabled = False


ael_variables = AelVariableHandler()
ael_variables.add('start_date',
                  label='Date',
                  default='Now',
                  collection=START_DATES,
                  alt='Start date',
                  hook=custom_start_date_hook)

ael_variables.add('start_date_custom',
                  label='Start Date Custom',
                  default=DateField.read_date('Now'),
                  alt='Custom start date',
                  enabled=False)

ael_variables.add_bool(
    "check_stale_prices",
    label="Stale Prices",
    default=False)
ael_variables.add("stale_price_report_filename",
                  label="Stale Price Filename",
                  default="C:\\tmp\\sett_control\\CHECK\\stale_price",
                  mandatory=True) 
ael_variables.add_bool(
    "check_nav_threshold",
    label="NAV Exceeding Threshold",
    default=False)
ael_variables.add("nav_threshold_report_filename",
                  label="NAV Exceeding Threshold Filename",
                  default="C:\\tmp\\sett_control\\CHECK\\nav_threshold",
                  mandatory=True)
ael_variables.add_bool(
    "check_short_end_provision",
    label="Short End Provision",
    default=False)
ael_variables.add("short_end_provision_report_filename",
                  label="Short End Provision Filename",
                  default="C:\\tmp\\sett_control\\CHECK\\short_end_provision",
                  mandatory=True)
ael_variables.add_bool(
    "check_on_off_tree",
    label="On-Off Tree",
    default=False)
ael_variables.add("on_off_tree_report_filename",
                  label="On-Off Tree Filename",
                  default="C:\\tmp\\sett_control\\CHECK\\on_off_tree",
                  mandatory=True)
ael_variables.add_bool(
    "check_external_id",
    label="External Id",
    default=False)
ael_variables.add("external_id_report_filename",
                  label="External Id Filename",
                  default="C:\\tmp\\sett_control\\CHECK\\external_id",
                  mandatory=True)
ael_variables.add("bp_name",
                  label="BP Name",
                  default="check",
                  mandatory=False)

def _run_report(check_obj):
    check_obj.run()
    check_obj.create_report()
    LOGGER.info("Secondary output wrote to %s", check_obj.full_file_path)
    

def ael_main(args):
    
    with bp_start("pb_data_maintenance.{0}".format(args['bp_name'])):
        if args['start_date'] == 'Custom Date':
            start_date = acm_date(args['start_date_custom'])
        else:
            start_date = DateField.read_date(args['start_date'])
            
        if args["check_stale_prices"]:
            report_filename = "{0}_{1}.csv".format(args["stale_price_report_filename"], start_date)
            checkStalePrices = CheckStalePrice(start_date, report_filename)
            _run_report(checkStalePrices)
            
        if args["check_nav_threshold"]:
            report_filename = "{0}_{1}.csv".format(args["nav_threshold_report_filename"], start_date)
            checkNAV = CheckNAV(start_date, 0.03, report_filename)
            _run_report(checkNAV)
        
        if args["check_short_end_provision"]:
            report_filename = "{0}_{1}.csv".format(args["short_end_provision_report_filename"], start_date)
            checkShortEndProvision = CheckShortEndProvision(start_date, report_filename)
            _run_report(checkShortEndProvision)
            
        if args["check_on_off_tree"]:
            report_filename = "{0}_{1}.csv".format(args["on_off_tree_report_filename"], start_date)
            checkOnOffTreePosition = CheckOnOffTreePosition(start_date, report_filename)
            _run_report(checkOnOffTreePosition)
            
        if args["check_external_id"]:
            report_filename = "{0}_{1}.csv".format(args["external_id_report_filename"], start_date)
            checkExternalId = CheckExternalId(start_date, report_filename)
            _run_report(checkExternalId)
