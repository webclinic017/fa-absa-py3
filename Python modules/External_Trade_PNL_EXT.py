'''
--------------------------------------------------------------------------------
# Purpose                       :  The code runs a predefined task, setting
#                                  'Profit/Loss: End Date Custom' to each day
#                                  in the current month. A report is generated
#                                  for each day in the current month.
#                                  For that reason, this code must run on the
#                                  last day of the relevant month. Code created to resolve JIRA FTF-241
#                                
# Department and Desk           :  PCG TREASURY FINANCE
# Requester                     :  James Moodie
# Developer                     :  Khaya Mbebe
# CR Number                     :  CHG1001558615
-----------------------------------------------------------------------------------
''' 

import acm
import FLogger

ael_variables = []

def ael_main(ael_dict):
    error_count = 0
    today = acm.Time.DateToday()
    report_date = acm.Time.FirstDayOfMonth(today)
    report_date = acm.Time.DateAddDelta(report_date, 0, 0, -1) #The last day of the previous month is required
    days_in_month = acm.Time.DaysInMonth(today)
    task = acm.FAelTask['External_Trade_PnL_EXT_Report_SERVER']
    file_name = task.Parameters().At("File Name")
    file_path = task.Parameters().At("File Path")
    task_name = task.Name()
    temp_dict = task.Parameters()

    logger = FLogger.FLogger(logToFileAtSpecifiedPath = file_path + '/log.txt')
    logger.LOG(task_name + ' started.')

    for day in range(days_in_month + 1):                        #The last day of the previous month is required
        date_file_name = file_name[:-10] + report_date
        temp_dict.AtPut("File Name", date_file_name)
        temp_dict.AtPutStrings("FTradeSheet_Portfolio Profit Loss End Date Custom", report_date)
        task.Parameters(temp_dict)
        try:
            task.Commit()
            task.Execute()
        except Exception, e:
            error_count += 1
            logger.ELOG(e, exc_info=1)
        logger.LOG(date_file_name + ' written to ' + file_path)
        report_date = acm.Time.DateAddDelta(report_date, 0, 0, 1)
        
    logger.LOG(task_name + ' complete. ' + str(days_in_month + 1) + \
                ' files processed with ' + str(error_count) + ' errors.')

