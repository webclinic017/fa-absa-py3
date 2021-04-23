"""-------------------------------------------------------------------------------------------------------
MODULE
    FCallMoneyASQLReport
    
    (c) Copyright 2011 by SunGard FRONT ARENA. All rights reserved.

DESCRIPTION
    no longer a ASQL report as suggested by the module name

-------------------------------------------------------------------------------------------------------"""

import ael
import acm
import re
import datetime
import os.path
import FReportOutput
import FASQLReport
import ArenaFunctionBridge



def get_ael_variables():
    """Retrieve the complete list of AEL variables used for FASQL report"""
    aelvars = [['start_date', 'Start Date', 'string', None, None, 0, 0, 'Start date for activity report', None, 1], \
            ['end_date', 'End Date', 'string', None, None, 0, 0, 'End date for activity report', None, 1], \
            ['fileName', 'File name2', 'string', None, None, 0, 0, 'Name of output file', None, 1] ] + \
            FReportOutput.getAelVariables()

    for variable in aelvars:
        if variable[0] == 'Print template (XSL)':
            variable[4] = 'FStandardTemplateClickable2'
    return aelvars

def write_asql_to_xml(writer, reportname, ca_columns, ca_values, result_columns, result_rows):
    writer.PRIMEReport()
    writer.Name(reportname).done()
    writer.Type().done()
    timestr = datetime.datetime.now().replace(microsecond=0).isoformat()
    writer.Time(timestr).done()
    writer.ReportContents()
    print_ca_setting(writer, ca_columns, ca_values)
    print_activities(writer, result_columns, result_rows)

def print_activities(writer, result_columns, result_rows):
    writer.Table()        
    writer.NumberOfColumns(len(result_columns)).done()
    xcolumns = writer.Columns()
    for colname in result_columns:
        print_column(writer, colname)
    xcolumns.done()

    writer.Rows()
    for row in result_rows:
        print_row(writer, row)
   
    writer.done()

def sort_activities(a, b):
    if ael.date(a[0]) > ael.date(b[0]):
        return 1
    elif ael.date(a[0]) < ael.date(b[0]):
        return -1
    else:
        if a[1].CashFlowType() == 'Call Fixed Adjustable' and b[1].CashFlowType() == 'Interest Reinvestment':
            return -1
        elif b[1].CashFlowType() == 'Call Fixed Adjustable' and a[1].CashFlowType() == 'Interest Reinvestment':
            return 1
        return 0
        
def print_ca_setting(writer, ca_columns, ca_values):
    atable=writer.Table()
    writer.NumberOfColumns(len(ca_columns)).done()
    acolumns=writer.Columns()
    for ca_column in ca_columns:
        print_column(writer, ca_column)
    acolumns.done()

    rr=writer.Rows()
    print_row(writer, ca_values)
    atable.done()

def print_column(writer, column):
    xcolumn = writer.Column()
    writer.ColumnId(column).done()
    writer.Label(column).done()
    xcolumn.done()

def print_row(writer, row):
    xrow = writer.Row()
    writer.RowType("ASQLResult").done()
    writer.Cells()
    for cell in row:
        print_cell(writer, cell)
    xrow.done()        
    
def print_cell(writer, cell):
    xcell = writer.Cell()
    writer.RawData(cell).done()
    writer.FormattedData(cell).done()
    xcell.done()
        
def perform_report(aelvars):
    writer, strbuf = FReportOutput.make_xmlreportwriter(aelvars)
    write_asql_to_xml(writer, "Call Account Activity Report", aelvars['ca_columns'], aelvars['ca_values'], aelvars['result_columns'], aelvars['result_rows'])
    xmltext = strbuf.getvalue()
    fname = aelvars['fileName']
    if not fname:
        fname = aelvars['default_file_name']
    FReportOutput.produceOutput(xmltext, fname, aelvars)

ael_variables=get_ael_variables()
FReportOutput.ael_variables = ael_variables

def runReport(invokationInfo):
    selectedInstruments = invokationInfo.ExtensionObject().ActiveSheet().Selection().SelectedInstruments()
    if not selectedInstruments:
        return 
        
    ins = selectedInstruments.At(0)
    if not ins:
        return
    
    leg = None
    legs = ins.Legs()
    if legs:
        leg = legs.At(0)
    if not leg or ins.InsType() != 'Deposit' or \
      (leg.LegType() != 'Call Fixed Adjustable' and leg.LegType() != 'Call Fixed' and leg.LegType() != 'Call Float'): 
        func=acm.GetFunction('msgBox', 3)
        func("Warning", "Activity Report is only available for Call Deposit/Loan.", 0)
        return

    acm.RunModuleWithParametersAndData('FCallMoneyASQLReport', '', invokationInfo)
    #acm.RunModuleWithParameters('FASQLReport', '')

def get_account_info(ins):
    ca_name=ins.Name()
    ca_notice=str(ins.NoticePeriodCount()) + ins.NoticePeriodUnit()
    ca_minimum=ins.MinimumPiece()
    ca_incomplete=ins.Incomplete()
    if ca_incomplete==0:
        ca_incomplete='No'
    elif ca_incomplete==4:
        ca_incomplete='Pledged'
    elif ca_incomplete==5:
        ca_incomplete='Frozen'
    ca_face=ins.FaceValue()   

    leg = ins.Legs().At(0)
    ca_rolling=str(leg.RollingPeriodCount()) + leg.RollingPeriodUnit()
    ca_eventbit=leg.EventBits()
    if ca_eventbit==0:
        ca_eventbit='No'
    elif ca_eventbit ==3:
        ca_eventbit='Yes'
    ca_reinvest=leg.Reinvest()
    if ca_reinvest==0:
        ca_reinvest='No'
    elif ca_reinvest==1:
        ca_reinvest='Yes'
    ins2=acm.FInstrument[ins.Oid()]
    nextIntDay = ins2.NextScheduledInterestDay()
    if not nextIntDay:
        ca_nextpayday = ''
    else:
        ca_nextpayday= ael.date(nextIntDay)
    ca_values = [ca_name, ca_notice, ca_rolling, ca_eventbit, ca_reinvest, ca_minimum, ca_incomplete, ca_face, ca_nextpayday]#, aelvars['start_date'], aelvars['end_date']]
    return ca_values

def get_activities(ins, sign, start_date=None, end_date=None):
    leg = ins.Legs().At(0)
 
    rows = []
    for cfw in leg.CashFlows():
        row=[cfw.PayDate(), cfw]
        rows.append(row)
    rows.sort(sort_activities)

    rate = 0.0
    #spread = 0.0
    #all_in = 0.0
    balance = 0.0
    result_rows=[]
    count = 0
    is_first_rate = 1
    for cfw in rows:
        count +=1
        reset_rows=[]
        spread = round(cfw[1].Spread(), 2)
        
        if cfw[1].CashFlowType() == 'Call Fixed Rate Adjustable':
            resets = cfw[1].Resets()
            for reset in resets:
                row = [reset.Day(), reset]
                reset_rows.append(row)
            reset_rows.sort(sort_activities)

            reset_count = 0             
            for reset in reset_rows:
                reset_count +=1
                if round(reset[1].FixingValue(), 2) != rate:
                    rate= round(reset[1].FixingValue(), 2)
                    #all_in = round(spread + rate, 2)
                    activity = [ael.date(reset[1].Day()), 'Rate Changed', '', rate,  '', round(balance, 2)]
                    if is_first_rate:
                        activity[1] = 'Rate'
                        is_first_rate = 0
                        if len(result_rows):
                            for i in range(0, len(result_rows)):
                                result_rows[i][3] = rate
                                #result_rows[i][4] = spread
                                #result_rows[i][5] = all_in
                #else:
                #    activity = [ael.date(reset[1].Day()), 'Rate', '', rate,  '', round(balance, 2)]
                    result_rows.append(activity)
                if reset_count == len(reset_rows) and balance != 0.0: #last reset, need to print interest
                    interest = ArenaFunctionBridge.GetProjectedCashFlow(cfw[1])*(-1)
                    if interest == 0.0: #no need to print a blank line
                        continue
                    if count == len(rows): #last cashflow 
                        activity = [ael.date(cfw[1].PayDate()), 'Interest Accrd', '', rate,  round(interest, 2), round(interest*sign + balance, 2)]
                    else:
                        activity = [ael.date(cfw[1].PayDate()), 'Interest Pay', '', rate,  round(interest, 2), round(balance, 2)]
                    result_rows.append(activity)
        elif cfw[1].CashFlowType() == 'Call Fixed Rate':
            rate = round(cfw[1].FixedRate(), 2)
            activity = [ael.date(cfw[1].PayDate()), 'Rate', '', rate,  '', round(balance, 2)]
            if is_first_rate:
                is_first_rate = 0
                if len(result_rows):
                    for i in range(0, len(result_rows)):
                        result_rows[i][3] = rate
                                #result_rows[i][4] = spread
                                #result_rows[i][5] = all_in
            interest = ArenaFunctionBridge.GetProjectedCashFlow(cfw[1])*(-1)
            if count == len(rows): #last cashflow 
                activity = [ael.date(cfw[1].PayDate()), 'Interest Accrd', '', rate,  round(interest, 2), round(interest*sign + balance, 2)]
            else:
                activity = [ael.date(cfw[1].PayDate()), 'Interest Pay', '', rate,  round(interest, 2), round(balance, 2)]
            result_rows.append(activity)
        elif cfw[1].CashFlowType() == 'Call Float Rate':
            resets = cfw[1].Resets()
            for reset in resets:
                row = [reset.Day(), reset]
                reset_rows.append(row)
            reset_rows.sort(sort_activities)

            reset_count = 0             
            for reset in reset_rows:
                reset_count +=1
                if round(reset[1].FixingValue() + spread, 2) != rate:
                    rate= round(reset[1].FixingValue(), 2) + spread
                    activity = [ael.date(reset[1].Day()), 'Rate', '', rate,  '', round(balance, 2)]
                    if is_first_rate:
                        is_first_rate = 0
                        if len(result_rows):
                            for i in range(0, len(result_rows)):
                                result_rows[i][3] = rate
                    result_rows.append(activity)
                if reset_count == len(reset_rows) and balance != 0.0: #last reset, need to print interest
                    interest = ArenaFunctionBridge.GetProjectedCashFlow(cfw[1])*(-1)
                    if interest == 0.0: #no need to print a blank line
                        continue
                    if count == len(rows): #last cashflow 
                        activity = [ael.date(cfw[1].PayDate()), 'Interest Accrd', '', rate,  round(interest, 2), round(interest*sign + balance, 2)]
                    else:
                        activity = [ael.date(cfw[1].PayDate()), 'Interest Pay', '', rate,  round(interest, 2), round(balance, 2)]
                    result_rows.append(activity)
        elif  cfw[1].CashFlowType() == 'Redemption Amount':
            continue
        else:
            amount = cfw[1].FixedAmount()*sign*ins.ContractSize()
            balance += amount
            type = cfw[1].CashFlowType()
            if type == 'Fixed Amount':
                type = 'Balance Adjust'
            elif type == 'Interest Reinvestment':
                type = 'Interest Reinv'
            activity= [ael.date(cfw[1].PayDate()), type, round(amount, 2), rate,  '', round(balance, 2)]
            result_rows.append(activity)     
    
    if start_date or end_date:
        return get_filtered_activities(result_rows, start_date, end_date)
    return result_rows

def get_filtered_activities(rows, start_date, end_date):
    if start_date and rows and (ael.date(rows[0][0])<ael.date(start_date)):
        start_rows = []
        for row in rows:
            if ael.date(row[0]) < ael.date(start_date):
                start_rows.append(row)
            else:
                break
        for row in  start_rows:
            rows.remove(row)
        first_row = start_rows[len(start_rows)-1]
        first_row[0]=ael.date(start_date) #date
        first_row[1]='Start Date'         #activity
        first_row[2]=''                   #movement
        #first_row[3]=''                   #rate
        #first_row[4]=''                   #spread
        #first_row[5]=''                   #all-in
        first_row[4]=''                   #interest
        rows.insert(0, first_row)
            
    if end_date and rows and (ael.date(rows[len(rows)-1][0]) > ael.date(end_date)):
        end_rows = []
        for row in rows:
            if ael.date(row[0]) > ael.date(end_date):
                end_rows.append(row)
        for row in end_rows:
            rows.remove(row)
        
        if rows:
            last_row=[ael.date(end_date), 'End Date', '', '',  '', rows[len(rows)-1][5]]
            """
            last_row[0]=ael.date(end_date)   #date
            last_row[1]='End Date'           #activity
            last_row[2]=''                   #movement
            last_row[3]=''                   #rate
            last_row[4]=''                   #spred
            last_row[5]=''                   #all-in
            last_row[6]=''                   #interest
            last_row[7]=rows[len(rows)-1][7] #balance
            """
            rows.append(last_row)
        
    return rows           


def get_activity_columns():
    return ['Date', 'Activity', 'Movement', 'Rate',  'Interest', 'Balance']

def get_account_columns():    
    return ['Account Name', 'Notice', 'Int. Period', 'Event', 'Reinvest', 'Min/Max Balance', 'Pledged/Frozen', 'P/F Amount', 'Next Schd Int Date']

def get_sign(eii):
    ins = get_instrument(eii)
    trades = eii.ExtensionObject().ActiveSheet().Selection().SelectedCell().RowObject().Portfolio().TradesIn(ins)
    if not trades:
        return 1
    return trades.At(0).Quantity()

def get_instrument(eii):
    instruments = eii.ExtensionObject().ActiveSheet().Selection().SelectedInstruments()
    if not instruments:
        return None
    return instruments.At(0)

def show_msg_box(level, msg):
    func=acm.GetFunction('msgBox', 3)
    func(level, msg, 0)
    
def ael_main_ex(aelvars, data):
    ins = get_instrument(data['customData'])
    sign = get_sign(data['customData'])
    
    sdate = aelvars['start_date']
    edate = aelvars['end_date']
    
    try:
        ael.date(sdate)
    except Exception as e:
        show_msg_box("Error", "Invalid start date " + sdate)
        return 
        
    try:
        ael.date(edate)
    except Exception as e:
        show_msg_box("Error", "Invalid end date " + edate)
        return 
    
    aelvars['ca_values']=get_account_info(ins)
    aelvars['ca_columns']=get_account_columns()
    aelvars['result_columns'] = get_activity_columns()
    aelvars['result_rows']=get_activities(ins, sign, aelvars['start_date'], aelvars['end_date']) 
    insname = ins.Name()
    if insname.find('/') != -1:
        insname = insname.replace('/', '-') 
    elif insname.find('\\') != -1:
        insname = insname.replace('\\', '-')
    aelvars['default_file_name']=insname
    perform_report(aelvars)
