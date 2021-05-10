# Config Month end dates
#-------------------------------------
import ael, acm, datetime
ael_variables = []

def ael_main(parameter):

    CurrentDate               = datetime.date.today()
    CurrentDate_Day           = -int(CurrentDate.strftime("%d"))
    CurrentDate_DayDifference = datetime.timedelta(days=(CurrentDate_Day))
    ReportEndDate             = CurrentDate + CurrentDate_DayDifference

    StartDate_Day             = -int(ReportEndDate.strftime("%d"))
    StartDate_DaysDifference  = datetime.timedelta(days=(StartDate_Day))
    ReportStartDate           = ReportEndDate + StartDate_DaysDifference

    # Changing parameters on a task
    #-------------------------------------

    task = acm.FAelTask['TradeRep_PLDerecog_SERVER']
    params = task.Parameters()
    params.AtPutStrings('FTradeSheet_overrideSheetSettings', True)
    params.AtPutStrings('FTradeSheet_Portfolio Profit Loss Start Date', 'Custom Date')
    params.AtPutStrings('FTradeSheet_Portfolio Profit Loss End Date', 'Custom Date')

    params.AtPutStrings('FTradeSheet_Portfolio Profit Loss Start Date Custom', str(ReportStartDate))
    params.AtPutStrings('FTradeSheet_Portfolio Profit Loss End Date Custom', str(ReportEndDate))
    c = task.Clone()
    c.Parameters(params)
    task.Apply(c)
    task.Commit()

