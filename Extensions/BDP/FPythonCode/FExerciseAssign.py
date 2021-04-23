""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/expiration/etc/FExerciseAssign.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
"""----------------------------------------------------------------------------
MODULE
    FExerciseAssign - Script for exercising or assigning positions in options
    and warrants that are not handled manually or from an exchange

DESCRIPTION
    This module exercises or assigns positions in options and warrants that
    are not automatically handled from an exchange or manually exercised, such
    as OTC instruments, instruments from other markets than EUREX, or American
    type derivatives.

    A. Cash settled instruments
    If the derivative is in-the-money and Cash settled, the derivative is
    closed at the intrinsic value, i.e. at
        price = settlement price - strike price.
    The premium is set accordingly.

    B. Physically settled instruments
    If the derivative is in-the-money and Physically settled, trades in both
    the underlying security and the derivative are entered.  There are 2 modes
    to choose between (this is chosen in the variable window):

    1. Market mode:
    The trade in the underlying security is done to the market price (the
    settlement price).  The closing derivative trade carries the difference
    between the strike price and the settlement price, i.e.
        price = settlement price - strike price.

    2. Strike mode:
    The trade in the underlying security is done at the strike price.  The
    closing derivative trade gets the price and premium zero.

    Trade status is set to Exercise for long positions and Assign for short.

    NOTE! Abandon is performed in this script if the derivative is
    out-of-the-money. In this case the trade is made at price and premium 0,
    and the trade status is set to Abandon.

    NOTE! This script is not intended to run as a batch job.

ENDDESCRIPTION
----------------------------------------------------------------------------"""

#Import Front modules
import acm
import FBDPGui
import importlib
importlib.reload(FBDPGui)
import FBDPCustomPairDlg


# Tool Tip
ttDoExeAss = ('Generate exercise and assignment transactions to close '
        'in-the-money positions')
ttDoAbandon = ('Generate abandon transactions to close out-of-the-money '
        'positions')
ttsettle_price = ('If defined, this price will be used instead of the '
        'underlying\'s settlement-price per expiration date. Should be '
        'expressed in the quote type of the underlying.')
tttrades = 'Select the positions that should be handled by the script'
ttsettlemarket = ('The underlying\'s settlement price will primarily be '
        'taken from this Market')
ttmode = ('Defines at what price the derivative position should be closed, '
        'and the corresponding underlying trade opened')
ttInstrument = ('Specify the instruments that will be processed.')
ttCloseAll = ('Close all the positions if checked.')
ttExerciseIfATM = ("Exercise if the option is 'At The Money'")
ttPartialExercise = ('Specify the percentage of partial exercise')

valid_modes = ['Market', 'Strike']

# Fill in smart default values
smarkets = map(lambda x: x.Name(), acm.FMTMMarket.Select(''))


q = FBDPGui.insertTrades(expiryEnd='0d', expiryStart='1900-01-01')

def customDealPkgDialog(shell, params):
    customDlg = \
        FBDPCustomPairDlg.SelectDealPackagesCustomDialog(shell, params)
    return acm.UX().Dialogs().ShowCustomDialogModal(shell,
            customDlg.CreateLayout(), customDlg)

defaultMode = 'Strike'
try:
    import FBDPHook
    importlib.reload(FBDPHook)
    defaultMode = FBDPHook.exercise_mode(1) and 'Strike' or 'Market'
except:
    pass


class FPositionsAndInstrumentsVariables(FBDPGui.FxPositionVariables):

    def __init__(self, *ael_variables):

        ttInstrument = ('Specify the instruments that will be processed.')
        ttDealPackage = ('Specify the deal package oid that will be' \
                         'processed.')

        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        self.createVariable(
                ['trades',
                        'Positions_Positions',
                        'FTrade', None, q,
                        0, 1, tttrades, None, 0])
        self.createVariable(
                ['instruments',
                        'Instrument_Positions',
                        'FInstrument', None, None,
                        0, 1, ttInstrument, self.object_cb])
        self.createVariable(
                ['dealpackage',
                        'Deal Package_Positions',
                        'string', "", "",
                        0, 1, ttDealPackage, self.object_cb, 1,
                        customDealPkgDialog])

        FBDPGui.FxPositionVariables.__init__(self, *ael_variables)

    def object_cb(self, index, fieldValues):
        tt = 'You can only select one type of object.'
        for field in (self.TradeQuery, self.TradeFilter,
                self.TradingPortfolios, self.instruments, self.dealpackage):
            if self[index] != field:
                field.enable(not fieldValues[index], tt)

        if (self.instruments.isEnabled() and
                fieldValues[self.instruments.sequenceNumber]
            or self.TradingPortfolios.isEnabled()
                and fieldValues[self.TradingPortfolios.sequenceNumber]):
            self.instruments.enable(1, tt)
            self.TradingPortfolios.enable(1, tt)
            self.TradeQuery.enable(0, tt)
            self.TradeFilter.enable(0, tt)
            self.dealpackage.enable(0, tt)
        elif (self.dealpackage.isEnabled() and
                fieldValues[self.dealpackage.sequenceNumber]):
            self.instruments.enable(0, tt)
            self.TradingPortfolios.enable(0, tt)
            self.TradeQuery.enable(0, tt)
            self.TradeFilter.enable(0, tt)

        return fieldValues


ael_variables = FPositionsAndInstrumentsVariables(
        # [VariableName,
        #       DisplayName,
        #       Type, CandidateValues, Default,
        #       Mandatory, Multiple, Description, InputHook, Enabled]
        ['DoExeAss',
                'Do Exercise Assign',
                'int', ['1', '0'], 1,
                1, 0, ttDoExeAss],
        ['DoAbandon',
                'Do Abandon',
                'int', ['1', '0'], 1,
                1, 0, ttDoAbandon],
        ['close_all',
                'Close All Positions',
                'int', ['1', '0'], 1,
                1, 0, ttCloseAll],
        ['exercise_if_ATM',
                'Exercise if ATM',
                'int', ['1', '0'], 0,
                0, 0, ttExerciseIfATM],
        ['partial_exercise',
                'Partially Exercise',
                'string', None, '100',
                0, 0, ttPartialExercise],
        ['settle_price',
                'Settle Price',
                'string', '', '',
                0, None, ttsettle_price],
        ['settlemarket',
                'Name of Settlement Market',
                'string', smarkets, FBDPGui.getMtMMarket(),
                2, None, ttsettlemarket],
        ['mode',
                'Mode',
                'string', valid_modes, defaultMode,
                2, None, ttmode])


def ael_main(dictionary):

    import FBDPString
    importlib.reload(FBDPString)
    ScriptName = "Exercise Assign"
    import FBDPCurrentContext
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'],
                      dictionary['MailList'],
                      dictionary['ReportMessageType'])

    import FBDPCommon
    importlib.reload(FBDPCommon)
    import FBDPRollback
    importlib.reload(FBDPRollback)
    import FBDPCalculatePosition
    importlib.reload(FBDPCalculatePosition)
    import FBDPInstrument
    importlib.reload(FBDPInstrument)
    import FExeAssPerform
    importlib.reload(FExeAssPerform)

    dictionary['trades'] = FBDPCommon.convertEntityList(dictionary['trades'],
            dictionary)
    dictionary['Positions'] = dictionary['trades']

    FBDPGui.setPortfolioGrouper(dictionary)
    FBDPCommon.execute_script(FExeAssPerform.perform_exercise_assign,
            dictionary)
