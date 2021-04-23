"""------------------------------------------------------------------------
MODULE
    FMarkitWireValidation -
DESCRIPTION:
    This file checks for any major changes that are done on the trade during update. This file is currently not being used  
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
allowedMiddlewareList = ['MW', 'VCON']

def validate_transaction(transaction_list, attrib_Dict):
    
    editableInstrumentAttributes = attrib_Dict['Instrument']
    editableTradeAttributes      = attrib_Dict['Trade']
    editableLegAttributes        = attrib_Dict['Leg']
        
    for (newObject, op) in transaction_list:
        oldObject = newObject.original()
        #Here further validation can be added
        
    return transaction_list

