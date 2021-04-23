import acm

def portf_is_graveyarded(portf):
    import acm
    
    if not portf:
        return False

    acm_portf = portf
    if isinstance(portf, str):
        acm_portf = acm.FPhysicalPortfolio[portf]

    if acm_portf.Name() == "GRAVEYARD":
        return True
    for l in acm_portf.MemberLinks():
        return portf_is_graveyarded(l.OwnerPortfolio())
    return False
    
ALIAS = "MATINBCI"

PSWAPS = list(acm.FPortfolioSwap.Select("name like '*%s*'" % ALIAS))
CALLACCS = list(acm.FDeposit.Select("name like '*%s*'" % ALIAS))
INSTRS = PSWAPS + CALLACCS

for instr in INSTRS:
    for t in instr.Trades():
        if t.Status() == "Terminated":
            print(instr.Name(), t.Oid(), t.Status(), t.PortfolioId(), portf_is_graveyarded(t.Portfolio()))
            t.Status('BO Confirmed')
            t.Commit()
            print('Changed to "BO Confirmed" status')
            
print('Completed successfully')
