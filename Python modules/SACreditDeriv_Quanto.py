import ael, math

def update_spreads(master, slave):
    spreadDictMaster=get_spreads(master)
    spreadDictSlave=get_spreads(slave)
    for issuer in spreadDictSlave:
        spreadDictSlaveIssuer=spreadDictSlave[issuer]
        spreadDictMasterIssuer=spreadDictMaster[issuer]
        for period in spreadDictSlaveIssuer:
            spread_clone=spreadDictSlaveIssuer[period].clone()
            #print spread_clone.spread
            newSpread=calculate_spread(spreadDictMasterIssuer[period].spread, issuer, period)
            #print spread_clone.spread, newSpread,issuer,period
            spread_clone.spread=newSpread
            spread_clone.commit()
            #print spread_clone.spread
def calculate_spread(orgSpread, issuer, period):
    #print spreadData[1][-1],spreadData[1][:-1]
    if period[-1]=='y':
        t=float(period[:-1])
    elif period[-1]=='m':
        t=float(period[:-1])/12
    elif period[-1]=='w':
        t=float(period[:-1])/52
    else:
        t=float(period[:-1])/365
    c1, c2, c3=0, 0, 0
    #print issuer
    try:
        c1=float(ael.Party[issuer].add_info('CDSQuanto1'))
        c2=float(ael.Party[issuer].add_info('CDSQuanto2'))
        c3=float(ael.Party[issuer].add_info('CDSQuanto3'))
    except:
        print 'Constant value is missing for ' +issuer
        pass
    
    spread=orgSpread*(c1*math.exp(c2*t)+c3)
    
    print issuer, spread, orgSpread, period, c1, c2, c3, float(period[:-1])
    return spread
    
def get_spreads(master):
    attributes=master.attributes()
    issuerDict={}
    for attr in attributes:
        print attr.issuer_ptynbr.ptyid
        spreads=attr.spreads()
        spreadDict={}
        for s in spreads:
            spreadDict[s.point_seqnbr.date_period]=s
            
        issuerDict[attr.issuer_ptynbr.ptyid]=spreadDict    
    #print issuerDict
    return issuerDict
yc1=ael.YieldCurve['CDIssuerCurve_HR_EUR']
yc2=ael.YieldCurve['CDIssuerCurve_HR_EURZAR']
update_spreads(yc1, yc2)
