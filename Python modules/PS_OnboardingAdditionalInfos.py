'''----------------------------------------------------------------------------------------------------------------------------------
# Purpose                       :  Sets additional infos on a single portfolio, child portfolios of a given compound portfolio and on party level.
                                    Two ways of setting: use the run script parameters or use a csv upload file.
                                    Python script: xxx can be used to check that values have been correctly set.
                                    Corrected variable errors for file upload.
# Department and Desk           :  Front Arena BTB/MO/CCG (part of Prime Brokerage client on-boarding)
# Requester                     :  Bhavnisha Sarawan
# Developer                     :  Bhavnisha Sarawan
# CR Number                     :  C156076, C175473
----------------------------------------------------------------------------------------------------------------------------------'''



import ael, acm, string


TableList     = ['Party', 'Portfolio']
ValuesList = {'MT940Recipient':acm.FParty.Select(''),'PS_ClientFundName':['']}
boolDict = {'Yes': True, 'No': False}
boolDictDisplay = boolDict.keys()

def enableAddInfoName(index, fieldValues):
    if fieldValues[0] == 'Party':
        ael_variables[1][9] = 1
        ael_variables[2][9] = 1
        ael_variables[3][9] = 0
        ael_variables[5][9] = 0
        enableAddValue(index, fieldValues)
    elif fieldValues[0] == 'Portfolio':
        ael_variables[3][9] = 1
        ael_variables[4][9] = 1
        ael_variables[1][9] = 0
        ael_variables[6][9] = 0
        enableAddValue(index, fieldValues)
    return fieldValues
    
def enableAddValue(index, fieldValues):
    if fieldValues[0] == 'Party':
        if ael_variables[1][9] == 1 and fieldValues[1] != '':
            ael_variables[5][9] = 1
            ael_variables[6][9] = 0
            showChoiceList(index, fieldValues)
    elif fieldValues[0] == 'Portfolio' and fieldValues[3] != '':
        if ael_variables[3][9] == 1:
            ael_variables[6][9] = 1
            ael_variables[5][9] = 0
            showChoiceList(index, fieldValues)
    return fieldValues

def showChoiceList(index, fieldValues):
    if ael_variables[5][9] == 1 and fieldValues[1] != '':
        if fieldValues[1] != '':
            ael_variables[6][9] = 0
            for k in ValuesList.keys():
                if fieldValues[1] == k:
                    choiceList = []
                    for a in ValuesList[k]:
                        choiceList.append(a)
                    ael_variables[5][3] = choiceList
                    ael_variables[5][9] = 1
    elif ael_variables[6][9] == 1 and fieldValues[3] != '':
        if fieldValues[3] != '':
            ael_variables[5][9] = 0
            for k in ValuesList.keys():
                if fieldValues[3] == k:
                    choiceList = []
                    for a in ValuesList[k]:
                        choiceList.append(a)
                    ael_variables[6][3] = choiceList
                    ael_variables[6][9] = 1
    return fieldValues

def enableUpload(index, fieldValues):
    if fieldValues[9] == 'Yes':
        ael_variables[0][9] = 0
        ael_variables[1][9] = 0
        ael_variables[2][9] = 0
        ael_variables[3][9] = 0
        ael_variables[4][9] = 0
        ael_variables[5][9] = 0
        ael_variables[6][9] = 0
        ael_variables[7][9] = 1
        ael_variables[8][9] = 1
        fieldValues[0] = ''
        fieldValues[1] = ''
        fieldValues[3] = ''
    elif fieldValues[9] == 'No':
        ael_variables[0][9] = 1
        ael_variables[1][9] = 1
        ael_variables[2][9] = 1
        ael_variables[3][9] = 0
        ael_variables[4][9] = 0
        ael_variables[5][9] = 1
        ael_variables[6][9] = 0
        ael_variables[7][9] = 0
        ael_variables[8][9] = 0
    return fieldValues

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Setting Prime Additonal Infos'}
                      
# these parameters are not mandatory as different combinations are needed to get the full set of data.
ael_variables = [ ['Entity', 'Entity', 'string', TableList, 'Party', 0, 0, 'table to set add info', enableAddInfoName, 1],
                  ['Party AddInfo Name', 'Party AddInfo Name', acm.FAdditionalInfoSpec, acm.FAdditionalInfoSpec.Select('recType = Party'), 'MT940Recipient', 0, 0, '', enableAddValue, 0],
                  ['Party Name', 'Party Name', acm.FParty, acm.FParty.Select(''), '', 0, 0, '', None, 0],
                  ['Portfolio AddInfo Name', 'Portfolio AddInfo Name', acm.FAdditionalInfoSpec, acm.FAdditionalInfoSpec.Select('recType = Portfolio'), 'PS_ClientFundName', 0, 0, '', enableAddValue, 0],
                  ['Portfolio Name', 'Portfolio Name', acm.FPhysicalPortfolio, acm.FPhysicalPortfolio.Select(''), '', 0, 0, '', None, 0],
                  ['Party AddInfo Value', 'Party AddInfo Value', 'string', [], '', 0, 0, '', showChoiceList, 0],
                  ['Portfolio AddInfo Value', 'Portfolio AddInfo Value', 'string', [], '', 0, 0, 'value to set', showChoiceList, 0],
                  ['Path', 'Path', 'string', None, '', 0, 0, 'value to set', None, 0],
                  ['Filename', 'Filename', 'string', None, '', 0, 0, 'value to set', None, 0],
                  ['Use Upload File', 'Use Upload File', 'string', boolDictDisplay, 'No', 0, 0, '', enableUpload, 1],
                  ['Set Single Portfolio', 'Set Single Portfolio', 'string', boolDictDisplay, 'No', 0, 0, '', None, 1] ]

def setAddInfo(entity, addInfoName, addInfoValue):
    print addInfoName, addInfoValue
    if entity.AdditionalInfo().GetProperty(addInfoName) == None:
        addInfo = acm.FAdditionalInfo()
        addInfo.Recaddr(entity.Oid())
        addInfo.AddInf(addInfoName)
        addInfo.Value(addInfoValue)
        try:
            addInfo.Commit()
        except Exception, e:
            print 'Commit failed', e
    else:
        addInfo = acm.FAdditionalInfo.Select('recaddr = %i' %entity.Oid())
        for i in addInfo:
            if i.AddInf().Name() == addInfoName:
                i.Value(addInfoValue)
                try:
                    i.Commit()
                except Exception, e:
                    print 'Commit failed', e



def FindPort(portfolio, addInfoName, addInfoValue):
    if not portfolio.Compound():
        setAddInfo(portfolio, addInfoName, addInfoValue)
    else:
        for pl in portfolio.SubPortfolios():
            FindPort(pl, addInfoName, addInfoValue)

def file_upload(filename):

    count = 0
    try:
    	f = open(filename)
    except:
    	print 'Could not open file'
	return

    line = f.readline()    	
    #line = f.readline()
    while line:
    	l = string.split(line, ',')
	entityType = l[0]
	entityName = l[1]
	AddInfoName = l[2]
        print AddInfoName 
	AddInfoValue = l[3]
	if entityType == 'Party':
            entity = acm.FParty[entityName]
            try:
                setAddInfo(entity, AddInfoName, AddInfoValue)
                count = count + 1
            except Exception, e:
                print 'Error: Could not update additional info value %s,%s' %(entity.Name(), AddInfoName)
                print e
        elif entityType == 'Portfolio':
            entity = acm.FPhysicalPortfolio[entityName]
            try:
                FindPort(entity, AddInfoName, AddInfoValue)
                count = count + 1
            except Exception, e:
                print 'Error: Could not update additional info value %s,%s' %(entity.Name(), AddInfoName)
                print e
        else:
            print 'incorrect entity type - ', entityType
        line = f.readline()  

    f.close()
    print 'AddInfos committed : ', count


def ael_main(parameter):

    Entity = parameter['Entity']
    if Entity == 'Party':
        PartyAddInfoName = parameter['Party AddInfo Name']
        PartyName = parameter['Party Name']
        PartyAddInfoValue = parameter['Party AddInfo Value']
        
        setAddInfo(PartyName, PartyAddInfoName, PartyAddInfoValue)
        print 'Completed'
        
    elif Entity == 'Portfolio':
        PortfolioAddInfoName = parameter['Portfolio AddInfo Name']
        PortfolioName = parameter['Portfolio Name']
        PortfolioAddInfoValue = parameter['Portfolio AddInfo Value']
        SetSinglePortfolio = parameter['Set Single Portfolio']
        
        if SetSinglePortfolio == 'Yes':
            setAddInfo(PortfolioName, PortfolioAddInfoName, PortfolioAddInfoValue)
        else:
            FindPort(PortfolioName, PortfolioAddInfoName, PortfolioAddInfoValue)
        print 'Completed'

    elif Entity == '':
        outputPath = parameter['Path']
        outputName = parameter['Filename']
        filename = outputPath + outputName
        
        print '\nStart Upload\n'
        file_upload(filename)
        print '\nUpload Complete\n'
        
