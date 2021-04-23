""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
        FDMPositionUtil- Module with utility classes used by FDMPosition

VERSION
        0.1.2

DESCRIPTION
         This module contains some utility classes used by FDMPosition
         There is an upper limit of the size of a ael module so it was a need to
                separate certain parts


HISTORY
         2002-04-25       Corrected time in CSP trade.
             2002-04-24       Now cash-post with qty 1.0.
         2002-02-06       Improved cash posting, now done by transactions.

REFERENCES
        FDMPosition

ENDDESCRIPTION
----------------------------------------------------------------------------"""

import FDMPosition
reload(FDMPosition)
from FDMPosition import *


def get_csp_instrument():
    """ Returns the cash posting instrument. Creates if not exists """
    return get_maint_instrument(CSP, CSP_EXTID1, CSP_EXTID2, 'For CashPosting')


def get_csp_party():
    """ Returns the cash posting party. Creates if not exists """
    return get_maint_party(CASH_PTYID, 'Internal Party', 'for adminstrating', 'cashposted positions')


def get_rollout_instrument():
    """ Returns the rollout instrument. Creates if not exists """
    return get_maint_instrument(ROLL_INSID, ROLL_EXTID1, ROLL_EXTID2, 'For Rollout')


def get_rollout_party():
    """ Returns the crollout party. Creates if not exists """
    return get_maint_party(CASH_PTYID, 'Internal Party', 'for adminstrating', 'cashposted positions')


"""----------------------------------------------------------------------------
CLASS
        FDMCSPTrade

INHERITS
        -

DESCRIPTION
        Helper class for managing the cash posting trade.

CONSTRUCTION
                        pos     - A FDMPosition object
                        curr    - A ael entity to the currency that should be used in calulation (optional). Default Accounting currency
                        d1              - The date object (optional)

METHODS (Exported)
                        Add(trades)     - Adds the rpl amount in the list of trades and archives them
                        UnWind()                - Rolls the process back

NOTE
                        The construction must be done outside a transaction to get correct trdnbr on the cash positing trade

MEMBERS
        Use only access functions!
----------------------------------------------------------------------------"""

class FDMCSPTrade:
    def __init__(self,pos,d1=None,curr=None):
        self.pos=pos
        self.trade=self.GetCSPTrade()
        if not curr:
            if ael.used_acc_curr():
                curr=ael.Instrument[ael.used_acc_curr()]
            else:
                curr=pos.Portfolio().curr
        if not d1: d1=suggest_date(ABA, self.pos.Instrument().insid)
        if not self.trade: self.trade=self.CreateCSPTrade(d1, curr)
        if not self.trade.trdnbr > 0:
            msg='This operation must be done outside a transaction'
            print msg
            raise RuntimeError, msg
        self.curr=curr
        self.trx_trdnbr = self.trade.trdnbr
        self.payment=self.trade.payments()[0]
        self.amount=self.payment.amount
        self.acc_amount=0.0
        if self.payment.text:
            m=re.search('\w+\((\d+\.\d+)', self.payment.text)
            if m:
                self.acc_amount=float(m.group(1))
        return

    def Amount(self):
        return self.amount

    def BuildTextKeys(self):
        """ Builds Text Keys that is used to mark from which position the CSP trade represents"""
        if len(self.pos.Instrument().insid)>29:
            text1=self.pos.Instrument().insid[:28]+'$'
            text2=self.pos.Instrument().insid[28:]+'/'+self.pos.Portfolio().prfid
            if len(text2) > 29: text2=text2[:28]+'$'
        else:
            text1=self.pos.Instrument().insid
            text2=self.pos.Portfolio().prfid
        return (text1, text2)


    def Add(self, trades):
        (amount, acc_amount)=self.CalcAmount(trades)
        self.amount=self.amount+amount
        if acc_amount != None:
            self.acc_amount=self.acc_amount+acc_amount
            text=("%s(%lf)" % (ael.used_acc_curr(), self.acc_amount))[:19]
        else:
            text=''
        t2=self.trade.clone()
        p=t2.payments()[0]
        p.amount=self.amount
        p.text=text
        #t2.quantity=1.0
        #t2.price=self.amount
        #t2.premium=t2.quantity*t2.price
        #t2.premium=self.amount
        t2.commit()
        for t in trades:
            t=t.clone()
            t.trx_trdnbr = self.trx_trdnbr
            t.archive_status=1
            t.commit()
        ael.poll()
        self.trade=t2
        self.payment=p


    def CalcAmount(self, trades):
        """ Calculates the amount contribution in the list of trades.
                If used currency is not accounting currency the second parameter
                is the value in accounting currency"""
        d1=self.payment.payday
        #d1=ael.date_today() # test
        curr=self.payment.curr
        rpl=ael.rpl(trades, ael.date('1970-01-01'), d1, curr, FDMPosition.AVG_TAG, 3)
        rpl2=None
        if ael.used_acc_curr() and ael.used_acc_curr() != curr.insid:
            rpl2=ael.rpl(trades, ael.date('1970-01-01'), d1, ael.Instrument[ael.used_acc_curr()], FDMPosition.AVG_TAG, 3)
        return (rpl, rpl2)


    def CreateCSPTrade(self, d1, curr):
        """ Creates a CSP Trade. Commit must be done by caller"""
        csp=get_csp_instrument()
        party=get_csp_party()
        t=ael.Trade.new(csp)
        t.type=FDMPosition.CLEAR_TAG
        #t.status='BO Confirmed'
        t.status = 'FO Confirmed'
        t.prfnbr=self.pos.Portfolio()
        ins=self.pos.Instrument()
        t.time=d1.to_time()+FDMPosition.LAST_SEC-2
        
        self.pos.setTradeDefaultValues(t)
        t.acquire_day=t.value_day=d1
        t.counterparty_ptynbr=party
        t.acquirer_ptynbr=party
        (t.text1, t.text2)=self.BuildTextKeys()
        t.curr=csp.curr
        t.quantity=1.0
        t.optional_key=self.genNewCSPKey()

        # Add the payment
        payment=ael.Payment.new(t)
        payment.payday=d1
        payment.ptynbr=get_csp_party()
        payment.type='Cash'
        payment.amount=0.0
        payment.curr=curr
        if ael.used_acc_curr() and ael.used_acc_curr() != curr.insid:
            payment.text=("%s(%lf)" % (ael.used_acc_curr(), 0.0))[:19]
        else:
            payment.text=''
        t.commit()
        ael.poll()
        return t


    def Delete(self):
        """ Deletes the cash-posting holder """
        self.trade.delete()

    def genNewCSPKey(self):
        s=str(self.pos.Portfolio().prfnbr)+'/'
        s=s+self.pos.Instrument().insid
        s=s[:35]
        k=s
        c=("optional_key='%s'" % s)
        t=ael.Trade.read(c)
        i=0
        while t:
            i=i+1
            n='/'+str(i)
            if len(s) + len(n) > 35:
                k=s[35-len(n)]+n
            else:
                k=s+n
            c=("optional_key='%s'" % k)
            t=ael.Trade.read(c)
        return k

    def GetCSPTrade(self):
        """ Returns the CSP trade if found. Also checks that if trx_trdnbr is used it is
          refering to the CSP trade (atleast until first CSP reference is found). If not raise RuntimeException"""
        csp=get_csp_instrument()
        t=self.pos.AggregateTrade()
        if not t and self.pos.ArchivedTrades():
            t=self.pos.ArchivedTrades()[-1]
        if t and t.trx_trdnbr > 0 and ael.Trade[t.trx_trdnbr] and ael.Trade[t.trx_trdnbr].insaddr == csp:
            return ael.Trade[t.trx_trdnbr]
        # Scan the csp trades
        (text1, text2)=self.BuildTextKeys()
        for t in csp.trades():
            if t.text1 == text1 and t.text2 == text2:
                return t
        return None


    def Sub(self, trades):
        (amount, acc_amount)=self.CalcAmount(trades)
        self.amount=self.amount-amount
        if acc_amount != None:
            self.acc_amount=self.acc_amount-acc_amount
            text=("%s(%lf)" % (ael.used_acc_curr(), self.acc_amount))[:19]
        else:
            text=''
        t2=self.trade.clone()
        p=t2.payments()[0]
        p.amount=self.amount
        p.text=text
        t2.commit()
        for t in trades:
            t=t.clone()
            t.trx_trdnbr = 0
            t.archive_status=0
            t.commit()
        ael.poll()
        self.trade=t2
        self.payment=p


