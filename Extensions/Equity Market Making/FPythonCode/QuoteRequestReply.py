"""----------------------------------------------------------------------------
MODULE
    QuoteRequestReply - Hooks for quote request reply.

    (c) Copyright 2014 by SunGard FRONT ARENA. All rights reserved.
 ---------------------------------------------------------------------------"""
import acm

def on_send_reply_button(invokation_info):
    button = invokation_info.Parameter('ClickedButton')
    if button:
        row = button.RowObject()
        send_reply_with_unfirm_alert(row.QuoteController().UI())

def send_reply_with_unfirm_alert(ui):
    ui.UnfirmQuoteAlert(True)
    ui.QuoteReply()
                     
def send_reply_without_unfirm_alert(ui):
    ui.UnfirmQuoteAlert(False)
    ui.QuoteReply()    

def stop_unfirm_alert(ui):
    ui.UnfirmQuoteAlert(False)

def get_reply_action(status):
    constraint = status.Constraint()
    if constraint == 'Bid':
        return 'You buy'
    elif constraint == 'Ask':
        return 'You sell'
    return 'Send'

def on_show_contributed_quote(invokation_info):
    button = invokation_info.Parameter('ClickedButton')
    if button:
        row = button.RowObject()    
    try:
        navigate_to_controller(get_contribution_controller(row.QuoteController()))
    except Exception as e:
        shell = invokation_info.Parameter('shell')
        if shell:
            acm.UX().Dialogs().MessageBox(shell, 'Error', str(e), 'OK', None, None,  'Button1', 'Button1')

def get_contribution_controller(rfq_controller):
    aggr_quote = acm.FAggregatedQuote(rfq_controller.TradingInterface())
    return acm.MarketMaking.GetActiveController(aggr_quote.Channel())

def navigate_to_controller(controller):
    if controller:
        acm.MarketMaking.NavigateToQuoteController(controller)

def ignore_and_send(ui):
    ui.IgnoreBreachedSafetyRules()
    ui.UnfirmQuoteAlert(True)
    ui.QuoteReply()

def take_countered_price(ui):
    ui.TakeCounteredPrice()

def send_reply_menu(cell_info, menu):
    row = cell_info.RowObject()
    controller = row.QuoteController()
    ui = controller.UI()
    status = controller.QuoteRequestReply()
    send_action = get_reply_action(status)
    can_be_answered = status.CanBeAnswered()
    can_take_countered = status.CanTakeCountered() 
    menu.AddItem(send_reply_with_unfirm_alert, ui, send_action, ' ', can_be_answered)
    menu.AddItem(send_reply_without_unfirm_alert, ui, send_action + ' & forget', ' ', can_be_answered)
    menu.AddItem(ignore_and_send, ui, 'Ignore breached safety rules & send', ' ', can_be_answered)
    menu.AddItem(stop_unfirm_alert, ui, 'Stop Monitoring', ' ', status.IsUnfirmQuoteAlertEnabled())
    menu.AddItem(take_countered_price, ui, 'Take countered price', ' ', can_take_countered)
