
import acm
import FLogger

logger = FLogger.FLogger.GetLogger("logger")



def get_order_types():
    enums = acm.FEnumeration['orderType']
    return enums.Values()
    

