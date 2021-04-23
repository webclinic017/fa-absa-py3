import acm


CLIENTS = [
    "OMIG ",
    "TAQUANTA AM ",
    "ABSA AM ",
    "CORONATION AM "
]

portfolio = acm.FPhysicalPortfolio["Call_2474"]
for id in CLIENTS:
    for trade in portfolio.Trades():
        if trade.Counterparty().Name().startswith(id):
            code = trade.Counterparty().Name().split(id)[1]
            if len(code.split(" ")) == 1:
                ins = trade.Instrument()
                if ins.ExternalId1() == "":
                    try:
                        ins.ExternalId1(code)
                        ins.Commit()
                        print("{0} --> {1}".format(code, ins.Name()))
                    except Exception as ex:
                        print("Code {0} already mapped: {1}".format(code, ex))
