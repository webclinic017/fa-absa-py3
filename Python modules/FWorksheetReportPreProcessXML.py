import acm
import re

ROUNDEDVALUES = []

def roundNumber(match):
    global ROUNDEDVALUES
    value = match.group()
    try:
        returnValue = str("<RawData>%.8f</RawData>" % float(value.split('>')[1].split('<')[0]))
    except:
        return value
    ROUNDEDVALUES.append((value, "%s" % returnValue)) 
    return returnValue

def removeScientificFormat(report, report_params, xmlReport):
    global ROUNDEDVALUES
    print "XML Before:"
    print  xmlReport
    p = re.compile("<RawData>[-+]?[0-9]*\.?[0-9]+[eE]([-+]?[0-9]+)?</RawData>")
    result= p.subn(roundNumber, xmlReport)
    xmlReportAfter = result[0]
    countReplace = result[1]
    print "XML After:"
    print xmlReportAfter
    print "\nScientific formated numbers found: %s" % countReplace
    print "\nReplacements done:"
    for v in ROUNDEDVALUES:
        print "%s --> %s" % (v[0], v[1])
    print ""
    ROUNDEDVALUES = []
    return xmlReportAfter
