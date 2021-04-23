
import thread
import threading
import Queue
import time
import string
import acm
import FLogger
import math

logger = FLogger.FLogger.GetLogger("logger")




# this is a threading class that is meant to look at the order command (OrderWorkItem) for updates
class OrderCommandWatcher( threading.Thread ):
    """worker thread that executs work items"""
    # static variables
    # WORKQ is a queue of OrderWorkItems
    WORKQ               = Queue.Queue()
    INSTANCE            = None
    LOCK                = threading.Lock()
    POLL_INTERVAL       = 1
            
    def __init__( self ): 
        # start the thread
        threading.Thread.__init__( self )
     
    # static function, python style
    @classmethod
    def put_work( cls, work_item ):
        # add/put a new OrderWorkItem in the queue
        cls.WORKQ.put( work_item )




        
    @classmethod
    def get_instance( cls ):
        """singleton contructor"""
        try:
            # lock the thread
            cls.LOCK.acquire()
            # there can be only one
            if not cls.INSTANCE:
                cls.INSTANCE = cls()
            return cls.INSTANCE
        finally:
            # unlock the thread
            cls.LOCK.release()
    
    # static 
    @classmethod
    def monitor_thread( cls ):
        """start thread if not started"""
        if not cls.INSTANCE or not cls.INSTANCE.isAlive():
            cls.INSTANCE = None
            # get a new thread
            worker_thread = cls.get_instance()
            # start the thread
            worker_thread.start() 


            

            
    def run( self ):
        """executed when thread is started"""
        while True:
            try:
                # prossess all objects in the queue 
                self.monitor_command()
                
                
                # go to sleep and wake up after a poll interval
                time.sleep( OrderCommandWatcher.POLL_INTERVAL )
            
            except Exception as err:
                logger.error( "Exception occurred while executing work item.", exc_info=1 )
                
                


                
                            
    def monitor_command( self ):
        """work to be performed by thread"""
        try:
            # this is a list
            
            work_items = []
            # as long as there is an object still in the queue
            if OrderCommandWatcher.WORKQ:
                while OrderCommandWatcher.WORKQ.qsize():
                    # add an item at the end of the work_items list, 
                    # and do that without blocking WORKQ, 
                    # (at the same time this is removed from WORKQ queue)
                    work_items.append( OrderCommandWatcher.WORKQ.get_nowait() )
            else:
                err = "OrderCommandWatcher.WORKQ does not exist yet"
                raise Exception
                
            #process the commands submitted from the other thread
            if work_items:
    
                for work_item in work_items:
                    

                    work_item.order_was_sent()
                    work_items.remove(work_item)
                    
        except Exception as err:
            logger.error("Exception caught while monitoring command: %s", str(err), exc_info=1)
            
    
# this is a wrapper class for orderCommand objects
class OrderWorkItem(object):  
    
    
    def __init__(self, order_command, parameters, originalQty, qtyOfOrderThatCausedThis, orderHandler, placeOrCancel):
        self.order_command = order_command
        self.parameters = parameters
        self.invokationInfo = parameters.invokationInfo
        self.originalQty = originalQty
        self.orderHandler = orderHandler
        self.placeOrCancel = placeOrCancel
        self.qtyOfOrderThatCausedThis = qtyOfOrderThatCausedThis
        


        
           

    def order_was_sent(self):
        try:
       
            
               
            # handle results from orders
            
            # error
            if self.order_command.Result() == 'Error':
                info = "Order Error: "
                
                for error in self.order_command.Errors():
                    info = info+error.Message()
                

                logger.error(info)
                self.parameters.info.Evaluator().Value(info)
                
                    
       
                
            # success 
            elif self.order_command.Result() == 'Success' and self.order_command.IsComplete():
               
            
                if "PlaceOrder" == self.placeOrCancel:
                    info = "Order sent successfully. Qty: "+str(self.originalQty)
                    logger.info(info)
                    self.parameters.info.Evaluator().Value(info)
                    sumOfSession = self.parameters.sessionSum.Value()
                    self.parameters.sessionSum.Evaluator().Value(sumOfSession+abs(self.originalQty))


                
               
            

  
                
                    
            # partial success 
            elif self.order_command.Result() == 'Success' and not self.order_command.IsComplete():
            
                if "PlaceOrder" == self.placeOrCancel:
                    info = "Partial Fill. Continuing ..."
                    self.parameters.info.Evaluator().Value(info)
                    storeQty  = self.parameters.target_quantity.Evaluator().Value() 
                    sumOfSession = abs(self.parameters.sessionSum.Value())
                    self.parameters.sessionSum.Evaluator().Value(sumOfSession+abs(self.originalQty)-self.orderhandler.Quantity())
                    logger.info(info)
                    OrderCommandWatcher.put_work(self)

                
            # unknown error
            elif self.order_command.Result() == -1:
                
                info = "Unkown Error sending order. Please try sending the order again."
                logger.info(info)
                self.parameters.info.Evaluator().Value(info)              
                
            else:
                info = "Unexpected result: %s" % self.order_command.Result()
                logger.info(info)
                self.parameters.info.Evaluator().Value(info)              
                
                raise Exception(info)

                
            
        except Exception as err:
            logger.error("Exception caught: %s ", str(err), exc_info=1)
            try:
                info = "Order did not get through, please try again or/and check market connectivity - status."
                self.parameters.info.Evaluator().Value(info)
            except Exception:
                logger.error("Exception caught: Didn't manage to update Trading manager with the latest error")

            
            
class Parameters(object):
   
    # static
    #enums
    ENUM_BUY_SELL = acm.FEnumeration['buyOrSell'] 
    
    #map to ColumnId of Column Definition 
    BUY_SELL    = 'Portfolio Order Buy Or Sell' 
    ACCOUNT     = 'Portfolio Order Account'
    EXP_TIME    = 'Portfolio Order Expiration Time'
    PRICE       = 'Portfolio Order Price'
    QUANTITY    = 'Portfolio Order Quantity'
    TARGET_QUANTITY    = 'Portfolio Order Target Quantity'
    ORDERBOOK   = 'Portfolio Order OrderBook'
    REFERENCE   = 'Portfolio Order Reference'
    USER        = 'Portfolio Order Trader'
    TYPE        = 'Portfolio Order Type'
    AUTO_UPDATE = 'Portfolio Order Auto Update'
    INFO        = 'Portfolio Status Info'
    IS_OB_CONNECTED = 'Portfolio Order Can Be Sent'
    QTY_SENT    = 'Portfolio Order Quantity Sent'
    SESSIONSUM = 'Portfolio Order Sum of Session Orders'
    INSTRUMENT  = 'Instrument'
    PORTFOLIO   = 'Portfolio'
    NO_SUCCESFULLY_SENT_ORDERS = 'Portfolio Order Number Of Session Orders'
    #CALCULATION = acm.Calculations().CreateCalculationSpace(acm.GetDefaultContext(), 'FPortfolioSheet').CalculateValue

     
    # list with the names 
    ORDER_COLUMNS_IDS =   [ BUY_SELL,
                            ACCOUNT, 
                            EXP_TIME, 
                            PRICE, 
                            QUANTITY, 
                            TARGET_QUANTITY,
                            ORDERBOOK, 
                            REFERENCE, 
                            USER,
                            TYPE,
                            AUTO_UPDATE, 
                            IS_OB_CONNECTED,
                            INFO,
                            NO_SUCCESFULLY_SENT_ORDERS,
                            QTY_SENT,
                            SESSIONSUM    ]
    
    # ctor 
    def __init__(self, params, invokationInfo):


        self.instrument = params.get(Parameters.INSTRUMENT)
        self.is_ob_connected = params.get(Parameters.IS_OB_CONNECTED)
        self.buysell = params.get(Parameters.BUY_SELL)
        self.account = params.get(Parameters.ACCOUNT)
        self.instrument = params.get(Parameters.INSTRUMENT)
        self.portfolio = params.get(Parameters.PORTFOLIO)
        self.quantity = params.get(Parameters.QUANTITY)
        self.target_quantity = params.get(Parameters.TARGET_QUANTITY)
        self.info    = params.get(Parameters.INFO)   
        self.price = params.get(Parameters.PRICE)
        self.exp = params.get(Parameters.EXP_TIME)
        self.orderbook = params.get(Parameters.ORDERBOOK)
        self.reference = params.get(Parameters.REFERENCE)
        self.trader = params.get(Parameters.USER)
        self.type = params.get(Parameters.TYPE)
        self.autoUpdate = params.get(Parameters.AUTO_UPDATE)
        self.invokationInfo = invokationInfo
        self.noSuccesfullySentOrders = params.get(Parameters.NO_SUCCESFULLY_SENT_ORDERS)
        self.quantitySent = params.get(Parameters.QTY_SENT)
        self.sessionSum = params.get(Parameters.SESSIONSUM)
        self.tradingSession = acm.FTradingSession(acm.FTradingSessionCustomInterface(self.portfolio))
   
        

    def validate(self):


        error = ""
        errorDetails = ""
        # make sure that all parameters are in place
        if not self.is_ob_connected:
            error = "\n".join([error, "Orderbook not connected, orderbook not set or column 'Portfolio Order OrderBook' not loaded."])
            errorDetails=errorDetails+str(" Orderbook")
        
        if not self.orderbook:
            error = "\n".join([error, "Column 'Portfolio Order OrderBook' not loaded."])
            errorDetails=errorDetails+str(" Buy Or Sell")
 
        if not self.buysell:
            error = "\n".join([error, "Column 'Portfolio Order Buy Or Sell' not loaded."])
            errorDetails=errorDetails+str(" Orderbook Column")
            
        if self.price:
            if str(self.price.Value().Number()) == "nan":        
                error = "\n".join([error, "Price is nan."])
                errorDetails=errorDetails+str(" Price")
        else:
            error = "\n".join([error, "There is no price or column 'Portfolio Order Price' not loaded."])
            errorDetails=errorDetails+str(" Price")
            
        if not self.target_quantity:
            error = "\n".join([error, "Column 'Portfolio Order Target Quantity' not loaded, or not in Automatic Update (Portfolio Order Auto Update)."])
            errorDetails=errorDetails+str(" Target Quantity")     
            
        if self.quantity:    
            if not self.quantity.Value():
                error = "\n".join([error, "Quantity not set."])
                errorDetails=errorDetails+str(" Qty")
        else:
            error = "\n".join([error, "There is no quantity set or column 'Portfolio Order Quantity' not loaded."])
            errorDetails=errorDetails+str(" Qty")
        if self.account:
            if not self.account.Value():
                error = "\n".join([error, "Account not set."])
                errorDetails=errorDetails+str(" Account")
        else:
            error = "\n".join([error, "There is no account set or column 'Portfolio Order Account' not loaded."])
            errorDetails=errorDetails+str(" Account")     

        if not self.reference:
            error = "\n".join([error, "Column 'Portfolio Order Reference' not loaded or set."])
            errorDetails=errorDetails+str(" Reference")   

        if not self.trader:
            error = "\n".join([error, "Column 'Portfolio Order Trader' not loaded or set."])
            errorDetails=errorDetails+str(" Trader") 

        if not self.quantitySent:
            error = "\n".join([error, "Column 'Portfolio Order Quantity Sent' not loaded."])
            errorDetails=errorDetails+str(" Quantity Sent")     
        if error:
            shell = self.invokationInfo.Parameter('shell')
            acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Error', 'Validation error (Order parameters missing or wrong) \n%s' % str(error))
            self.info.Evaluator().Value("Validation error: "+str(errorDetails))
            return False
        else:

            return True


                
def on_send_button(invokationInfo):


    try:
        params = Parameters(get_order_parameters(invokationInfo), invokationInfo)
        if params.validate():
            send_order(params) 
        else:
            logger.error("Parameters did not validate: missing or erroneous parameters")
                   
    except Exception as err:
        try:
            shell = invokationInfo.Parameter('shell')
            acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Error', 'Error sending order: \n%s' % str(err))
        except Exception as e:
            logger.error("Error popping dialog while activating sending button", exc_info=True)



def on_remove_button(invokationInfo):


    try:
        params = Parameters(get_order_parameters(invokationInfo), invokationInfo)
        if params.orderbook:
            remove_orders(params) 
        else:
            logger.error("Parameters did not validate: missing or erroneous orderbook. (Is Portfolio Order OrderBook column loaded ?)")
                   
    except Exception as err:
        try:
            shell = invokationInfo.Parameter('shell')
            acm.UX().Dialogs().MessageBoxOKCancel(shell, 'Error', 'Error removing orders: \n%s' % str(err))
        except Exception as e:
            logger.error("Error popping dialog while activating remove button", exc_info=True)
            
def remove_orders(params):

    try:

        session = params.tradingSession
        listOfMyOrders = session.Orders(params.orderbook.Evaluator().Value(), "Owner").AsIndexedCollection()   
        for oo in listOfMyOrders:
            oo.DeleteOrder()
    except Exception as err:
        msg = "Error removing parameters: %s" % str(err)
        logger.info(msg)
        params.info.Evaluator().Value(msg)
        
# this function is used to build a dictionary with the values as 
# they are retrieved from the columns with their respective names   
def get_order_parameters(invokationInfo):

    try:
        # dictionary
        parameters = {}

        sheet = invokationInfo.ExtensionObject().ActiveSheet()
        button = invokationInfo.Parameter("ClickedButton")
        
        # start associating parameters with keys
        parameters[Parameters.INSTRUMENT] = button.RowObject().Instrument()
        parameters[Parameters.PORTFOLIO] = button.RowObject().Portfolio()
        
        # continue iteratively by fetching the elemens of the sheet cells 
        row_iterator = button.Tree().Iterator()
        iter = sheet.GridColumnIterator()
        while iter:
            col = iter.GridColumn()
            if col:
                col_name = col.ColumnId().AsString()
                
                if col_name in Parameters.ORDER_COLUMNS_IDS:
                    
                    cell = sheet.GetCell(row_iterator, iter)
                    if cell.Value() != None:
                        parameters[col_name] = cell

            iter = iter.Next()
            
        # will return the dictionary IF all columns are loaded
        return parameters
    except Exception as err:
        msg = "Error reading parameters: %s" % str(err)
        logger.info(msg)



def create_and_send_order(buyOrSellio, params, newprice, qtyToSend, session):
    try:
        if qtyToSend > 0:
            order = session.CreateOrder(params.orderbook.Value()) 

            if order:
                order.BuyOrSell(buyOrSellio)
                if newprice <> 0:
                    order.Price(newprice)
                else:
                    order.Price(params.price.Evaluator().Value())
                order.Quantity(qtyToSend)
                order.Account(params.account.Evaluator().Value())
                order.ExpirationDateTime(params.exp.Evaluator().Value())
                order.Reference(params.reference.Evaluator().Value())
                order.UserId(params.trader.Evaluator().Value())
                order.OrderType(params.type.Evaluator().Value())
                order.IsIndependentModifyEnabled(True)
                command = order.SendOrder() 
                originalQty = params.quantity.Value()
                OrderCommandWatcher.put_work(OrderWorkItem(command, params, originalQty, qtyToSend, order, "PlaceOrder")) 
                info = "Wait: Sending order for "+str(params.instrument.Name()+ "...")
                logger.info(info) 
                params.info.Evaluator().Value(info)

            else:
                info = "Order could not be created for  "+str(params.instrument.InsType())+str(params.instrument.Name())
                logger.info(info)
    except Exception as err:
        msg = "Exception while trying to send order: %s" % str(err)
        logger.info(msg)
        params.info.Evaluator().Value(msg)  



def send_order(params):

    try:
        
        
        # sum all buy orders minus all sell orders
        # Delete inactives
        # split all orders to two pqueues based on quantity
        # runs in O(n2): O(n) for the entire loop, times O(n) for every insertion in a priority queue 
        
        
        
        # Get various information

        session = params.tradingSession
        
        buyListQ = Queue.PriorityQueue()
        sellListQ = Queue.PriorityQueue()
        
        listOfMyOrders = session.Orders(params.orderbook.Evaluator().Value(), "Owner").AsIndexedCollection()   
        qtyToSend = abs(params.quantity.Evaluator().Value())
        buyOrSellio = params.buysell.Evaluator().Value()
        ourNewPrice = params.price.Evaluator().Value()

        
        
        for oo in listOfMyOrders:
        
    
            
            # check if this should be deleted
            if (0 == oo.Quantity()) or  oo.IsOrderDone() or oo.IsOrderInactive():
                oo.DeleteOrder()
   
            elif oo.IsOrderDeleted():
                pass
            else:

            
 
                # increment the appropriate counter and 
                # split the orders to buys and sells for further processing
                if  ('Buy' == oo.BuyOrSell()):
                    x = ( -oo.Quantity(), oo)
                    buyListQ.put(x)
                    
                else:
                    x = ( -oo.Quantity(), oo)
                    sellListQ.put(x)               
            

        

        # DELETE OPPOSITE SIGN ORDERS and UPDATE sumOrderbookQty
        if "Buy" == buyOrSellio:
            while(not sellListQ.empty()):
                data = sellListQ.get()
                oo = data[1]
                oo.DeleteOrder()

                
        else:
            while(not buyListQ.empty()):
                data = buyListQ.get()
                oo = data[1]
                oo.DeleteOrder()
            
   

   
        # RESIZE SAME SIZE ORDERS and change price if they are different
        if "Sell" == buyOrSellio:
            while(not sellListQ.empty()):
                # retrieve and remove the order from the queue
                data = sellListQ.get()
                oo = data[1]
                
                # if there is not outstanding order qty either because we zeroed it out
                # or because it was zero in the first place ...
                if 0 >= qtyToSend:

                    oo.DeleteOrder()
                    continue
                    
                # just leave the orders with qties that sum up to the orignal qty
                if (abs(qtyToSend) < oo.Quantity()):
           
                    
                    oo.Quantity(abs(qtyToSend))
                    qtyToSend = 0
                    if oo.Price() <> ourNewPrice:
                        oo.Price(ourNewPrice)
                    oo.SendOrder()
                    
                elif (abs(qtyToSend) >= oo.Quantity()):
     
                    qtyToSend -= oo.Quantity()
          
                    if oo.Price() <> ourNewPrice:
                        oo.Price(ourNewPrice)
                        oo.SendOrder()
                    
                    
        else:
            while(not buyListQ.empty()):
                data = buyListQ.get()
                oo = data[1]
                         
                if 0 >= qtyToSend:
       
                    oo.DeleteOrder()
                    continue
                    
               # just leave the orders with qties that sum up to the orignal qty
                if (abs(qtyToSend) < oo.Quantity()):
     
                    
                    oo.Quantity(abs(qtyToSend))
                    qtyToSend = 0
                    if oo.Price() <> ourNewPrice:
                        oo.Price(ourNewPrice)
                    oo.SendOrder()
                    
                elif (abs(qtyToSend) >= oo.Quantity()):
   
                    qtyToSend -= oo.Quantity()
                    if oo.Price() <> ourNewPrice:
                        oo.Price(ourNewPrice)
                        oo.SendOrder()   
            
        # now send whatever qty is left
        if qtyToSend > 0:
            create_and_send_order(buyOrSellio, params, ourNewPrice, qtyToSend, session)
        
        params.quantity.Evaluator().RemoveSimulation()
        
    except Exception as err:
        msg = "Error while sending order: %s" % str(err)
        logger.info(msg)
        params.info.Evaluator().Value(msg)

    
    

def show_send_button(invokationInfo):
    cell = invokationInfo.Parameter("Cell")
    if cell:
        row_object = cell.RowObject()
        if row_object:
            if row_object.IsKindOf(acm.FSingleInstrumentAndTrades):
                if row_object.Instrument().OrderBooks().Size() > 0:
                    return True
                else:
                    return False
    return False
          







# start the static function
OrderCommandWatcher.monitor_thread()


