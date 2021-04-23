"""-----------------------------------------------------------------------
MODULE
    ABSAGeneratePortfolioSwap

    Created from FSEQGeneratePortfolioSwap

DESCRIPTION
    Institutional CFD Project

    Date                : 2010-10-23
    Purpose             : GUI for the ABSAPortfolioSwap module.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Micheal Klimke, Herman Hoon
    CR Number           : 455227

HISTORY
================================================================================
Date       Change no     Developer          Description
--------------------------------------------------------------------------------
2014-11-20 CHG0002450799 Pavel Saparov      Fixing errors and exception handling
2019-08-05 FAU-324       Tibor Reiss        Adjust for Upgrade2018
2019-09-19 FAU           Tibor Reiss        Remove dividendFix
2019-10-03 FAU-454       Tibor Reiss        Set nominal scaling on dividend leg
-----------------------------------------------------------------------"""

import time

import acm
import ael
import FBDPGui
from at_logging import getLogger, bp_start

import ABSAPortfolioSwap
import importlib
importlib.reload(ABSAPortfolioSwap)
import ABSAPortfolioSwapGuiUtil
importlib.reload(ABSAPortfolioSwapGuiUtil)
import ABSAPortfolioSwapUtil as Util
importlib.reload(Util)


LOGGER = getLogger()


def NameComp(x, y):
    if x.Name().upper() > y.Name().upper():
        return 1
    elif x.Name().upper() < y.Name().upper():
        return -1
    return 0


def SortByName(collection):
    collection.sort(NameComp)


def isDividendLeg(leg):
    if leg and leg.PayLeg() and leg.LegType() == 'Fixed':
        return True
    else:
        return False


def fix_upgrade_2018(pswap):
    # UPGRADE to 2018.4
    # 1. Automatically created cashflows with type "Fixed Rate" need to be deleted
    # 2. On funding cash flow, Nominal Scaling and Simple Overnight resets are automatically
    #    created if there are no resets, thus the first Return reset with 0.0 value needs to
    #    be generated.
    #    Note: we are taking advantage here of the fact that funding on the start date of the
    #          pswap should be always 0.0
    # 3. The "Total Return" leg's cashflow is automatically generated in AddNewLegs ->
    #    GeneratePerSecurityCashFlows with CashFlowType = "Total Return" instead of
    #    "Position Total Return"
    pswap_start_date = pswap.StartDate()
    zar_calendar = acm.FCalendar["ZAR Johannesburg"]
    reset_date = zar_calendar.AdjustBankingDays(pswap_start_date, 0)
    reset_start_date = reset_date
    reset_end_date = zar_calendar.AdjustBankingDays(pswap_start_date, 1)
    for leg in pswap.Legs():
        if isDividendLeg(leg):
            if leg.NominalScaling() != "Dividend":
                leg.NominalScaling("Dividend")
                leg.Commit()
        if leg.LegType() == "Fixed":
            for cf in leg.CashFlows()[:]:
                if cf.CashFlowType() == "Fixed Rate":
                    cf.Delete()
        elif leg.LegType() == "Total Return":
            for cf in leg.CashFlows():
                if cf.CashFlowType() == "Total Return":
                    try:
                        cf.CashFlowType("Position Total Return")
                        cf.Commit()
                    except Exception as e:
                        cf.Undo()
                        LOGGER.error("Could not change cashflow type from \"Total Return\""
                                     " to \"Position Total Return\" for cf {} leg {}"
                                     " indexref {}".format(cf.Oid(), leg.Oid(),
                                     leg.IndexRef().Name()))
                        raise RuntimeError(e)
        elif leg.LegType() == "Float":
            for cf in leg.CashFlows():
                old_funding_resets = []
                new_funding_reset = False
                if cf.CashFlowType() == "Float Rate":
                    for reset in cf.Resets():
                        if reset.ResetType() in ["Nominal Scaling", "Simple Overnight"]:
                            old_funding_resets.append(reset)
                        if reset.ResetType() == "Return":
                            new_funding_reset = True
                    acm.BeginTransaction()
                    try:
                        if not new_funding_reset:
                            new_reset = acm.FReset()
                            new_reset.CashFlow(cf)
                            new_reset.ResetType("Return")
                            new_reset.Day(reset_date)
                            new_reset.StartDate(reset_start_date)
                            new_reset.EndDate(reset_end_date)
                            new_reset.FixingValue(0.0)
                            new_reset.ReadTime(acm.Time.TimeNow())
                            new_reset.Commit()
                        for reset in old_funding_resets[:]:
                            reset.Delete()
                        acm.CommitTransaction()
                    except Exception as trans_error:
                        acm.AbortTransaction()
                        LOGGER.error("Could not delete resets for leg {}".format(leg.Oid()))
                        raise RuntimeError(trans_error)


today = acm.Time.DateToday()
calendars = [calendar for calendar in acm.FCalendar.Select("")]
daycountMethods = [e for e in acm.FEnumeration["enum(DaycountMethod)"].Enumerators() if str(e) != "None"]
paydayOffsetMethods = [e for e in acm.FEnumeration["enum(BusinessDayMethod)"].Enumerators() if str(e) != "None"]
SortByName(calendars)
daycountMethods.sort()
paydayOffsetMethods.sort()

ttTerminate = 'If toggled, the portfolio swap will be terminated and the end return resets will be fixed.'
ttPfSwap = 'Portfolio swap instrument(s)'
ttRollingBaseDay = 'The start day of the first rolling period (portfolio swap start date is default)'
ttFixPeriod = 'Use fix period lengths without adjustment for weekends'
ttPaydayOffset = 'The number of banking days from cash flow end day until cash flow pay day'
ttpaydayOffsetMethod = 'Defines how weekends should be handled when calculating cash flow pay day'

ttStartDate = 'The start date (inclusive) of the Portfolio Swap generate script.'
ttStartDateCustom = 'Custom start date.'
ttEndDate = 'The end date (inclusive) of the Portfolio Swap generate script.'
ttEndDateCustom = 'Custom end date.'

psquery = ABSAPortfolioSwapGuiUtil.instrumentQuery(instype=('Portfolio Swap',))
StartDateList = ABSAPortfolioSwapGuiUtil.StartDateList
EndDateList = ABSAPortfolioSwapGuiUtil.EndDateList

class PortfolioSwapVariables(FBDPGui.AelVariables):
    def __init__(self):
        # [fieldId, fieldLabel, fieldType, fieldValues, defaultValue,
        # isMandatory, insertItemsDialog, toolTip, callback, enabled]
        self.ael_variables = [
            ['startDate', 'Start Date', 'string', StartDateList.keys(), 'Yesterday', 1, 0, ttStartDate],
            ['startDateCustom', 'Start Date Custom', 'string', None, StartDateList['Yesterday'], 1, 0, ttStartDateCustom],
            ['endDate', 'End Date', 'string', EndDateList.keys(), 'Now', 1, 0, ttEndDate],
            ['endDateCustom', 'End Date Custom', 'string', None, EndDateList['Now'], 1, 0, ttEndDateCustom],

            ['terminate', 'Terminate Swap_Termination', 'int', [0, 1], 0, 0, 0, ttTerminate],
            ['portfolioSwaps', 'Portfolio Swap(s)_Parameters', 'FInstrument', None, psquery, 1, 1, ttPfSwap],

            ['calendar', 'Reset calendar_Parameters', 'FCalendar', calendars, 'ZAR Johannesburg', 1, 0],
            ['daycountMethod', 'Day count method_Parameters', 'string', daycountMethods, 'ACT/365', 1, 0],
            ['rollingBaseDay', 'Rolling base day_Parameters', 'string', None, '', 0, 0, ttRollingBaseDay],
            ['isFixPeriod', 'Fix Period_Parameters', 'int', [0, 1], 0, 0, 0, ttFixPeriod],
            ['paydayOffset', 'Payday offset_Parameters', 'dateperiod', None, '0d', 1, 0, ttPaydayOffset],
            ['paydayOffsetMethod', 'Pay Offset Method_Parameters', 'enum(BusinessDayMethod)', paydayOffsetMethods, 'Following', 1, 0, ttpaydayOffsetMethod],

            ['payOrReceive', 'Total return leg pay or receive_Parameters', 'string', ['Pay', 'Receive'], 'Pay', 0, 0],
            ['clientName', 'Short name', 'string', None, 'CLIENT', 0, 0]
        ]

        FBDPGui.AelVariables.__init__(self, *self.ael_variables)


def ValidatePfSwap(pfSwap, resetStartDate, resetEndDate):
    isValidInput = True
    pfSwapName = pfSwap.Name()
    pfsEndDate = pfSwap.ExpiryDate()

    if "Terminated" == pfSwap.OpenEnd():
        LOGGER.error("ERROR: %s will not be fixed: Portfolio swap is terminated.", pfSwapName)
        isValidInput = False

    if not pfSwap.FundPortfolio():
        LOGGER.error("ERROR: %s will not be fixed: No valid portfolio selected.", pfSwapName)
        isValidInput = False

    if acm.Time.DateDifference(resetStartDate, resetEndDate) > 0:
        LOGGER.error("ERROR: %s will not be fixed: Does not start within or before the reset period.", pfSwapName)
        isValidInput = False

    if "Open End" != pfSwap.OpenEnd() and acm.Time.DateDifference(resetEndDate, pfsEndDate) > 0:
        LOGGER.error("ERROR: %s will not be fixed: Can not generate resets after portfolio swap end date.", pfSwapName)
        isValidInput = False

    if pfSwap.add_info('PSONPremIndex') == '':
        LOGGER.error("ERROR: %s will not be fixed: No Overnight Premium Index defined.", pfSwapName)
        isValidInput = False

    floatRef = acm.FRateIndex[pfSwap.add_info('PSONPremIndex')]
    if floatRef == None:
        LOGGER.error("ERROR: %s will not be fixed: Overnight Premium is not a Rate Index.", pfSwapName)
        isValidInput = False

    return isValidInput


ael_variables = PortfolioSwapVariables()


def ael_main(dictionary):
    process_name = "ps.generate.{0}".format(dictionary["clientName"])
    with bp_start(process_name):
        terminate = dictionary["terminate"]
        pfSwaps = dictionary["portfolioSwaps"]
        previousPfSwap = None
        calendar = dictionary["calendar"]
        daycountMethod = dictionary["daycountMethod"]
        rollingBaseDay = dictionary["rollingBaseDay"]
        isFixPeriod = dictionary["isFixPeriod"]
        paydayOffset = dictionary["paydayOffset"]
        paydayOffsetMethod = dictionary["paydayOffsetMethod"]
        payOrReceive = dictionary["payOrReceive"]
        spreadLong = 0.0
        spreadShort = 0.0

        if dictionary['startDate'] == 'Custom Date':
            resetStartDate = ael.date(dictionary['startDateCustom'])
        else:
            resetStartDate = ael.date(StartDateList[dictionary['startDate']])

        if dictionary['endDate'] == 'Custom Date':
            resetEndDate = ael.date(dictionary['endDateCustom'])
        else:
            resetEndDate = ael.date(EndDateList[dictionary['endDate']])

        if acm.Time.DateDifference(resetStartDate, resetEndDate) > 0:
            LOGGER.error("ERROR: Start date can not be later than end date. Please check reset dates.")
            return

        if acm.Time.DateDifference(resetEndDate, acm.Time.DateToday()) > 0:
            LOGGER.error("ERROR: Can not generate resets later than today's date. Please select an earlier to date.")
            return

        if calendar.IsNonBankingDay(None, None, resetStartDate):
            resetStartDate = calendar.ModifyDate(None, None, resetStartDate)
            LOGGER.warning("WARNING: Fixing will begin on the first banking day in the period: %s.", resetStartDate)

        returnLegIsPayLeg = ("Pay" == payOrReceive) and True or False
        has_errors = False

        LOGGER.info("INFO: Portfolio Swaps will be fixed from %s to %s", resetStartDate, resetEndDate)

        for pfSwap in pfSwaps:
            acm.Log('---------------------------------------------------------')
            # use Exception handling when running multiple portfolio swaps in sequence
            try:
                pfSwapName = pfSwap.Name()
                pfsStartDate = pfSwap.StartDate()
                if not rollingBaseDay:
                    rollingBaseDay = pfsStartDate
                localResetStartDate = resetStartDate

                # Set reset start date to PSwap Start Date if the resetStartDate is before the pfsStartDate
                if acm.Time.DateDifference(resetStartDate, pfsStartDate) < 0:
                    localResetStartDate = pfsStartDate

                # Logic to determine if the PSwap needs to be regenerated if the pfsStartDate falls in the reset period
                if acm.Time.DateDifference(pfsStartDate, localResetStartDate) >= 0 \
                        and acm.Time.DateDifference(pfsStartDate, resetEndDate) <= 0:
                    regenerate = True
                else:
                    regenerate = False

                if ValidatePfSwap(pfSwap, localResetStartDate, resetEndDate):
                    floatRef = acm.FRateIndex[pfSwap.add_info('PSONPremIndex')]

                    pfsParameters = Util.PortfolioSwapParameters({
                        "portfolioSwap" : pfSwap,
                        "previousPfSwap" : previousPfSwap,
                        "floatRef" : floatRef,
                        "calendar" : calendar,
                        "daycountMethod" : daycountMethod,
                        "rollingBaseDay" : rollingBaseDay,
                        "isFixPeriod" : isFixPeriod,
                        "paydayOffset" : paydayOffset,
                        "paydayOffsetMethod" : paydayOffsetMethod,
                        "spreadLong" : spreadLong,
                        "spreadShort" : spreadShort,
                        "returnLegIsPayLeg" : returnLegIsPayLeg
                    })

                    # If no trades have been booked into the underlying portfolio (hence no
                    # legs on the pswap) then this error check mustn't be run and legs will
                    # be generated from the start date of the pswap when the client starts trading.
                    pswapLegs = pfSwap.Legs()
                    if "Open End" == pfSwap.OpenEnd() \
                            and pswapLegs \
                            and not ABSAPortfolioSwap.CheckEndReturnResets(pfsParameters, localResetStartDate):
                        LOGGER.error("ERROR: The Portfolio Swap (Open ended) has not been extended "
                                     "until the selected from date and cannot be extended from this "
                                     "date. Please select an earlier from date or, if necessary, "
                                     "regenerate the Portfolio Swap from start.")
                        continue

                    if terminate:
                        LOGGER.info('INFO: Terminating %s', pfSwapName)
                        ABSAPortfolioSwap.TerminatePortfolioSwap(pfsParameters)
                    else:
                        if regenerate:
                            LOGGER.info('INFO: Regenerating %s from %s to %s',
                                        pfSwapName, localResetStartDate, resetEndDate)
                            ABSAPortfolioSwap.GeneratePortfolioSwap(pfsParameters)
                        else:
                            LOGGER.info('INFO: Fixing %s from %s to %s',
                                        pfSwapName, localResetStartDate, resetEndDate)

                            ABSAPortfolioSwap.RestorePortfolioSwapEndDate(pfsParameters, resetEndDate)
                            ABSAPortfolioSwap.AddNewLegs(pfsParameters, localResetStartDate, resetEndDate)

                            ABSAPortfolioSwap.ClearResetsFromDateUntilEnd(pfsParameters, localResetStartDate, True)
                            ABSAPortfolioSwap.ClearCashFlowsFromDateUntilEnd(pfsParameters, localResetStartDate)
                            ABSAPortfolioSwap.ClearPaymentsFromDateUntilEnd(pfSwap, localResetStartDate)

                        acm.PollDbEvents()
                        fix_upgrade_2018(pfSwap)

                        t0 = time.time()
                        acm.PollDbEvents()
                        ABSAPortfolioSwap.PerformDailyUpdatesInPeriod(pfsParameters, localResetStartDate, resetEndDate)
                        LOGGER.info('INFO: Daily fixing took %s minutes', (time.time() - t0) / 60)
            except Exception:
                name = pfSwap.Name() if hasattr(pfSwap, 'Name') else pfSwap
                LOGGER.exception('ERROR: Portfolio swap %s was not fixed.', name)
                has_errors = True

        if has_errors:
            msg = 'Some portfolio swaps were not correctly fixed (see the log for more details).'
            raise RuntimeError(msg)
        else:
            LOGGER.info('Completed successfully')

# Added so that this module can be executed from a Menu Extension
def startRunScript(eii):
    acm.RunModuleWithParameters('ABSAGeneratePortfolioSwap', acm.GetDefaultContext())
