import acm
 
def showStartStopButtons(invokationInfo):
    return True

def start_algo(handler):
    if handler and handler.CanStartAgent():
        handler.SetAlgoAgentState('Pending Execution')
        return True
    return False
    
def stop_algo(handler):
    if handler and handler.CanStopAgent():
        handler.SetAlgoAgentState('Pending Stop')
        return True
    return False
    
def algo_order_do(order, session, block):
    result = False
    strategy = order.TradingStrategy()
    if strategy != None and order.IsKindOf(strategy.OrderClass()):
        handler = session.AttachOrder(order, True)
        result = block(handler)
    else:
        orders = order.OwnOrders()
        for o in orders:
            if algo_order_do(o, session, block):
                result = True
    return result
        
def invokation_order_do(invokationInfo, block):
    session = invokationInfo.ExtensionObject().ActiveSheet().TradingSession()
    button = invokationInfo.Parameter('ClickedButton')
    if session and button:
        order = button.RowObject()
        return algo_order_do(order, session, block)
    return False

def onStartButton(invokation_info):
    invokation_order_do(invokation_info, start_algo)

def onStopButton(invokation_info):
    invokation_order_do(invokation_info, stop_algo)

def onStartStopButton(invokation_info):
    if not invokation_order_do(invokation_info, stop_algo):
        invokation_order_do(invokation_info, start_algo)
