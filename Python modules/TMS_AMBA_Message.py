''' =======================================================================
    TMS_AMBA_Message
    Purpose                 :   Module responsible for building AMBA messages
                                for TMS-bound feed processing. Checks that a message
                                is supported and if so, instantiates the appropriate 
                                trade handler class. The message is then built using
                                the custom class.
    Department and Desk     :   SM IT Pricing & Risk
    Requester               :   Matthew Berry
    Developer               :   Eben Mare, Peter Kutnik
    CR Number               :   196109
    =======================================================================
    Purpose		    : Added function to handle RecieverModifyHook changes and delegate the construction of the updated bounce back
                            : message from Synthesis Adaptor, changes to handle FValidation for Allowable instrument conversions for FX Products.
    Department and Desk	    :
    Requester		    : Mathew Berry
    Developer		    : Babalo Edwana
    CR Number		    : 261644

==================================================================================================================================================='''
#Developer:      Peter Kutnik
#Date:           2010-04-06
#Detail:         Updated CreateTradeMessage - added source and TXNBR params
#                to preserve original message headers
#CR number:      274189
#------------------------------------------------------------------------------

import amb

import TMS_TradeWrapper_Base
import TMS_TradeWrapper_Common
import TMS_TradeWrapper_FX

from TMS_Config_Trade import *

AMBA_ID = "TMS TEST MESSAGE2"
AMBA_VERSION = "1.0"

class EnumOperation:
    INSERT = 1
    UPDATE = 2

def _processElement(parentMsg, element):
    # create a message part for this element
    msg = parentMsg.mbf_start_list( element.getTypeName() )

    # Add the properties
    for property in element.properties():
        name = property[0]
        value = property[1]
        if type(value) == int:
            msg.mbf_add_int(name, value)
        elif type(value) == float:
            msg.mbf_add_double(name, value)
        elif type(value) == str:
            msg.mbf_add_string(name, value)
        elif value == None:
            msg.mbf_add_string(name, "")
        else:
            print "name ", property[0], "value ", property[1]
            raise ValueError("Unhandled property type: %s" % repr(type(value)))

    # Now recursively do the children
    for child in element.children():
        _processElement(msg, child)

def SupportsTradeMessage(trade):
    # Check if there is a factory for this trade type
    factories = getTradeFactories()
    if factories:
        for factory in factories:
            if factory.supports(trade):
                return factory

def _SupportsTradeMessage_(instr):
    # Check if there is a factory for this trade type
    factories = getTradeFactories()
    if factories:
        for factory in factories:
            if factory._supports(instr):
                return factory

def EntityOriginal(entity):
    try:
        e = entity.original()
    except:
        e = entity

    return e

def AllowConversion(trdFrom, trdTo, instr, instr_o):
    assetClass = getPrfAssetClassConversions(trdFrom)
    if assetClass == getPrfAssetClassConversions(trdTo):
        f1 = _fxSupportsTradeMessage_(instr_o)
        f2 = _fxSupportsTradeMessage_(instr)
        if f1 and f2:
            return (f1._name(), f2._name()) in assetClass._allowableConversions() or f1._name() == f2._name()

def CreateTradeMessage(factory, trade, msgType, source, txnbr):

    # Get the required trade wrapper
    assert factory.supports(trade)
    wrapper = factory.create(trade)

    if type(wrapper) == amb.mbf_object:
        return wrapper
    else:
        # Create a message for this trade
        msg = amb.mbf_start_message(
                    None,
                    msgType == EnumOperation.UPDATE and "UPDATE_TRADE" or "INSERT_TRADE",
                    AMBA_VERSION,
                    None,
                    source)
        
        msg.mbf_add_string('TXNBR', txnbr)

        _processElement(msg, wrapper)

        return msg

def Indent(indent, level):
    return " "*(level*indent)

def PrintHeader(name, indent, level):
    return "%s<%s>\n" % (Indent(indent, level), name)

def PrintKeyValue(name, value, indent, level):
    return "%s<%s>%s</%s>\n" % (Indent(indent, level), name, value, name)

#Function to recursively print an AMB message to a string
#This is used as mbf_object_to_string fails for compressed messages.
def MessageToString(msg, indent = 2, level = 0):
    strMsg = ""
    if msg:
        strMsg += PrintHeader(msg.mbf_get_name(), indent, level)
        obj = msg.mbf_first_object()
        while obj:
            if obj.mbf_is_list():
                strMsg += MessageToString(obj, indent, level+1)
            else:
                strMsg += PrintKeyValue(obj.mbf_get_name(), obj.mbf_get_value(), indent, level+1)

            obj = msg.mbf_next_object()

        strMsg += PrintHeader("/" + msg.mbf_get_name(), indent, level)

    return strMsg
  
"""
    Function to create TMS Response Message
"""
def CreateResponseMessage(factory, trade, fieldName, tmsID, source):
    """
Function to create TMS Response Message
    """
    # Get the required trade wrapper
    assert factory.supports(trade)
    wrapper = factory.create(trade, fieldName, tmsID)

    if type(wrapper) == amb.mbf_object:
        return wrapper
    else:
        # Create a message for this trade
        msg = amb.mbf_start_message(
                    None,
                   "UPDATE_ADDITIONALINFO",
                    AMBA_VERSION,
                    None,
                    source)

        _processElement(msg, wrapper)

        return msg
        
def _fxSupportsTradeMessage_(instr):
    if instr:
        if instr.instype == "Option" and instr.und_instype == "Curr" and \
               instr.exotic_type == "None" and not instr.digital:
            return TMS_TradeWrapper_FX.FXVanillaTradeWrapperFactory()
         
        if instr.instype == "Option" and instr.und_instype == "Curr" and \
               instr.exotic_type == "None" and instr.digital:
            return TMS_TradeWrapper_FX.FXCashOrNothingTradeWrapperFactory()
        
        if instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.exotic_type != "None" and not instr.digital:
            return TMS_TradeWrapper_FX.FXBarrierTradeWrapperFactory()
        
        if instr.instype == "Option" and instr.und_instype == "Curr" \
            and instr.exotic_type != "None" and instr.digital:
            return TMS_TradeWrapper_FX.FXTouchTradeWrapperFactory()
