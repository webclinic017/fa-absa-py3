import acm
import FClearingTradeAttributes
import FFpMLACMUserAPIs
# The context parameter is an instance of FBusinessProcessCallbackContext
# Conditions return True or False
#
# Name convention is 
# 'condition_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
"""
    Business process receives context, which contains swml Message in 'swmlMessage' parameter. Can be accessed as 
    
    swml_message = contex.get('swmlMessage')
    
    Follwoing APIs are available for user to add/ override some attributes on the FpML/swml on business process handles,
    
    1. getValueOfNode()
        e.g.  businessCenter = FFpMLACMUserAPIs.getValueOfNode(fpmlMsg, \
           "SWML.swStructuredTradeDetails.FpML.trade.swap.swapStream @{'id':'fixedLeg'}.earlyTerminationProvision.optionalEarlyTermination.cashSettlement@{'id':'cashSettlement'}.businessCenter")
        Now this function returns businessCenter which can be mapped to any possible acmTradeObj attribute.
        More help on getValueOfNode() can be found in the installation document.
    
    2. updateValueOfNode() 
        e.g. fpmlMsg = FFpMLACMUserAPIs.updateValueOfNode(fpmlMsg, 'productType', 'InterestRate:BondFutureForward')
        This function updates the value of the given xml element in the fpml message before its sent to AMB.
        More help on updateValueOfNode() can be found in the installation document.
    
    3. createNewNode()
        e.g fpmlMsg  = FFpMLACMUserAPIs.createNewNode(fpmlMsg, 'onBehalfOf', 'ourOrganization', 'ABC Corp')
        This function will create new tag  'ourOrganization' under the 'onBehalfOf' tag and set its value to 'ABC Corp'
        More help on createNewNode() can be found in the installation document.
    
    4. deleteChildNode()
        e.g. fpmlMsg = FFpMLACMUserAPIs.deleteChildNode(fpmlMsg, 'ourOrganization')
        This function will delete the node from the generated fpml.
        More help on deleteChildNode() can be found in the installation document.
        
    5. getAllValuesOfNode() 
        e.g.  adjustedDatesArray = FFpMLACMUserAPIs.getAllValuesOfNode(fpmlMsg, \
           "trade.swap.earlyTerminationProvision.optionalEarlyTermination.cashSettlement.cashSettlementPaymentDate.adjustableDates.unadjustedDate")
        Now this function returns all the adjustedDates in an array which can be used further.
        More help on getAllValuesOfNode() can be found in the installation document.

    6. getValueOfAttribute() 
        e.g.  payerPartyReference = FFpMLACMUserAPIs.getValueOfAttribute(fpmlMsg, \
           "trade.swap @{'id':'fixedLeg'}.payerPartyReference", 'href')
        Now this function returns value of the attribute href for the node payerPartyReference.
        More help on getValueOfAttribute() can be found in the installation document.

    7. getAllValuesOfAttribute() 
        e.g.  swapIds = FFpMLACMUserAPIs.getAllValuesOfAttribute(fpmlMsg, \
           "trade.swap.swapStream", 'id')
        Now this function returns value of all the attribute id of node swap in an array which can be used further.
        More help on getAllValues    
        
    
    """
def condition_entry_state_initiated(context):
    print("Condition Entry state of Initiated")
    return True
    
def condition_exit_state_agreed(context):
    print("Condition Exit state of Agreed")
    return True
    
# Entry/Exit callbacks do not return anything
#
# Name convention is 
# 'on_' + 'entry_'/'exit_' + state name in lowercase and underscore
#
def on_entry_state_initiated(context):
    #context.Subject().Status('Simulated')
    pass

def on_entry_state_agreed(context):
    FClearingTradeAttributes.setCounterpartySwitch(context.Subject())
    #context.Subject().Status('FO Confirmed')
    pass
    
def on_exit_state_agreed(context):
    print("on Exit state of Agreed")
    pass

