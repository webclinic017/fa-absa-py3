import acm, ael
import math
import csv
import at_time
import collections
import ABSA_Rate
from at_ael_variables import AelVariableHandler
from DateUtils import PDate
from datetime import datetime

ael_variables = AelVariableHandler()

ael_variables.add('Curve',
    label='Yield Curve(s)',
    cls='FYieldCurve',
    multiple=True)

ael_variables.add('Outpath',
    label='Output Path',
    default='/services/frontnt/Task/')

ael_variables.add('filename',
    label='Filename',
    default='RiskViewerRates.csv')    
    
class RateType:
    Continuous = acm.FEnumeration['enum(IrRateType)'].Enumeration('Continuous')
    Annual = acm.FEnumeration['enum(IrRateType)'].Enumeration('Annual Comp')
    Simple = acm.FEnumeration['enum(IrRateType)'].Enumeration('Simple')

class DateBasis:
    Act365 = acm.FEnumeration['enum(DaycountMethod)'].Enumeration('Act/365')

 
def date_add_tenor(acm_date, tenor, calendar, roll_convention):
    ''' Adds the tenor to the date and adjusts to a business day according
        to the roll_convention and calendar.
    '''   
    if roll_convention.lower() == 'mf':
        roll_code = acm.FEnumeration['enum(BusinessDayMethod)'].Enumeration('Mod. Following')
    elif roll_convention.lower() == 'f':
        roll_code = acm.FEnumeration['enum(BusinessDayMethod)'].Enumeration('Following')
    elif roll_convention.lower() == 'p':
        roll_code = roll_code = acm.FEnumeration['enum(BusinessDayMethod)'].Enumeration('Preceding')
    else:
        raise ValueError('roll_convention must be one of: "MF", "F" or "P"')
       
    end_date = acm.Time().DateAdjustPeriod(acm_date, tenor)
    return calendar.ModifyDate(None, None, end_date, roll_code) 

def write_file(name, data):
    f = file(name, 'wb')
    for row in data:
        for column in row:            
            f.write('%s,' %column)            
        f.write('\n') 
        
    print("Done\nWrote to secondary output %s" % name)
    f.close()
 
 
def ael_main(config):
 
    #generate date list for rate extraction
    year_list=[2, 15, 30]

    #time period for generating dates. The setup of year_list, and tenor list imply that we will generate weekly dates untill 2 years, then dates at 2w intervals
    #from 2y till 15y and then monthly dates until 30y

    tenor_list=['1w', '2w', '1m']

    #Curve name
    curve_data= config['Curve']
    
    todays_date=acm.Time().DateToday()
    year_today=int(todays_date[:4])
    month_today=int(todays_date[5:7])
    days_today= int(todays_date[8:10])

    depo_data_for_each_curve=[]

    report = [] 
    for curve_index in range(0, len(curve_data)):
        next_date=acm.Time().DateToday()
        yield_curve = curve_data[curve_index ]
        depo_params=[]
       
        for i in range(0, len(year_list)):
            date_marker= acm.Time().DateFromYMD(year_today+year_list[i], month_today, days_today) # calculate the 2y date, 15 year date and 30y date
            calendar= acm.FCalendar['ZAR Johannesburg']
            while next_date <= date_marker:
                next_date= date_add_tenor(next_date, tenor_list[i], calendar, 'F')                
                forward_rate=yield_curve.IrCurveInformation().Rate(todays_date, next_date, 6, 2, 1)
                depo_params.append((curve_data[curve_index].Name(), todays_date, next_date, forward_rate))
        for data in depo_params:
            report_data = (data[0], data[1], data[2], data[3])
            print data[0], data[1], data[2], data[3]
            report.append(report_data)
            
    repDate =  ael.date_today().to_ymd()
    repDateFormatted = str(repDate[2])+str(repDate[1]) +str(repDate[0])[-2:]
    
    output_path = config['Outpath']+ config['filename']
    write_file(output_path, report)
    print "print Completed Successfully ::"
        
        #depo_data_for_each_curve.append(depo_params)
        #print depo_data_for_each_curve

     
    #display curve data




