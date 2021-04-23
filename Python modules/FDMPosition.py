""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
    FDMPosition - Wrapper module/class for Portfolio/Id positions

DESCRIPTION
    This module contains the class FDMPosition and other convinient
    operations for maintenaning portfolio/id-positions.
    By using the class FDMPosition you can abandon/Close/Clear-PL/CashPosition
    the positions.

REQUIREMENTS
    The module FCACustimization must be available for importing by this module

NOTE		
    Fee's is not handle which means that only if the user had set up
    FRONT ARENA to include fee's if the P/L calculations fees will be
    cleared.
    Otherwise not.
    The FDMPosition uses "Open Average" to calculate average price.

REFERENCES	
    FDMCascadeHandler, [genagg]

ENDDESCRIPTION
----------------------------------------------------------------------------"""


import ael
from types import *
import time, re, os

from FDMPositionUtil import *

VERSION=0.4 # Always good to check version in a soft way




#------------------------------------------------------------------------
# Exported Constants
#------------------------------------------------------------------------

ABA='Abandon'
ACH='Archiving'
DCH='DeArchive'
AGG='Aggregate'
DGG='DeAggregate'
CLO='Close'
CSP='CashPosting' # Also default name on the cash positing instrument
RPL='ClearRPL'
UPL='ClearUPL'
TPL='ClearTPL'
XPL='ClearXPL'
DEL='Delete'
#
# CURR_STYLES_KEYWORDS: The cuurency to use could be determent by the KEYWORDS
# below or the insid of a currency instrument
#
CURR_STYLES_KEYWORDS=["Accounting", "Portfolio", "Instrument"]
VALID_CURR_STYLES=[] # List of valid values, will be created after connect

SETTLE_PTYID='SETTLEMENT'
CASH_PTYID='CASH-POSTING'
ROLL_PTYID='ROLLOUT'
ROLL_INSID='RolledOut'

ARCH_DAYS_ALIVE=30  # Change if needed
ARCH_NBR_OF_TRADES=3 # Change if needed
verbose=0
date='NONE'
abandon_types=['Option', 'Warrant', 'Future/Forward']


# ---------------------------------------------------------------------------------
# Special extern_id1 and extern_id2 for the cash-posting  and rollout instrument so
# that customer could change the id. Don't change this below
# ---------------------------------------------------------------------------------
CSP_EXTID1='##(Fastolph Smallburrows)##'
CSP_EXTID2='##(of Sandydowns)##'

ROLL_EXTID='##(Longo Proudneck)##'
ROLL_EXTID2='##(of Tuckborough)##'

# ---------------------------------------------------------------------------------

#------------------------------------------------------------------------
# Local used functions (but exported)
#------------------------------------------------------------------------
def exp_day_to_date(ins):
    """ Operation for converting the exp_day to true exp_day """
    a_day=24*60*60
    if ins.exp_time > a_day and ins.exp_time < 2 * a_day:
        return ins.exp_day.add_days(-1)
    else:
        return ins.exp_day

def exp_time_to_time(ins):
    """ Operation for converting the exp_time to the true exp_time """
    a_day=24*60*60
    d=exp_day_to_date(ins)
    return d.to_time() + (ins.exp_time%a_day)
    

is_maint_ins_checked={} # Externid1 of created main instruments
def get_maint_instrument(insid,ext_id1,ext_id2,text=''):
    """ Returns the maint instrument. Creates if not exists. """
    global is_maint_ins_checked
    for t, c in [(insid, 'insid'), (ext_id1, 'extern_id1'), (ext_id2, 'extern_id2')]:
        i=ael.Instrument.read("%s='%s'" % (c, t))
        if i:
            if not is_maint_ins_checked.has_key(ext_id1) and not (i.extern_id1 == ext_id1 and i.extern_id2 == ext_id2):
                i2=i.clone()
                i2.extern_id1 =ext_id1
                i2.extern_id2 = ext_id2
                i2.commit()
                is_maint_ins_checked[ext_id1]=None
                ael.poll()
                return i2
            else:
                is_maint_ins_checked[ext_id1]=None
                return i

    i=ael.Instrument.new('FreeDefCF')
    i.insid=insid
    i.extern_id1 = ext_id1
    i.extern_id2 = ext_id2
    i.contr_size=1.0
    i.spot_banking_days_offset=0
    i.free_text=text[:19]
    i.commit()
    is_maint_ins_checked[ext_id1]=None
    ael.poll()
    return i

def get_maint_party(ptyid,text1='',text2='',text3=''):
    """ Returns maint  party. Creates if not exists """
    party=None
    try: party=ael.Party[ptyid]
    except:pass
    if not party:
        party=ael.Party.new()
        party.ptyid=ptyid
        party.type='Intern Dept'
        party.free1=text1[:19]
        party.free2=text2[:19]
        party.free3=text3[:19]
        party.commit()
        ael.poll()
    return party




def get_settle_party():
    """ Returns the settlement party. Creates if not exists """
    try:
        party=ael.Party[SETTLE_PTYID]
    except:
        pass
    if not party:
        party=ael.Party.new()
        party.ptyid=SETTLE_PTYID
        party.type='MtM Market'
        party.commit()
        ael.poll()
    return party


def get_valid_styles():
    """ Returns a list of valid currency style keywords than one can use """
    global CURR_STYLES_KEYWORDS, VALID_CURR_STYLES
    if not VALID_CURR_STYLES:
        VALID_CURR_STYLES=[]
        for s in CURR_STYLES_KEYWORDS:
            VALID_CURR_STYLES.append(s)
        for i in ael.Instrument.select('instype=Curr'):
            VALID_CURR_STYLES.append(i.insid)
    return VALID_CURR_STYLES


#------------------------------------------------------------------------
# Operations for suggesting a price and date that should be used
# when performing certain operations.
#
#------------------------------------------------------------------------

def get_settlement_price(insid, date):
    ins=ael.Instrument[insid]
    if not ins:
        s='The instrument %s does not exist' % insid
        print s
        raise s
    settle_market = ael.Party.read('ptyid = %s' % SETTLE_PTYID)
    if not settle_market:
        s='The MtM Market %s does not exist' % SETTLE_PTYID
        print s
        raise s
    else:
        mkt_nbr=settle_market.ptynbr
        
	settle_price = \
	ael.Price.read('insaddr=%d and day="%s" and curr=%d and ptynbr=%d'
	               %(ins.insaddr, date, ins.curr.insaddr, mkt_nbr))
    if not settle_price:
        temp_price = \
        ael.Price.read('insaddr=%d  and curr=%d and ptynbr=%d'
                       %(ins.insaddr, ins.curr.insaddr, mkt_nbr))
        if (temp_price and temp_price.day == ael.date(date)):
            settle_price = temp_price
        elif ins.mtm_price(date):
            s='No settlement price for %s on %s (%s market) will use mtm_price instead'\
               %(insid, date, settle_market.ptyid)
            print s
            settle_price = ins.mtm_price(date)

    if settle_price:
        return settle_price.settle
    else:
        s='No settlement price found for %s on date %s' % (insid, date)
        print s
        raise s

    
def suggest_price(method, id,date=None):
    """ Suggests a price depending on method and date """
    i=ael.Instrument[id]
    if not i:
        detail=("Instrument [%s] doens't exists!" % id)
        raise detail
    exp_date=None
    if not i:
        return (float(0.0), '-error-')
    if not date:
        try:
            date=exp_day_to_date(i)
        except:
            date=ael.date_today()
    if method in [ABA, CLO]:
        if i.instype == 'Option' or i.instype == 'Warrant':
            return (float(0.0), 'by definition')
        elif i.instype == 'Future/Forward':
            return (get_settlement_price(id, date), "SETTLEMENT")
        else:
            return (float(0.0), '-undef-')
    elif method == RPL:
        return (float(-4711.0), 'Mean')
    elif method == UPL or method == TPL or method == XPL:
        if date:
            if isinstance(date, StringType):
                date=ael.date(date)
        else:
            date=ael.date_today()
        if date.days_between(ael.date_today()) > 0:
            price = i.mtm_price(date, i.curr.insid, 3)
            price_type = 'mtm_price'
        else:
            if i.mtm_from_feed:
                price = i.used_price(date)
                price_type = 'used_price'
            else:
                if i.instype in ['Stock', 'EquityIndex']:
                    price = i.used_price(date)
                    price_type = 'used_price'
                else:
                    price = i.theor_price()
                    price_type = 'theor_price'
        return (price, price_type)
    elif method == DEL:
        return (float(-4711.0), '-not used-')
    else:
        return (float(-4711.0), '-not used-')


def suggest_date(method, id):
    """returns the date (as date)"""
    i=ael.Instrument[id]
    if not i:
        detail=("Instrument [%s] doens't exists!" % id)
        raise detail
    if method in [ABA, CLO, CSP]:
        try:
            if i.exp_day:
                return exp_day_to_date(i)
            return ael.date_today()
        except:
            return ael.date_today()
    elif method == DEL:
        return ael.date_today()
    elif method in [ACH, AGG]:
        d=ael.date_today()
        d=d.add_days(-ARCH_DAYS_ALIVE)
        try:
            if d > i.exp_day:
                return i.exp_Day
            return d
        except:
            return d

    else:
        date=ael.date_today()
        return date    

#------------------------------------------------------------------------
# Auxillary operations
#------------------------------------------------------------------------

def save_settlement_price(insid, date, price):
    """ saves a price for insid using party SETTLEMENT"""
    party=get_settle_party()
    # Look up price first
    i=ael.Instrument[insid]
    for p in i.prices():
        if p.ptynbr.ptynbr == party.ptynbr and p.day == date:
            np=p.clone()
            np.day = date
            np.settle = price
            np.commit()
            ael.poll()
            return 1
    for p in i.historical_prices():
        if p.ptynbr.ptynbr == party.ptynbr and p.day == date:
            np=p.clone()
            np.day = date
            np.settle = price
            np.commit()
            ael.poll()
            return 1
    #Create if not found
    i=ael.Instrument[insid]
    p=ael.Price.new()
    p.insaddr=i.insaddr
    p.curr=i.curr
    p.ptynbr=party.ptynbr
    p.settle=price
    p.day = date
    p.commit()
    ael.poll()
    return 1




#-----------------------------------------------------------------------
# Local operations
#-----------------------------------------------------------------------

def zero(value):
    """ Predicate for checking if a value (float) is zero """
    #if abs(value) < 1e-12:
    if abs(value) < 1e-10:
        return 1
    return 0

def ttos(sec):
    return time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(sec))
    
def cmp_trade(t1, t2):
    return t1.time-t2.time
  
"""----------------------------------------------------------------------------
CLASS			
	FDMPosition

INHERITS
	-
  	    	
DESCRIPTION		
	The 

CONSTRUCTION	
	port    - Portfolio name or id number.
	id      - Instrument name or id number.
	
METHODS (Exported)
        Maintenance Methods
        -------------------
        abandon
            aggregate
        archive
        close
            cash_pos
        clear_rpl
        clear_upl
        clear_tpl
        clear_xpl
        dearchive
        delete
            uncash_post

        Methods For Calculated Values
        -----------------------------
        Averge
        Fee
        Mean
        Rpl
        Upl
        Tpl
        Qty


MEMBERS
        Use only access functions!
----------------------------------------------------------------------------"""

class FDMPosition:
    """FDMPosition, Wrapper class for handling Portfilio,Id Positions"""
    
    #===============================================================================
    # CONSTANTS
    #===============================================================================
    LAST_SEC=(24*60*60)-1           # 23:59:59 seconds today
    DEFAULT_USERID='logged_on_user' # Change if not the one you wan't

    is_ael_mode_checked=0           # Only checked once
    maint_party_ptynbr=None
    
    # get special enum tags
    for i in range(20):
        if re.search('Open Average', ael.enum_to_string('AggregateType', i), re.I):
            AVG_TAG=ael.enum_to_string('AggregateType', i)
        elif re.search('Mean', ael.enum_to_string('AggregateType', i), re.I):
            MEAN_TAG=ael.enum_to_string('AggregateType', i)

    # TradeType for Clear RPL, UPL,TPL
    CLEAR_TAG=None
    for i in range(20):
        if re.search('End', ael.enum_to_string('TradeType', i), re.I):
            CLEAR_TAG=ael.enum_to_string('TradeType', i)
        elif CLEAR_TAG==None and re.search('Adjust', ael.enum_to_string('TradeType', i), re.I):
            CLEAR_TAG=ael.enum_to_string('TradeType', i)

    #===============================================================================
    # CONSTRUCTOR
    #===============================================================================
    def __init__(self, port, id):
        """Constructor,  could by called with address or name. Raise IOError on failure"""
        try:
            p=ael.Portfolio[port] # String or Int
            i=ael.Instrument[id] # String or Int
            found=1 
            stmt=("""select i.insid from instrument i
                        where i.insaddr = %d and exists (
                            select * from trade t
                                where i.insaddr = t.insaddr and t.prfnbr = %d)""" % (i.insaddr, p.prfnbr))
            try: 
            	# Will work against a sybase server or perhaps SQL-Server
            	row=ael.dbsql(stmt)[0]
            except: 
            	# SQL-Server handles this
                stmt=("""if exists ( select * from trade where
                		insaddr = %d and prfnbr = %d) select 1""" % (i.insaddr, p.prfnbr))
                row=ael.dbsql(stmt)[0]
            if not row[0] or row[0][0] == 0:
                found=0
            if not found:
                detail=("No such position: [%s:%s]" % (p.prfid, i.insid))
                raise IOError, detail
            
            #-----------------------
            # Attributes with calculated values.
            #-----------------------
            self.qty=None
            self.active_trades=None
            self.archived_trades=None
            self.rpl=None
            self.upl=None
            self.tpl=None
            self.avg_price=None
            self.mean=None
            self.fee=None
            self.used_calc_date=None

            #---------------------------
            # Special
            #---------------------------
            self.fake_agg_trades=[]
            
            #-------------------------
            # Default atttributes
            #-------------------------
            self.port=p
            self.ins=i
            self.cons=('t.insaddr = %d and t.prfnbr = %d' % (self.ins.insaddr, self.port.prfnbr))
            #
            # Create default party if it doesn't exists
            #
            
            if FDMPosition.maint_party_ptynbr == None:
                maint_party=ael.Party['FMAINTENANCE']
                if not maint_party:
                    s='\nA party called FMAINTENANCE of type "Intern Dept" has to be defined.'
                    print s
                    raise s
               	else:
               	    if maint_party.type != 'Intern Dept':
               	        print 'Party FMAINTENANCE is not of type "Intern Dept".' +\
               	        'Changing the type to "Intern Dept".'
               	        try:
               	            p=maint_party.clone()    
               	            p.type='Intern Dept'
               	            p.commit()
               	        except:
               	            print 'Could not change type for party FMAINTENANCE to "Intern Dept"'
                FDMPosition.maint_party_ptynbr=maint_party.ptynbr
            self.maint_party_ptynbr=FDMPosition.maint_party_ptynbr
            
            try:
                if FDMPosition.DEFAULT_USERID == 'logged_on_user':
                    self.defaulttrader_usrnbr=ael.user().usrnbr
                else:
                    self.defaulttrader_usrnbr=ael.User[FDMPosition.DEFAULT_USERID].usrnbr
            except:
                self.defaulttrader_usrnbr=ael.user().usrnbr
            
            return
        except:
            detail=("No such position: [%s:%s]" % (str(port), str(id)))
            raise IOError, detail


    #===============================================================================
    # INTERNAL USED METHODS
    #===============================================================================

    def getDefaultParty(self):
        return self.maint_party_ptynbr

    def setTradeDefaultValues(self, t):
        """ call this operation just before commit to fix unset values"""
        t.counterparty_ptynbr=self.getDefaultParty()
        t.acquirer_ptynbr=self.getDefaultParty()
        t.trader_usrnbr=self.defaulttrader_usrnbr
        t.curr=self.ins.curr
        try:
            import FCACustomization
            FCACustomization.fill_in_trade_keys(t)
        except ImportError:
            pass

        if self.ins.instype == 'Future/Forward':
            t.premium=0.0
        elif self.ins.quote_type == 'Per Contract':
            t.premium=-t.price*t.quantity*1.0
        elif self.ins.quote_type in ['Pct of Nominal', 'Pct of nominal']:
            t.premium=-t.price*t.quantity*self.ins.contr_size*0.01
        elif self.ins.quote_type == 'Clean':
            accrued=self.ins.interest_accrued(None, t.value_day, self.ins.curr.insid)
            t.premium=-(t.price*0.01*self.ins.contr_size+accrued)*t.quantity
        else:
            t.premium=-t.price*t.quantity*self.ins.contr_size*1.0
        #t.creat_time=t.updat_time=time.time()
        #t.creat_usrnbr=t.updat_usrnbr=ael.User[ael.userid()].usrnbr


    def clearCalcValues(self,active_trades=None):
        """ clears calculated values when new set of trades is loaded """
        self.qty=None
        self.rpl=None
        self.upl=None
        self.tpl=None
        self.avg_price=None
        self.fee=None
        self.mean=None
        if active_trades:
            self.active_trades = None

    def checkUsedCalcDate(self, d1):
        """ Checks the used calc date. Clear Calv values if needed """
        if self.used_calc_date and self.used_calc_Date != d1:
            self.clearCalcValues()


    #----------------------------------------------------------------------------
    # Special get operations for calculated values.
    # All operations has a force parameter that can be used to force 
    # recalculation but normally the calculation is suppressed.
    #----------------------------------------------------------------------------
    
    def ActiveTrades(self,force=0):
        """ returns a list if ael.trades that are active i.e visible from ael.
            All trades could be read but this is a safer way then above implemented
            were aggregate trade is faked! """
        if force or self.active_trades == None:
            excl_status="(%d,%d,%d)" % (ael.enum_from_string('TradeStatus', 'Void'),
                                      ael.enum_from_string('TradeStatus', 'Confirmed Void'),
                                      ael.enum_from_string('TradeStatus', 'Simulated'))
            if ael.archived_mode():
                archive_cons="((t.archive_status=0 and t.aggregate=0) or (t.archive_status=1 and t.aggregate=0))"
            else:
                archive_cons="((t.archive_status=0 and t.aggregate=0) or (t.archive_status=0 and t.aggregate=1))"
            stmt=("""select distinct t.trdnbr,t.time
                    from
                        trade t
                    where
                        t.status not in %s and %s and %s order by t.time""" % (excl_status, self.cons, archive_cons))
            tmp=[]
            for row in ael.dbsql(stmt)[0]:
                t=ael.Trade[int(row[0])]
                if t:
                    tmp.append(t)
            self.clearCalcValues()
            self.active_trades=tmp
        return self.active_trades

    def AggregateTrade(self):
        """ returns the aggregate trade """
        stmt="""select t.trdnbr from trade t where t.aggregate = 1 and %s""" % self.cons
        for row in ael.dbsql(stmt)[0]:
            t=ael.Trade[int(row[0])]
            if not t:
                detail=("Aggregate Trade %d is not visible! " % int(row[0]))
                raise IOError, detail
            return t


    def ArchivedTrades(self,force=1):
        """ returns a list if ael.trades that are archived i.e. archive_stratus=1 in time order.
                Aggregate trades are by definition not included"""
        if force or self.archived_trades == None:
            stmt=("""select distinct t.trdnbr,t.time
                        from
                            trade t
                        where
                            t.archive_status=1 and %s order by t.time""" % (self.cons))
            self.archived_trades=[]
            tmp=[]
            for row in ael.dbsql(stmt)[0]:
                t=ael.Trade[int(row[0])]
                if not t:
                    detail=("Trade %d is not visible! This operation must be performed in archive mode" % int(row[0]))
                    raise IOError, detail
                tmp.append(t)
            self.archived_trades=tmp
            return self.archived_trades


    #===============================================================================
    # CALCULATION METHODS.
    # Note: because it is not allowed to have attribute with the same name as an
    # operation corresponding operations are written in upper case
    #===============================================================================
   
    def Average(self,d1=None,curr=None):
        """ SAvg, True average price adjusted for contr_size division. """
        if self.avg_price==None:
            if d1==None: d1=ael.date_today()
            self.checkUsedCalcDate(d1)
            if curr==None: curr=self.ins.curr
            try:
                self.avg_price=ael.avg_price(self.ActiveTrades(), d1, curr, FDMPosition.AVG_TAG, 3)
            except:
                self.avg_price=ael.avg_price(self.ActiveTrades(), d1, curr, FDMPosition.AVG_TAG, 1)
        return self.avg_price




    def CreateRolloutMarkers(mean, avg, qty, time):
        """ Creates or updates existing rollout markers.
                Returns the markers without commiting the changes.
        ------------------------------------------------------------------
                Method A, qty/nbr <> 0:
              Generate two trades:
                1) Price = Avg, Qty=nbr*2.
                2) Price = 2*avg - Mean, Qty=-nbr

                Method B,  qty/nbr == 0:
                Generate two trades:
                a) Mean >= 0
                1) Price = Mean, Qty=1.
                2) Price = 0,    Qty=-1

                b) Mean < 0
                1) Price = 0,    Qty=1.
                2) Price = -Mean,Qty=-1"""
        pass


    def Fee(self,d1=None):
        """ Fee's for trades up to d1 """
        if d1==None: d1=ael.date_today()
        upto=d1.to_time()+FDMPosition.LAST_SEC
        self.checkUsedCalcDate(d1)
        if self.fee==None:
            fee = 0.0
            for t in self.ActiveTrades(): 
                if t.status != 'Void' and t.time <= upto:
                    fee=fee+t.fee
                #print "Calc By ActiveSet [%s:%s] %lf" % (self.port.prfid,self.ins.insid, self.qty)
            self.fee=fee
        return self.fee

    def GetCurr(self, style):
        if not style in get_valid_styles():
            detail="Invalid currency style %s! Valid values are %s " % (style, string.join(get_valid_styles(), ''))
            raise RuntimeError, detail
        if style == 'Accounting':
            if not ael.used_acc_curr():
                raise RuntimeError, "No accounting currency defined!"
            return ael.Instrument[ael.used_acc_curr()]
        elif style == 'Portfolio':
            return self.Portfolio().curr
        elif style == 'Instrument':
            return self.Instrument().curr
        else:
            return ael.Instrument[style]


    def Log(self,text,flag='+'):
        import time
        now=time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))
        print "%s : %s %s" % (now, flag, str(text))

    def WLog(self, text):
        self.Log(text, '-')

    def ELog(self, text):
        self.Log(text, '!')

    def Instrument(self):
        return self.ins

    def Name(self):
        return "[%s:%s]" % (self.Portfolio().prfid, self.Instrument().insid)

    def Mean(self,d1=None,curr=None):
        """ SMean, True mean price adjusted for contr_size division. """
        if self.mean==None:
            if d1==None: d1=ael.date_today()
            self.checkUsedCalcDate(d1)
            if curr==None: curr = self.ins.curr
            try:
                self.mean=ael.avg_price(self.ActiveTrades(), d1, curr, FDMPosition.MEAN_TAG, 3)
            except:
                self.mean=ael.avg_price(self.ActiveTrades(), d1, curr, FDMPosition.MEAN_TAG, 1)
        return self.mean


    def Portfolio(self):
        return self.port


    def Rpl(self,stop=None, curr=None):
        """ RPL from 1970 to stop (date). Default stop date is today() """
        if self.rpl==None:
            start=ael.date('1970-01-01')
            if stop==None: stop=ael.date_today()
            self.checkUsedCalcDate(stop)
            if curr==None: curr = self.ins.curr
            #for t in self.ActiveTrades():
            #    print t.trdnbr,t.time,t.quantity,t.price,t.aggregate,t.aggregate_pl
            self.rpl=ael.rpl(self.ActiveTrades(), start, stop, curr, FDMPosition.AVG_TAG, 3)
        return self.rpl

    def Upl(self,stop=None,curr=None):
        """ MaUPL from 1970 to stop (date). Default stop date is today().
            IMPROVEMENTS: FIX CURR, i.e convert used _price
            """
        if self.upl==None:
            start=ael.date('1970-01-01')
            if stop==None: stop=ael.date_today()
            self.checkUsedCalcDate(stop)
            avg=self.Average(stop, curr)
            used_price=self.ins.used_price(stop)
            if  avg == used_price : # Bugg fix
                return 0.0
            qty=self.Qty(stop)
            return ( (used_price-avg)*qty*self.ins.contr_size )
            #self.upl=ael.upl(self.ActiveTrades(), start,stop,self.ins.curr,FDMPosition.AVG_TAG,0)
        return self.upl

    def Tpl(self,stop=None,curr=None):
        """ MaTPL from 1970 to stop (date). Default stop date is today() """
        if self.tpl==None:
            rpl=self.Rpl(stop, curr)
            upl=self.Upl(stop, curr)
            #print "RPL=%lf, UPL=%lf" % (rpl,upl)
            self.tpl=rpl+upl
        return self.tpl

    
    def Qty(self, d1=None):
        """Calculates the total quantity in active trades"""
        if d1==None: d1=ael.date_today()
        self.checkUsedCalcDate(d1)
        upto=d1.to_time()+FDMPosition.LAST_SEC
        if self.qty==None:
            qty = 0.0
            for t in self.ActiveTrades(): 
                if t.status != 'Void' and t.time <= upto:
                    qty=qty+t.quantity
                #print "Calc By ActiveSet [%s:%s] %lf" % (self.port.prfid,self.ins.insid, self.qty)
            self.qty=qty
        return self.qty


    
            
            
            

    

        
    
        
    #===============================================================================
    # MAINTENANCE METHODS
    #===============================================================================

        

    def abandon(self, d1=None, price=None):
        """Abandon the position. For future/forward a price could be given"""
        global abandon_types
        if self.ins.instype not in abandon_types:
            print "Abondoning positions in instruments with instype %s is not supported" % \
                  self.ins.instype
            return
        exp_day=exp_day_to_date(self.ins)
        if d1==None:
            d1=exp_day
        if price==None:
            price=suggest_price(ABA, self.ins.insid, exp_day)[0]
        
        qty=self.Qty(exp_day)
        if qty == 0.0:
            #Nothing to Abandon
            print "Nothing to Abandon"
            return 1
        t=ael.Trade.new(self.ins)
        t.price=price
        t.quantity= -qty
        t.type='Abandon'
        t.prfnbr=self.port.prfnbr
        t.time=d1.to_time()+FDMPosition.LAST_SEC-2 # So you can abandon and Clear
        curr=ael.Instrument[self.ins.curr.insid]
        t.value_day=t.acquire_day=d1
        self.setTradeDefaultValues(t)
        
        t.commit()
        ael.poll()
        self.clearCalcValues(1)
        return 1
            

    def aggregate(self,d1=None,force=None,verbose=1):
        """ Aggregate and archives part the position. Use force to recalc the positions """
        import genagg
        
        if d1==None:
            d1=ael.date_today().add_days(-ARCH_DAYS_ALIVE)
        M={}
        M['prf_list']=[self.port.prfid]
        M['ins_list']=[self.ins.insid]
        M['date']=d1.to_string()
        M['sv_date']=("'%s'" % d1.to_string())
        M['und_list']=[]
        M['given_instype']=[self.ins.instype]
        M['arch_from'] = '0'
        if force:
            M['arch_to']   = '1'
            M['use_daysalive']=0
            M['no_of_trades'] = '0'
        else:
            M['arch_to']   = '0'
            M['use_daysalive']=0
            M['no_of_trades'] = str(ARCH_NBR_OF_TRADES)
            #M['no_of_trades']=ARCH_NBR_OF_TRADES       # Check if genagg version behavious diffrently
        M['cl_pl_time'] = "'1970-01-01 00:00:00'"
        
        M['verbose']   = verbose
        M['correct_agg']='Aggregate' # 3.2.X and later

        type='eq'
        if self.ins.instype == 'Bond':
            type='bond'
        elif self.ins.instype in ['Option', 'Future/Forward'] and self.ins.und_insaddr.instype == 'Bond':
            type='bond'

        if genagg.__dict__.has_key('agg_portfolio'): # 3.1.X 
	    genagg.init_values(M)
            if type == 'eq':
                genagg.init_eq_values(M)
            else:
                genagg.init_bond_values(M)
            genagg.agg_portfolio(M, self.port.prfid, type)

        else:
            genagg.perform_agg_and_arch(M, type) # 3.2.X and later
        self.clearCalcValues(1)
        return 1


    def archive(self):
        """ Just archives a whole positions trades included the aggregate trade.
        Already archived trades will get archive_status == 2 so that this operation
        can be reverted.
        """
        stmt="""select t.trdnbr, t.archive_status from trade t
                    where t.archive_status=0 and %s""" % (self.cons)
        from FDMCascadeHandler import FDMCascadeHandler
        h=FDMCascadeHandler()
        for row in ael.dbsql(stmt)[0]:
            (trdnbr, archive_status) = row[0]
            h.archive_object('trade', int(trdnbr), int(archive_status)+1) # Will not archive already archived to this level

    def cash_post(self, d1=None, curr=None, do_abandon=None, do_delete=1):
        """ CashPosting the position i.e. represent the RPL as one trade
            If needed the positions could first be abandon to clear UPL.
                  If do_delete==0 the position is just archived.
               The structure built up is that all live trades are refering to the cash posted trade
               by trx_trdnbr and at the same time, archived.
               At the end the whole position is deleted if wanted."""
        # -----------------------------------
        # Default values and default handling
        # -----------------------------------
        if not d1: d1=suggest_date(ABA, self.Instrument().insid)
        if not curr:
            if ael.used_acc_curr():
                curr=ael.Instrument[ael.used_acc_curr()]
            else: curr=self.Instrument().curr
        qty=self.Qty(d1)
        if not zero(qty):
            if not do_abandon or not self.abandon(d1):
                raise RuntimeError, "Position %s Qty=%lf is not zero" % (self.Name(), qty)
        # -----------------------------------
        # build a list of trades that should be included
        # -----------------------------------
        trades=[]
        found_aggregate=None
        for t in self.ActiveTrades():
            if not t.archive_status: trades.append(t)
            if t.aggregate: found_aggregate=1
        if not found_aggregate:
            tmp=self.AggregateTrade()
            if tmp: trades=[tmp]+trades
        if not trades:
            self.Log('Nothing to cashpost in position %s!' % self.Name())
            if do_delete: self.delete()
            return

        # -----------------------------------
        # Where the work is done
        # -----------------------------------
        csp_trade=FDMCSPTrade(self, d1, curr)
        tmp=[]
        n_bunch=500
        n=0
        while trades:
            tmp.append(trades.pop(0))
            n=n+1
            if len(tmp) == n_bunch:
                ael.begin_transaction()
                csp_trade.Add(tmp)
                ael.commit_transaction()
                ael.poll()
                tmp=[]
        if tmp:
            ael.begin_transaction()
            csp_trade.Add(tmp)
            ael.commit_transaction()
            ael.poll()
        self.Log('CashPosted %s with amount=%lf in %s' % (self.Name(), csp_trade.amount, curr.insid))
        if do_delete: self.delete()
        return 1


    def close(self, d1=None, price=None):
        """Closes the position. For future/forward a price could be given"""
        if self.ins.instype not in abandon_types:
            print "Closing positions in instruments with instype %s is not supported" % \
                  self.ins.instype
            return
        if ael.date_today().days_between(self.ins.exp_day) >= 0:
            print "Only positions in expired instruments can be closed"
            return
        if d1==None:
            d1=suggest_date(CLO, self.ins.insid)
        if price==None:
            price=suggest_price(CLO, self.ins.insid, d1)[0]
        
        qty=self.Qty(d1)
        if qty == 0.0:
            print "Nothing to Close"
            return 1
        t=ael.Trade.new(self.ins)
        t.price=price
        t.quantity= -qty
        t.type='Closing'
        t.prfnbr=self.port.prfnbr
        t.time=d1.to_time()+FDMPosition.LAST_SEC-2 # So you can abandon and Clear
        curr=ael.Instrument[self.ins.curr.insid]
        t.value_day=t.acquire_day=d1.add_banking_day(curr, self.ins.spot_banking_days_offset)
        self.setTradeDefaultValues(t)
        
        #print t.pp()
        t.commit()
        ael.poll()
        self.clearCalcValues(1)
        return 1

        

    def clear_pl(self,method,d1,market_price=None,price_source=''):
        """ Main method for clearing, if called things should be cleared """

        qty=self.Qty(d1) 
        m=re.search('Clear(\w+)', method)
        if m:
            tag=m.group(1)
        else:
            tag=method
                       
        if zero(qty):
            #
            # Open position to price 0.0 and close to mean price.
            # Will only be applied when clearing RPL or TPL (then UPL is zero)
            #
            # UPL == 0.0 => RPL == TPL
            t=ael.Trade.new(self.ins)
            t.prfnbr=self.port.prfnbr
            t.quantity=1.0
            
            #Use spot day to calculate to interest settled and interest accrued
            curr=ael.Instrument[self.ins.curr.insid]
            value_day=d1.add_banking_day(curr, self.ins.spot_banking_days_offset)
            t.acquire_day=t.value_day=value_day
            self.clearCalcValues()    #Ugly fix, needed because Rpl has been called previously with
            rpl = self.Rpl(value_day) #date d1. Should be fixed differently, but do not have the guts to do it now
            
            #For bonds the accrued and settled interest is included in the rpl function
            #Accrued and settled interest is not cleared
            pos_accrued=self.ins.interest_accrued(None, value_day, None, self.port)
            pos_settled=self.ins.interest_settled(None, value_day, None, self.port)
            trading_rpl=rpl-pos_accrued-pos_settled
            
            accrued=self.ins.interest_accrued(None, value_day, self.ins.curr.insid)
            
            if rpl > 0.0:
                if self.ins.quote_type == 'Per Contract': 
                    t.price=rpl
                elif self.ins.quote_type in ['Pct of Nominal', 'Pct of nominal']:
                    t.price=trading_rpl*100/self.ins.contr_size
                elif self.ins.quote_type == 'Clean':
                    t.price=(trading_rpl-accrued)*100/self.ins.contr_size
                else:
                    t.price=rpl/self.ins.contr_size
            else:
                if self.ins.quote_type == 'Clean':
                    t.price=-accrued*100/self.ins.contr_size
                else:
                    t.price=0.0
            t.type=FDMPosition.CLEAR_TAG
            text=('%s,Open 0.0' % tag)
            t.text1=text[:29]
            t.time=d1.to_time()+FDMPosition.LAST_SEC-1
            self.setTradeDefaultValues(t)
            t.commit()
            ael.poll()
            t=ael.Trade.new(self.ins)
            t.prfnbr=self.port.prfnbr
            t.quantity=-1.0
            t.acquire_day=t.value_day=value_day
            if rpl > 0.0:
                if self.ins.quote_type == 'Clean':
                    t.price= - accrued*100/self.ins.contr_size
                else:
                    t.price=0.0
            else:
                if self.ins.quote_type == 'Per Contract': 
                    t.price=-rpl
                elif self.ins.quote_type in ['Pct of Nominal', 'Pct of nominal']:
                    t.price=-trading_rpl*100/self.ins.contr_size
                elif self.ins.quote_type == 'Clean':
                    t.price=-(trading_rpl+accrued)*100/self.ins.contr_size
                else:
                    t.price=-rpl/self.ins.contr_size
            t.type=FDMPosition.CLEAR_TAG
            rpl = self.Rpl(d1)  # UPL == 0.0 => RPL == TPL            
            text=('%s,%lf'% (tag, rpl))
            t.text1=text[:29]
            t.time=d1.to_time()+FDMPosition.LAST_SEC
            self.setTradeDefaultValues(t)
            t.commit()
            ael.poll()
            self.clearCalcValues(1)
            return

        if method == RPL:
            closing_price   = self.Mean(d1)       
            open_price      = self.Average(d1)   
            rpl             = self.Rpl(d1)
            text1=('%s,%lf' % (tag, rpl))
        elif method == UPL:
            closing_price   = self.Average(d1)   
            open_price      = market_price             
            upl             = self.Upl(d1)
            text1           = ('%s,%lf' % (tag, upl))
        elif method == TPL:
            closing_price   = self.Mean(d1)      # Suppress reload
            open_price      = market_price             
            tpl             = self.Tpl(d1)
            text1           = ('%s,%lf' % (tag, tpl))
        
        curr=ael.Instrument[self.ins.curr.insid]
        value_day=d1.add_banking_day(curr, self.ins.spot_banking_days_offset)
        
        #accrued adjustment due to bug in avg_price function
        if self.ins.quote_type in ['Pct of Nominal', 'Pct of nominal']:
            accrued_adjustment=(self.ins.interest_accrued(None, value_day, self.ins.curr.insid) - 
                   self.ins.interest_accrued(None, d1, self.ins.curr.insid))*100/self.ins.contr_size
        else:
            accrued_adjustment=0
        
        t=ael.Trade.new(self.ins)
        t.prfnbr=self.port.prfnbr
        t.price=closing_price+accrued_adjustment
        t.quantity=-qty
        t.type=FDMPosition.CLEAR_TAG
        t.text1=text1[:29]
        t.time=d1.to_time()+FDMPosition.LAST_SEC-1
        t.value_day=t.acquire_day=value_day
        self.setTradeDefaultValues(t)
        t.commit()

        t=ael.Trade.new(self.ins)
        t.prfnbr=self.port.prfnbr
        t.price=open_price+accrued_adjustment
        t.quantity=qty
    
        
        t.type=FDMPosition.CLEAR_TAG
        text2=('%s, Open %.2lf' % (tag, open_price))
        if market_price:
            tmp=('source %s' % price_source)
            t.text2 = tmp[:29]
        t.text1=text2[:29]
        t.time=d1.to_time()+FDMPosition.LAST_SEC
        t.value_day=t.acquire_day=value_day
        self.setTradeDefaultValues(t)
        t.commit()
        ael.poll()
        self.clearCalcValues(1)
        return
                  
        

    def clear_rpl(self,d1=None):
        """ Clears RPL by entering one or two trades """
        if d1==None:
            d1=suggest_date(RPL, self.ins.insid)
        else:
            if d1.days_between(ael.date_today()) < 0:
                print "%s is a future date. P/L cannot be cleared in the future" % d1
                return
        rpl=self.Rpl(d1)
        if zero(rpl):
            print "Nothing to ClearRPL"
            return
        self.clear_pl(RPL, d1)



    def clear_upl(self,d1=None, market_price=None, next_day_prices=0):
        """ Clears UPL by entering one or two trades """
        if d1==None:
            d1=suggest_date(UPL, self.ins.insid)
        else:
            if d1.days_between(ael.date_today()) < 0:
                print "%s is a future date. P/L cannot be cleared in the future" % d1
                return
        upl=self.Upl(d1)
        if zero(upl):
            print "Nothing to ClearUPL"
            return
        if market_price==None:
            if next_day_prices:
                if d1:
                    curr=ael.Instrument[self.ins.curr.insid] 
                    d1=d1.add_banking_day(curr, 1)    
            market_price=suggest_price(UPL, self.ins.insid, d1)
        if isinstance(market_price, TupleType):
            self.clear_pl(UPL, d1, market_price[0], market_price[1])
        else:
            self.clear_pl(UPL, d1, market_price[0], 'By User')



    def clear_tpl(self,d1=None, market_price=None, next_day_prices=0):
        """ Clears TPL by entering one or two trades """
        if d1==None:
            d1=suggest_date(UPL, self.ins.insid)
        else:
            if d1.days_between(ael.date_today()) < 0:
                print "%s is a future date. P/L cannot be cleared in the future" % d1
                return
        tpl=self.Tpl(d1)
        if zero(tpl):
            print "Nothing to ClearTPL"
            return
        if market_price==None:
            if next_day_prices:
                curr=ael.Instrument[self.ins.curr.insid] 
                if d1:
                    curr=ael.Instrument[self.ins.curr.insid] 
                    d1=d1.add_banking_day(curr, 1)
            market_price=suggest_price(TPL, self.ins.insid, d1)
        if isinstance(market_price, TupleType):
            self.clear_pl(TPL, d1, market_price[0], market_price[1])
        else:
            self.clear_pl(TPL, d1, market_price, 'By User')


    def clear_xpl(self,d1=None, market_price=None):
        """ Special method: Clears TPL if UPL < 0.0 otherwise RPL """
        if d1==None:
            d1=suggest_date(UPL, self.ins.insid)
        else:
            if d1.days_between(ael.date_today()) < 0:
                print "%s is a future date. P/L cannot be cleared in the future" % d1
                return
        upl=self.Upl(d1)
        if upl < 0.0:
            self.clear_tpl(d1, market_price)
        else:
            self.clear_rpl(d1)



    def deaggregate(self):
        """ Deaggregates a position """
        stmt=("""select t.trdnbr from trade t
                    where %s and t.aggregate=1""" % (self.cons))
        row=ael.dbsql(stmt)
        if not row or not row[0]:
            return 0 # If no aggregate trade exists it is archived.
        aggregate=row[0][0][0]
        try:
            t=ael.Trade[aggregate]
            archive_mode=None
        except:
            archive_mode=1
        if not archive_mode: # Good, executed in archive mode.
            for t in self.ArchivedTrades(1):
                t2=t.clone()
                t2.archive_status=0
                t2.aggregate_trdnbr=0
                t2.commit()
            ael.poll()
        else:
            stmt=("""select t.trdnbr from trade t  
                        where insaddr=%d and prfnbr=%d and aggregate=0""" % (self.ins.insaddr, self.port.prfnbr))
            for row in ael.dbsql(stmt)[0]:
                stmt=("""update trade set archive_status=0,aggregate_trdnbr=0  
                            where trdnbr=%d""" % (r[0][0]))
                ael.dbsql('begin transaction')
                ael.dbsql(stmt)
                ael.dbsql('commit')            
        #print "Delete aggregate"
        # if OK sofar delete the aggregate trade
        from FDMCascadeHandler import FDMCascadeHandler
        h=FDMCascadeHandler()
        h.delete_object('trade', int(aggregate))
        ael.poll()
        self.clearCalcValues(1)
        return 1




    def dearchive(self):
        """ Just dearchives a whole positions trades included the aggregate trade.
        The FDMCascadeHandler operation dearchive method will just subtract one to the
        archive_status flag which means that the position looks the same as when archived"""
        
        stmt="""select t.trdnbr, t.archive_status from trade t
                    where t.archive_status=0 and %s""" % (self.cons)
        from FDMCascadeHandler import FDMCascadeHandler
        h=FDMCascadeHandler()
        for row in ael.dbsql(stmt)[0]:
            (trdnbr, archive_status) = row[0]
            h.dearchive_object('trade', int(trdnbr), int(archive_status)-1) # Will not dearchive already archived to this level

            

    def delete(self,stop=None):
        """ Deletes the position up to stop (if defined). Do not use position after this. """
    
        from FDMCascadeHandler import FDMCascadeHandler
        h=FDMCascadeHandler()
        stmt="select t.trdnbr,t.time from trade t where %s" % (self.cons)
        for row in ael.dbsql(stmt)[0]:
            try:
                t=ael.Trade[row[0]]
                if stop==None or t.time <= stop:
                    h.delete_object('trade', t.trdnbr)
            except:
                if stop==None or row[1] <= stop:
                    h.delete_object('trade', row[0])
        return 1


    def uncash_post(self,n_bunch=500):
        """ Reverts a position that is cash-posted."""
        csp_trade=FDMCSPTrade(self) # A trade will always be created
        amount=csp_trade.Amount()
        tmp=[]
        n=0
        trades=self.ArchivedTrades()
        while trades:
            t=trades.pop()
            if t.trx_trdnbr != csp_trade.trx_trdnbr: break
            tmp.insert(0, t)
            n=n+1
            if len(tmp) == n_bunch:
                ael.begin_transaction()
                csp_trade.Sub(tmp)
                ael.commit_transaction()
                ael.poll()
                tmp=[]
        if tmp:
            ael.begin_transaction()
            csp_trade.Sub(tmp)
            ael.commit_transaction()
            ael.poll()
        csp_trade.Delete()
        self.Log('UnCash-Posted %d trades with the amount=%lf' % (n, amount))
        return n










