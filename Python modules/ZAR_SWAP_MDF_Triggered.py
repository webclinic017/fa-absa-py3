"""-----------------------------------------------------------------------------
PURPOSE                 :  extract rates from ZAR-SWAP curve, runs intraday
                           Market Data Feeds (Pricing and Risk) use the output.
                           called by the Market Data Feeds, once it has feed the ZAR-SWAP
                           Curve with ME data.
DEPATMENT AND DESK      :  
REQUESTER               :  Marlyn Anthonyrajah 
DEVELOPER               :  Edmundo Chissungo
DATE:                   :  2015-08-11
CR NUMBER               :  CHNG0003017278
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no, Developer               Description
--------------------------------------------------------------------------------
"""

import sys
import xml.dom.minidom as xml
import ael
import acm
import os
import time
import warnings

class ZarSwapExtract():
    
    def __init__(self):
        self.path = ""

    def log(self, message):
        """log the message with current date and time."""
        print "{0}: {1}".format(acm.Time.TimeNow(), message)


    def retrieve_environment(self, env_config):
        """
        Determine which FA environment (Dev/Uat/Prod)
        the script is running in.
        Returns the specified path contained in the
        FExtensionValue which differs for each
        environment.
        
        """

        arena_data_server = acm.FDhDatabase["ADM"].ADSNameAndPort().upper()
        configuration = acm.GetDefaultValueFromName(
            acm.GetDefaultContext(), acm.FObject, env_config)

        dom_xml = xml.parseString(configuration)
        tags = dom_xml.getElementsByTagName("Host")
        for element in tags:
            if element.getAttribute("Name") == arena_data_server:
                self.path = element.getElementsByTagName(
                    "output_path")[0].childNodes[0].data
        
        if self.path == "":
            warnings.warn("path is empty!!!")

    def rate_data(self):
        '''
            Extract the curve rate data, daily until 2y 
        '''
        Act365 = acm.FEnumeration['enum(DaycountMethod)'].Enumeration('Act/365')
        
        curve = acm.FYieldCurve['ZAR-SWAP']
        swap_dates = []
        instrument_list = [('ZAR-JIBAR-ON-DEP', '0d'), ('ZAR-JIBAR-3M', '3m'), \
                    ('ZAR/FRA/JI/3X6', '6m'), ('ZAR/FRA/JI/6X9', '9m'), \
                    ('ZAR/FRA/JI/9X12', '12m'), ('ZAR/FRA/JI/12X15', '15m'),\
                    ('ZAR/FRA/JI/15X18', '18m'), ('ZAR/FRA/JI/18X21', '21m'), \
                    ('ZAR/FRA/JI/21X24', '2y'), ('ZAR/IRS/GEN/3Y', '3y'), \
                    ('ZAR/IRS/GEN/4Y', '4y'), ('ZAR/IRS/GEN/5Y', '5y'), \
                    ('ZAR/IRS/GEN/6Y', '6y'), ('ZAR/IRS/GEN/7Y', '7y'), \
                    ('ZAR/IRS/GEN/8Y', '8y'), ('ZAR/IRS/GEN/9Y', '9y'), \
                    ('ZAR/IRS/GEN/10Y', '10y'), ('ZAR/IRS/GEN/12Y', '12y'), \
                    ('ZAR/IRS/GEN/15Y', '15y'), ('ZAR/IRS/GEN/20Y', '20y'), \
                    ('ZAR/IRS/GEN/25Y', '25y'), ('ZAR/IRS/GEN/30Y', '30y')]


        for ins_name, tenor in instrument_list:
            instrument = acm.FInstrument[ins_name]
            if tenor == '2y':
                date_2y = instrument.ExpiryDate()

            if instrument.InsType() == 'Swap':
                swap_dates.append(instrument.ExpiryDate())

        calendar = acm.FCalendar['ZAR Johannesburg']
        start_date = acm.Time().DateToday()
        daily_dates = self.generate_daily_dates(start_date, date_2y, calendar)
        output = [['RateType', 'start date', 'end date', 'Rate']]
        
        for end_date in daily_dates: 
            zar_swap_simple = curve.IrCurveInformation().Rate(start_date, end_date,\
                            'Simple', Act365, 'Spot Rate')
            output.append(['Deposit Price', start_date, end_date, zar_swap_simple])

        for end_date in swap_dates: 
            zar_swap_simple = curve.IrCurveInformation().Rate(start_date, end_date,\
                            'Quarterly', Act365, 'Par Rate')
            output.append(['Swap Price', start_date, end_date, zar_swap_simple])

        return output


    def generate_daily_dates(self, start_date, end_date, calendar):
        '''
            Generate the dates for the curve points,excluding non banking days.
        '''
        next_date = start_date
        date_list = [start_date]
        while next_date <= end_date:
            next_date = acm.Time().DateAddDelta(next_date, 0, 0, 1)
            if not calendar.IsNonBankingDay(None, None, next_date):
                date_list.append(next_date)
        return date_list

    def write_data_to_file(self, data, location):
        '''
            Rate extract written to file then picked up by Pricing & Risk team.
        '''
        reporter = 0
        while (True):
            try:
                with open(location, "w") as f:
                    for row in data[1:]:
                        output_string =row[0]+ ',' + self.date_to_string(row[1]) + ',' + \
                                        self.date_to_string(row[2]) +',' + str(row[3])+"\n"
                        f.write(output_string)
                    break
            except IndexError, a:
                raise
            except (OSError, IOError) as e:
                reporter+=1
                time.sleep(1) #back off for one second as lock is replaced by the Market data feeds
                if reporter >=5:
                    self.log("5th failed attempt to open the destination file")
        self.log('complete')


    def date_to_string(self, input_date):
        '''
            Helper function for date formatting
        '''
        Y, M, D=acm.Time().DateToYMD(input_date)
        return str(Y)+ "/"+str(M)+"/"+str(D)

    def run_zar_swap_extractor(self):
        """Subscribe to instrument tables."""

        self.log("Starting...")
        path = "\\\\Intranet.barcapint.com\\\dfs-emea\\GROUP\\Jhb\\FALanding\\Prod\\PnR"
        #self.retrieve_environment("ETFTradeConfigSettings")
        self.log("output_path: " + path)
        self.log("Started in main.")
        result = self.rate_data()
        write_to_location = os.path.join(path, "ZARSWAPRateOutput" + ".csv")
        self.write_data_to_file(result, write_to_location)
        self.log("result written to: "+write_to_location )


