"""
Name      : SAMM_CALL_IT3D
Purpose   : Perorm IT3D functions - produce output files for statements
Developer : Pavel Saparov
Date      : 22-02-2012
"""
from __future__ import division
import csv
import ael
import FRunScriptGUI
from collections import namedtuple


# Dictionary with month number to its full name 
MONTHS = dict(list(zip(range(1, 13), (
    'January', 'February', 'March', 'April',
    'May', 'June', 'July', 'August', 'September',
    'October', 'November', 'December'
))))


# Create TradeInterest namedtuple object
TradeInterest = namedtuple('TradeInterest', (
    'ClientCode', 'AccountNumber', 'Fica', 'MarchCredit', 
    'AprilCredit', 'MayCredit', 'JuneCredit', 'JulyCredit',
    'AugustCredit', 'SeptemberCredit', 'OctoberCredit', 
    'NovemberCredit', 'DecemberCredit', 'JanuaryCredit', 
    'FebruaryCredit', 'MarchDebit', 'AprilDebit', 
    'MayDebit', 'JuneDebit', 'JulyDebit', 'AugustDebit', 
    'SeptemberDebit', 'OctoberDebit', 'NovemberDebit', 
    'DecemberDebit', 'JanuaryDebit', 'FebruaryDebit'
))


class SAMMIT3DRunScript(FRunScriptGUI.AelVariablesHandler):
    """FRunScriptGUI class defining GUI parameters."""
    
    output_dir = FRunScriptGUI.DirectorySelection()
     
    def __init__(self):
        tax_years = []
        date = ael.date("2010-03-01")
        while date <= ael.date_today():
            tax_years.append(date)
            date = date.add_years(1) # plus 1-year
        
        ael_vars = [
            ['tax_year', 'Tax date', 'date', tax_years, tax_years[-1], 1, 0, 'Tax date', None, 1],
            ['front_to_midbase', 'Front Midbase Mapping?', 'string', None, r'y:\Jhb\Operations Secondary Markets\Income Tax\IT3b_2011\Front and Midbase data.csv', 1, 0, 'Midbase file', None, 1],
            ['filename', 'Output Filename', 'string', None, r'C:\SARS.IT3D.ACAP.FEB2012.txt', 1, 0, 'Output filename for yearly report', None, 1],
        ]
        
        FRunScriptGUI.AelVariablesHandler.__init__(self, ael_vars)


def calculate_interest(trade, tax_year):
    """
    Arguments:
    trade - ael.Trade class
    tax_year - ael date with begining of tax year
    
    Function returns populated namedtuple object
    """
    exclude_incomplete_clients = (
      '15036', '2335', '15043',
      '7032', '30574' '6781',
      '119175', '29580', '45023'
    )
    
    try:
        ptynbr = trade.counterparty_ptynbr.ptynbr
        client_code = midbase_mapping[str(ptynbr)] \
                          ['Midbase_Counterparty_UserRefCode']
        
        if client_code not in exclude_incomplete_clients:
            party = ael.Party[ptynbr]
            data = {}
            
            # Account Number - Call Deposit/Loan accounts have
            # unique Instrument name
            data['AccountNumber'] = trade.insaddr.insid[:20]
            
            # Client code obtained from Midbase CSV file
            data['ClientCode'] = client_code
            
            # Single character indicating if client is
            # FICA compliant
            data['Fica'] = party.add_info('FICA_Compliant')[0]
            
            # Calculate interest for each trade
            # and update ``data`` dictionary
            for i in range(0, 12):
                # Calculate accrued interest for the period
                tax_month = tax_year.add_months(i)
                int_set = trade.interest_settled(tax_month,
                              tax_month.add_months(1).add_days(-1),
                              'ZAR')
                int_acc = trade.interest_accrued(tax_month,
                              tax_month.add_months(1).add_days(-1),
                              'ZAR')
                interest = (int_set + int_acc) * trade.quantity
                interest = int(interest * 100)
                
                chronology = tax_month.to_ymd()[1] # obtain month
                key1, key2 = ("Credit", "Debit") if \
                    interest > 0 else ("Debit", "Credit") 
                
                # Setting calculated interest to ``data``
                data[MONTHS[chronology] + key1] = abs(interest)
                data[MONTHS[chronology] + key2] = 0
            
            # return populated namedobject
            return TradeInterest(**data)
    except KeyError:
        ael.log("Couldn't find Midabase key for"
            " Counterparty ID: {0}".format(ptynbr))

# Define variables for `ael_variables` used in GUI
ael_variables = SAMMIT3DRunScript()

def ael_main(kargv):
    """Main function"""
    global midbase_mapping
    
    ael.log("Starting {0}".format(__name__))
    
    trades = []
    tax_year_start = ael.date(kargv['tax_year'])
    tax_year_end = tax_year_start.add_years(1).add_days(-1)

    # Read trades from trade filters and populate ``trades`` list
    trade_filter1 = ael.TradeFilter['Call_All_Trades'].trades()
    trade_filter2 = ael.TradeFilter['SAMM_Primary_Trades'].trades()
    
    for trade in trade_filter1:
        trades.append(trade)

    for trade in trade_filter2:
        if (trade.insaddr.exp_day >= tax_year_start and 
            trade.value_day <= tax_year_end and 
            not(trade.mirror_trdnbr)):
            if trade not in trades:
                trades.append(trade)
    
    # Read Midbase to Front Arena mapping and store it in
    # global variable ``midbase_mapping``
    midbase_mapping = {}
    fp = open(kargv['front_to_midbase'], "r")
    for record in csv.DictReader(fp, delimiter=','):
        midbase_mapping[record['PTYNBR']] = record
    fp.close()

    # Main loop
    with open(kargv['filename'], "w") as fin:
        # Use pivot to indicate progress
        pivot = int(len(trades) / 100)
        
        for c, trade in enumerate(trades):
            
            # Very simple progress bar
            progress = c / pivot
            if progress.is_integer() and 0 <= progress <= 100:
                print("Progress - {0:>3.0f}%".format(progress))
            
            # Write calculated interest into output file
            ti = calculate_interest(trade, tax_year_start)
            if isinstance(ti, TradeInterest):
                fin.write((
                    "{0.ClientCode:>10}"
                    "{0.AccountNumber:>20}"
                    "{0.Fica}"
                    "{0.MarchCredit:>018}"
                    "{0.AprilCredit:>018}"
                    "{0.MayCredit:>018}"
                    "{0.JuneCredit:>018}"
                    "{0.JulyCredit:>018}"
                    "{0.AugustCredit:>018}"
                    "{0.SeptemberCredit:>018}"
                    "{0.OctoberCredit:>018}"
                    "{0.NovemberCredit:>018}"
                    "{0.DecemberCredit:>018}"
                    "{0.JanuaryCredit:>018}"
                    "{0.FebruaryCredit:>018}"
                    "{0.MarchDebit:>018}"
                    "{0.AprilDebit:>018}"
                    "{0.MayDebit:>018}"
                    "{0.JuneDebit:>018}"
                    "{0.JulyDebit:>018}"
                    "{0.AugustDebit:>018}"
                    "{0.SeptemberDebit:>018}"
                    "{0.OctoberDebit:>018}"
                    "{0.NovemberDebit:>018}"
                    "{0.DecemberDebit:>018}"
                    "{0.JanuaryDebit:>018}"
                    "{0.FebruaryDebit:>018}"
                ).format(ti))
                fin.write("\n")
    
    ael.log("Output written to {0}".format(kargv['filename']))
    ael.log("Completed successfully")
