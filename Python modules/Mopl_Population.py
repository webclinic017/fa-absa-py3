"""
# Purpose                       :  Returns PV and Cash for the Front vs MoPL recon. File run is split into 4 runs depending on user parameter settings.
                                    (1) All portfolios that are Not Amort Cost and excluding portfolios that contain call accounts and excluding
                                        problem portfolios (returns # values at portfolio level)
                                    (2) All portfolios that are Amort Cost and excluding portfolios that contain call accounts
                                    (3) All portfolios that contain call accounts trades and excluding large # trade portfolios
                                    (4) Large trade volume portfolios
                                    (5) Runs (at trade level) the portfolios that returned # values at portfolio level
                                    These files are concatenated into 1 file (Front_MoPL_PV_Cash_yyyymmdd.csv) and sent to IMatch for recon.

                                    These are the tasks and their filenames:
                                        MoPL_Amort_SERVER.xml.task   MoPL_Amort_yymmdd.csv
                                        MoPL_CallAccounts_SERVER.xml.task   MoPL_CallAccounts_yymmdd.csv
                                        MoPL_ExcludedPortfolios_SERVER.xml.task   MoPL_ExcludedPortfolios_yymmdd.csv
                                        MoPL_ExcludedPortfolios2_SERVER.xml.task   MoPL_ExcludedPortfolios2_yymmdd.csv
                                        MoPL_NotAmort_SERVER.xml.task   MoPL_NotAmort_yymmdd.csv,
                        Changed column used in Open Ended Call Accounts and AmortCost calculation to trade level.
                        Changes to Current Nominal calculation.
                        Changes for fx rate used in ZARNominalTemp and ZARBalance. New column - ZARBalance.

# Purpose                       :  [Deployment],[Added exception handling on all Trading Manager values so that backend does not fail due to error values],
                                    [Added PV and Cash population],[Excluded 'Call I/div 32 day' and added CRE calculation to getNotAmortCalc to pull PV
                                    from add_infos for CRE trades]
# Department and Desk           :  [],[IT Pricing and Risk],[PCG],[PCG], [IT]
# Requester                     :  [],[Matthew Stephanou],[Dirk Strauss],[Jan Kotze & Simon Mahudu], [Heinrich Momberg]
# Developer                     :  [Bhavnisha Sarawan],[Heinrich Cronje],[Tshepo Mabena],[Willie van der Bank], [Bhavnisha Sarawan]
# CR Number                     :  [C568686, C583820, C589480, C604398, 767842, 830269], [], [], [2012-06-26 278571], [2013-07-16]
"""

import time

import acm
import ael


context = acm.GetDefaultContext()
calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')
calc_space2 = acm.Calculations().CreateCalculationSpace(context, 'FTradeSheet')



ael_gui_parameters = {'hideExtracControls': True,
                      'windowCaption': 'Trade Extract'}

# these parameters are not mandatory as different combinations are needed to get the full set of data.
ael_variables = [ ['Path', 'Path', 'string', None, '', 0],
                  ['Filename', 'Filename', 'string', None, 'MoPL_Population.csv', 0],
                  ['Filter', 'Filter', 'string', None, 'MoPL_Population_callAcc', 0],
                  ['Mopl Set', 'Mopl Set', 'string', ['Amort', 'NotAmort', 'CallAccount'], '', 0],
                  ['Portfolio', 'Portfolio', 'FPhysicalPortfolio', acm.FPhysicalPortfolio.Select(''), None, 0, 1],
                  ['Exclude Portfolio', 'Exclude Portfolio', 'FPhysicalPortfolio', acm.FPhysicalPortfolio.Select(''), None, 0, 1]]

def CalcP(calc_space, column_id, node, port):
    """
    Return the value from the requested column.
    for portfolio level, values are pulled at portfolio level.
    for trade level, values are pulled at trade level and summed in CallAccount function.
    trade level calculation is used for all portfolios that contain call accounts trade where
    different columns need to used depending on add_info set by PCG
    """
    node_calc = calc_space.CreateCalculation(node, column_id)
    try:
        value = node_calc.Value()
    except:
        print 'WARNING on : %s with value : %s' %(port, node_calc)
        value = 0
    return value

def getExclPortfolios(tradeFilter, exPort, choice):
    """
    Return the list of the portfolios excluded from the MoPL recon. Uses the ASQL - Mopl_Population_CallAcc.
    Excludes any portfolios specified in the parameters.
    If choice is set to CallAccount (which runs all the portfolios that has trades which are Call Accounts) - the portfolios
    specified need to be excluded from this run as it contains too many trades and impacts the run time.
    If choice is set to NotAmort (which runs all portfolios are do not have Yes in the addinfo) - the portfolios specified need
    to excluded along with the portfolios containing Call Accounts (i.e. added to the list that contains all portfolios to be excluded from the calc).
    """
    portfolio = []
    trd = tradeFilter.Trades()
    for t in trd:
        if t.Portfolio().Oid() not in portfolio:
            portfolio.append(t.Portfolio().Oid())

    if exPort != '':
        for p in exPort:
            if choice == 'CallAccount':
                if p.Name() in portfolio:
                    portfolio.remove(p.Name().strip())
            elif choice == 'NotAmort':
                portfolio.append(p.Name().strip())
            elif choice == 'Amort':
                portfolio.append(p.Name().strip())
    return portfolio

def getPortfolioSet(portlist, myList, tradeFilter, choice, exPort):
    """
    Return the portfolio set to be used.
    the last if statement block is used to run portfolios that are too big or return # values at portfolio level.
    """
    #if mopl_pop set to Yes
    if choice == 'Amort':
        for p in portlist:
            #p = acm.FPhysicalPortfolio[ports]
            if p.Portfolio().AdditionalInfo().MoPL_Population() and not p.Portfolio().Compound():
                if p.Portfolio().AdditionalInfo().MoPL_AmortCost():
                    list = getExclPortfolios(tradeFilter, exPort, choice)
                    if p.Portfolio().Oid() not in list and p.Portfolio().Oid() not in myList:
                        myList.append(p.Portfolio().Oid())
    elif choice == 'NotAmort':
        for p in portlist:
            #p = acm.FPhysicalPortfolio[ports]
            if p.Portfolio().AdditionalInfo().MoPL_Population() and not p.Portfolio().Compound():
                if not p.Portfolio().AdditionalInfo().MoPL_AmortCost():
                    list = getExclPortfolios(tradeFilter, exPort, choice)
                    if p.Portfolio().Oid() not in list and p.Portfolio().Oid() not in myList:
                        myList.append(p.Portfolio().Oid())
    elif choice == 'CallAccount':
        for p in portlist:
            #p = acm.FPhysicalPortfolio[ports]
            if p.Portfolio().AdditionalInfo().MoPL_Population() and not p.Portfolio().Compound():
                list = getExclPortfolios(tradeFilter, exPort, choice)
                if p.Portfolio().Oid() in list and p.Portfolio().Oid() not in myList:
                    myList.append(p.Portfolio().Oid())

    elif choice == '':
        for p in exPort:
            #p = acm.FPhysicalPortfolio[ports]
            if p.Portfolio().AdditionalInfo().MoPL_Population() and not p.Portfolio().Compound():
                myList.append(p.Portfolio().Oid())
    return myList

def CREPort(port):
    """
    Check whether a portfolio is a CRE portfolio.
    """
    return port.AdditionalInfo().MTM_From_External()

def getAmortCalc(myList, outfile):
    """
    Return the values for all portfolios that are set to amort cost, at portfolio level.
    """
    for ml in myList:
        print ml, ',', 'portfolio'
        mlport = acm.FPhysicalPortfolio[ml]
        InsPort = acm.FDictionary()
        tag = acm.CreateEBTag()
        trades = mlport.Trades()
        for t in trades:
            ins = t.Instrument()
            key = t.Portfolio().Oid()

            if not InsPort.HasKey(key):
                myObject = acm.FDictionary()
                myObject['Portfolio'] = str(t.Portfolio().Oid())  #portfolio number
                myObject['Area'] = t.Portfolio().AdditionalInfo().Parent_Portfolio()
                myObject['PV'] = 0
                myObject['Cash'] = 0
                InsPort[key] = myObject

            myWorkingObject = InsPort[key]

            if t.add_info('Funding Instype') not in [ 'Call I/Div', 'Call I/Div SARB', 'Call I/Div DTI', 'Call I/div 32 day']:
                if t.Status() not in ('Simulated', 'Void'):
                    node = calc_space.InsertItem(t)
                    currentNom = 0
                    accrued = 0
                    try:
                        cash = CalcP(calc_space, 'Portfolio Cash End', node, t.Oid()).Number()
                    except:
                        cash = CalcP(calc_space, 'Portfolio Cash End', node, t.Oid())

                    if ins.InsType() not in ('SecurityLoan', 'Swap', 'FRA'):
                        nom_id = 'Current Nominal in Instrument Currency'
                        try:
                            currentNom = CalcP(calc_space, nom_id, node, t.Oid()).Number()
                        except:
                            currentNom = CalcP(calc_space, nom_id, node, t.Oid())
                    try:
                        accrued = CalcP(calc_space, 'Portfolio Accrued Interest', node, t.Oid()).Number()
                    except:
                        accrued = CalcP(calc_space, 'Portfolio Accrued Interest', node, t.Oid())
                    calc_space.Clear()

                    if t.add_info('Funding Instype') == 'IRD Funding':
                        PV = accrued
                    else:
                        try:
                            PV = currentNom + accrued
                        except:
                            PV = str(currentNom) + str(accrued)

                    try:
                        myWorkingObject['PV'] += float(PV)
                    except:
                        print 'WARNING: Trade %s has a string value for PV' %t.Oid()

                    try:
                        myWorkingObject['Cash'] += float(cash)
                    except:
                        print 'WARNING: Trade %s has a string value for Cash' %t.Oid()

        for key in InsPort.Keys():
            myWorkingObject = InsPort[key]

            outLine = myWorkingObject['Portfolio'].replace(',', '')
            outLine += ',' + str(myWorkingObject['PV']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Cash']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Area']).replace(',', '')
            outfile.write(outLine + '\n')

def getNotAmortCalc(myList, outfile):
    """
    Return the values for all portfolios that are not set to amort cost, at portfolio level.
    """
    for ml in myList:
        try:
            portfolio = acm.FPhysicalPortfolio[ml]
            IsCREPort = CREPort(portfolio)
            node = calc_space.InsertItem(portfolio)
            node2 = calc_space2.InsertItem(portfolio)
        except:
            node = calc_space.InsertItem(ml)
            node2 = calc_space2.InsertItem(ml)
            IsCREPort = CREPort(ml)

        try:
            cash = CalcP(calc_space, 'Portfolio Cash End', node, ml).Number()
        except:
            cash = CalcP(calc_space, 'Portfolio Cash End', node, ml)

        if IsCREPort:
            try:
                valend = CalcP(calc_space, 'ExternalValMopl', node, ml).Number()
            except:
                valend = CalcP(calc_space2, 'ExternalValMopl', node2, ml)
        else:
            try:
                valend = CalcP(calc_space, 'Portfolio Value End', node, ml).Number()
            except:
                valend = CalcP(calc_space, 'Portfolio Value End', node, ml)

        outfile.write('%s,%s,%s,%s\n' % (ml, valend, cash, portfolio.AdditionalInfo().Parent_Portfolio()))
        calc_space.Clear()

def RemoveCallTrades(trds):
    for t in trds:
        ins = t.Instrument()
        try:
            if (ins.InsType() == 'Deposit' and t.AdditionalInfo().Funding_Instype() in ('Call I/Div', 'Call I/Div SARB', 'Call I/Div DTI', 'Call I/div 32 day')):
                trds.Remove(t)
        except:
            pass
    return trds

def getCallAccount(myList, outfile):
    """
    Return the values for Call Accounts at trade level, which is then summed to portfolio level.
    this function checks for all scenarios (amort/not amort/call accounts)
    """
    for ml in myList:
        mlport = acm.FPhysicalPortfolio[ml]
        InsPort = acm.FDictionary()
        #tag = acm.CreateEBTag()
        trds = mlport.Trades()

        trades = RemoveCallTrades(trds)

        for t in trades:
            ins = t.Instrument()
            key = t.Portfolio().Oid()

            if not InsPort.HasKey(key):
                myObject = acm.FDictionary()
                myObject['Portfolio'] = str(t.Portfolio().Oid())  #portfolio number
                myObject['Area'] = t.Portfolio().AdditionalInfo().Parent_Portfolio()
                myObject['PV'] = 0
                myObject['Cash'] = 0
                InsPort[key] = myObject

            myWorkingObject = InsPort[key]

            if t.Status() not in ('Simulated', 'Void'):
                node = calc_space.InsertItem(t)
                currentNom = 0
                accrued = 0
                try:
                    cash = CalcP(calc_space, 'Portfolio Cash End', node, t.Oid()).Number()
                except:
                    cash = CalcP(calc_space, 'Portfolio Cash End', node, t.Oid())
                isCall = ins.OpenEnd() == 'Open End' and ins.InsType() == 'Deposit'
                if not t.Portfolio().AdditionalInfo().MoPL_AmortCost():
                    try:
                        PV = CalcP(calc_space, 'Portfolio Value End', node, t.Oid()).Number()
                    except:
                        PV = CalcP(calc_space, 'Portfolio Value End', node, t.Oid())
                else:
                    if isCall and t.maturity_date() > ael.date_today() and ins.InsType() not in ('SecurityLoan', 'Swap', 'FRA'):
                        nom_id = 'ZARBalance'
                        node2 = calc_space2.InsertItem(t)
                        try:
                            currentNom = -1 * CalcP(calc_space2, nom_id, node2, t.Oid()).Number()
                        except:
                            try:
                                currentNom = -1 * CalcP(calc_space2, nom_id, node2, t.Oid())
                            except:
                                currentNom = '-' + str(CalcP(calc_space2, nom_id, node2, t.Oid()))
                        calc_space2.Clear()
                    elif not isCall and ins.InsType() not in ('SecurityLoan', 'Swap', 'FRA'):
                        nom_id = 'Current Nominal in Instrument Currency'
                        try:
                            currentNom = CalcP(calc_space, nom_id, node, t.Oid()).Number()
                        except:
                            currentNom = CalcP(calc_space, nom_id, node, t.Oid())
                    try:
                        accrued = CalcP(calc_space, 'Portfolio Accrued Interest', node, t.Oid()).Number()
                    except:
                        accrued = CalcP(calc_space, 'Portfolio Accrued Interest', node, t.Oid())
                    calc_space.Clear()

                    try:
                        PV = currentNom + accrued
                    except:
                        PV = str(currentNom) + str(accrued)
                try:
                    myWorkingObject['PV'] += float(PV)
                except:
                    print 'WARNING: Trade %s has a string value for PV' %t.Oid()

                try:
                    myWorkingObject['Cash'] += float(cash)
                except:
                    print 'WARNING: Trade %s has a string value for Cash' %t.Oid()

        for key in InsPort.Keys():
            myWorkingObject = InsPort[key]

            outLine = myWorkingObject['Portfolio'].replace(',', '')
            outLine += ',' + str(myWorkingObject['PV']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Cash']).replace(',', '')
            outLine += ',' + str(myWorkingObject['Area']).replace(',', '')
            outfile.write(outLine + '\n')

def tradeCheck(list):
    """
    misc () to check the number of trades in a portfolio. used for testing purposes.
    if a file fails, issue could be that there is too many trades in the portfolio -
    remove file from normal run and add to ExcludedPortfolio's run.
    """
    for l in list:
        port = acm.FPhysicalPortfolio[l]
        print port.Name(), ",", port.Trades().Size()

def ael_main(parameter, *rest):
    """
    main function to get parameters to determine appropriate calculation functions to be used.
    """
    count = 0
    tm = time.clock()
    header = 'Portfolio,PV,Cash,Area \n'

    # filename, path, parameters setup
    outputPath = parameter['Path']
    outputName = parameter['Filename']
    fileName = outputPath + outputName
    tradeFilter = acm.FTradeSelection[parameter['Filter']]
    selPort = parameter['Portfolio']
    exPort = parameter['Exclude Portfolio']
    choice = parameter['Mopl Set']

    #data is written to file as calculated line by line due to performance constraints from using a list to hold the data and to write once.
    #code will need write in batches to the file.
    outfile=  open(fileName, 'w')
    outfile.write(header)
    #portlist = ['STIRT - FRA Trading']  #front end testing list, if used getPortfolioSet() needs to convert these into objects.
    myList = []
    portlist = acm.FPhysicalPortfolio.Select('')

    # Amort, NotAmort and CallAccount will have selPort as empty and perhaps exclude portfolios.
    # ExcludedPortfolios is used to run all portfolios that cannot be run normally. Does not require the filter for exclusion.
    # if file fails, print populatedList to see which portfolio the backend hangs on - use tradeCheck to see if there is too many trades.
    if selPort.IsEmpty():
        populatedList = getPortfolioSet(portlist, myList, tradeFilter, choice, exPort)
    else:
        populatedList = getPortfolioSet(portlist, myList, tradeFilter, choice, selPort)

    # if statements to determine calculation to call based on the parameter settings.
    if choice == 'Amort':
        #tradeCheck(populatedList)
        getAmortCalc(populatedList, outfile)
        #print populatedList
    elif choice == 'NotAmort':
        #tradeCheck(populatedList)
        getNotAmortCalc(populatedList, outfile)
    elif choice == 'CallAccount':
        #tradeCheck(populatedList)
        getCallAccount(populatedList, outfile)
    elif choice == 'Amort' and selPort != '':
        #tradeCheck(populatedList)
        getAmortCalc(populatedList, outfile)
    elif choice == '' and selPort != '':
        #tradeCheck(populatedList)
        getCallAccount(populatedList, outfile)

    outfile.close()
    print 'Output Complete', time.clock() - tm
    print 'Wrote secondary output to::: ' + fileName
