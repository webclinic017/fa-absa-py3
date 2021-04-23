"""-----------------------------------------------------------------------------
PROJECT                 :  Security Borrowing and Lending
PURPOSE                 :  Generates a partial return for a security loan.  This script will terminate the existing trade and
                           open a new trade representing the remaining quantity.
DEPATMENT AND DESK      :  Prime Services, Securities Lending
REQUESTER               :  Linda Breytenbach
DEVELOPER               :  Paul Jacot-Guillarmod
CR NUMBER               :  243997

History:

Date            Who                             What
    
2010-03-19      Paul Jacot-Guillarmod           Amended the order in which an instrument and trade is terminated
                                                so that the termination process works in conjunction with
                                                FValidation
                                                
2010-04-14      Paul Jacot-Guillarmod           CR 282030: Made sure that trade status is validated 
                                                before a full return gets made
                                                
2010-06-08      Paul Jacot-Guillarmod           CR 332471: Copy the SL_RecallDate additional info from the parent trade to the new child trade

2010-08-12      Paul Jacot-Guillarmod           CR 400423: Partial returns needed to be amended to correctly generate a mirror trade

2010-10-16      Paul Jacot-Guillarmod           CR 494829: Update partial returns to take returns on CFD loans into account and to 
                                                perform same day returns.
2010-11-23      Francois Truter                 CR 502781
2011-01-20      Willie van der Bank             CR 5502363: Updated to set the Execution time instead of copying the original.
2011-05-19      Paul Jacot-Guillarmod           CR 657625: Updated the terminate_trade function to leave the trade status in its current status 
                                                instead of changing it to Terminated status
2011-12-08      Willie van der Bank             Updated to not copy over the value of Add_info SL_Instruction_Note when creating partial.
2012-08-10      Peter Fabian                    CR 381295 Find the mirror trade correctly
2014-05-20      Manan Ghosh                     Enhancement to the partial return booking process to accomodate the mirroring of the replacement 
                                                trades in line with the requirement for Enhancement of trade booking process for Stock Borrowing and
                                                Lending(SBL)
2015-22-01      Andreas Bayer                   ABITFA-2803 Backdated partial and full returns
2019-06-06      Qaqamba Ntshobane               FTF-292 Preventing partial returns on terminated trades
2020-02-21      Sihle Gaxa                      PCGDEV-142 Created close trade functionality
-----------------------------------------------------------------------------"""
import acm
import sbl_booking_utils as sbl_booker
import sbl_booking_validator as sbl_validator


def partial_return(trade, return_date, return_quantity, 
                   return_datetime=None, swift_flag=None, is_corp_action=None):

    return_trade = None
    sl_validator = sbl_validator.ReturnValidator(trade, return_date, return_quantity)
    
    if sl_validator.is_valid_loan_return():
        
        if sl_validator.is_full_return():
            return_trade = sbl_booker.generate_full_return(trade, return_date, return_quantity,
                                                           return_datetime, swift_flag, is_corp_action)
        else:
            return_trade = sbl_booker.generate_partial_return(trade, return_date, return_quantity,
                                                              return_datetime, swift_flag)

    return return_trade

ael_variables = sbl_booker.get_ael_variables()


def get_trade(additional_data):
    
    trade = None
    object = additional_data.At('customData')
    if object.ExtensionObject().IsKindOf(acm.FUiTrdMgrFrame):
        try:
            trades = object.ExtensionObject().ActiveSheet().Selection().SelectedCell().RowObject().Trades()
            if trades.Size() != 1:
                raise Exception('Partial return failed: Expected 1 trade, got %i' % trades.Size())
            trade = trades.AsArray().At(0)
        except Exception as e:
            raise Exception('Partial return failed: Unable to select trade to return because : ' + str(e))
    else:
        trade = object.ExtensionObject().OriginalTrade()
    
    return trade

# Menu call defined in FMenuExtension
def run_partial_return(extensionInvokationInfo):
    acm.RunModuleWithParametersAndData('sl_partial_returns', 'Standard', extensionInvokationInfo) 


def ael_main_ex(dictionary, additional_data):

    return_trade = None
    trade = get_trade(additional_data)
    swift_flag = dictionary["swift_flag"]
    is_corp_action = dictionary["is_corp_action"]
    return_datetime = dictionary["return_tradetime"]
    return_quantity = float(dictionary['return_quantity'].replace(",", ""))
    return_date = sbl_booker.CALENDAR.AdjustBankingDays(dictionary["return_date"], 0)

    return_trade = partial_return(trade, return_date, return_quantity,
                                  return_datetime, swift_flag, is_corp_action)
        
    if return_trade:
        acm.StartApplication('Instrument Definition', return_trade)

def revert_return(trade):

    instrument = trade.Instrument()
    if instrument.InsType() != "SecurityLoan":
        raise Exception("Can only revert security loan instruments")

    instrument_status = instrument.OpenEnd()

    if instrument_status != "Terminated":
        raise Exception("{ins} needs to be in Terminated status to revert".format(
                        ins=instrument.Name()))
    
    acm.BeginTransaction()
    try:
        last_trade = trade.SLPartialReturnLastTrade()
        
        if last_trade:
            second_last_trade = last_trade.SLPartialReturnPrevTrade()
            
            while True:
                if second_last_trade:
                    second_last_trade.SLPartialReturnNextTrade(None, True)
                    
                last_trade.Status("Void")
                last_trade.Commit()
                
                last_trade = second_last_trade
                
                if not last_trade or last_trade == trade:
                    break
                    
                second_last_trade = last_trade.SLPartialReturnPrevTrade()
                
        trade.Status("BO Confirmed")
        instrument.OpenEnd("Open End")
        instrument.Commit()
        trade.Commit()
        
        acm.CommitTransaction()
    
    except Exception as e:
        acm.AbortTransaction()
        raise Exception("Could not revert {ins} because {error}".format(
                        ins=instrument.Name(), error=str(e)))
