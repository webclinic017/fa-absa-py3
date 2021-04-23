import acm

PAYMENT_TYPE = "Broker Fee"

PAYMENT_LIST = [
    # JOB11
    [55862165, -70429.4103875],
    [55862182, -97051.9849725],
    [56404222, -68309.81759],
    [61052906, -65016.7881075],
    [61873226, -460257.264095],
    [61873256, -466875.702515],
    [62167510, -194158.44686],
    [62167521, -244400.12983],
    [62167527, -241828.291952],
    [77727763, -20.1174075],
    [83170821, -53.67215],

    # Other portfolios
    [12361058, 15.9059999984],
    [12361212, -68395.2717321],
    [12460143, -3682.20215852],
    [13369649, -15867.75],
    [13572521, -1048.848],
    [32305694, -12990.9365676],
    [35467241, -23592.840177],
    [53251754, -5811.80424884],
    [54455671, 360.197274677],
    [54663186, -11347.5472373],
    [54663218, -19.1543534014],
    [54897581, -12022.104998],
    [55337669, -19279.3899867],
    [56101978, 76.7625],
    [57216054, -1774.2063818],
    [57635042, -4549.70053576],
    [57635063, -6.7296243906],
    [57635065, -897.89136],
    [57635082, -680.5059],
    [63657225, -3876.25695727],
    [64268440, -69385.092571],
    [64268857, -29694.3252663],
    [64268898, -97060.0981223],
    [68367370, -15002.9459434],
    [70242682, -2289.216],
    [81574778, -6151.6907525],
    [81576617, -2266.80193507],
    [82363476, -4533.60387015],
    [82363936, -20525.6412165],
    [82364032, -1.78809228],
    [82364495, -2.520141],
    [83442592, -8.279205084],
]


def _update_broker_fee(trade, amount):
    for payment in trade.Payments():
        if payment.Type() == PAYMENT_TYPE and payment.Party() == trade.Counterparty():
            print("U Updating payment on trade %i (%s:%s)" % (
                trade.Oid(), trade.Portfolio().Name(), trade.Instrument().Name()))
            payment.Amount(payment.Amount() + amount)
            payment.Commit()
            return True

    print("A Adding payment to trade %i (%s:%s)" % (trade.Oid(), trade.Portfolio().Name(), trade.Instrument().Name()))
    payment = trade.CreatePayment()
    payment.Type(PAYMENT_TYPE)
    payment.Party(trade.Counterparty())
    payment.PayDay(trade.ValueDay())
    payment.ValidFrom(trade.ValueDay())
    payment.Currency(trade.Currency())
    payment.Amount(amount)
    payment.Commit()


print("Updating aggregate trades:")
for aggregate_id, amount in PAYMENT_LIST:
    trade = acm.FTrade[aggregate_id]
    _update_broker_fee(trade, amount)
