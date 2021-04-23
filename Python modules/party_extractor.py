import acm


CODES = [
    "ALSUPF",
    "OMDEMF",
    "ISBAMB",
    "MAFEMB",
    "MAGAFN",
    "MGMMMB",
    "OMDFFU",
    "OMUTMF",
    "SWABAL",
    "OM3MMB",
    "RGACMB",
    "SABCBD",
    "ATTFCB",
    "ATTIMB",
    "BIDPRV",
    "BONMMB",
    "CCT001",
    "ISPFIL",
    "MHCMMB",
    "NABPMB",
    "OMGTMF",
    "OMICMF",
    "OMIMMF",
    "OMIPMF",
    "OMSMMB",
    "POPF01",
    "SMIAB2",
    "STANMM"
]


TRADES = acm.FPhysicalPortfolio["Call_2474"].Trades()

for code in CODES:
    parties = acm.FParty.Select("name like *%s*" % code)
    if parties:
        print(code)
        for party in parties:
            party_trades = []
            for trade in TRADES:
                if trade.Counterparty() == party:
                    ins = trade.Instrument()
                    print("\t{0} {1} {2} {3} {4}".format(party.Name(), ins.Name(), ins.ExternalId1(), trade.Oid(), trade.Status()))
                    #if ins.ExternalId1() == "":
                    #    ins.ExternalId1(code)
                    #    ins.Commit()
                    


