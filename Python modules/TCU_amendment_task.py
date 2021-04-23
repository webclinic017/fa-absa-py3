"""
-------------------------------------------------------------------------------
DESCRIPTION
    Purpose             : Automatize correction of trades, instruments
    Department and Desk : TCU
    Requester           : Martin Herbst, James Stevens, Floyd Malatji, Natasha Williams, Jennitha Jugnath
    Developer           : Marian Zdrazil, Tibor Reiss

HISTORY
===============================================================================
Date        CR / JIRA #         Developer         Description
-------------------------------------------------------------------------------
2019-05-23  CHG1001777219       Marian Zdrazil    Initial implementation.
2019-06-06  FAPE-68             Marian Zdrazil    Adding voiding trade, instr. termination + update of leg's end date
2020-01-09  CHG0073639          Libor Svoboda     Update sec loan regenerate logic.
2020-06-06  CHG0103218          Libor Svoboda     Update price/quantity amendment logic.
"""
import csv
from math import copysign

import acm
import FRunScriptGUI
from at_ael_variables import AelVariableHandler
from at_logging import getLogger


LOGGER = getLogger()
DATE_TODAY = acm.Time().DateToday()
CALC_SPACE = acm.Calculations().CreateStandardCalculationsSpaceCollection()

FILE_SELECTION = FRunScriptGUI.InputFileSelection(FileFilter="CSV Files (*.csv)|*.csv")


ael_variables = AelVariableHandler()
ael_variables.add(
    name='amendments_file',
    label='File with amendments to apply',
    cls=FILE_SELECTION,
    default='/services/frontnt/Task',
    mandatory=True,
    multiple=True,
    alt="Input CSV file with various amendments on each row"
)


def read_corrections_file(csv_file_name):
    """
        Input CSV file with amendments has the following format:
        There are 4 columns in the input comma separated/delimited file:
            -------------------------------------------------------------------------------------------------------------------------
            1st column: trade number (integer)
            2nd column: amendment value (quantity, price, rate, Open End, Terminate, Void, (end date in MM/DD/YYYY format), etc.)
            3rd column: field description (Price, Quantity, SL_VAT, Open End, Rate, Terminate, Void)
            4th column: object (Instrument, Trade, Open End, Instrument AdditionalInfo, Trade AdditionalInfo)
            -------------------------------------------------------------------------------------------------------------------------
            Ex:
            ===
            Price, quantity amendment, VAT field un-ticking, re-opening, rate change
            108984438,1.58,Price,Instrument
            95032378,200000,Quantity,Trade
            108725637,TRUE,SL_VAT,Instrument AdditionalInfo
            98499295,Open End,Open End,Instrument
            107767545,0.3,Rate,Trade AdditionalInfo
            97627257,Terminate,Terminate,Instrument
            97627257,06/06/2019,Terminate,Instrument
            110031992,Void,Void,Trade

    """
    try:
        with open(csv_file_name, 'rb') as corr_file:
            corr_reader = csv.reader(corr_file, delimiter=',')
            corrections = [(int(row[0]), row[1], row[2], row[3])
                           for row in corr_reader if len(row) > 1]
            LOGGER.info("Corrections from %s file" % csv_file_name)
        return corrections
    except IOError as io_exception:
        LOGGER.error("Missing file with corrections: %s", csv_file_name)
        raise io_exception


def update_attribute(acm_object, attribute, new_value, obj_desc):
    try:
        if 'AdditionalInfo' in obj_desc:
            old_value = getattr(acm_object.AdditionalInfo(), attribute)()
            object_clone = acm_object.Clone()
            setattr(object_clone.AdditionalInfo(), attribute, new_value)
        else:
            old_value = getattr(acm_object, attribute)()
            object_clone = acm_object.Clone()
            setattr(object_clone, attribute, new_value)
        acm_object.Apply(object_clone)
        acm_object.Commit()
    except Exception as err:
        acm_object.Undo()
        LOGGER.error("Changes for object %s of type %s cannot be committed to FA: %s"
                     % (acm_object.Oid(), acm_object.ClassName(), str(err)))
    else:
        LOGGER.info("Update successful for object %s on attribute %s: %s --> %s"
                    % (acm_object.Oid(), attribute, old_value, new_value))


def update_loan_value(acm_trade, attribute, new_value):
    ins = acm_trade.Instrument()
    underlying = ins.Underlying()
    quotation_factor = ins.Quotation().QuotationFactor()
    contract_size = ins.ContractSize()
    loan_quantity = acm_trade.FaceValue()
    loan_price = acm_trade.AllInPrice() * quotation_factor
    old_value = ''
    if attribute == 'Price':
        old_value = loan_price
        loan_price = new_value
    elif attribute == 'Quantity':
        old_value = abs(loan_quantity)
        loan_quantity = copysign(new_value, loan_quantity)
    
    trade_image = acm_trade.StorageImage()
    ins_image = ins.StorageImage()
    trade_quantity = loan_price * loan_quantity / contract_size
    ref_val = contract_size / loan_price
    ref_price = loan_price / quotation_factor
    if underlying.InsType() in ('Bond', 'IndexLinkedBond'):
        ref_price = underlying.Calculation().PriceConvert(
            CALC_SPACE, ref_price, 'Pct of Nominal', underlying.Quotation(), 
            ins.StartDate())
    trade_image.Quantity(trade_quantity)
    ins_image.RefValue(ref_val)
    ins_image.RefPrice(ref_price)
    acm.BeginTransaction()
    try:
        ins_image.Commit()
        trade_image.Commit()
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        LOGGER.exception("Failed to update %s for trade %s." % (attribute, acm_trade.Oid()))
    else:
        LOGGER.info("Update successful for trade %s on attribute %s: %s --> %s"
                    % (acm_trade.Oid(), attribute, old_value, new_value))


def reopen(instr):
    """ 
        FAPE-68: Reopen terminated instruments - reopennning and extending terminated SBL instruments
        when instrument manually reopened by TCU, CFs are not necessarily being regenerated.
    """
    if instr.InsType() == 'SecurityLoan':
        leg = instr.Legs()[0]
        old_value_oe = getattr(instr, "OpenEnd")()
        new_value_oe = "Open End"
        old_value_leg = getattr(leg, "EndDate")()
        new_value_leg = acm.Time.DateAddDelta(getattr(leg, "StartDate")(), 0, 0, 1)
        old_value_roll_period_base = getattr(leg, "RollingPeriodBase")()
        new_value_roll_period_base = getattr(instr, "StartDate")()

        if old_value_oe != "Open End":
            try:
                instr_clone = instr.Clone()
                setattr(instr_clone, "OpenEnd", new_value_oe)
                instr.Apply(instr_clone)
                instr.Commit()
            except Exception as err:
                instr.Undo()
                LOGGER.error("Reopening failed for instrument %s with the following exception: %s" % (instr.Name(), err))
            else:
                LOGGER.info("Update successful for instrument %s - Open Ending: %s --> %s " % (
                    instr.Name(), old_value_oe, new_value_oe))

        if old_value_leg <= DATE_TODAY:
            try:
                leg_clone = leg.Clone()
                setattr(leg_clone, "EndDate", new_value_leg)
                setattr(leg_clone, "RollingPeriodBase", new_value_roll_period_base)
                leg.Apply(leg_clone)
                leg.Commit()
            except Exception as err:
                leg.Undo()
                LOGGER.error("Extending failed for instrument %s with the following exception: %s" % (instr.Name(), err))
            else:
                LOGGER.info("Update successful for leg %s of instrument %s - Extending: Leg start date %s --> %s and "
                            "Rolling Period Base %s --> %s" % (leg.Oid(), instr.Name(), old_value_leg, new_value_leg,
                                                               old_value_roll_period_base, new_value_roll_period_base))
            instr.SLExtendOpenEnd()
            instr.SLGenerateCashflows()
    else:
        LOGGER.error("Trade on instrument {} is not on a security loan".format(instr.Name()))


def terminate(instr, end_date):
    """ 
        FAPE-68: Terminate instruments + update leg's end date field
    """
    if instr.InsType() == 'SecurityLoan':
        leg = instr.Legs()[0]
        old_value_oe = getattr(instr, "OpenEnd")()
        new_value_oe = "Terminated"
        old_value_leg = getattr(leg, "StartDate")()

        if old_value_oe != "Terminated":
            try:
                instr_clone = instr.Clone()
                setattr(instr_clone, "OpenEnd", new_value_oe)
                instr.Apply(instr_clone)
                instr.Commit()
            except Exception as err:
                instr.Undo()
                LOGGER.error("Termination failed for instrument %s with the following exception: %s" % (instr.Name(), err))
            else:
                LOGGER.info("Update successful for instrument %s - Terminating: %s --> %s " % (
                    instr.Name(), old_value_oe, new_value_oe))
        
        if end_date != 'Terminate':
            try:
                leg_clone = leg.Clone()
                setattr(leg_clone, "EndDate", end_date)
                leg.Apply(leg_clone)
                leg.Commit()
            except Exception as err:
                leg.Undo()
                LOGGER.error("End date update failed for instrument %s with the following exception: %s" % (instr.Name(), err))
            else:
                LOGGER.info("Update successful for leg %s of instrument %s - Leg end date: %s --> %s" % 
                    (leg.Oid(), instr.Name(), old_value_leg, end_date))

    else:
        LOGGER.error("Trade on instrument {} is not on a security loan".format(instr.Name()))


def implement_updates(corrections):
    for (trdnbr, corr_value, att_desc, obj_desc) in corrections:
        trade = acm.FTrade[trdnbr]
        if trade is not None:
            if trade.ArchiveStatus() == 0:
                if trade.Aggregate() == 0:
                    ins = trade.Instrument()
                    if att_desc in ('Price', 'Quantity'):
                        update_loan_value(trade, att_desc, float(corr_value))
                    elif obj_desc == 'Instrument' and att_desc == 'Open End':
                        """ Open Ending & Extending Instrument """
                        reopen(ins)
                    elif obj_desc == 'Instrument' and att_desc == 'Terminate':
                        """ Terminating Instrument """
                        terminate(ins, corr_value)
                    elif obj_desc == 'Trade' and att_desc == 'Void':
                        """ Voiding Instrument """
                        update_attribute(trade, "Status", corr_value, obj_desc)                       
                    elif obj_desc == 'Instrument AdditionalInfo' and att_desc == 'SL_VAT':
                        """ Tick/Untick SL VAT instrument additional info field """
                        if 'TRUE' in corr_value:
                            update_attribute(ins, "SL_VAT", True, obj_desc)
                        elif 'FALSE' in corr_value:
                            update_attribute(ins, "SL_VAT", False, obj_desc)
                    elif obj_desc == 'Trade AdditionalInfo' and att_desc == 'Rate':
                        """ Amend instrument rates """
                        update_attribute(trade, "SL_G1Fee2", float(corr_value), obj_desc)
                        update_attribute(ins.Legs()[0], "FixedRate", float(corr_value), "Leg")
                    else:
                        LOGGER.error("Attribute flag not recognized - please check the 3rd column in the CSV file")
                else:
                    LOGGER.error("Cannot execute request on Aggregate Trade {}".format(trdnbr))
            else:
                LOGGER.error("Cannot execute request on Archived Trade {}".format(trdnbr))
        else:
            LOGGER.error("Trade {} does not exist".format(trdnbr))


def ael_main(ael_dict):
    LOGGER.msg_tracker.reset()
    corrections = read_corrections_file(str(ael_dict['amendments_file']))
    implement_updates(corrections)
    if LOGGER.msg_tracker.errors_counter:
        raise RuntimeError("ERRORS occurred. Please check the log.")
    LOGGER.info('Completed successfully.')
