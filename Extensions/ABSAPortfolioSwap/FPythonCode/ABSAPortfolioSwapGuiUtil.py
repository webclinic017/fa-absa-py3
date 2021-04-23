"""-----------------------------------------------------------------------
MODULE
    ABSAPortfolioSwapGuiUtil

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : GUI Utility functions used by the PortfolioSwap scipts.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Herman Hoon
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import ael

INCEPTION               = ael.date('1970-01-01')
TODAY                   = ael.date_today()
FIRSTOFYEAR             = TODAY.first_day_of_year()
FIRSTOFMONTH            = TODAY.first_day_of_month()
PREVBUSDAY              = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -1) 
TWOBUSDAYSAGO           = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -2) 
FIVEBUSDAYSAGO          = TODAY.add_banking_day(ael.Calendar['ZAR Johannesburg'], -5)
TWODAYSAGO              = TODAY.add_days(-2)
YESTERDAY               = TODAY.add_days(-1)

StartDateList   = { 'Inception':INCEPTION.to_string(ael.DATE_ISO),\
                    'First Of Year':FIRSTOFYEAR.to_string(ael.DATE_ISO),\
                    'First Of Month':FIRSTOFMONTH.to_string(ael.DATE_ISO),\
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO),\
                    'TwoBusinessDaysAgo':TWOBUSDAYSAGO.to_string(ael.DATE_ISO),\
                    'FiveBusinessDaysAgo':FIVEBUSDAYSAGO.to_string(ael.DATE_ISO),
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),
                    'Custom Date':TODAY,\
                    'Now':TODAY.to_string(ael.DATE_ISO)} 

EndDateList     = { 'Now':TODAY.to_string(ael.DATE_ISO),\
                    'TwoDaysAgo':TWODAYSAGO.to_string(ael.DATE_ISO),\
                    'PrevBusDay':PREVBUSDAY.to_string(ael.DATE_ISO),\
                    'Yesterday':YESTERDAY.to_string(ael.DATE_ISO),\
                    'Custom Date':TODAY.to_string(ael.DATE_ISO)}

def instrumentQuery(instype=()):
    # Create empty question or get default question for certain class
    q = acm.CreateFASQLQuery(acm.FInstrument, 'AND')
    
    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Name', 'RE_LIKE_NOCASE', None)

    # enum
    op = q.AddOpNode('OR')
    if instype:
        for i in instype:
            op.AddAttrNode('InsType', 'EQUAL', ael.enum_from_string('InsType', i))
    else:
        op.AddAttrNode('InsType', 'EQUAL', None)

    # integer field
    op = q.AddOpNode('AND')
    op.AddAttrNode('Trades.Oid', 'GREATER_EQUAL', None)
    op.AddAttrNode('Trades.Oid', 'LESS_EQUAL', None)

    # Text field
    op = q.AddOpNode('OR')
    op.AddAttrNode('Trades.Portfolio.Name', 'EQUAL', None)
    
    # enum
    op = q.AddOpNode('OR')
    op.AddAttrNode('Trades.status', 'EQUAL', None)

    return q



