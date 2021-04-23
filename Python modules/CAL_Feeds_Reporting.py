import csv
import os
import CAL_Feeds_Utils
import acm
from datetime import datetime
from SecureConfigReader import SecureConfigReader

csv_init_flag = False
control_init_flag = False
#CONFIG_MODULE = "CAL_Feeds_Config"
CONFIG_MODULE = 'CALConfigSettings'
#reporting_config = CAL_Feeds_Utils.get_ats_config(CONFIG_MODULE, acm.FDhDatabase['ADM'].ADSNameAndPort().lower())

secureConfigReader = SecureConfigReader(CONFIG_MODULE)

directory = secureConfigReader.getElementValue('OutputPath')
report_file_name = secureConfigReader.getElementValue('OutputFileName')
filename_date_format = secureConfigReader.getElementValue('OutputFileDateFormat')

class CalFeedsOutput(object):

    Cal_Column_Headings = ["Trade_Date",
                     "Book_ID",
                     "Book_Name",
                     "Book_System",
                     "Originating_Trade_System",
                     "Trade_ID",
                     "Settlement_Date",
                     "Version_Nbr",
                     "Event_Entry_Time",
                     "CLAS_Flag",
                     "PV",
                     "PV_Delta",
                     "Quantity",
                     "Price",
                     "Trade Side",
                     "Rate",
                     "Trade_Updater_GID",
                     "Trade_Updater_AB",
                     "Trade_Booked_By_GID",
                     "Trade_Booked_By_AB",
                     "CounterParty_SDSID",
                     "Currency",
                     "Otc",
                     "Region_Code",
                     "Amended_Field",
                     "Old_Value",
                     "New_Value",
                     "Event_Entry_Location",
                     "Business_Date",
                     "Capacity_Code",
                     "Trade_Type",
                     "Product_Type",
                     "Product_Description",
                     "Product_Description_Type",
                     "Activity_Ind",
                     "Underlying_Instrument"]
    
    
    def __init__(self):
        
        global directory
        
        csv_dir_path = directory
        
        self.__csv_file_dir_path = csv_dir_path
        self.__csv_file_name = self.get_file_name()
        self.__full_file_path = os.path.join(self.__csv_file_dir_path, self.__csv_file_name + ".csv")
        
        self.__control_file_path = os.path.join(self.__csv_file_dir_path, self.__csv_file_name + ".ctl")

    def initialise_csv_file(self):

        global csv_init_flag
        
        if csv_init_flag == False:
        
            try:
                with open(self.__full_file_path, "rb") as cal_feeds_csv_file:
                    csv_init_flag = True
                    
            except:
                try:
                    with open(self.__full_file_path, "wb") as cal_feeds_csv_file:
                        csv_writer = csv.writer(cal_feeds_csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                        csv_writer.writerow(CalFeedsOutput.Cal_Column_Headings)
                        csv_init_flag = True
                        
                except IOError as e:
                        print(e)

    def initialise_control_file(self):
            
        global control_init_flag
        
        if control_init_flag == False:
            try:
                with open(self.__control_file_path, "r") as control_file:
                    control_init_flag = True
                    
            except:
                try:
                    with open(self.__control_file_path, "wb") as control_file:
                        control_file.write("FILE|%s\nTIMESTAMP|%s\nASOFDATE|%s\nROWS|%s" % (
                            self.__csv_file_name + ".csv",
                            datetime.now().strftime('%Y%m%d-%H:%M:%S'),
                            self.__csv_file_name.split('_')[-1],
                            str(0)))
                        
                except IOError as e:
                        print(e)
                    
    def reset_init_flag(self):
        
        if csv_init_flag == True:
            csv_init_flag = False
            

    @property
    def csv_dir_path(self):
        return self.__csv_file_dir_path

    @csv_dir_path.setter
    def csv_dir_path(self, value):

        if not isinstance(value, str):
            pass

        else:
            self.__csv_file_dir_path = value

    @property
    def csv_file_name(self):
        return self.__csv_file_name

    @csv_file_name.setter
    def csv_file_name(self, value):

        if not isinstance(value, str):
            pass

        else:
            self.__csv_file_name = value
            
    @property
    def csv_file_url(self):
        return self.__full_file_path
            
    def add_row_to_csv(self, row):
        
        assert csv_init_flag == True, "Csv file has not been initialised."
        
        if row:
             with open(self.__full_file_path, "ab") as cal_feeds_csv_file:
                csv_writer = csv.writer(cal_feeds_csv_file, delimiter = ',', quotechar = '"', quoting = csv.QUOTE_MINIMAL)
                csv_writer.writerow(row)
                self.__increment_row_in_control()
    
    def __increment_row_in_control(self):
        
        control_file_lines = []
        
        with open(self.__control_file_path, "r") as control_file:
            control_file_lines = control_file.readlines()
        
        row_count = int(control_file_lines[-1].split('|')[-1].strip())
        row_count += 1
        
        control_file_lines[-1] = '|'.join(["ROWS", str(row_count)]) + "\n"
        #split_lines = control_file_lines[-1].split('|')
        #row_counter = int(split_lines[-1])
        #row_counter += 1
        #split_lines[-1] = str(row_counter)
        
        #control_file_message = "|".join(split_lines)
        #control_file_lines[1] = control_file_message
        
        with open(self.__control_file_path, "wb") as control_file:
            control_file.writelines(control_file_lines)

    def get_reporting_date(self):
        
        from at_time import to_date
        global filename_date_format
        
        return to_date('TODAY').strftime(filename_date_format)
        
    def get_file_name(self):
        
        global report_file_name
        
        return report_file_name + self.get_reporting_date()   
    
