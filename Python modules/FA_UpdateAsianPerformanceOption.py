import acm
import sys

cl  = acm.FChoiceList()
cl.List = "Valuation Extension"
cl.Name = 'theorAsianPerformance'
try:
    cl.Commit()
except:
    print >> sys.stderr, "Failed to commit valuation extension theorAsianPerformance to the chice list, possibly duplicate"
    
#inss = acm.FOption.Select('')
#insArray=inss.AsArray()     

insNames=['ZAR/EQ/ALSI/17NOV14/C/100/ASIA/INOUT', 'ZAR/EQ/ALSI/17NOV14/C/124.07/ASIA/INOUT']

context=acm.FContext['ACMB Global']

for insName in insNames:
    print insName
    ins=acm.FOption[insName]
    print >> sys.stderr, ins.Name()
    cl = acm.FContextLink()
    cl.Context = context
    cl.Instrument=ins
    cl.MappingType = 'Instrument'
    cl.Name = 'theorAsianPerformance'
    cl.Type = 'Valuation Extension'
    try:
        cl.Commit()
        print >> sys.stderr, "Asian Performance Option", ins.Name(), "has been successfully setup"
    except: 
        print >> sys.stderr, "Failed to commit context link for option ", ins.Name(), " possibly duplicate"

'''The code below is too performance consuming therefore we will pick up the options specifying the names
for ins in insArray:
    print ins.Name()
    if ins.AdditionalInfo().Forward_Start_Type()=="Performance":
        print >> sys.stderr, ins.Name()
        cl = acm.FContextLink()
        cl.Instrument=ins
        cl.MappingType = 'Instrument'
        cl.Name = 'theorAsianPerformance'
        cl.Type = "Valuation Extension"
        cl.Commit()
        print "Asian Performance Option", ins.Name()'''
