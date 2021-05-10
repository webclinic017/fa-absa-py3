import ael

def createPayment(amount, trade):
    t = trade.clone()
    p = ael.Payment.new(t)
    p.payday = ael.date_today()
    p.amount = amount
    p.curr = ael.Instrument["ZAR"]
    p.type = 'Internal Fee'
    p.ptynbr = ael.Party["ABSA BANK LTD"]
    p.text = "2013 Upgrade"
    p.commit()

def create_correction_payments():
    createPayment(-44032.53, ael.Trade[7560177])
    createPayment(-44032.53, ael.Trade[7576091])
    createPayment(-44032.53, ael.Trade[7589221])
    createPayment(-44032.53, ael.Trade[7604197])
    createPayment(13267.12, ael.Trade[9373621])
    createPayment(-13267.12, ael.Trade[9441951])
    createPayment(-9075.68, ael.Trade[9493646])
    createPayment(7037, ael.Trade[14300600])
    createPayment(-343230375, ael.Trade[3508968])
    createPayment(-33460675, ael.Trade[3631197])
    createPayment(331188914, ael.Trade[6316914])
    createPayment(864645, ael.Trade[6567533])

ael_variables = []
    
def ael_main(parameters):
    create_correction_payments()
