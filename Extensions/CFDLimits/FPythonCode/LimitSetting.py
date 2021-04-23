"""-----------------------------------------------------------------------
MODULE
    LimitSetting

DESCRIPTION
    Institutional CFD Project
    
    Date                : 2010-10-23
    Purpose             : Sets the trading position limits for each Stock in a Portfolio.
                          For compound portfolios, all the underlying member portfolios will be included.
    Department and Desk : Prime Services
    Requester           : Francois Henrion
    Developer           : Marco Cerutti
    CR Number           : 455227

ENDDESCRIPTION
-----------------------------------------------------------------------"""
import acm
import FBDPGui
reload(FBDPGui)
import LimitUtils
reload(LimitUtils)

FACTOR = 4

def getMemberPortfolios(port, result):
    if port.Compound():
        result.append( port.Name())
        for ol in port.OwnerLinks():
            getMemberPortfolios(ol.MemberPortfolio(), result)
    else:
        result.append(port.Name())


def createLimit(ins, portf, limit):
    """Set the ExtensionValue, with name based on portfolio and instrument"""
    
    #print "%s|%s|%f" % (portf.Name(), ins.Name(), limit)
    
    extContext = acm.FExtensionContext[LimitUtils.EXTENSION_CONTEXT]
    module = acm.FExtensionModule[LimitUtils.EXTENSION_MODULE]
    
    extValText = "FInstrumentAndTrades:PortfolioProfitLossPeriodPositi'%s/%s'\n%f" % \
                    (portf.Name(), ins.Name(), limit)
                    
    extContext.EditImport('FExtensionValue', extValText, None, module)
    module.Commit()
    extContext.Commit()
    
def date_cb(index, fieldValues):
 
    endDate = fieldValues[index]
    
    if endDate == 'Custom Date':
        ael_variables.endDateCustom.enable(endDate, ttCustomDate)
    else:
        ael_variables.endDateCustom.enable(None, ttEndDateInactive)
    
    fieldValues[ael_variables.endDateCustom.sequenceNumber] = LimitUtils.EndDateList[endDate]
        
    return fieldValues 
 

#Global Constants    
#GUI Globals
ttPortfolio = 'The Portfolios to evaluate. If you select a compound portfolio, all the underlying member portfolios will be included.'
ttCustomDate = 'The date to set the limit for.'
ttEndDateInactive = "A custom date has to be selected to use this field. "
 
#Physical and compound portfolios
ListOfPortfolios = [all.Name() for all in acm.FPhysicalPortfolio.Select('')]
ListOfPortfolios.sort()
 
ael_variables = FBDPGui.LogVariables(
    ['Portfolio', 'Portfolio_Limit Setting', 'string', ListOfPortfolios, '', 1, 1, ttPortfolio, ttPortfolio, None],
    ['endDate', 'End Date_Limit Setting', 'string', LimitUtils.EndDateListSortedKeys, 'Now', 1, 0, ttCustomDate, date_cb, 1],
    ['endDateCustom', 'End Date Custom_Limit Setting', 'string', None, LimitUtils.EndDateList['Now'], 1, 0, ttEndDateInactive, None, 0])
 
def ael_main(parameters):

    if parameters['endDate'] == 'Custom Date':
        enddate = parameters['endDateCustom']
    else:
        enddate = LimitUtils.EndDateList[parameters['endDate']]

    for portName in parameters['Portfolio']: 
        portfolios = []
        port = acm.FPhysicalPortfolio[portName]
        getMemberPortfolios(port, portfolios)
        
        for portfolio in portfolios:
            portf = acm.FPhysicalPortfolio[portfolio]
            for ins in sorted(portf.Instruments(), key=lambda this: this.Name()):
                
                price = acm.FPrice.Select01("instrument = %s and market = '%s' and day = %s" % 
                                          (ins.Oid(), LimitUtils.THREE_MONTH_MARKET, enddate),
                                          'NaN')
                if price:
                    settle = price.Settle()
                    if settle > 0:
                        createLimit(ins, portf, FACTOR * settle)
                else:
                    print "Limit not set: no Average price for: ", ins.Name()
