import ael

   
def FromParty(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    if p.ptynbr != 2247 and p.ptynbr != 2246: #Funding Desk, Money Market Desk
        for ssi in p.settle_instructions():
            if ssi.seqnbr == seqnbr:
                if ssi.counterparty_ptynbr:
                    if ssi.counterparty_ptynbr.ptynbr != 2247 and ssi.counterparty_ptynbr.ptynbr != 2246: #Funding Desk, Money Market Desk
                        return 1
                else:
                    return 1
    return 0

def Curr(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for ssi in p.settle_instructions():
        if ssi.seqnbr == seqnbr:
            if ssi.display_id('curr') != 'ZAR':
                return 1
            else:
                return 0
        else:
            return 0

def SettleCFType(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for ssi in p.settle_instructions():
        if ssi.seqnbr == seqnbr:
            if ssi.settle_cf_type == 'Call Fixed Rate Adjustable':
                return 0
            elif ssi.settle_cf_type == 'Fixed Amount':
                return 0
            elif ssi.settle_cf_type == 'Redemption Amount':
                return 0
            elif ssi.settle_cf_type == 'Fixed Rate':
                return 0
            elif ssi.settle_cf_type == 'Premium':
                return 0
            elif ssi.settle_cf_type == 'Fixed Rate Adjustable':
                return 0
            else:
                return 1
        else:
            return 0

def Instype(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for ssi in p.settle_instructions():
        if ssi.seqnbr == seqnbr:
            if ssi.instype != 'Deposit':
                return 1
            else:
                return 0
        else:
            return 0

def SSIAccType(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for ssi in p.settle_instructions():
        if ssi.seqnbr == seqnbr:
            if ssi.account_type != 'Cash':
                return 1
            else:
                return 0
        else:
            return 0

def AccName(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if not a.name:
                return 1
            else:
                if a.correspondent_bank_ptynbr:
                    for al in a.correspondent_bank_ptynbr.aliases():
                        if al.type.alias_type_name == 'SWIFT':
                            bic = al.alias[0:4]
                            accountnbr = a.account[7:]
                            ac = (str)(bic) + '/' + (str)(accountnbr) + '/Z'
                            if a.name == ac:
                                return 0
                            else:
                                return 1
                            
                else:
                    return 1
    return 0

def AccCurr(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.display_id('curr') != 'ZAR':
                return 1
            else:
                return 0
        return 0

def AccType(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.account_type == 'Cash' or a.account_type == 'Cash and Security':
                return 0
            else:
                return 1
        else:
            return 0

def AccNetwork(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.display_id('network_alias_type') == 'SWIFT':
                return 0
            else:
                return 1
        else:
            return 0

def AccCorBank(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.correspondent_bank_ptynbr:
                if a.correspondent_bank_ptynbr.ptynbr == 9759: #ABN AMRO BANK NV JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 209: #ABSA BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 10748: #CALYON CORP AND INVEST BANK JHB
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 10426: #'FIRSTRAND BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 297: #INVESTEC BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 487: #MERCANTILE  BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 319: #NEDBANK LIMITED 
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 17000: #STANDARD CHARTERED BANK JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 337: #STANDARD BANK SA
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 346: #SOCIETE GENERALE JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 538: #SARB
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 9527: #CITI BANK NA JHB
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 0

def AccNbr(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if len(a.account) > 7:
                if a.account[6] != ' ':
                    return 1
                else:
                    if a.account[7:] == 'DIRECT':
                        return 0
                    elif (a.correspondent_bank_ptynbr.ptynbr == 9759 or a.correspondent_bank_ptynbr.ptynbr == 209  or a.correspondent_bank_ptynbr.ptynbr == 487 or a.correspondent_bank_ptynbr.ptynbr == 319 or a.correspondent_bank_ptynbr.ptynbr == 9527)  and len(a.account[7:]) == 10: #ABN AMRO BANK NV JOHANNESBURG, ABSA BANK LTD, MERCANTILE  BANK LTD, NEDBANK LIMITED, CITI BANK NA JHB
                        return 0
                    elif (a.correspondent_bank_ptynbr.ptynbr == 10426 or a.correspondent_bank_ptynbr.ptynbr == 17000 or a.correspondent_bank_ptynbr.ptynbr == 297) and len(a.account[7:]) == 11: #FIRSTRAND BANK LTD, STANDARD CHARTERED BANK JOHANNESBURG, INVESTEC BANK LTD
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 337 and len(a.account[7:]) == 9: #STANDARD BANK SA
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 346 and len(a.account[7:]) == 13: #SOCIETE GENERALE JOHANNESBURG
                        return 0
                    else:
                        return 1
            else:
                return 1
        else:
            return 0

def CPCode(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.correspondent_bank_ptynbr:
                if a.bic_seqnbr:
                    if a.correspondent_bank_ptynbr.ptynbr == 9759 and a.bic_seqnbr.alias == 'ABNAZAJJ':       #ABN AMRO BANK NV JOHANNESBURG
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 209 and a.bic_seqnbr.alias == 'ABSAZAJJ':      #ABSA BANK LTD
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 10748 and a.bic_seqnbr.alias == 'BSUIZAJJ':    #CALYON CORP AND INVEST BANK JHB
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 10426 and a.bic_seqnbr.alias == 'FIRNZAJJ':    #FIRSTRAND BANK LTD
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 297 and a.bic_seqnbr.alias == 'IVESZAJJ':      #INVESTEC BANK LTD
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 487 and a.bic_seqnbr.alias == 'LISAZAJJ':      #MERCANTILE  BANK LTD
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 319 and a.bic_seqnbr.alias == 'NEDSZAJJ':      #NEDBANK LIMITED
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 17000 and a.bic_seqnbr.alias == 'SCBLZAJJ':    #STANDARD CHARTERED BANK JOHANNESBURG
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 337 and a.bic_seqnbr.alias == 'SBZAZAJJ':      #STANDARD BANK SA
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 346 and a.bic_seqnbr.alias == 'SOGEZAJJ':      #SOCIETE GENERALE JOHANNESBURG
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 538 and a.bic_seqnbr.alias == 'SARBZAJP':      #SARB
                        return 0
                    elif a.correspondent_bank_ptynbr.ptynbr == 9527 and a.bic_seqnbr.alias == 'CITIZAJX':      #CITI BANK NA JHB
                        return 0
                    else:
                        return 1
                else:
                    return 1
            else:
                return 0
        else:
            return 0

def BranchCode(temp,ptynbr,accnbr,*rest):
    p = ael.Party[ptynbr]
    for a in p.accounts():
        if a.accnbr == accnbr:
            if a.correspondent_bank_ptynbr:
                if a.correspondent_bank_ptynbr.ptynbr == 9759 and a.account[0:6] == '740000':       #ABN AMRO BANK NV JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 209 and a.account[0:6] == '632005':      #ABSA BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 10748 and a.account[0:6] == '400105':    #CALYON CORP AND INVEST BANK JHB
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 10426 and a.account[0:6] == '255005':    #FIRSTRAND BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 297 and a.account[0:6] == '580105':      #INVESTEC BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 487 and a.account[0:6] == '450905':      #MERCANTILE  BANK LTD
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 319 and a.account[0:6] == '109114':      #NEDBANK LIMITED
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 17000 and a.account[0:6] == '730000':    #STANDARD CHARTERED BANK JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 337 and a.account[0:6] == '051001':      #STANDARD BANK SA
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 346 and a.account[0:6] == '194405':      #SOCIETE GENERALE JOHANNESBURG
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 538 and a.account[0:6] == '900145':      #SARB
                    return 0
                elif a.correspondent_bank_ptynbr.ptynbr == 9527 and a.account[0:6] == '350000':      #CITI BANK NA JHB
                    return 0
                else:
                    return 1
            else:
                return 1
        else:
            return 0

