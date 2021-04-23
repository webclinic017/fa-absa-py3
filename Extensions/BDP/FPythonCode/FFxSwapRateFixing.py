""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/fx_position_rolls/etc/FFxSwapRateFixing.py"
#----------------------------------------------------------------------------
#    (c) Copyright 2020 SunGard Front Arena. All rights reserved.
#----------------------------------------------------------------------------
import acm
import ael

import FBDPGui
reload(FBDPGui)
import FBDPCurrentContext
import FFxSwapRateFixingPerform

ScriptName = "FxSwapRateFixing"

FBDPGui.DefaultVariables.defaults = FBDPGui.Parameters('FBDPParameters', 'FFxPositionRollover')

ttMarket                = 'The market which Deposit rates will be taken from and Swap points stored in.'
ttDeposits              = 'Deposit instruments from which bid/ask rates will be taken.'
ttDepositPrefix                = ('The prefix of Deposit instruments from which rates will be used'
                           ' for the calculation of FX Swap Points. If the instrument does not exist,'
                           ' it will be created.')
ttFXSwapInstruments     = 'FX Swap instruments on which bid/ask points will be stored.'
ttCalendar              = 'The default calendar for calculating daycount fractions.'
ttFXSwapPrefix                = ('The prefix of FX Swap instrument names on which points will be stored in'
                           ' the form: <Prefix>_EURUSD_SN. If the instrument does not exist, it will be created.')

ael_variables=FBDPGui.LogVariables(

['calendar', 'Default Calendar_Deposits', 'FCalendar', None, None, 0, 1, ttCalendar],
['market', 'Market_Deposits', 'FParty', None, None, 0, 1, ttMarket],
['deposits', 'Deposit Instruments_Deposits', 'FDeposit', None, None, 0, 1, ttDeposits],
['depositPrefix', 'Deposit Prefix_Deposits', 'string', None, None, 0, 0, ttDepositPrefix],
['fxSwaps', 'FX Swap Instruments_FX Swaps', 'FFxSwap', None, None, 0, 1, ttFXSwapInstruments],
['fxSwapPrefix', 'FX Swap Prefix_FX Swaps', 'string', None, None, 0, 0, ttFXSwapPrefix],
)
'''-----------------------------------------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
def ael_main(dictionary):
    #import FBDPString
    #reload(FBDPString)
    import FBDPCommon
    reload(FBDPCommon)
    FBDPCurrentContext.CreateLog(ScriptName,
                      dictionary['Logmode'],
                      dictionary['LogToConsole'],
                      dictionary['LogToFile'],
                      dictionary['Logfile'],
                      dictionary['SendReportByMail'], 
                      dictionary['MailList'], 
                      dictionary['ReportMessageType'])
    FBDPCommon.execute_script(FFxSwapRateFixingPerform.perform_swap_rate_fixing, dictionary)
    
    
'''--------------------------------------------------------------------------
-----------------------------------------------------------------------------------------------------------'''
