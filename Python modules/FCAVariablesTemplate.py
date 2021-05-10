""" CorporateActions:1.2.2 """

"""----------------------------------------------------------------------------
MODULE
    FCAVariables - Module with variables needed by the Corp Action script.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    In this module are some Corporate Action variables that can be chosen by 
    the customer.
    
NOTE 
    Please rename the file to FCAVariables. 
    
----------------------------------------------------------------------------"""
import ael

### Choose between the two methods 'Close Out' and 'Adjust':
DefaultMethod = 'Close' 
#DefaultMethod = 'Adjust'

### If you have chosen the Close Out method, you can choose if you
### want all trades to be opened at zero prices, or if you want the prices
### to be calculated from the Average Price of the position. (The
### Corporate Actions Merger and Spin-off base their calculations on the
### MtM Price of the day before the ExDate.)
Price = 1        ### Calculate prices, based on average price per portfolio.
#Price = 0       ### Set price to zero in trades.
#Price = 'MtM'   ### Use mtmprice when calculating.

### Choose default currency for cash payments, close out and open up trades
### in case Close out method is used.
#Curr = 'InstrumentCurr'
Curr = 'PortfolioCurr'
#Curr = None # Necessary to specify None if want to change to AccCurr without
            # restarting client.

### Choose which trade date you want to compare Record Date with:
ComparisonDate = 'Acquire Date'
#ComparisonDate = 'Trade Time'

### This date will be displayed as CorpAct Date in the Macro variables 
### window when FCAExecute is run. It is corporate action with ExDate before 
### this date that will be performed.
defaultCorpActDate = ''
#defaultCorpActDate = str(ael.date_today())
#defaultCorpActDate = '2222-02-22'  ### An infinite future date.

### Specify the Accounting Method which should be used to calculate Average
### Price.
Acc_Method = 'Open Average'
#Acc_Method = 'Average Simple'
#Acc_Method = 'FIFO'
#Acc_Method = 'LIFO'
#Acc_Method = 'LIFO Intra Day'
#Acc_Method = 'Mean'
#Acc_Method = None      ### If Acc_Method = None the position calculation 
                        ### method will be taken from the Accounting 
                        ### Parameters application. 

### Specify the name of your MtM_Market for settlement prices.
MtM_Market = 'internal'
#MtM_Market = 'SETTLEMENT'

### Specify a list of the names of your markets where no historical prices 
### should be adjusted:
Protected_Markets = ['']
#Protected_Markets = ['internal']
#Protected_Markets  = ['protected_ptyid_1', 'protected_ptyid_2']

### Specify for how many days back to search for a settlement price:
Max_Days = 2

### Specify if you want to be able to perform rollback on historical prices:
### If 'Save_Price_Changes' is set to 1, every price change will be saved and a
### rollback can take hours to perform. If set to 0, a new Corporate Action
### from the Corporate Action application has to be created in order to
### rollback prices.
#Save_Price_Changes = 0
Save_Price_Changes = 1

### Not used for latest ATLAS release. Kept for backwards compatibility.
### This variable is overridden by Market in the Corporate Action application.
#Default_Deriv_Exch = 'Eurex'
#Default_Deriv_Exch = 'OM'
Default_Deriv_Exch = '' ### No default

### If rights_distribution = 1 no stock adjustments will be made at all, only 
### the actual rights will be distributed in the respective portfolios.
### If rights_distribution = None, rights will be distributed to the 
### portfolios, plus the stocks will be adjusted in price. 
### The only way not to get any rights distributed is to leave the Corporate
### Action application field "New instrument" blank.
rights_distribution = None
#rights_distribution = 1

### Please consider the following:
### commit and verb are set in the macro variable window when run from client
commit = 1  # 1 to save transactions to the db; 0 to save nothing to the db.
verb   = 1  # 1 to log useful information to console or to file.
debug  = 1  # 1 to print extra information to console or to file, for debug.
pp     = 0  # 1 to print extra information about updated / changed db records.
log    = 0  # 1 to log to file; 0 to log to the console.

### If log = 1, specify a log file:
#logfile = 'c:\\temp\\corpact.txt'
logfile = None
### The following line will place the logfile in e.g.
### '/opt/front/arena/log/prod':
#logfile = '%s/ca_%s.log' % (environ['FCS_DIR_LOG'], environ['CONFIG_NAME'])

### Enable Voluntary Corporate Actions. If close out or adjustment should only 
### occur in a certain portfolio at a certain quantity. Can also be used to 
### customize code, e.g. calculate prices of stocks from supplied values.
#Voluntary = 1
Voluntary = None
#rounding = '6_decimals'
rounding = None
Auto_Cancel_Premiums = 0

"""231346 To rename an option series, specify the substring to be replaced 
in one of the fields: insid, external_id1 or external_id2 of the 
underlying instrument to the original options. In the corresponding field 
of the new underlying, specify the new substring.
The field used for this purpose (insid, external_id1 or external_id2)  
is specified as the variable ShortCodeFieldName. The default
value of this variable is '', which means that the options will keep their 
original naming standard."""

ShortCodeFieldName = ''
#ShortCodeFieldName = 'insid'
#ShortCodeFieldName = 'extern_id1'
#ShortCodeFieldName = 'extern_id2'



