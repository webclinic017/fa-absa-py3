import acm, csv, string, FRunScriptGUI

'''
Date                    : 2010-08-03
Purpose                 : Displays specific additional info fields for all portfolios in specified input portfolios
Requester               : Marko Milutinovic 
Developer               : Rohan van der Walt
CR Number               : 392371
'''

def listOfPortfolios():
    return acm.FPhysicalPortfolio.Select('')
    
directorySelection=FRunScriptGUI.DirectorySelection()

ael_variables = [
['Portfolios', 'Portfolios', acm.FPhysicalPortfolio, listOfPortfolios(), '9806,9399', 1, 1, 'Portfolios to do check on', None, 1],
['OutputPath', 'Report Directory', directorySelection, None, directorySelection, 1, 1, 'The directory where the report will be generated.', None, 1],
]

ael_gui_parameters = {'windowCaption':'Portfolios Additional info report'}

def ael_main(dict):
    if not str(dict['OutputPath'])[-1] == "\\":
        dict['OutputPath'] = str(dict['OutputPath']) + '\\'
    nsTime = acm.Time()
    listOfPortfolios = dict['Portfolios']
    result = [['Portfolio', 'SL_AllocatedDesk', 'SL_Portfolio_Type', 'SL_ReservedStock', 'SL_Sweeping', 'Parent_Portfolio']]
    for i in listOfPortfolios:
        result = checkPortfolio(i, result)
    file = None
    try:
        YMD = nsTime.DateToYMD(nsTime.DateToday())
        y = str(YMD[0])
        m = string.zfill(str(YMD[1]), 2)
        d = string.zfill(str(YMD[2]), 2)
        filepath = str(dict['OutputPath'])+'SL_AdditionalInfoReport_'+y+m+d+'.csv'
        file = open(filepath, 'wb')
        writer = csv.writer(file)
        for row in result:
            writer.writerow(row)
    except:
        print 'ERR: Could not open/write file'
    finally:
        if file:
            file.close()
            print 'File written to:', filepath
    
def checkPortfolio(port, result):
    if port.Compound():
        for ol in port.OwnerLinks():
            result = checkPortfolio(ol.MemberPortfolio(), result)
    else:
        result.append([port.Name(), port.add_info('SL_AllocatedDesk'), port.add_info('SL_Portfolio_Type'), port.add_info('SL_ReservedStock'), port.add_info('SL_Sweeping'), port.add_info('Parent_Portfolio')])
    return result

