
import acm
USER_MODULE_EXISTS = False
try:
    import CashManagementHooks
    USER_MODULE_EXISTS = True
except:
    pass
import CashManagementHooksDefault

def AdjustmentInitialAttributeValues(row):
    if USER_MODULE_EXISTS and hasattr(CashManagementHooks, 'AdjustmentInitialAttributeValues'):
        return CashManagementHooks.AdjustmentInitialAttributeValues(row)
    else:
        return CashManagementHooksDefault.AdjustmentInitialAttributeValues(row)

def FXRateFixingInitialSourceAttributeValues(row):
    if USER_MODULE_EXISTS and hasattr(CashManagementHooks, 'FXRateFixingInitialSourceAttributeValues'):
        return CashManagementHooks.FXRateFixingInitialSourceAttributeValues(row)
    else:
        return CashManagementHooksDefault.FXRateFixingInitialSourceAttributeValues(row)
        
def FXRateFixingInitialDestinationAttributeValues(row):
    if USER_MODULE_EXISTS and hasattr(CashManagementHooks, 'FXRateFixingInitialDestinationAttributeValues'):
        return CashManagementHooks.FXRateFixingInitialDestinationAttributeValues(row)
    else:
        return CashManagementHooksDefault.FXRateFixingInitialDestinationAttributeValues(row)
        
def TransferInitialSourceAttributeValues(row):
    if USER_MODULE_EXISTS and hasattr(CashManagementHooks, 'TransferInitialSourceAttributeValues'):
        return CashManagementHooks.TransferInitialSourceAttributeValues(row)
    else:
        return CashManagementHooksDefault.TransferInitialSourceAttributeValues(row)
        
def TransferInitialDestinationAttributeValues(row):
    if USER_MODULE_EXISTS and hasattr(CashManagementHooks, 'TransferInitialDestinationAttributeValues'):
        return CashManagementHooks.TransferInitialDestinationAttributeValues(row)
    else:
        return CashManagementHooksDefault.TransferInitialDestinationAttributeValues(row)
