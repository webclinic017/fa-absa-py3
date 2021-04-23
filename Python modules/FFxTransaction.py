""" Standard_Queries:1.0.0 """

'''---------------------------------------------------------------------------------
 MODULE
     FFxTransaction - Sets FX Rate to a selected value for a selection of trades, by
                      generating two payments.
     
     (c) Copyright 2000 by Front Capital Systems AB. All rights reserved.
     
 DESCRIPTION
     The function allows you to create a selection of trades based on trading day,
     instrument, currency or portfolio, and then create two payments with a defined
     FX Rate. Only trades where the trade currency differs from the selected currency
     (default accounting currency) are displayed. You have the possibility to view
     the selection before you actually create the payments by setting the operation
     parameter to "View Selection" and then press the Apply button. When you are
     satisfied with your selection, change the operation parameter to "Update FX Rate".

     The selection of trades will consist of:
     "Trade Date" AND " Instrument" AND "Premium Currency" AND "Portfolio"
     
     Your selection can not contain more than one Premium currency, or you will not
     be able to create the payments.
     
     Only the "Trade Date" parameter is mandatory.
     
     
     Input parameters:
     
     Premium Currency   Select trades made in a specified currency (Optional)
     Trade Date         The trades executed this day will recieve the new FX Rate.
     Operation          Here you can select if you want to display your trade selection
                        before you execute the update.
     Settle Currency    The transaction currency (default accounting currency)
     FX Rate            The FX Rate that you want to set.
     Instrument         Select trades made in a specified instrument (Optional)
     Portfolio          Select trades from a selected portfolio (Optional)
     
 NOTE
     Only trades where the trade currency differs from the selected Settle Currency
     are displayed.
     Only instruments traded during the last 10 days are displayed in the
     instrument list.
     Only portfolios used during the last 10 days are displayed in the
     instument list.
     Only trade currencies used during the last 10 days are displayed in the
     Premium Currency list.
     
 DATA-PREP
     <E.g, how to define a correct instrument, only if relevant>
     
 REFERENCES
     <Articles, books, other modules etc>
 ENDDESCRIPTION
----------------------------------------------------------------------------------'''

import ael
import string
import time

'''----------------------------------------------------------------------------------
 FUNCTION
     findTrade - Creates a dictionary with all trades in all selected instruments
     
 DESCRIPTION
      The function returns a dictionary with instruments as keys and all trades for
      that instrument in a list. Only trades where accounting currency differs from
      trade currency will be returned.
     
 ARGUMENTS
     
     dat        string  The first trading day that you want to fetch trades for
                        "YYYY-MM-DD"
     days       int     The number of days from dat that you want to fetch trades
                        for starting from dat
     i          string  Instrument, the instrument you want to get the trades for.
                        'All' if all instruments are to be fetched. Default set to 1
     pf         string  Selected portfolio
     cu         string  Selected currency
      
     
 RETURNS
   
     result {}      {Instrument: [[Trade.trdnbr, Trade.curr, Trade.prfnbr], 
                                  [Trade.trdnbr,...                      ],
                     Instrument2:[Trade.trdnbr,..]...}
         
----------------------------------------------------------------------------------'''


def findTrade(dat, days, i=None, pf = None, cu = None, fx = ael.used_acc_curr()):
    result = {}
    acc_curr = fx
    start=ael.date(dat).to_time()               # trades after this time
    end=ael.date(dat).add_days(days).to_time()  # trades before this time
# Check for erroneous user input
    if i != None and type(ael.Instrument[i]) != ael.ael_entity: 
        print "*** Instrument does not exist ***"
        return result
        
    if i != None:                           # Get trades for a specific instrument
        ins = ael.Instrument[i].insaddr
        for t in ael.Trade.select('insaddr=%s'%(ins)):
# Do not include trades with default accounting currency            
            if t.curr.insid != acc_curr:        
               result = insTrade(t, result, start, end, pf, cu)
                     
                     
    else:                                   # Get trades for all instrument traded
        trd = ael.dbsql('select trdnbr from trade where time >="%s" and aggregate = 0\
                     '%(dat+' 00:00:00'))
        for t_num in trd[0]:        # during the selected period
# Do not include trades with default accounting currency
            t = ael.Trade[int(t_num[0])]
            if t.curr.insid != acc_curr:
                result = insTrade(t, result, start, end, pf, cu)
    return result

'''----------------------------------------------------------------------------------
 FUNCTION
     insTrade - Inserts trades into a dictionary of instruments
     
 DESCRIPTION
     The function returns a dictionary with instruments as keys and all trades for
     that instrument in a list.
     
 ARGUMENTS
     
     t          Trade   The trade that will be inserted into dictionary if
                        conditions are fulfilled.
     result     {}      Dictionary that shall be appended with new trades.
     start      time    Start time for trade selection
     end        time    End time for trade selection
     pf         string  Selected portfolio
     cu string  Selected currency
      
     
 RETURNS
   
     result {}      {Instrument: [[Trade.trdnbr, Trade.curr, Trade.prfnbr], 
                                  [Trade.trdnbr,...                      ],
                     Instrument2:[Trade.trdnbr,..]...}
         
----------------------------------------------------------------------------------'''

def insTrade(t, result, start, end, pf, cu):
    # Inserts trade number, trade currency and portfolio
    # number into a dictionary of instruments
#    print time.ctime(start), time.ctime(end) 
#    print time.ctime(t.time), t.curr.insid, t.acquire_day, t.book_day, t.value_day
    if t.time > start and t.time <= end:
        if cu == None or cu == t.curr.insid:
            if pf == None or (type(t.prfnbr)==ael.ael_entity and pf == t.prfnbr.prfid):
                if result.has_key(t.insaddr.insid):
                    result[t.insaddr.insid].append([t.trdnbr, t.curr, t.prfnbr])
                else:
                    result[t.insaddr.insid] = [[t.trdnbr, t.curr, t.prfnbr]]
    return result  

'''----------------------------------------------------------------------------------
 FUNCTION
     getDates - Gets a list of days ranging from now and back in time.
     
 DESCRIPTION
     The function returns a list of date objects the length of the list is defined
     By the days parameter. The banking days returned are based on the Frankfurt
     calendar.
     
 ARGUMENTS
     
     days  int     The number of dates that the list shall contain.
      
     
 RETURNS
   
     d     []       ['YYYY-MM-DD','YYYY-MM-DD',...]
         
----------------------------------------------------------------------------------'''
def getDates(n):
    d = []
    for i in range(n):
        d1 = ael.date_today().add_days(-i)
        d.append(d1.to_string())  
    return (ael.date(d[-1]).days_between(ael.date(d[0])), d)

'''----------------------------------------------------------------------------------
 FUNCTION
     getPortfolios - returns a dictionary with all Portfolios used in the ins_dict.
     
 DESCRIPTION
     From the instrument dictionary, containing all trades executed during a defined
     period of time, (set by the "no_of_days" variable) all portfolios used for these
     trades are displayed
     
 ARGUMENTS
     
     ins_dict   {}      The instrument dictionary that was returned from findTrade()
      
     
 RETURNS
   
     pf    {}       {prfid : prfnbr, prfid : prfnbr, ...}
         
----------------------------------------------------------------------------------'''

def getPortfolios(ins_dict):
    pf = {}
    for i in ins:                               
        for t in range(len(ins_dict[i])):
            if ins_dict[i][t][2] != None:
                pfid = ins_dict[i][t][2].prfid
                if not pf.has_key(pfid):
                    pf[pfid] = ins_dict[i][t][2].prfnbr
    return pf

'''----------------------------------------------------------------------------------
 FUNCTION
     getCurr - returns a dictionary with all Currencies used in the ins_dict.
     
 DESCRIPTION
     From the instrument dictionary, containing all trades executed during a defined
     period of time, (set by the "no_of_days" variable) all currencies used for these
     trades are displayed
     
 ARGUMENTS
     
     ins_dict   {}      The instrument dictionary that was returned from findTrade()
      
     
 RETURNS
   
     pf    {}       {insid : inaddr, insid : insaddr, ...}
         
----------------------------------------------------------------------------------'''

def getCurr(ins_dict):
    cu = {}
    for i in ins_dict.keys():                           
        for t in range(len(ins_dict[i])):
            cuid = ins_dict[i][t][1].insid
            if not cu.has_key(cuid):
                cu[cuid] = ins_dict[i][t][1].insaddr
    return cu      

'''----------------------------------------------------------------------------------
 FUNCTION
     create_payments - creates payments for a selection of trades.
     
 DESCRIPTION
     Creates payments for a selection of trades and prints the trade numbers of
     the trades that are updated. 
     
 ARGUMENTS
     
     trad       {}      The instrument dictionary that was returned from findTrade()
     rate       float   The rate that you want to set the fx_rate to.
      
     
 RETURNS
   
     None
         
----------------------------------------------------------------------------------'''

def create_payments(trad, rate, currency, fx):

    if len(trad.keys()) == 0:
        print "No trades available for the defined selection criteria."
        return
        
    for i in trad.keys():
        print "Instrument %s" % (i)

        for j in trad[i]:
            transaction_exists = None
            fx_pay = []
            t = ael.Trade[j[0]].clone()
            for p in t.payments():
                if p.fx_transaction == 1:
                    transaction_exists = 1
                    fx_pay.append(p)
            if not transaction_exists:
                p_close = ael.Payment.new(t)
                p_open = ael.Payment.new(t)
                print "\t Trade: %i \tPayments generated" % (j[0])
            else:
                if not len(fx_pay) == 2:
                    print "ERROR: The number of FX Payments for trade: %s \
                           is not equal to two."%(t.trdnbr)
                p_close = fx_pay[0]
                p_open = fx_pay[1]
                print "\t Trade: %i \tFX transactions updated" %(j[0])
                
            p_close.type = 'Premium'
            p_close.payday = t.value_day
            p_close.fx_transaction = 1
            p_close.curr = t.curr
            p_close.amount = -(t.premium)
            p_open.type = 'Premium'
            p_open.payday = t.value_day
            p_open.fx_transaction = 1
            p_open.curr = ael.Instrument[fx].insaddr
            p_open.amount = t.premium * float(rate)
            t.updat_time = time.time()                     # Workaround for SPR 16332
            t.commit()

'''----------------------------------------------------------------------------------
 FUNCTION
     printSelection - Displays the selection created based on the user input
     
 DESCRIPTION
     This function displays the selection based on the criteria defined by the user.
     
 ARGUMENTS
     
     trad       {}      The instrument dictionary that was returned from findTrade()
      
     
 RETURNS
   
     None
         
----------------------------------------------------------------------------------'''

def printSelection(trad):
    if len(trad.keys()) > 0:
        for i in trad.keys():
            print "Instrument %s" % (i)
            print "Selected Trades"
            for j in trad[i]:
                exist = ''
                for p in ael.Trade[j[0]].payments():
                    if p.fx_transaction == 1:
                        if p.curr <> ael.Trade[j[0]].curr:
                            exist = 'FX Payments Exist in %s/%s'%\
                                     (ael.Trade[j[0]].curr.insid, p.curr.insid)
                if j[2] != None:
                    print "\t Trade: %i Prem. Curr: %s Portfolio: %-29s \t%s" % \
                        (j[0], ael.Trade[j[0]].curr.insid, j[2].prfid, exist)
                else:
                    print "\t Trade: %i Prem. Curr: %s Portfolio: %-29s \t%s" % \
                    (j[0], ael.Trade[j[0]].curr.insid, 'None', exist)
    else:
        print "No trades available for the defined selection criteria."
                


#************************************************************************************
#                                   Main
#************************************************************************************
    
ins = []        # List of all instruments traded during the last 30 days
ins_dict = {}   # Dictionary of instruments [tradenumber, currency_ref, prfnbr_ref]
dates = []      # A list of dates listing the last 11 days.
trad = {}       # Dictionary containing instruments and all trades in those instr.
                # for the selected period of time.
pf_dict = {}    # Dictionary of all portfolios in the system {prfid : prfnbr}
cu_dict = {}    # Dictionary with all used currencies
all_curr = []   # List of all defined currencies.


(no_of_days, dates) = getDates(10)  # Creates list of 10 dates for user interaction

                                    # Find all instruments traded the last no_of_days
                                        
start_date = dates[-1]
ins_dict = findTrade(start_date, no_of_days+1)  
ins = ins_dict.keys()

# Dictionary of all portfolios used during the last no_of_days
pf_dict = getPortfolios(ins_dict)       

# Dictionary of all currencies used for trading the last no_of_days
cu_dict = getCurr(ins_dict)             

curr_obj = ael.Instrument.select('instype=Curr')
for c in curr_obj:
    all_curr.append(c.insid)


# Variables presented in the ael macro for user interaction.    
fx = ael.used_acc_curr()
if len(cu_dict.keys()):
    cu = cu_dict.keys()[0]
else:
    cu = fx
rate = str(ael.Instrument[cu].used_price(ael.date_today(), fx))

ael_variables=[('date', 'Trade Date', 'string', dates, ael.date_today().to_string()),
               ('instr', 'Instrument', 'string', ins, '', 0),
               ('fx_rate', 'FX Rate', 'string', [], rate, 0),
               ('disp', 'Operation', 'string', ['Update FX Rate',\
                'View selection (no update)'], 'View selection (no update)'),
               ('pf', 'Portfolio', 'string', pf_dict.keys(), '', 0),
               ('cu', 'Premium Currency', 'string', cu_dict.keys(), cu, 0),
               ('fx', 'Settle Currency', 'string', all_curr, fx, 1)]
def ael_main(dict):
    global cu, fx
                                        #Fetch all trades based on user input
    cu = dict['cu']
    fx = dict['fx']
    trad = findTrade(dict['date'], 1, dict['instr'], dict['pf'], dict['cu'], dict['fx'])
    curr = getCurr(trad) 
    
    print ''
    print "*********************************************\
****************************"
    print ''
    print 'The Accounting currency is: %s'%(ael.used_acc_curr())
    if cu in cu_dict.keys():
        print 'The Currency Rate for %s/%s is: %.4f'\
               %(cu, fx, float(dict['fx_rate']))
    print ''
    
    if dict['disp'] == 'Update FX Rate': 
        try:
            rate = float(dict['fx_rate'])
        except:
            print 'Illegal FX Rate "%s"'%(dict['fx_rate'])
        else:
            if rate > 1E-10 and (dict['cu']== '' or len(curr.keys()) == 1):
                if len(curr.keys())==1:
                    dict['cu'] = curr.keys()[0]   
# Create payments for selected trades.
                create_payments(trad, dict['fx_rate'], dict['cu'], dict['fx']) 
            else:
                print ''
                if len(curr.keys()) > 1 and rate <= 0:
                    print 'Currency and FX Rate must be defined to generate payments.'
                elif len(curr.keys()) > 1:
                    print 'Currency must be defined to generate payments.'
                elif rate <= 0:
                    print 'FX Rate must be larger than Zero.'
                print ''
        
    else:
        printSelection(trad)                # Only display trades selected by user
