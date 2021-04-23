import ael, acm, time
from zak_funcs import write_file

#===============================
# Zaakirah 2009
# Audit for vol
#================================


today = ael.date_today()
yes = today.add_banking_day(ael.Instrument['ZAR'], -1)
yesd=  yes.to_string('%m/%d/%y')
tdict = acm.FDictionary()
call = {'True': 'CALL', 'False':'PUT'}

va = ['Currency', 'Framework', 'InterpolationMethod', 'IsHullWhiteStructure', 'ReferenceInstrument', 'RiskType', 'StructureType',
 'StrikeType', 'VolatilityValueType', 'UseUnderlyingMarketPrice', 'VolatilityValueType', 'BondVolatilityType', 'DisplayIR', 'Points']

vol_att =['.' + x + '()' for x in va]

def trds(instrs):
    global tdict
    for o in instrs:
        trds = o.Trades()
        vol = o.MappedVolatilityLink().Link().VolatilityStructure().Name()
        if not tdict.HasKey(vol):
            tdict.AtPut(vol, 0)
        for t in trds:
            if t.Status() not in ('Simulated', 'Void', 'Terminated'):
                tdict[vol]+= 1
                
options = acm.FInstrument.Select('insType = "Option" and generic = 0 and expiryDate > "%s" and archiveStatus = 0' %yesd)
caps = acm.FInstrument.Select('insType = "Cap" and generic = 0 and expiryDate > "%s" and archiveStatus = 0' %yesd)
floors = acm.FInstrument.Select('insType = "Floor" and generic = 0 and expiryDate > "%s" and archiveStatus = 0' %yesd)
trds(options)
trds(caps)
trds(floors)                
#print 'done getting trades'
def get_att(yc):
    att = []
    for p in yc.Points():
        spread = acm.FYCSpread.Select("point = '%s'" %p.Oid())
        for s in spread:
            
            if yc.AttributeType() == 'Issuer':
                if s.Attribute().Issuer().Name() not in att:
                    att.append(s.Attribute().Issuer().Name())
            if yc.AttributeType() == 'Currency':
                if s.Attribute().Issuer().Name() not in att:
                    att.append(s.Attribute().Currency().Name())
    return att


def check_vols():
    results = [['VOL SURFACE', 'PROPERTY', 'BEFORE', 'AFTER', 'LAST UPDATE USER', 'USER GROUP', 'NUMBER OF TRADES']]
    vols = acm.FVolatilityStructure.Select("historicalDay = ''" )

    for v in vols:
        
        if ael.date_from_time(v.UpdateTime()) == today:
            yl = acm.FVolatilityStructure.Select("originalStructure = '%s' and historicalDay = '%s'" %(v.Oid(), yesd))

            for a in vol_att:
                
                if len(yl) > 0:
                    y = yl.At(0)

                    if a == '.Points()':
                        oldp = []
                        newp = []
                        for x in v.Points():
                            if x.Benchmark():
                                newp.append(x.Benchmark().Name())
                            else:
                                newp.append(call[str(x.Call())]+ '/'+x.ExpiryPeriod()+ '/' +  x.UnderlyingMaturityPeriod() + '/'+ str(x.Strike()))
                        
                        for x in y.Points():
                            if x.Benchmark():
                                oldp.append(x.Benchmark().Name())
                            else:
                                oldp.append(call[str(x.Call())]+ '/'+x.ExpiryPeriod()+ '/' +  x.UnderlyingMaturityPeriod() + '/'+ str(x.Strike()))
                        e1 = set(newp)
                        e2 = set(oldp)
                        
                        for b in e1.difference(e2):
                            
                            results.append([v.Name(), 'BENCHMARK INS', b, 'ADDED TO CURVE', v.UpdateUser().Name(), v.UpdateUser().UserGroup().Name(), tdict[v.Name()]])
                        for b in e2.difference(e1):
                            
                            results.append([v.Name(), 'BENCHMARK INS', b, 'REMOVED FROM CURVE', v.UpdateUser().Name(), v.UpdateUser().UserGroup().Name(), tdict[v.Name()]])
                            
                    else:
                        if eval("v" + a) != eval("y" + a):
                            #print v.Name(), a, eval("v" + a), eval("y" + a)
                            results.append([v.Name(), a[1:(len(a)-2)], eval("v" + a), eval("y" + a), v.UpdateUser().Name(), v.UpdateUser().UserGroup().Name(), tdict[v.Name()]])
                            
                else:
                    results.append([v.Name(), 'UNABLE TO LOCATE VPS CURVE FOR COMPARE',  ael.date_from_time(v.UpdateTime()).to_string('%m/%d/%Y'), '', v.UpdateUser().Name(), v.UpdateUser().UserGroup().Name(), tdict[v.Name()]])            
        else:
            if ael.date_from_time(v.UpdateTime()) < today.add_banking_day(ael.Instrument['ZAR'], -5):
                results.append([v.Name(), 'STALE VOL SURFACE',  ael.date_from_time(v.UpdateTime()).to_string('%m/%d/%Y'), '', v.UpdateUser().Name(), v.UpdateUser().UserGroup().Name(), tdict[v.Name()]])
                
    return results
                            
r = []                
r = check_vols()
prod = '//services/frontnt/BackOffice/Atlas-End-Of-Day/' +  ael.date_today().to_string('%Y-%m-%d') + '/'
#'//apps/frontnt/REPORTS/BackOffice/Atlas-End-Of-Day'
if len(r) > 1:
    #write_file('f://VOL_SURFACE.csv', r)
    write_file(prod + 'SAGEN_AUDIT_VOL_CONST.csv', r)
else:
    ael.log('SAGEN_AUDIT_VOL_CONST: NO AMENDMENTS TO VOL SURFACES')
