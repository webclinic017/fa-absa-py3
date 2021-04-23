import acm
import ael
import sys

context=acm.FContext["ACMB Global"]
links = context.ContextLinks()

for link in links:
    try:
#Remove underlying future mapping for stock future 
        if link.MappingType()== "Attribute2" and link.Type()=="Underlying Future Method" and link.Attribute1()=="Stock": 
            print >> sys.stderr, "Underlying future mapping for stock future is Removed"
            link.Delete()
#Replace ValOptAIC.Theor by core valuation function Black-Scholes-BESA
        if link.MappingType()== "Val Group" and link.Name()== "ValOptAIC_E.Theor":
            link.Type("Core Valuation Function")
            link.Name("Black-Scholes-BESA")
            print >> sys.stderr, "Context Link ValOptAIC_E.Theor is Updated for ", link.Name()
            link.Commit()
#Replace Yield Curve for Bond ZAR/R157 
        if link.MappingType()== "Instrument" and link.Instrument()== acm.FInstrument['ZAR/R157'] and link.Type()=="Yield Curve":
            link.Name("ZAR_Bond_discount_R157")
            link.Currency("ZAR")
            print >> sys.stderr, "Context Link for the Bond ZAR/R157 is Updated with ", link.Name()
            link.Commit()
    except:
        print >> sys.stderr, "Fail to update Context Definition Table"


#Link to be added to the ACMB Context:
#Instrument,Curr,Mapping Type,Parameter Name,Parameter Type
linkList =[['ZAR/R186', 'ZAR', 'Instrument', 'ZAR_Bond_discount_R186', 'Yield Curve'],
['ZAR/R209', 'ZAR', 'Instrument', 'ZAR_Bond_discount_R209', 'Yield Curve']]

count=0
for link in linkList:
    try:
        cl = acm.FContextLink()
        cl.Context = 'ACMB Global'
        cl.Instrument = acm.FInstrument[link[0]]
        if link[1] != 'None':
            cl.Currency = acm.FInstrument[link[1]]
        cl.MappingType = link[2]
        cl.Name = acm.FYieldCurve[link[3]]
        cl.Type = link[4]
        cl.Commit()
        count=count + 1
    except:
        print >> sys.stderr, "Fail to create context link for ", link
print >> sys.stderr, count, " Context Links for Bonds out of ", len(linkList), " were added successfully"
