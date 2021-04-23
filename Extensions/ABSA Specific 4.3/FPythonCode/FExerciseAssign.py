""" Compiled: 2011-06-29 20:34:26 """

"""----------------------------------------------------------------------------
MODULE
    FExerciseAssign - Script for exercising or assigning positions in options
    and warrants that are not handled manually or from an exchange

DESCRIPTION
    This module exercises or assigns positions in options and warrants that
    are not automatically handled from an exchange or manually exercised,
    such as OTC instruments, instruments from other markets than EUREX, or
    American type derivatives.


    A. Cash settled instruments
    If the derivative is in-the-money and Cash settled, the derivative is
    closed at the intrinsic value, i.e. at
    price = settlement price - strike price
    The premium is set accordingly.

    B. Physically settled instruments
    If the derivative is in-the-money and Physically settled, trades in
    both the underlying security and the derivative are entered.
    There are 2 modes to choose between (this is chosen in the variable
    window):

    1. Market mode:
    The trade in the underlying security is done to the market price
    (the settlement price).
    The closing derivative trade carries the difference between the
    strike price and the settlement price, i.e.
    price = settlement price - strike price

    2. Strike mode:
    The trade in the underlying security is done at the strike price.
    The closing derivative trade gets the price and premium zero.

    Trade status is set to Exercise for long positions and Assign for
    short.

    NOTE! Abandon is performed in this script if the derivative is
    out-of-the-money. In this case the trade is made at price and premium 0,
    and the trade status is set to Abandon.

    NOTE! This script is not intended to run as a batch job.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

#Import Front modules
import acm
import FBDPGui
reload(FBDPGui)

if  __name__ == '__main__':
    print 'Running FExerciseAssign from the platform has not been '\
        'implemented, Must be run from within the client.'
else:

    # Tool Tip
    ttDoExeAss = "Generate exercise and assignment transactions to close in-the-money positions"
    ttDoAbandon =  "Generate abandon transactions to close out-of-the-money positions"
    ttsettle_price = "If defined, this price will be used instead of the underlying's settlement-"\
                     "price per expiration date. Should be expressed in the quote type of the underlying."
    tttrades = "Select the positions that should be handled by the script"
    ttsettlemarket = "The underlying's settlement price will primarely be taken from this Market"
    ttmode = "Defines at what price the derivative position should be closed, and the "\
             "corresponding underlying trade opened"
    ttDoFixPhysicals = ("Fix physically settled futures and options so that the "
    "close-out trade has pay date and acquire date equal to the expiry date of "
    "the future/option")

    valid_modes=['Market', 'Strike']

    # Fill in smart default values
    smarkets = map(lambda x: x.Name(), acm.FMTMMarket.Select(''))

    q = FBDPGui.insertTrades(expiryEnd='0d', expiryStart='1900-01-01')

    defaultMode = 'Strike'
    try:
        import FBDPHook
        reload(FBDPHook)
        defaultMode = FBDPHook.exercise_mode(1) and 'Strike' or 'Market'
    except:
        pass

    ael_variables = FBDPGui.TestVariables(
        ('DoExeAss', 'Do Exercise Assign', 'int', ['1', '0'], 1, 1, 0, ttDoExeAss),
        ('DoAbandon', 'Do Abandon', 'int', ['1', '0'], 1, 1, 0, ttDoAbandon),
        ('settle_price', 'Settle Price', 'string', '', '', 0, None, ttsettle_price),
        ('trades', 'Positions', 'FTrade', None, q, 2, 1, tttrades),
        ('settlemarket', 'Name of Settlement Market', 'string', smarkets, \
            FBDPGui.getMtMMarket(), 2, None, ttsettlemarket),
        ('mode', 'Mode', 'string', valid_modes, defaultMode, 2, None, ttmode),
        ('DoFixPhysicals', 'Fix physically settled futures/options', 'int', ['1', '0'], 1, 1, 0, ttDoFixPhysicals))

    def ael_main(dictionary):
        import FBDPString
        reload(FBDPString)
        logme = FBDPString.logme
        ScriptName = "Exercise Assign"
        logme.setLogmeVar(ScriptName,
                          dictionary['Logmode'],
                          dictionary['LogToConsole'],
                          dictionary['LogToFile'],
                          dictionary['Logfile'],
                          dictionary['SendReportByMail'],
                          dictionary['MailList'],
                          dictionary['ReportMessageType'])

        import FBDPCommon
        reload(FBDPCommon)
        import FBDPRollback
        reload(FBDPRollback)
        import FBDPCalculatePosition
        reload(FBDPCalculatePosition)
        import FBDPInstrument
        reload(FBDPInstrument)
        import FExeAssPerform
        reload(FExeAssPerform)

        dictionary['Positions'] = dictionary['trades'] = FBDPCommon.convertEntityList(dictionary['trades'], dictionary)


        FBDPCommon.execute_script(FExeAssPerform.perform_exercise_assign, dictionary)

