import ael, string

#Created by Heinrich Cronje 2007-04-05
#This ael pulls two files:
#       1-The file from the JSE
#       2-The file from the query: eq_Stock_Recons
#It writes exceptions if the number of contracts differs and if there are
#portfolios and/or instruments missing from the JFE/Front file.

def StockRecon(temp,*rest):

#--------------------------------Date-------------------------------------
    d = ael.date_today()
    date = d.add_banking_day(ael.Instrument['ZAR'], -1)
#-------------------------------------------------------------------------

#------------------------------Get External Files-------------------------    
    #fileJSE = 'C:/As_End_day/Eugene/' + date.to_string('%Y-%m-%d') + '/' + date.to_string('%b%Y') + date.to_string('%Y%m%d') + 'BDAExport.csv'
    #fileStock = 'C:/As_End_day/Eugene/' + date.to_string('%Y-%m-%d') + '/' + 'Eq_Stock_Recon_' + date.to_string('%Y%m%d') + '.csv'
    fileJSE = '/services/frontnt/BackOffice/Atlas-End-Of-Day/StockPosRecon/2009-07-31' + '/' + '20090731BDAExport.csv'
    fileStock = '/services/frontnt/BackOffice/Atlas-End-Of-Day/StockPosRecon/2009-07-31' + '/' + 'SAEQ_Stocks_and_Warrants_20090731.csv'
    #fileJSE = '/services/frontnt/BackOffice/Atlas-End-Of-Day/StockPosRecon/' + date.to_string('%Y-%m-%d') + '/' + date.to_string('%Y%m%d') + 'BDAExport.csv'
    #fileStock = '/services/frontnt/BackOffice/Atlas-End-Of-Day/StockPosRecon/' + date.to_string('%Y-%m-%d') + '/' + 'SAEQ_Stocks_and_Warrants_' + date.to_string('%Y%m%d') + '.csv'
#-------------------------------------------------------------------------

#--------------------------Read JSE File----------------------------------    
    filenameJSE = open(fileJSE)
    lineJSE = filenameJSE.readline()
    lineJSE = filenameJSE.readline()
    
    JSEList = []
    JSEDictionary = {}

    while lineJSE:
        linJSE = string.split(lineJSE, ',')
        insJSE1 = linJSE[2].replace(' ', '')
        insJSE2 = insJSE1.replace('"', '')
        accJSE1 = linJSE[1].replace(' ', '')
        accJSE2 = accJSE1.replace('"', '')
        nbr1 = linJSE[3].replace('"', '')
        key = accJSE2 + ('ZAR/' + insJSE2)
        JSEDictionary[key] = nbr1
        lineJSE = filenameJSE.readline()
#-------------------------------------------------------------------------

#--------------------------Read Stock File--------------------------------
    filenameStock = open(fileStock)
    lineStock = filenameStock.readline()
    lineStock = filenameStock.readline()
    
    StockList = []
    StockDictionary = {}
    
    while lineStock:
        linStock = string.split(lineStock, ',')
        insStock = linStock[0].rstrip()
        port = linStock[2].rstrip()
        portfolio = port[0:5]
        key = portfolio + insStock
        StockDictionary[key] = linStock[1]
        lineStock = filenameStock.readline()
#-------------------------------------------------------------------------

#--------------------------Open Output File-------------------------------
    #fileOutput = 'C:/As_End_day/Eugene/' + date.to_string('%Y-%m-%d') + '/Output' + date.to_string('%Y%m%d') + '.csv'
    fileOutput = '/services/frontnt/BackOffice/Atlas-End-Of-Day/StockPosRecon/' + date.to_string('%Y-%m-%d') + '/SAEQ_Stock_Recon_' + date.to_string('%Y%m%d') + '.csv'
    
    outfile = open(fileOutput, 'w')
    outfile.write('Date' + ',' + 'Accountnbr+Sharename' + ',' + 'JSE' + ',' + 'Front' + ',' + 'Difference\n')
#-------------------------------------------------------------------------

#---------------------------Test For Differences (Stock)------------------
    for k in JSEDictionary.keys():
        if StockDictionary.has_key(k):
            if (abs((float)(JSEDictionary[k]) - (float)(StockDictionary[k])) > 0):
                outfile.write((str)((str)(date) + ',' + (str)(k) + ',' + (str)(JSEDictionary[k]) + ',' + (str)(StockDictionary[k]) + ',' + (str)((float)(JSEDictionary[k]) - (float)(StockDictionary[k])) + '\n'))
        else:
            outfile.write((str)((str)(date) + ',' + (str)(k) + ',' + (str)(JSEDictionary[k]) + ',' + 'Not On Front' + ',' + (str)(JSEDictionary[k]) + '\n'))
#-------------------------------------------------------------------------

#--------------------------On Front - Not On JSE--------------------------
    for j in StockDictionary.keys():
        if JSEDictionary.has_key(j):
            pass
        else:
            outfile.write((str)((str)(date) + ',' + (str)(j) +  ',' + 'Not On JSE' + ','  + (str)(StockDictionary[j]) + ',' + (str)(0 - (float)(StockDictionary[j])) + '\n'))
#-------------------------------------------------------------------------            
    filenameJSE.close()
    filenameStock.close()
    outfile.close()
    print 'Complete'
    return 'Complete'

