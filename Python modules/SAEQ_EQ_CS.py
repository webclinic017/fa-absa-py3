# -------------------------------------
# PURPOSE                 :  Used in SAEQ_Equity_CostStructure to get first day of month and current date
# DEPATMENT AND DESK      :  Prime Services
# REQUESTER               :  James Jackson
# DEVELOPER               :  Douglas Finkel
# CR NUMBER               :  C000000614955
# -------------------------------------

import ael, acm, datetime

def SAEQ_EQ_CS_MTD(temp,DateOption,*rest):
    ReportEndDate               = datetime.date.today()
    CurrentDate_DayDifference   = datetime.timedelta(days=(-int(ReportEndDate.strftime("%d"))+1))
    ReportStartDate             = ReportEndDate + CurrentDate_DayDifference

    if DateOption == 'ReportStartDate':
        return str(ReportStartDate)
    elif DateOption == 'ReportEndDate':
        return str(ReportEndDate)
    else:
        return str(DateOption)
