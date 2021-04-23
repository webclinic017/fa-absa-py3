"""-----------------------------------------------------------------------
MODULE
    ABSAPSSweep

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Sweeps the daily TPL from the Portolfio Swap to the Call Account.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael
from collections import defaultdict
import os

import ABSAPortfolioSwapCustom
reload(ABSAPortfolioSwapCustom)
import ABSAPortfolioSwapGuiUtil
reload(ABSAPortfolioSwapGuiUtil)
import FCallDepositFunctions
import SAGEN_IT_Functions
from at_logging import  getLogger, bp_start
from at_report import CSVReportCreator
from at_time import acm_date
from PS_Functions import get_pb_call_account


LOGGER = getLogger(__name__)


'''================================================================================================
================================================================================================'''
ttStartDate = 'The start date (inclusive) of the sweeping script.'
ttEndDate = 'The end date (inclusive) of the sweeping script.'
ttStartDateCustom = 'Custom start date.'
ttEndDateCustom = 'Custom end date.'
ttPfSwap = 'Portfolio swap instrument(s) that will be sweeped.'

StartDateList = ABSAPortfolioSwapGuiUtil.StartDateList
EndDateList = ABSAPortfolioSwapGuiUtil.EndDateList
psquery = ABSAPortfolioSwapGuiUtil.instrumentQuery(instype=('Portfolio Swap',))

# [fieldId, fieldLabel, fieldType, fieldValues, defaultValue, isMandatory, insertItemsDialog, toolTip, callback, enabled]
ael_variables = \
[
    ['startDate', 'Start Date', 'string', StartDateList.keys(), 'Yesterday', 1, 0, ttStartDate],
    ['startDateCustom', 'Start Date Custom', 'string', None, StartDateList['Yesterday'], 1, 0, ttStartDateCustom],
    ['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 1, 0, ttEndDate],
    ['endDateCustom', 'End Date Custom', 'string', None, EndDateList['Now'], 1, 0, ttEndDateCustom],
    ['portfolioSwaps', 'Portfolio Swap(s)', 'FInstrument', None, psquery, 1, 1, ttPfSwap],
    ['clientName', 'Short name', 'string', None, 'CLIENT', 1, 0],
    ['output_dir', 'Output dir', 'string', None, 'C:\\Temp2\\', 1, 0, 'Report ouput path', None, 1],
    ['output_filename', 'File Name', 'string', None, 'ValReport', 1, 0, 'Report ouput filename WITHOUT any extension', None, 1]
]
'''================================================================================================

================================================================================================'''
def ael_main(ael_dict):
    process_name = "ps.sweeping.{0}".format(ael_dict['clientName'])
    with bp_start(process_name):
        
        PortfolioSwapList = ael_dict['portfolioSwaps']
    
        if ael_dict['startDate'] == 'Custom Date':
            startDate = ael.date(ael_dict['startDateCustom'])
        else:
            startDate = ael.date(StartDateList[ael_dict['startDate']])
    
        if ael_dict['endDate'] == 'Custom Date':
            endDate = ael.date(ael_dict['endDateCustom'])
        else:
            endDate = ael.date(EndDateList[ael_dict['endDate']])
        
        calendar = acm.FCalendar["ZAR Johannesburg"]
    #------------------------------------------------------------------------------------------------------------
        has_errors = False
        calcSpace = acm.Calculations().CreateCalculationSpace('Standard', 'FPortfolioSheet')
        
        result_totals = []
        
        for PortfolioSwap in PortfolioSwapList:
            try:
                showLegs = acm.FACMServer().GetUserPreferences().ShowLegsInSheet()
                acm.FACMServer().GetUserPreferences().ShowLegsInSheet(True)
    
                PSSweepBaseDay = ael.date(PortfolioSwap.add_info('PSSweepBaseDay'))
                PSSweepFreq = int(PortfolioSwap.add_info('PSSweepFreq'))
                fromDate = startDate   
                SweepDate = get_last_sweepday(PSSweepBaseDay, PSSweepFreq, None, startDate)
                
                CallAccount = get_pb_call_account(PortfolioSwap.Trades()[0].Counterparty())
                              
                while fromDate <= endDate:
                    result = []
                    if SweepDate == fromDate:
                        
                        calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date', 'Custom Date')
                        xDate = SweepDate.add_banking_day(ael.Calendar['ZAR Johannesburg'], (PSSweepFreq * -1))
                        calcSpace.SimulateGlobalValue('Portfolio Profit Loss Start Date Custom', xDate)
                        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date', 'Custom Date')
                        calcSpace.SimulateGlobalValue('Portfolio Profit Loss End Date Custom', SweepDate)
                        
                        TopNode = calcSpace.InsertItem(PortfolioSwap.Trades())
                        calcSpace.Refresh()
    
                        PnlColumn = 'Portfolio Total Profit and Loss'
                        
                        InsIter = TopNode.Iterator().FirstChild()
                        # This is an equivalent to 'Show Legs'.
                        InsIter.Tree().Expand(True)
                        calcSpace.Refresh()
                        TotalTPLOverLegs = 0
                        while InsIter:
                            LegIter = InsIter.Clone().FirstChild()
                            while LegIter:
                                try:
                                    TPL = calcSpace.CreateCalculation(LegIter.Tree(),
                                                                      PnlColumn).Value().Number()
                                    TotalTPLOverLegs += TPL
                                    IndexRef = calcSpace.CreateCalculation(LegIter.Tree(),
                                                                           "Leg Index Ref").Value()
                                    LegDesc = calcSpace.CreateCalculation(LegIter.Tree(),
                                                                          "Leg Description").Value()
                                    
                                    line_item = LineItems(TPL, IndexRef.Name(), LegDesc)
                                    result.append(line_item)
                                    
                                    LOGGER.info("%s %s %s %s", SweepDate, TPL, IndexRef.Name(), LegDesc)
                                except Exception as e:
                                    LOGGER.exception('Could not get TPL for leg %s.', LegIter.Tree().Item().Leg().Oid())
                                    raise
                                LegIter = LegIter.NextSibling()
                            InsIter = InsIter.NextSibling()
                            LOGGER.info("%s %s TPL total: %s", PortfolioSwap.Name(), SweepDate, TotalTPLOverLegs)
                        
                        # MKLIMKE There should only be one trade to the TPL will be based on all the trades if there are more.
                        DailyTPL = TotalTPLOverLegs
                        DailyTPL = DailyTPL * -1
                        Sweep(PortfolioSwap, CallAccount, round(DailyTPL, 6), SweepDate)
                        total_line = TotalLineItem(PortfolioSwap.Name(), SweepDate, "TPL total", round(DailyTPL, 6), result)
                        result_totals.append(total_line)
                            
                        SweepDate = SweepDate.add_banking_day(ael.Calendar['ZAR Johannesburg'], PSSweepFreq)

                    fromDate = fromDate.add_days(1) 
    
                calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date Custom')
                calcSpace.RemoveGlobalSimulation('Portfolio Profit Loss End Date')
                
                
                LOGGER.info('INFO: Portfolio swap %s was swept to %s', PortfolioSwap.Name(), CallAccount.Name())
            except Exception:
                LOGGER.exception('Portfolio swap %s was not swept.', PortfolioSwap.Name())
                has_errors = True
            finally:
                acm.FACMServer().GetUserPreferences().ShowLegsInSheet(showLegs)
            
            file_name = "{0}_{1}_{2}.csv".format(ael_dict["clientName"],
                                                 ael_dict["output_filename"],
                                                 endDate.to_string("%Y%m%d"))
            
            report_file_path = os.path.join(ael_dict["output_dir"], file_name)
        
            report = SweepingReport(report_file_path, result_totals)
            report.create_report()
            LOGGER.info("Wrote secondary output to: %s", report_file_path)

        if has_errors:
            msg = 'Some portfolioswaps haven\'t been swept (see the log for details).'
            raise RuntimeError(msg)
        else:
            LOGGER.info('Completed successfully')
    
'''================================================================================================
================================================================================================'''
def get_last_sweepday(BaseDay, Frequency, PSSweepDayConv, StartDay):
    while BaseDay < StartDay:
        BaseDay = BaseDay.add_banking_day(ael.Calendar['ZAR Johannesburg'], Frequency)
    return BaseDay
'''================================================================================================
================================================================================================'''
def Sweep(PortfolioSwap, CallAccount, TPL, Date):

    if acm.Time().DateDifference(CallAccount.StartDate(), Date) <= 0:  # Cannnot sweep before startdate of Call Account
        DateToday = acm.Time().DateToday()
        if IsCurrentInterestPeriod(CallAccount, Date):
            Total = GetCurrentTotal(PortfolioSwap.Name(), CallAccount, Date)
            if Total != TPL:
                NewAmount = TPL - Total
                LOGGER.info("Date = %s\nTPL = %s\nTot = %s\nSWA = %s", Date, TPL, Total, NewAmount)
                if abs(NewAmount) > 0.009:
                    tradeList = CallAccount.Trades()
                    CashFlow = FCallDepositFunctions.adjust(CallAccount, NewAmount, Date, "Prevent Settlement", None, None, 1, trades=tradeList)
                    if CashFlow: 
                        SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(CashFlow, 'PSCashType', PortfolioSwap.Name())

        else:
            Total = GetTotal(PortfolioSwap.Name(), CallAccount, Date)
            if Total != TPL:
                NewAmount = TPL - Total
                LOGGER.info("Date = %s\nTPL = %s\nTot = %s\nSWA = %s", Date, TPL, Total, NewAmount)
                if abs(NewAmount) > 0.009:
                    NewCF = FCallDepositFunctions.backdate(CallAccount, NewAmount, Date, DateToday, "Prevent Settlement", None, None, 1)
                    if NewCF: 
                        SAGEN_IT_Functions.set_AdditionalInfoValue_ACM(NewCF, 'PSCashType', PortfolioSwap.Name())
'''================================================================================================
================================================================================================'''
def startRunScript(eii):
    acm.RunModuleWithParameters('ABSAPSSweep', acm.GetDefaultContext()) 
'''================================================================================================
================================================================================================'''
def HasAddInfo(ael_Entity, AddInfo):
    for add_info in ael_Entity.additional_infos():
        if add_info.addinf_specnbr.field_name == AddInfo:
            return add_info
    return None
'''================================================================================================
================================================================================================'''
def IsCurrentInterestPeriod(CallAccount, Date):
    NextInsterestDay = CallAccount.NextScheduledInterestDay() 
    LastInterestDay = acm.Time.DateAddDelta(NextInsterestDay, 0, -1, 0)  # Should pass rolling period here?
    if (acm.Time().DateDifference(Date, NextInsterestDay) <= 0) and (acm.Time().DateDifference(Date, LastInterestDay) >= 0): 
        return True
    else:
        return False
'''================================================================================================
================================================================================================'''
def GetTotal(PSName, CallAccount, Date):

    Total = 0
    Leg = CallAccount.Legs()[0]
 
    for CF in Leg.CashFlows():
    
        # NOTE: FixedAmount is PayDay Original TPL Payment  
        if not acm.Time.DateDifference(Date, CF.PayDate()) and CF.add_info('PSCashType') == PSName:  
            Total = Total + round(CF.FixedAmount(), 6)
            
        # NOTE: And Fixed Rate Adjustable is StartDate Adjustment a adjustable
        if not acm.Time.DateDifference(Date, CF.StartDate()) and CF.add_info('PSCashType') == PSName:  
            Total = Total + round(CF.FixedAmount(), 6)

    return Total
'''================================================================================================
================================================================================================'''
def GetCurrentTotal(PSName, CallAccount, Date):

    Total = 0
    Leg = CallAccount.Legs()[0]
 
    for CF in Leg.CashFlows():
    
        if acm.Time().FirstDayOfMonth(Date): 
        
            # NOTE: And Fixed Rate Adjustable is StartDate Adjustment a adjustable
            if acm.Time.DateDifference(Date, CF.PayDate()) == 0 and  CF.StartDate() == '': 
                if CF.add_info('PSCashType') == PSName and CF.CashFlowType() == 'Fixed Amount':  
                    Total = Total + round(CF.FixedAmount(), 6)            
        else:    
            # NOTE: And Fixed Rate Adjustable is StartDate Adjustment a adjustable
            if not acm.Time.DateDifference(Date, CF.StartDate()) and CF.add_info('PSCashType') == PSName:  
                Total = Total + round(CF.FixedAmount(), 6)

    return Total    


#  sweeping report classes
class LineItems(object):
    
    def __init__(self, value, inst_name, value_type):
        self.value = value
        self.inst_name = inst_name
        self.value_type = value_type
    
    def __str__(self):
        return "{0};{1};{2}".join(self.value, self.inst_name, self.value_type)

class TotalLineItem(object):
    
    def __init__(self, portfolio, date, value_type, value, data_lines):
        self.portfolio = portfolio
        self.date = date
        self.value_type = value_type
        self.value = value
        self.data_lines = data_lines
    
    def __str__(self):
        return ";".join([self.portfolio, self.date, self.value_type, self.value])
    
class SweepingReport(CSVReportCreator):
    
    def __init__(self, full_file_path, total_lines):
        file_name = os.path.basename(full_file_path)
        file_name_only = os.path.splitext(file_name)[0]
        file_suffix = os.path.splitext(file_name)[1][1:]
        file_path = os.path.dirname(full_file_path)
        
        self.total_lines = total_lines

        super(SweepingReport, self).__init__(file_name_only,
                                             file_suffix,
                                             file_path)
    
    def _collect_data(self):
        """Collect PnL and cash movement data."""
        rows = defaultdict(lambda: defaultdict(float))
        for total_line in self.total_lines:
            for data_line in total_line.data_lines:
                key = "%s|%s|%s" % (total_line.portfolio, total_line.date, data_line.inst_name)
                rows[key]["Instrument"] = data_line.inst_name + "/CFD"
                rows[key]["Portfolio"] = total_line.portfolio
                rows[key]["Date"] = total_line.date
                rows[key][data_line.value_type] += float(data_line.value)
                rows[key]["Instrument Type"] = "CFD"
                if data_line.value_type not in self._header():
                    LOGGER.warning("Got something new '%s'", data_line.value_type)
        
        for key in rows.keys():
            line = []
            for header_column in self._header():
                line.append(rows[key][header_column])
            self.content.append(line)
                
    def _header(self):
        return ["Portfolio", "Date", "Instrument", "Instrument Type", "Short Premium", "Mtm", "Overnight Premium", "Execution Premium", "Dividend"]
