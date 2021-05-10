
import acm

def create_completion(invokation_info, caption):
    shell = get_shell(invokation_info)
    return acm.Trading.CreateCommandCompletion(shell, caption)
    
def accept_quote_price(side, request, invokation_info):
    sheet = get_sheet(invokation_info)
    session = sheet.TradingSession()
    quote = request.Answer()
    order = session.CreateQuoteRequestOrder(request, True)
    order.BuyOrSell('Sell' if side == 'Bid' else 'Buy')
    order.Price(quote.BidPrice() if side == 'Bid' else quote.AskPrice())
    order.Quantity(quote.BidQuantity() if side == 'Bid' else quote.AskQuantity())
    order.SendOrder()

def reject_price(request, invokation_info):
    acm.Trading.DeleteQuoteRequests([request], create_completion(invokation_info, 'Reject Quote'))

def improve_price(request, invokation_info):
    message = get_message(invokation_info, 'Improve Quote - Message')
    if message is not None:
        acm.Trading.RequestNewQuote(request, message, create_completion(invokation_info, 'Improve Quote'))
    
def get_row(invokation_info):
    button = invokation_info.Parameter('ClickedButton')
    if button:
        return button.RowObject()
    return None

def get_sheet(invokation_info):
    return invokation_info.Parameter('sheet')
    
def get_message(invokation_info, caption):
    return acm.UX.Dialogs().GetTextInput(get_shell(invokation_info), caption, '')
    
def get_shell(invokation_info):
    return invokation_info.Parameter('shell')


""" Quote Price Handling
"""       
def get_bid_price(invokation_info):
    return get_row(invokation_info).BidQuotePrice()

def get_ask_price(invokation_info):
    return get_row(invokation_info).AskQuotePrice()

def get_bid_price_request(invokation_info):    
    return get_bid_price(invokation_info).Request()

def get_ask_price_request(invokation_info):    
    return get_ask_price(invokation_info).Request()

def on_accept_quote_price(quote_price, invokation_info):
    accept_quote_price(quote_price.BidOrAsk(), quote_price.Request(), invokation_info)
        
def on_accept_quote_price_ask(invokation_info):
    on_accept_quote_price(get_ask_price(invokation_info), invokation_info)
    
def on_accept_quote_price_bid(invokation_info):
    on_accept_quote_price(get_bid_price(invokation_info), invokation_info)
    
def on_reject_quote_price_ask(invokation_info):
    reject_price(get_ask_price_request(invokation_info), invokation_info)
    
def on_reject_quote_price_bid(invokation_info):
    reject_price(get_bid_price_request(invokation_info), invokation_info)

def on_improve_quote_price_ask(invokation_info):
    improve_price(get_ask_price_request(invokation_info), invokation_info)
    
def on_improve_quote_price_bid(invokation_info):
    improve_price(get_bid_price_request(invokation_info), invokation_info)

def show_quote_price_button(invokation_info):
    return True

""" Trading Activity Handling
"""       
def get_quote_request(invokation_info):
    return get_row(invokation_info).QuoteRequestInfo()

def on_accept_trading_activity_ask(invokation_info):
    accept_quote_price('Ask', get_quote_request(invokation_info), invokation_info)
    
def on_accept_trading_activity_bid(invokation_info):
    accept_quote_price('Bid', get_quote_request(invokation_info), invokation_info)
    
def on_reject_trading_activity_quote(invokation_info):
    reject_price(get_quote_request(invokation_info), invokation_info)
    
def on_improve_trading_activity_ask(invokation_info):
    improve_price(get_quote_request(invokation_info), invokation_info)
    
def on_improve_trading_activity_bid(invokation_info):
    improve_price(get_quote_request(invokation_info), invokation_info)

def show_trading_activity_button(invokation_info):
    row = invokation_info.Parameter('Cell').RowObject()
    if row.QuoteRequestInfo():
        return True
    return False
