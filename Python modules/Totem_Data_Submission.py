"""-----------------------------------------------------------------------------
MODULE
    Totem_Data_Submission

DESCRIPTION
    Date                : 2021-02-05
    Purpose             : Automate the population of the daily TOTEM Equities Templates.
    Department and Desk : PCG Valuations
    Requester           : Ryan Fagri (Ryan.Fagri@absa.africa)
    Developer           : Buhlebezwe Ngubane
ENDDESCRIPTION

Required columns (expected values):
OptionType: ['Put', 'Call']
StrikeType: ['Rel Spot Pct', 'Rel Spot Pct 100']
StrikePercent
Underlying
ValuationDate
ExpiryDate
ClientReferenceLevel
ClientPrice
ClientImpliedSpot
ClientDiscountFactor

Expected file format:
CSV


HISTORY
=============================================================================================
Date            Change no               Developer               Description
---------------------------------------------------------------------------------------------
2021-02-05                              Buhlebezwe Ngubane      Initial implementation
------------------------------------------------------------------------------------------"""

import acm, FRunScriptGUI, FUxCore, csv
from decimal import Decimal, getcontext
from datetime import datetime
from dateutil.parser import parse
from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from at_feed_processing import SimpleCSVFeedProcessor

fileFilterInput = "CSV Files (*.csv)|*.csv"
fileFilterOutput = "CSV File (*.csv)|*.csv"
inputFile = FRunScriptGUI.InputFileSelection(FileFilter=fileFilterInput)
outputFile = FRunScriptGUI.OutputFileSelection(FileFilter=fileFilterOutput)

ael_variables = AelVariableHandler()
ael_variables.add(
    'input_file',
    label='InputFile',
    cls=inputFile,
    default=inputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV format.'
)

ael_variables.add(
    'output_file',
    label='OutputFile',
    cls=outputFile,
    default=outputFile,
    mandatory=True,
    multiple=True,
    alt='Input file in CSV format.'
)

LOGGER = getLogger(__name__)

class TotemDataSubmissionCSV(SimpleCSVFeedProcessor):
    #For front arena Equity Index 
    default_und_map = {
        "JALS": "ALSI",
        "JSE AFRICA FINDI 30 INDEX": "FINI",
        "JSE CAPPED TOP 40": "DCAP",
        "JSE TOP 40 SHAREHOLDER WEIGHTED": "SWIX",
    }
    
    columns = ["ClientID", "ValuationDate", "AssetClass", "ServiceName", "ServiceFrequency",
                    "SubArea", "SchemaVersion", "Underlying", "ReferenceType", "ReferenceID",
                    "ClientReferenceLevel", "InstrumentType", "ExpiryDate", "StrikePercent", "OptionType",
                    "ExerciseStyle", "ClientPrice", "ClientImpliedSpot", "ClientDiscountFactor", "Region",
                    "Currency", "TermReference", "Term"]

    def __init__(self, input_file, output):
        SimpleCSVFeedProcessor.__init__(self, input_file)
        self.input_file = str(input_file).split("\\")[-1]
        self.output_path = str(output)
        self.output_path = self.output_path if self.output_path[-3:] == "csv" else self.output_path+".csv"
        self.record_data = []
        
        getcontext().prec = 14
        
        #Creating calculation spaces to access calculated values
        context = acm.GetDefaultContext()
        self.cs_obs = acm.Calculations().CreateCalculationSpace(context, 'FOrderBookSheet')
        self.cs=acm.Calculations().CreateStandardCalculationsSpaceCollection()
        
        self.prev_option_forw_price = 0
        self.prev_option = None
        self.dis_fact_consist = {}
        self.totem_dct_lst = []
        
        self.strike_minus = 0
        self.strike_type = "Rel Spot Pct 100"
        self.forw_price_multiply = 100
        
        #If file contains equity index underlying change default values
        if "INDEX" in self.input_file:
            self.forw_price_multiply = 1
            self.strike_minus = 100
            self.strike_type = "Rel Spot Pct"
            
        self.prop_val_dict = {"StrikeType":self.strike_type}
        
        
    def _process_record(self, record, dry_run):
        (_index, record_data) = record
        
        try:
            #if a row does not meet column header format then skip
            if None in record_data.values():
                LOGGER.warning("None type recieved")
                return
        
        
            val_date = parse(record_data[self.columns[1]]).date()
            
            exp_date = parse(record_data[self.columns[-11]]).date()
            
            und_name = str(record_data[self.columns[7]])
            
            und_map_name = self.default_und_map[und_name] if und_name in self.default_und_map else und_name[:3]
            
            #Example name: ZAR/EQ/SWIX/Dec22/C/200/TOTEM
            option_name = str(record_data[self.columns[-3]])+"/"\
                    +str(record_data[self.columns[2]])+"/"\
                    +und_map_name+"/"\
                    +str(exp_date.strftime("%b")) \
                    + str(exp_date.year)[-2:]+"/"\
                    +str(record_data[self.columns[-9]])[0]+"/"\
                    +str(int(record_data[self.columns[-10]]))+"/"+"TOTEM"
            
            self.prop_val_dict["Name"] = option_name
            self.prop_val_dict["Underlying"] = str(record_data[self.columns[-3]])+"/"+und_map_name
            self.prop_val_dict["ExpiryDate"] = exp_date.isoformat()
            self.prop_val_dict["OptionType"] = str(record_data[self.columns[-9]])
            self.prop_val_dict["StrikePrice"] = str(int(record_data[self.columns[-10]])-self.strike_minus)
            
            num_to_append = 1
            
            #Ensuring that there are no existing instruments that are not options with the same naming convention.
            while acm.FInstrument[self.prop_val_dict['Name']]:
                if isinstance(acm.FInstrument[self.prop_val_dict['Name']], type(acm.FOption())):
                    option = acm.FOption[self.prop_val_dict['Name']]
                    LOGGER.warning("Using existing option %s", option_name)
                    break
                
                self.prop_val_dict['Name'] = self.prop_val_dict['Name'] + str(num_to_append)
                
                num_to_append += 1
            else:
                option = acm.FOption
                option = option(name=self.prop_val_dict['Name'])
                    
            #Ensuring option has the required properties         
            optdec = acm.FOptionDecorator(option, None)
            for property, value in self.prop_val_dict.items():
                optdec.SetProperty(property, value)
            
            optdec.Commit()
            
            und_ins = option.Underlying()
            
            und_ins_calcs = und_ins.Calculation()
            
            option_forw_price = (self.cs_obs.CalculateValue(option, "Price Theor").Number()/
                                self.cs_obs.CalculateValue(option, 'Underlying Spot OTC').Number())*self.forw_price_multiply
            
            discount_fact = 0
            
            #Ensuring discount factors are consistent across maturities
            if "{}{}".format(und_name, str(exp_date)) not in self.dis_fact_consist:
                self.dis_fact_consist["%s%s"%(und_name, exp_date)] = discount_fact =  self.cs_obs.CalculateValue(option, 'Discount Rate')
            else:
                discount_fact = self.dis_fact_consist["%s%s"%(und_name, exp_date)]
            
            #Ensuring from put to call price should increase as we approach ATM and then decrease as we move away from ATM
            if self.prev_option and self.prev_option.OptionType() == option.OptionType() and self.prev_option_forw_price > 0:
                after_comma = len(str(self.prev_option_forw_price).split(".")[1])
                add_sub = Decimal(1) / Decimal(10**after_comma)
                
                if option.OptionType() == "Put" and self.prev_option_forw_price > option_forw_price:
                    option_forw_price = Decimal(self.prev_option_forw_price) + add_sub
                elif option.OptionType() == "Call" and self.prev_option_forw_price < option_forw_price:
                    option_forw_price = Decimal(self.prev_option_forw_price) - add_sub
            
            time_to_exp = self.cs_obs.CalculateValue(option, 'Time to Expiry')
                
            self.prev_option = option
            self.prev_option_forw_price = option_forw_price
            
            for header in self.columns:
                if header == "ClientPrice":
                    record_data[header] = option_forw_price
                elif header in ["ClientReferenceLevel", "ClientImpliedSpot"]:
                    if "ALSI" in und_map_name and header == "ClientReferenceLevel":
                        record_data[header] = und_ins_calcs.TheoreticalPrice(self.cs).Number()
                    else:
                        record_data[header] = self.cs_obs.CalculateValue(option, 'Underlying Spot OTC').Number()
                elif header == "ClientDiscountFactor":
                    record_data[header] = 1/((1+discount_fact)**(float(time_to_exp/365.0)))
                elif header == "ValuationDate":
                    record_data[header] = str(val_date)
                elif header == "ExpiryDate":
                    record_data[header] = str(exp_date)
                    
            self.totem_dct_lst.append(record_data)
        except Exception as ex:
            LOGGER.exception(ex)
            raise
        
    def write_to_csv(self):
        with open(str(self.output_path), 'wb') as output_file:
            #Add StockName column to output if exists in record_data
            if len(self.totem_dct_lst) > 0 and "StockName" in self.totem_dct_lst[0]:
                self.columns.append(self.columns[-1])
                self.columns[-2] = "StockName"
                
            dict_writer = csv.DictWriter(output_file, fieldnames=self.columns)
            dict_writer.writeheader()
            dict_writer.writerows(self.totem_dct_lst)
            
        LOGGER.info( "Successfully saved records! File saved: {}".format(self.output_path))
        
def ael_main(ael_dict):
    input_file = str(ael_dict['input_file'])
    output_file = str(ael_dict['output_file'])
    
    LOGGER.info("Input file: {}".format(input_file))
    LOGGER.info("Output file: {}".format(input_file))
    
    totem_file = TotemDataSubmissionCSV(input_file, output_file)
    totem_file.process(False)
    
    totem_file.write_to_csv()
