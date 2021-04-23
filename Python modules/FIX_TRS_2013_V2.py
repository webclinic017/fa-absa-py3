import acm


def getFirstLeg(i, legTypes, nominalScalings):
    legs = [l for l in i.Legs() if l.LegType() in legTypes and l.NominalScaling() in  ('Dividend', 'Dividend Initial Price')]
    return legs[0] if legs else None

def getFirstLegHavingType(i, legTypes):
    legs = [l for l in i.Legs() if l.LegType() in legTypes]
    return legs[0] if legs else None


            
def deleteResetsForLegCashflows(legs, typeList):
    for leg in legs:
        if leg:
            for cf in leg.CashFlows():
                if cf.CashFlowType() in typeList:
                    for r in cf.Resets():
                        r.Delete()
    


for i in acm.FTotalReturnSwap.Instances():

    divLeg = getFirstLeg(i, ['Fixed'], ('Dividend', 'Dividend Initial Price'))
    trLeg = getFirstLegHavingType(i, ['Total Return'])
    callLeg = getFirstLeg(i, ['Call Fixed', 'Call Float'], ('Dividend', 'Dividend Initial Price'))
    fixedLeg = getFirstLeg(i, ['Fixed'], ('Dividend', 'Dividend Initial Price'))
    
    if i.Name() in ('ZAR/EQSWAP/IMP/19NOV09_19NOV10'):
        divLeg.NominalScaling('Dividend')
        divLeg.Commit()
        
    if i.Name() in ('ZAR/TRS/MTNDIVSWAP/110317#1'):
        deleteResetsForLegCashflows([l for l in i.Legs() if l.LegType() == 'Call Fixed'], ('Fixed Amount'))
        
    if divLeg and trLeg:
    
        if divLeg and trLeg.RollingPeriodCount() == 0 and trLeg.NominalScaling() == 'Initial Price' and len([cf for cf in divLeg.CashFlows() if cf.CashFlowType() == "Dividend"]) > 0:
            trLeg.NominalScaling('Price')
            trLeg.Commit()
            divLeg.NominalScaling('Dividend')
            divLeg.Commit()


        if trLeg.NominalScaling() in ('Price', 'Initial Price', 'None') and divLeg.NominalScaling() == 'Dividend':
            deleteResetsForLegCashflows([divLeg, callLeg], ('Fixed Amount'))
            deleteResetsForLegCashflows([divLeg], ('Dividend'))


names = [ i.Name() for i in acm.FTotalReturnSwap.Instances() if len(i.Legs()) == 4 and not i.IsExpired()]
print names
legnbrs = [1421675, 1312011, 1421744]

for legnbr in legnbrs:
    leg = acm.FLeg[legnbr]
    if leg:
    	leg.Delete()
