
import acm

def handleOrderFlowEvent(orderFlowEvent, orderBooks):
    print ('Order Flow Event: ', orderFlowEvent)
    print ('Target Order Books: ')
        
    for ob in orderBooks:
        print (ob.StringKey() + '(' + ob.MarketPlace().Name() + ')')
    print ('\n')
