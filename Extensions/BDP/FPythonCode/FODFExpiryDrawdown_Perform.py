""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_odf_drawdown/etc/FODFExpiryDrawdown_Perform.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FODFExpiryDrawdown_Perform- Script for ODF Expiry at EOD.
                        Process Drawdown of remaining amount.

DESCRIPTION
    This module will process ODF Drawdown of remaining amount by
    generating an FX trade.

ENDDESCRIPTION
----------------------------------------------------------------------------"""


#Import Front modules
import ael
import acm
import FBDPCommon
import FBDPRollback
from FBDPCurrentContext import Summary
from FBDPCurrentContext import Logme
import importlib


def perform_expiry_drawdown(args):
    e = ODFExpiryDrawdown('ODF Expiry Drawdown', args['Testmode'], args)
    e.perform()
    e.end()


class ODFExpiryDrawdown(FBDPRollback.RollbackWrapper):

    def readArguments(self):
        self.cpairl = self.ael_variables_dict['ODFcurrpair']
        self.sldtenum = self.ael_variables_dict['ODFlastperiodenum']
        self.explicitldt = self.ael_variables_dict['ODFlastdate']
        status = self.ael_variables_dict['ODFDrawdownstatus']
        if status == 'FOConfirmed':  # presentation layer vs.
            status = 'FO Confirmed'  # enum lookup has blank
        self.drawdown_status = status
        self.tradel = self.ael_variables_dict['trades']

    def validateODF(self):
        if self.drawdown_status == None:
            Logme()('Missing mandatory field drawdown status.', 'ERROR')
            return False
        if self.sldtenum == 'Explicit last date':
            if self.explicitldt == 'None':
                Logme()('Explicit last date, missing last date entry.',
                        'ERROR')
                return False
        return True

    def perform(self):
        Logme()('ODFExpiryDrawdown', 'INFO')
        # read given arguments
        self.readArguments()

        if not self.validateODF():
            Logme()('Errors, cannot perform ODF Drawdown', 'ERROR')
            return

        # Populate instrument dictionary with trade
        positions = self.odfdrawdown_lastdate_select_filter()

        for (ins, trade) in positions.items():
            self.adjustPosition_ODF(ins, trade.Oid())

        ael.poll()

    def adjustPosition_ODF(self, ins, trdnbr):
        Logme()('- ' * 23, 'DEBUG')
        Logme()('Processing %s' % ins.Name(), 'DEBUG')

        ftrd = acm.FTrade[trdnbr]
        try:
            remaining_amt_odf = ftrd.RemainingDrawdownAmount()
        except Exception, exp:
            Logme()('Exception: "%s".' % str(exp))
            print FBDPCommon.get_exception()
            Summary().fail(Summary().POSITION, Summary().action,
                    'Failed in adjustPosition_ODF()', ins.Name())
            return
        if remaining_amt_odf == 0.00:
            Summary().ignore(Summary().POSITION, Summary().action,
                    'Zero position', ins.Name())
            return

        # Drawdown an ODF position at expiry.
        # The ending price is from the final window.
        acmTrade = acm.FTrade[trdnbr]
        odfIns = acm.FOdf[ins.Oid()]

        if odfIns == None:
            msg = "Instrument %s is not of type FXOptionDatedFwd" % ins.Name()
            Summary().fail(Summary().POSITION, Summary().action, msg,
                    ins.Name())
            return
        array = acm.FArray()  # Will be two trades returned.
        ldrawdt = odfIns.LastDrawdownDate()
        en_drawdown_status = ael.enum_from_string('TradeStatus',
                self.drawdown_status)
        ret = acmTrade.PerformDrawdown(ldrawdt, remaining_amt_odf,
                en_drawdown_status, array)
        if len(array) != 2:
            msg = ('Bad return values from code PerformDrawdown %s, %s .' %
                    (ret, array))
            Logme()(msg, 'ERROR')
            Summary().fail(Summary().POSITION, Summary().action, msg,
                    ins.Name())
            return

        try:
            self.abortTransaction()
        except Exception:
            pass
        self.beginTransaction()
        for acmTrd in array:
            try:
                trd = ael.Trade[acmTrd.Oid()]
                # offsetting trade. Not on drawdown trade
                if acmTrd == array[1]:
                    trd.type = 'Closing'
                self.logSaveTrade(trd)
                trd.premium = FBDPCommon.calculate_premium(trd)
                # Prevent commit error when trade time is after value day
                valueTime = trd.value_day.to_time()
                if trd.time > valueTime:
                    trd.time = valueTime
                rc = self.add_trade(trd)
                if rc != None:  # 'Error'. Or Exception, Two error modes.
                    Logme()('Bad return code from add_trade %s .' % (rc),
                            'ERROR')
                    raise Exception
            except Exception:
                self.abortTransaction()
                msg = 'Failed during add of PerformDrawdown trade.'
                Summary().fail(Summary().POSITION, Summary().action, msg,
                        ins.Name())
                return
        try:
            self.commitTransaction()
        except Exception, ex:
            Logme()('Commit exception: %s' % str(ex), 'ERROR')
            msg = 'Failed during commit of PerformDrawdown trades'
            Summary().fail(Summary().POSITION, Summary().action, msg,
                    ins.Name())
            return
        Summary().ok(Summary().POSITION, Summary().CLOSE)

    def odfdrawdown_lastdate_select_filter(self):
        param_helper = Param_Helper('0')  # get accounting_currency
        tod = ael.date_today()
        tom = tod.add_banking_day(param_helper.accounting_currency, 1)
        if self.tradel == None:
            return
        insAndTradeDic = {}
        insDic = {}
        for trdi in self.tradel:
            trd = acm.FTrade[trdi.Name()]
            trdnbr = trd.Oid()
            if trd.Status() in ['Simulated', 'Void']:
                Logme()(('ODF Trade %s is a %s trade, and cannot be used for '
                        'drawdown') % (trdnbr, trd.Status()), 'WARNING')
                continue
            ins = acm.FInstrument[trd.Instrument().Oid()]
            if ins in insDic:
                continue
            insDic[ins] = ins
            if ins.InsType() != 'FXOptionDatedFwd':
                Logme()(('Skip position, other instr:     "%s, %s".' %
                        (trdnbr, ins.Name())), 'ERROR')
                Summary().fail(Summary().POSITION, Summary().action,
                        'Inst Type is not FX Option Dated Fwd',
                        '[%s]' % (ins.InsType()))
                continue
            if ins.Currency() == None or ins.Underlying() == None:
                Logme()(('Skip position, Instr, Instr Currency or Underlying '
                        'is None:     "%s, %s, %s, %s".') % (trdnbr,
                        ins.Name(), ins.Currency(), ins.Underlying()), 'ERROR')
                Summary().fail(Summary().POSITION, Summary().action,
                        'Inst Currency or Underlying is None', ins.InsType())
                continue
            currpair = ins.Currency().Name() + '/' + ins.Underlying().Name()
            currpair = acm.FCurrencyPair[currpair]
            if currpair == None:
                currpair = (ins.Underlying().Name() + '/' +
                        ins.Currency().Name())
                currpair = acm.FCurrencyPair[currpair]
                if currpair == None:
                    Logme()(('Skip position, Instr. PROBLEM: currpair None; '
                            'Instr Currency, Underlying:     '
                            '"%s, %s, %s, %s".') % (trdnbr, ins.Name(),
                            ins.Currency(), ins.Underlying()), 'ERROR')
                    Summary().fail(Summary().POSITION, Summary().action,
                            'No currency pair', trdi.Name())
                    continue
            if (self.cpairl != None and len(self.cpairl) > 0 and
                    currpair not in self.cpairl):
                Logme()(('Skip position, Instr. currpair not in list:     '
                        '"%s, %s, %s".') % (trdnbr, ins.Name(),
                        currpair.Name()), 'INFO')
                Summary().ignore(Summary().POSITION, Summary().action,
                        'Not in currency pair list', trdi.Name())
                continue
            cpair_spotdate = ael.date(currpair.SpotDate(tod))
            cpair_spotnext = ael.date(currpair.spot_date(tom))

            ldrawdt = ins.LastDrawdownDate()
            if not ldrawdt or len(ldrawdt) < 10:
                Logme()(('ODF Trade %s, ODF Instrument %s does not have a '
                        'valid Last Drawdown Date %s.') % (trdnbr, ins.Name(),
                        ldrawdt), 'ERROR')
                Summary().fail(Summary().POSITION, Summary().action,
                        ('ODF Instrument does not have a valid last Drawdown '
                        'date'), '[%s]' % (ins.Name()))
                continue
            else:
                Logme()(('ODF Trade %s, Value Day %s, ODF Instrument %s, '
                        'Last Drawdown Date %s.') % (trdnbr, trd.ValueDay(),
                        ins.Name(), ldrawdt), 'INFO')

            ckdate = ael.date(ldrawdt[:10])
            if self.sldtenum == 'Today' and ckdate <= tod:
                Logme()('cutoff Today %s.' % (tod))
                insAndTradeDic[ins] = trd
            elif self.sldtenum == 'Tomorrow' and ckdate <= tom:
                Logme()('cutoff Tom %s.' % (tom))
                insAndTradeDic[ins] = trd
            elif self.sldtenum == 'Spot' and ckdate <= cpair_spotdate:
                Logme()('cutoff Curr Pair spot date %s.' % (cpair_spotdate))
                insAndTradeDic[ins] = trd
            elif self.sldtenum == 'Spot next' and ckdate <= cpair_spotnext:
                Logme()('cutoff Curr Pair spot next %s.' % (cpair_spotnext))
                insAndTradeDic[ins] = trd
            elif self.sldtenum == 'Explicit last date':
                xdt = ael.date(self.explicitldt)
                if ckdate <= xdt:
                    Logme()('cutoff Explicit last date %s.' % (
                            self.explicitldt))
                    insAndTradeDic[ins] = trd
                else:
                    Logme()(('Skip position %s, Expiry date %s not <= %s.' %
                            (trdnbr, ckdate, xdt)), 'INFO')
                    Summary().ignore(Summary().POSITION, Summary().action,
                            'Date range', '[%s:%s]' % (xdt, trdnbr))
        return insAndTradeDic

#___end__class__ODFExpiryDrawdown

##______________________________________
## CalcExtract helper, get accounting_currency
import FPLCashFlowColExtract
importlib.reload(FPLCashFlowColExtract)
rptCalcModule = FPLCashFlowColExtract


class Param_Helper:
    def __init__(self, logmode):
        self.logmode = logmode
        self.initAcctgCurrCalcExtract()

    # uses pref context from getPrefDefaultContextName()
    def initAcctgCurrCalcExtract(self):
        rparm = rptCalcModule.ReportParamCS('ODFParm', self.logmode)
        self.accounting_currency = rparm.setAcctgParm_CalcExtract()

#___end__class__Param_Helper
