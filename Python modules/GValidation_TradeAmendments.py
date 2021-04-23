'''
Created on 24 Jun 2016

@author: conicova
'''

import acm
import FUxTradeAmendDialog
import at_addInfoSpecEnum
import at_addInfo
from TradeAmendments import requires_amendment_reason, requires_amendment_reason_ael
from at_logging import getLogger

LOGGER = getLogger()

# A GUI validation error.
class ValidationError(Exception):
    pass

def popup(shell, message):
    return acm.UX.Dialogs().MessageBoxInformation(shell, message)

def input_amendment_reason(shell, modified_entity):
    '''Pop up a dialog for selecting an amendment reason and amend it whenever
    the object requires amendment reason. If the object does
    not requires a reason, simply skips the process.
    
    modified_entity - An acm object representing the Gui edition
    shell - 
    '''
    if not _trade_reason_required(modified_entity):
        return
    
    original_entity = modified_entity.Original()
    voiding = False
    if modified_entity.IsKindOf('FTrade') and modified_entity.Status() == 'Void':
        voiding = True

    if modified_entity.IsKindOf('FTrade'):
        caption = 'Select amendment reason for trade {0}'.format(original_entity.Oid())
        obj_type = 'trade'
    if modified_entity.IsKindOf('FInstrument'):
        caption = 'Select amendment reason for instrument'
        obj_type = 'instrument'
    selected_choice = _dialog_select_choice(shell, caption, obj_type, voiding)
    _set_amend_reason(selected_choice, modified_entity, original_entity)
    
def commit_multiple_with_reason(invocation_info):
    extension_object = invocation_info.ExtensionObject()
    shell = extension_object.Shell()
    selection = extension_object.ActiveSheet().Selection()
    cells = selection.SelectedCells()
    trades = set(cell.RowObject().Trade() for cell in cells)

    if not trades:
        return

    voided_trades = [trade for trade in trades if trade.Status() == 'Void']
    backdate_trades = [trade for trade in trades if _trade_backdate_reason_required(trade)]
    amended_trades = len(trades) != len(voided_trades)

    selected_choice_amend = [None, None]
    selected_choice_bkdate = [None, None]
    selected_choice_void = [None, None]
    
    if backdate_trades:
        try:
            # Display the "amendment reason" dialog.
            selected_choice_bkdate = _dialog_select_choice(shell, 'Select amendment reason for backdated trades', 'trade', False, True)
        except ValidationError as e:
            # Print error message to Prime's console.
            LOGGER.error("Validation Error: %s", e)
            return None
    if voided_trades:
        try:
            # Display the "amendment reason" dialog.
            selected_choice_void = _dialog_select_choice(shell, 'Select amendment reason for voided trades', 'trade', True)
        except ValidationError as e:
            # Print error message to Prime's console.
            LOGGER.error("Validation Error: %s", e)
            return None
    if amended_trades:
        try:
            # Display the "amendment reason" dialog.
            selected_choice_amend = _dialog_select_choice(shell, 'Select amendment reason for trades', 'trade')
        except ValidationError as e:
            # Print error message to Prime's console.
            LOGGER.error("Validation Error: %s", e)
            return None


    acm.BeginTransaction()
    try:
        for trade in trades:
            LOGGER.info("Amended trade: %s", trade.Oid())
            original_trade = trade.Original()
            if not original_trade:
                # Not an amendment.
                LOGGER.info("Nothing was amended on trade %s", trade.Oid())
                continue
    
            if trade in voided_trades:
                selected_choice = selected_choice_void
            elif trade in backdate_trades:
                selected_choice = selected_choice_bkdate
            else:
                selected_choice = selected_choice_amend
            
            try:
                original_trade.Touch()
                original_trade.Apply(trade)
                _set_amend_reason(selected_choice, original_trade, original_trade, True)
                original_trade.Commit()
            except Exception as ex:
                LOGGER.exception("Amendment reason could not be saved.")

        acm.CommitTransaction()
    except Exception as ex:
        acm.AbortTransaction()
        raise ex

def _set_amend_reason(selected_choice, entity, original_entity, use_addInfo=False):

    amend_add_info_name = ""
    amend_add_info_name_tmp = ""  # hack, see the at_addInfoSpecEnum for additional information on this
    amend_type_add_info_name = ""
    if entity.IsKindOf('FTrade'):
        amend_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TRD
        amend_type_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TYPE_TRD
        if selected_choice[1] == 'Backdate':
            amend_add_info_name_tmp = at_addInfoSpecEnum.AMEND_REASON_TRD_TMP
    if entity.IsKindOf('FInstrument'):
        amend_add_info_name = at_addInfoSpecEnum.AMEND_REASON_INS
        amend_type_add_info_name = at_addInfoSpecEnum.AMEND_REASON_TYPE_INS

    if not amend_add_info_name or not amend_type_add_info_name:
        raise ValidationError('Unexpected entity type. Additional info specification not defined.')

    if (not hasattr(entity.AdditionalInfo(), amend_add_info_name) or
        not hasattr(entity.AdditionalInfo(), amend_type_add_info_name)):
        LOGGER.error("%s %s attributes not found", amend_add_info_name, amend_type_add_info_name)
        return False

    current_reason = getattr(entity.AdditionalInfo(), amend_add_info_name)()
    if current_reason:
        LOGGER.warning("Overriding current amendment reason (%s)", current_reason)

    LOGGER.info("Id %s, reason: %s, %s, %s", entity.Oid(), selected_choice, amend_add_info_name, amend_type_add_info_name)
    if use_addInfo:
        at_addInfo.save(entity, amend_add_info_name, selected_choice[0])
        at_addInfo.save(entity, amend_type_add_info_name, selected_choice[1])
        if amend_add_info_name_tmp:
            at_addInfo.save(entity, amend_add_info_name_tmp, selected_choice[0])
    else:
        getattr(entity.AdditionalInfo(), amend_add_info_name)(selected_choice[0])
        getattr(entity.AdditionalInfo(), amend_type_add_info_name)(selected_choice[1])
        if amend_add_info_name_tmp:
            getattr(entity.AdditionalInfo(), amend_add_info_name_tmp)(selected_choice[0])
    return True

def _dialog_select_choice(shell, caption, obj_type, voiding=False, creating_backdated=False):

    selected_choice = FUxTradeAmendDialog.ShowDialog(shell, {'caption':caption,
                                                             'obj_type':obj_type,
                                                             'voiding':voiding,
                                                             'creating_backdated':creating_backdated})

    error = None

    if not selected_choice:
        error = 'Amendment reason and type is required'
    else:
        if not selected_choice[0]:
            error = 'Amendment reason is required'
        if not selected_choice[1]:
            error = 'Amendment type is required'

    if error:
        popup(shell, error)
        raise ValidationError(error)

    return selected_choice

def _trade_backdate_reason_required(obj):
    """
    1.    If execution date smaller or equal trade time => no backdate reason required => return False
    2.    If trade status Simulated or Void => no backdate reason required => return False
    3.    If trade time not amended (according to 1st condition it is smaller than execution date)
    and original status was not Simulated or Void (according to 2nd condition it is not Simulated
    or Voided) => backdate reason was already provided and no backdate reason required = return false
    4.    In all other cases provide a backdate reason => return True
    """
    if not obj.IsKindOf('FTrade'):
        return False
    LOGGER.debug('exec time: %s, trade time: %s', obj.ExecutionDate(), obj.TradeTime())
    if obj.ExecutionDate() <= obj.TradeTime():
        return False
    
    ignore_statuses = ['Simulated', 'Void']
    if obj.Status() in ignore_statuses:
        return False
    
    original_entity = obj.Original()
    if original_entity:
        # original was not simulated and backdated with reason -> no reason required
        trade_time_amended = original_entity.TradeTime() != obj.TradeTime() 
        if not trade_time_amended and original_entity.Status() not in ignore_statuses:
            return False
    
    return True

def trade_backdate_reason_required_ael(obj):
    if obj.record_type != 'Trade':
        return False
    LOGGER.debug('exec time: %s, trade time: %s', obj.execution_time, obj.time)
    if obj.execution_time <= obj.time:
        return False
    
    ignore_statuses = ['Simulated', 'Void']
    if obj.status in ignore_statuses:
        return False
    
    original_entity = obj.original()
    if original_entity:
        # original was not simulated and backdated with reason -> no reason required
        trade_time_amended = original_entity.time != obj.time 
        if not trade_time_amended and original_entity.status not in ignore_statuses:
            return False
    
    return True

def _trade_reason_required(modified_entity):

    if not modified_entity.IsKindOf('FTrade') and not modified_entity.IsKindOf('FInstrument'):
        return False

    original_entity = modified_entity.Original()
    if not original_entity:
        return False
    
    # JP and Simon have asked to not display the amendment reason if the trade status is FO confirmed (01/10/2015)
    if  modified_entity.IsKindOf('FTrade') and  modified_entity.Status() in ['Simulated', 'FO Confirmed']:
        return False
    
    if not requires_amendment_reason(original_entity, modified_entity):
        return False
    
    return True

def trade_reason_required_ael(modified_entity):

    if modified_entity.record_type not in ['Trade', 'Instrument']:
        return False
    original_entity = modified_entity.original()
    if not original_entity:
        return False
    # JP and Simon have asked to not display the amendment reason if the trade status is FO confirmed (01/10/2015)
    if  modified_entity.record_type == 'Trade' and  modified_entity.status in ['Simulated', 'FO Confirmed']:
        LOGGER.debug('GValidation: input_amendment_reason_ael, exiting, ignored status: %s', modified_entity.status)
        return False
    
    if not requires_amendment_reason_ael(original_entity, modified_entity):
        return False
    
    return True

def input_backdate_reason(shell, obj):
    '''Check if a backdate reason is required and persist the provides one.
    
    Returns None if the backdate reason is not required else return True.
    
    1.    If execution date smaller or equal trade time => no backdate reason required
    2.    If trade status Simulated or Void => no backdate reason required
    3.    If trade time not amended (according to 1st condition it is smaller than execution date)
    and original status was not Simulated or Void (according to 2nd condition it is not Simulated
    or Voided) => backdate reason was already provided and no backdate reason required
    4.    In all other cases provide a backdate reason
    '''
    if not _trade_backdate_reason_required(obj):
        return
    
    caption = 'Select amendment reason for backdated trade'
    obj_type = 'trade'
    selected_choice = _dialog_select_choice(shell, caption, obj_type, False, True)
    _set_amend_reason(selected_choice, obj, None)
    return True
