import ael
trds = ael.Portfolio['Equity Script Lending'].trades()
for t in trds:
    tc = t.clone()
    flag = 0
    if t.status != 'Void' and t.status != 'Simulated':
        if t.counterparty_ptynbr.ptyid == 'ABCAP':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES ABCAP']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABDEOML':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES ABSA AEDOML']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABGOLD':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES SBSA GOLD']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABSAB':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES SBSA GOLD']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABSASB':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES SBSA COLLATERAL']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABSCM':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES ABSCM']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'ABSTRA':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES ABSTRA']
            flag = 1
        if t.counterparty_ptynbr.ptyid == 'CAPITAL 360':
            tc.counterparty_ptynbr = ael.Party['EQUITY DERIVATIVES SOC GEN COLLATERAL']
            flag = 1
        if flag == 1:
            tc.commit()
