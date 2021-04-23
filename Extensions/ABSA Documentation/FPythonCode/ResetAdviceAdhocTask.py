"""
-------------------------------------------------------------------------------
MODULE
    ResetAdviceAdhocTask


DESCRIPTION
    Task to generate adhoc confirmations and advices for IRS. Based on the date 
    range and document option  suplied the task will generate a document according to 
    the business rules defined for IRS Presettlement Advices and Confirmations

HISTORY
===============================================================================
2018-08-21   Tawanda Mukhalela   FAOPS:168  initial implementation
-------------------------------------------------------------------------------
"""

import acm
import ael

from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from ResetAdviceCreator import ResetAdviceGenerator
from ResetConfirmationTask import generate_confirmation
from ResetConfirmationEventHooks import VALID_TRADE


LOGGER = getLogger(__name__)
ael_variables = AelVariableHandler()
message_box = acm.GetFunction('msgBox', 3)

ael_variables.add(
    'Option',
    label='Document Type',
    cls='string',
    collection=['IRS Presettlement Advice', 'IRS Presettlement Confirmation'],
    default='IRS Presettlement Advice',
    mandatory=True,
    alt=" Document Type")
    
ael_variables.add(
    'Trades',
    label='Trade(s) Selection',
    cls=acm.FTrade,
    collection=None,
    mandatory=True,
    multiple=True,
    alt=" Date of reset")

ael_variables.add(
    'from_date',
    label='From Date',
    cls='date',
    collection=None,
    mandatory=True,
    alt=" Date of reset")

ael_variables.add(
    'to_date',
    label='To Date',
    cls='date',
    collection=None,
    mandatory=True,
    alt=" Date of reset")
    

def ael_main(dict_param):
    try:
        if dict_param["Trades"]: 
            from_date = dict_param["from_date"].to_string(ael.DATE_ISO)
            to_date = dict_param["to_date"].to_string(ael.DATE_ISO)                
            adhock = True
            days_to_generate = ael.date(from_date).days_between(ael.date(to_date)) 
            found = False
            message = ''
            for trade in dict_param["Trades"]:
                for count in range(days_to_generate+1):                    
                    date = acm.Time.DateAddDelta(from_date, 0, 0, count)
                    print(date, dict_param["Option"] == 'IRS Presettlement Advice')
                    if dict_param["Option"] == 'IRS Presettlement Advice':
                        for reset in get_resets(trade, 'Advice'):
                            if reset.Day() == date:
                                found = True
                                ResetAdviceGenerator(trade, date, to_date, adhock).generate_advice()
                            
                    elif dict_param["Option"] == 'IRS Presettlement Confirmation':
                        if VALID_TRADE(trade):
                            pay_leg = trade.Instrument().PayLeg()
                            rec_leg = trade.Instrument().RecLeg()
                            pay_leg_cash_flows = None
                            rec_leg_cash_flows = None
                            if pay_leg.IsFloatLeg():
                                pay_leg_cash_flows = acm.FCashFlow.Select('leg={leg} and payDate={pay_date}'.format(
                                        leg=pay_leg.Oid(), pay_date=date))
                            if rec_leg.IsFloatLeg():
                                rec_leg_cash_flows = acm.FCashFlow.Select('leg={leg} and payDate={pay_date}'.format(
                                        leg=rec_leg.Oid(), pay_date=date))
                            dates = []
                            if pay_leg_cash_flows:
                                dates.extend(get_reset_days(pay_leg_cash_flows))
                            if rec_leg_cash_flows:
                                dates.extend(get_reset_days(rec_leg_cash_flows))
                            found = True
                            if len(dates) > 1:
                                generate_confirmation(trade, dates[0], dates[1])
                            generate_confirmation(trade, dates[0], dates[0])
                        message = 'Trade not Valid for Presettlement Advice Creation : '

                message += 'No Reset(s) or Confirmation(s) found for the date range supplied'
                if not found:
                    return message_box('IRS PreSettlement Advices', message, 1) == 1

    except Exception as exception:
        LOGGER.exception(exception)
        raise


def get_resets(trade, option):
    """
    Gets all Resets
    """
    all_resets = []
    legs = trade.Instrument().Legs()
    for leg in legs:
        if leg.IsFloatLeg():
            for cf in leg.CashFlows():
                for reset in cf.Resets():
                    all_resets.append(reset)

    return all_resets


def get_reset_days(cashflows):
    """
    Get all valid reset days
    """
    reset_dates = [cash_flow.Resets()[-1].Day()
                   for cash_flow in cashflows
                   if cash_flow.CashFlowType() == 'Float Rate']

    return reset_dates


def run_script(extension_invocation_info):
    """
    Function used for executing the script from a menu
    extension.
    """
    acm.RunModuleWithParameters(__name__, acm.GetDefaultContext())



