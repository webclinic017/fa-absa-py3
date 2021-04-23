'''
Purpose: Changed acm.FIndex to acm.FEquityIndex as part of the 2010.2 upgrade.
Developer: Willie van der Bank
20/08/2011
'''

import acm
import sys


if (not (acm.FPhysInstrGroup["NonSplitIndexesPricedFromMarket"])):
    page = acm.FPageGroup["FPages"]
    newPage = acm.FPhysInstrGroup()
    newPage.Name = "NonSplitIndexesPricedFromMarket"
    newPage.Cid = "Instruments"
    newPage.SuperGroup = page
    newPage.Terminal = "true"
    newPage.Commit()

    indexes=acm.FEquityIndex.Select('')
    nonSplitIndexPage = acm.FPhysInstrGroup["NonSplitIndexes"]
    nonSplitIndexSecondPage = acm.FPhysInstrGroup["NonSplitIndexesPricedFromMarket"]
    count=0

    for ins in indexes:
        if (nonSplitIndexPage.Includes(ins)):
            isg = acm.FInstrGroupMap(ins)
            isg.Instrument(ins.Name())
            firstPage=acm.FPhysInstrGroup["NonSplitIndexesPricedFromMarket"]
            x=firstPage.Clone()
            x.InstrGroupMaps().Add(isg)
            firstPage.Apply(x)
            firstPage.Commit()
            count=count+1
    print(count, " Indexes are added to the NonSplitIndexesPricedFromMarket Page", file=sys.stderr)        
            
            
    for ins in indexes:
            if not (nonSplitIndexPage.Includes(ins)):
                isg = acm.FInstrGroupMap(ins)
                isg.Instrument(ins.Name())
                secondPage=acm.FPhysInstrGroup["NonSplitIndexes"]
                y=secondPage.Clone()
                y.InstrGroupMaps().Add(isg)
                secondPage.Apply(y)
                secondPage.Commit()
                count=count+1
        
    print(count, " Indexes are added to the NonSplitIndexes Page", file=sys.stderr)

    count=0

    for ins in indexes:
        if (len(ins.InstrumentMaps())==0) and (not (nonSplitIndexSecondPage.Includes(ins))) and (ins.Name()<>'EquityIndexDefault') and (ins.Name()<>'Test_Basket_Template2'):
            isg = acm.FInstrGroupMap(ins)
            isg.Instrument(ins.Name())
            secondPage=acm.FPhysInstrGroup["NonSplitIndexesPricedFromMarket"]
            z=secondPage.Clone()
            z.InstrGroupMaps().Add(isg)
            secondPage.Apply(z)
            secondPage.Commit()
            count=count+1

    print(count, " Indexes without Components are added to the NonSplitIndexesPricedFromMarket Page", file=sys.stderr)
else:
    print("Page NonSplitIndexesPricedFromMarket does already exist", file=sys.stderr)
