"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapWrapper

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Wraps and calls the other Portfolio Swap scripts.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import time 

import acm
import ael
import FBDPGui


import ABSAPortfolioSwapMTM
reload(ABSAPortfolioSwapMTM)
import ABSAPortfolioSwapGuiUtil
reload(ABSAPortfolioSwapGuiUtil)
import ABSAGeneratePortfolioSwap
reload(ABSAGeneratePortfolioSwap)
import ABSAPSSweep
reload(ABSAPSSweep)
import ABSAPSTimeSeries
reload(ABSAPSTimeSeries)

from at_logging import getLogger, bp_start

LOGGER = getLogger()

def NameComp(x, y):
    if x.Name().upper() > y.Name().upper():
        return 1
    elif x.Name().upper() < y.Name().upper():
        return -1
    return 0
    
def SortByName(collection):
    collection.sort(NameComp)
 
def get_additional_info_specs():
    List = []
    for Spec in ael.AdditionalInfoSpec.select():
        List.append(Spec.field_name)
    return List


today = acm.Time.DateToday()
calendars = [calendar for calendar in acm.FCalendar.Select("")]
daycountMethods = [e for e in acm.FEnumeration["enum(DaycountMethod)"].Enumerators() \
                    if str(e) != "None"]
paydayOffsetMethods = [e for e in acm.FEnumeration["enum(BusinessDayMethod)"].Enumerators() \
                    if str(e) != "None"]

SortByName(calendars)
daycountMethods.sort()
paydayOffsetMethods.sort()

tttimeseries = 'If toggled, the Time Series values will be updated.'
ttgenerate = 'If toggled, the Portfolio Swap(s) will be generated.'
ttmtm = 'If toggled, the Portfolio Swap(s) MtM will be calulated.'
ttsweeping = 'If toggled, the Portfolio Swap TPL will be sweeped to the Call Account(s).'
ttaddInfo = 'Additional info fields for which the Time Series values will be updated.'

ttStartDate = 'The start date (inclusive) of the Portfolio Swap generate script.'
ttStartDateCustom = 'Custom start date.'
ttEndDate = 'The end date (inclusive) of the Portfolio Swap generate script.'
ttEndDateCustom = 'Custom end date.'

ttTerminate = 'If toggled, the portfolio swap will be terminated and the end return resets will be fixed.'

ttPfSwap = 'Portfolio swap instrument(s)'
ttRollingBaseDay = 'The start day of the first rolling period (portfolio swap start date is default)'
ttFixPeriod = 'Use fix period lengths without adjustment for weekends'
ttPaydayOffset = 'The number of banking days from cash flow end day until cash flow pay day'
ttpaydayOffsetMethod = 'Defines how weekends should be handled when calculating cash flow pay day'

psquery = ABSAPortfolioSwapGuiUtil.instrumentQuery(instype=('Portfolio Swap',))
StartDateList = ABSAPortfolioSwapGuiUtil.StartDateList
EndDateList = ABSAPortfolioSwapGuiUtil.EndDateList

class PortfolioSwapWrapperVariables(FBDPGui.AelVariables):
    def __init__(self):
        # [fieldId, fieldLabel, fieldType, fieldValues, defaultValue, isMandatory, insertItemsDialog, toolTip, callback, enabled]
        self.ael_variables = [
            ['generate', 'Portfolio Swap(s) Generate_Scripts', 'int', [0, 1], 1, 0, 0, ttgenerate],
            ['mtm', 'Portfolio Swap(s) MtM_Scripts', 'int', [0, 1], 1, 0, 0, ttmtm],
            ['sweeping', 'Portfolio Swap(s) Sweeping_Scripts', 'int', [0, 1], 1, 0, 0, ttsweeping],
            
            ['startDate', 'Start Date_Dates', 'string', StartDateList.keys(), 'Yesterday', 1, 0, ttStartDate],
            ['startDateCustom', 'Start Date Custom_Dates', 'string', None, StartDateList['Yesterday'], 1, 0, ttStartDateCustom],
            ['endDate', 'End Date_Dates', 'string', EndDateList.keys(), 'Now', 1, 0, ttEndDate],
            ['endDateCustom', 'End Date Custom_Dates', 'string', None, EndDateList['Now'], 1, 0, ttEndDateCustom],
            
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

    def cBTimeSeries(self, index, fieldValues):
        isTimeseries = '0' != fieldValues[index] and 1 or 0

        self.addInfo.enable(isTimeseries)
        return fieldValues

ael_variables = PortfolioSwapWrapperVariables()


def ael_main(ael_dict):
    process_name = "ps.pswap_wrapper.{0}".format(ael_dict["clientName"])
    with bp_start(process_name):
        
        startDate = ael_dict['startDate']
        endDate = ael_dict['endDate']
    
        if ael_dict['generate']:
            t0 = time.time()
            LOGGER.info('START: Generate Script')
            ABSAGeneratePortfolioSwap.ael_main(ael_dict)
            LOGGER.info('STOP: Generate Script')
            LOGGER.info('Generate script took %s minutes', (time.time() - t0) / 60)
            
        if ael_dict['mtm']:
            t0 = time.time()
            LOGGER.info('START: MTM Script')
            ABSAPortfolioSwapMTM.ael_main(ael_dict)
            LOGGER.info('STOP: MTM Script')
            LOGGER.info('MTM script took %s minutes', (time.time() - t0) / 60)
            
        if ael_dict['sweeping']:
            t0 = time.time()
            LOGGER.info('START: Sweeping Script')
            ABSAPSSweep.ael_main(ael_dict)
            LOGGER.info('STOP: Sweeping Script')
            LOGGER.info('Sweeping script took %s minutes', (time.time() - t0) / 60)
        
'''================================================================================================
================================================================================================'''
def startRunScript(eii):                
    acm.RunModuleWithParameters('ABSAPortfolioSwapWrapper', acm.GetDefaultContext()) 
'''================================================================================================
================================================================================================'''        
