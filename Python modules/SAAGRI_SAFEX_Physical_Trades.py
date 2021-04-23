import ael, string

def Physical_Trades(temp,DealDate,exceptionFileLocation,filePortfolio,fileTrades,fileFlag,*rest):

    dealdate = ael.date(DealDate)
    
    #-------------------------Location of files Start (Testing Only)------------------------
    
    #Exception File Location
    #exceptionFileLocation = '//v036syb104001/safex/Agri/Exception'      #Testing
    #exceptionFileLocation = '//services/frontnt/Safex/Agri/Exception'      #Production
    
    #Portfolio and Option Expity Mapping File Location
    #filePortfolio = '//v036syb104001/Safex/Agri/Portfolio.csv'  #Testing
    #filePortfolio = '//services/frontnt/Safex/Agri/Portfolio.csv'      #Production

    #AIS file location with all the trades that need to be reconciled and booked.
    #fileTrades = '//v036syb104001/Safex/Agri/Deals_' + dealdate.to_string('%Y%m%d') + '.csv'    #Testing
    #fileTrades = '//services/frontnt/Safex/Agri/Deals_' + dealdate.to_string('%Y%m%d') + '.csv'    #Production
    
    #Flag File. If this exist then the validation on that file has been done. If not, no booking takes place.
    #fileFlag = '//v036syb104001/Safex/Agri/Flag/Flag' + dealdate.to_string('%Y%m%d') + '.txt'    #Testing
    #fileFlag = '//services/frontnt/Safex/Agri/Flag/Flag' + dealdate.to_string('%Y%m%d') + '.txt'    #Production
    
    #--------------------------------Location of files End----------------------------------
    
    #--------Open all files: If one file doesn't open then nothing gets booked Start--------
    
    openFileFlag = 0
    #Exception file. All errors per run will be written to this file.
    exceptionFilename = getExceptionFile(exceptionFileLocation, dealdate)
    fileException = open(exceptionFilename, 'a')
    
    filePortfolio = openFile(filePortfolio, exceptionFilename)
    if filePortfolio == 'Error':
        openFileFlag = 1
    
    fileTrades = openFile(fileTrades, exceptionFilename)
    if fileTrades == 'Error':
        openFileFlag = 1
    
    fileFlag = openFile(fileFlag, exceptionFilename)
    if fileFlag == 'Error':
        openFileFlag = 1
    else:
        fileFlag.close()
        
    #--------Open all files: If one file doesn't open then nothing gets booked End----------
    
    #---------------If one of the files didn't open then nothing gets booked----------------
    #------------------------------------------MAIN-----------------------------------------
    
    if not openFileFlag:

        #-----Create and populate lists for the Client and Original portoflios from the Mapping file Start-----
        
        linePortfolio = filePortfolio.readline()
        linePortfolio = filePortfolio.readline()
        linePortfolio = filePortfolio.readline()

        ClientPortfolio = []
        OriginalPortfolio = []
        OptionExpityDictionary = {}
        
        while linePortfolio:
            linePortfolio = linePortfolio.rstrip()
            linPortfolio = string.split(linePortfolio, ',')
            ClientPortfolio.append(linPortfolio[0])
            OriginalPortfolio.append(linPortfolio[1])
            OptionExpityDictionary[linPortfolio[2]] = linPortfolio[3]
            linePortfolio = filePortfolio.readline()
        
        #-----Create and populate lists for the Client and Original portoflios from the Mapping file End------
        
        #-------------Read through the AIS file until the fourth line where the data start Start--------------
        
        lineTrades = fileTrades.readline()
        lineTrades = fileTrades.readline()
        lineTrades = fileTrades.readline()
        lineTrades = fileTrades.readline()
        lineTrades = fileTrades.readline()
        
        #-------------Read through the AIS file until the fourth line where the data start End---------------
        
        #-------------Ditctionay to keep track of the position of the instruments per portfolio--------------
        instrumentdic = {}
        
        #---------------Loop through the AIS trade file and reconsile and book line for line.----------------
        #If there is an error with the booking of the trade, the error will be written to the exception file.
        
        while lineTrades:
            errorflag = 0
            linTrades = string.split(lineTrades, ',')
            
            #--------------------------Initialize all variables from AIS trade file Start--------------------
            
            tradedate = ael.date_from_string(linTrades[0], '%d/%m/%Y')
            clientPortf = linTrades[2]
            contract = linTrades[3]
            typeContract = linTrades[4]
            date = ael.date_from_string(linTrades[5], '%d/%m/%Y')
            strike = linTrades[6]
            buySell = linTrades[7]
            nbrContract = linTrades[8]
            price = linTrades[9]
            originalPortf = linTrades[10]
            monthYear = date.to_string('%b%y')            
            #--------------------------Initialize all variables from AIS trade file End---------------------
            
            #------Initialize the factor of the trade. Negitive for a Sell, Positive for a Buy. Start-------
            
            if buySell == 'S':
                factor = -1
            elif buySell == 'B':
                factor = 1
            else:
                fileException.write('-----------------------Error with column B/S-----------------------\n')
                fileException.write('-----------------The following line is not booked:-----------------\n')
                fileException.write(lineTrades + '\n')
                fileException.write('-------------------------------------------------------------------\n')
                errorflag = 1
            
            #------Initialize the factor of the trade. Negitive for a Sell, Positive for a Buy. End--------
            
            #Only entries from the AIS file with originalPortfolio and clientPortfolio that are in the Mapping file are booked.
            
            if not errorflag:
                if ((originalPortf[0:3] == 'ABL' and clientPortf in ClientPortfolio) or (clientPortf == 'ABL' and originalPortf in OriginalPortfolio)):
                    
                    #------------------------Initializing the underlying contract. Start------------------------
                    
                    if contract in ('SSP', 'SUNS'):
                        und = 'SUNS'
                    elif contract in ('WHP', 'WMS', 'WOP', 'WOPT', 'WMAZ'):
                        und = 'WMAZ'
                    elif contract in ('SOYA', 'SYP'):
                        und = 'SOYA'
                    elif contract == 'WEAT':
                        und = 'WEAT'
                    elif contract in ('YMAZ', 'YMS'):
                        und = 'YMAZ'
                    elif contract == 'CORN':
                        und = 'CORN'
                    else:
                        fileException.write('---------------------Error with column Contract--------------------\n')
                        fileException.write('-----------Underlying Instrument could not be identified.----------\n')
                        fileException.write(lineTrades + '\n')
                        fileException.write('-------------------------------------------------------------------\n')
                        errorflag = 1
                        
                    #------------------------Initializing the underlying contract. End-------------------------
                    
                    #--------------------Initializing the Val Group of the instruments. Start------------------
                    if not errorflag:
                        if contract in ('SSP', 'SUNS'):
                            val = 'SUNS'
                        elif contract in ('WHP', 'WMS', 'WOP', 'WMAZ', 'CORN'):
                            val = 'WMAZ'
                        elif contract == 'WOPT':
                            val = 'WMAZ2'
                        elif contract in ('SOYA', 'SYP'):
                            val = 'SOYA'
                        elif contract == 'WEAT':
                            val = 'WHEAT'
                        elif contract in ('YMAZ', 'YMS'):
                            val = 'YMAZ'
                        else:
                            fileException.write('---------------------Error with column Contract--------------------\n')
                            fileException.write('-----------------Val Group could not be identified.----------------\n')
                            fileException.write(lineTrades + '\n')
                            fileException.write('-------------------------------------------------------------------\n')
                            errorflag = 1
                            
                        
                        #--------------------Initializing the Val Group of the instruments. End-------------------
                        
                        #---------------------------Initialize the contract size. Start---------------------------
                        
                        if not errorflag:
                            if und in ('WMAZ', 'WHP', 'WMS', 'WOP', 'WOPT', 'YMAZ', 'CORN'):
                                contsize = 100
                            elif und in ('WEAT', 'SUNS', 'SSP'):
                                contsize = 50
                            elif und == 'SOYA':
                                contsize = 25
                            else:
                                fileException.write('---------------------Error with column Contract--------------------\n')
                                fileException.write('---------------Contract size could not be determined.--------------\n')
                                fileException.write(lineTrades + '\n')
                                fileException.write('-------------------------------------------------------------------\n')
                                errorflag = 1
                                
                            #---------------------------Initialize the contract size. End----------------------------
                            
                            #----------------------------Initializing portfolios. Start------------------------------
                            
                            if not errorflag:
                                if clientPortf in ClientPortfolio:
                                    portf = clientPortf
                                else:
                                    portf = originalPortf
                                
                                #----------------------------Initializing portfolios. End--------------------------------
                                
                                #--------------------Setting up the instrument part of the trade Start-------------------
                                #---------------------------------Future/Forward. Start----------------------------------
                                
                                if typeContract == 'F':
                                    
                                    #-----------------------------------Setting Insid------------------------------------
                                    insid = 'ZAR/' + contract + '/SAFEX/' + (str)(monthYear.upper())
                                    
                                    #---Selecting the instrument and relevant positions. If the instument doesn't exist--
                                    #--then create a new instrument based upon the underlying. If the underlying doesn't-
                                    #---------------------exist then write to the exception report.----------------------
                                    
                                    try:
                                    
                                        #-------------------------Selecting the instrument. Start------------------------
                                        instrument = ael.Instrument[insid]
                                        i_new = instrument.clone()
                                        key = i_new.insid + portf
                                        if instrumentdic.has_key(key):
                                            PositionPrev = instrumentdic[key]
                                            Position = instrumentdic[key]
                                        else:
                                            PositionPrev = instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, -1), None, None, ael.Portfolio[portf])
                                            Position = instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, 0), None, None, ael.Portfolio[portf])
                                        
                                        #-------------------------Selecting the instrument. End--------------------------
                                        
                                    except:
                                        
                                        #------The relevant instrument does not exist. Create a new instrument with-------
                                        #------the relevant underlying. If the underlying does not exist, then write------
                                        #-----------------------------to the exception file.------------------------------
                                        
                                        try:
                                        
                                            #------------------Selecting the relevant underlying. Start-------------------
                                            
                                            i_new = ael.Instrument.new('Future/Forward')
                                            i_new.und_insaddr = ael.Instrument['ZAR/' + und + '/SAFEX']
                                            i_new.und_instype = 'Commodity'
                                            i_new.insid = insid
                                            i_new.quote_type = 'Per Unit'
                                            key = i_new.insid + portf
                                            PositionPrev = 0
                                            Position = 0
                                            
                                            #------------------Selecting the relevant underlying. End---------------------
                                            
                                        except:
                                        
                                            #--The instrument and underlying does not exist. Write to the exception file.-
                                            
                                            fileException.write('---------------------Underlying does not exist.--------------------\n')
                                            fileException.write(lineTrades + '\n')
                                            fileException.write('-------------------------------------------------------------------\n')
                                            errorflag = 1
                                    
                                    #---------------------Set the expity day of the instrument. Start---------------------
                                    
                                    expDate = date.to_string('%Y/%m/%d')
                                    i_new.exp_day = ael.date_from_string(expDate, '%Y/%m/%d')
                                    
                                    #---------------------Set the expity day of the instrument. End-----------------------
                                    
                                #----------------------------------Future/Forward. End------------------------------------
                                
                                #-----------------------------------Call Option. Start------------------------------------
                                
                                elif typeContract == 'c':
                                
                                    #--------------------Initializing the strike and the insid. Start---------------------
                                    
                                    strike = (float)(strike)
                                    insid = 'ZAR/FUT/' + und + '/SAFEX/' + (str)(monthYear.upper()) + '/C/' + str((int)(strike)) + '.00'
                                    
                                    #--------------------Initializing the strike and the insid. End-----------------------
                                    
                                    #---Selecting the instrument and relevant positions. If the instument doesn't exist--
                                    #--then create a new instrument based upon the underlying. If the underlying doesn't-
                                    #---------------------exist then write to the exception report.----------------------
                                    
                                    try:
                                    
                                        #-------------------------Selecting the instrument. Start------------------------
                                        
                                        instrument = ael.Instrument[insid]
                                        i_new = instrument.clone()
                                        key = i_new.insid + portf
                                        
                                        if instrumentdic.has_key(key):
                                            PositionPrev = instrumentdic[key]
                                            Position = instrumentdic[key]
                                        else:
                                            PositionPrev = (instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, -1), None, None, ael.Portfolio[portf]) / contsize)
                                            Position = (instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, 0), None, None, ael.Portfolio[portf]) / contsize)
                                        
                                        #-------------------------Selecting the instrument. End--------------------------
                                        
                                    except:
                                    
                                        #------The relevant instrument does not exist. Create a new instrument with-------
                                        #------the relevant underlying. If the underlying does not exist, then write------
                                        #-----------------------------to the exception file.------------------------------
                                    
                                        try:
                                        
                                            #------------------Selecting the relevant underlying. Start-------------------
                                            
                                            i_new = ael.Instrument.new('Option')
                                            i_new.und_insaddr = ael.Instrument['ZAR/' + und + '/SAFEX/' + monthYear.upper()]
                                            i_new.und_instype = 'Future/Forward'
                                            i_new.insid = insid
                                            i_new.quote_type = 'Per Unit'
                                            key = i_new.insid + portf
                                            PositionPrev = 0
                                            Position = 0
                                            
                                            #------------------Selecting the relevant underlying. End---------------------
                                            
                                        except:
                                        
                                            #--The instrument and underlying does not exist. Write to the exception file.-
                                            
                                            fileException.write('---------------------Underlying does not exist.--------------------\n')
                                            fileException.write(lineTrades + '\n')
                                            fileException.write('-------------------------------------------------------------------\n')
                                            errorflag = 1
                                            
                                            
                                    #-------------------------Initialize option expiry day. Start-------------------------
                                    if not errorflag:
                                        newdate = date.to_string('%y-%b')
                                        if OptionExpityDictionary.has_key(newdate):
                                            newexpday = ael.date_from_string(OptionExpityDictionary[newdate], '%d/%m/%Y')
                                            i_new.exp_day = newexpday
                                            i_new.exp_time = newexpday.to_time()
                                        else:
                                            fileException.write('--------------Error with column Option Expiry (Mapping)------------\n')
                                            fileException.write('------The Expiry Date and Mapping Option Expiry dates differ.------\n')
                                            fileException.write(lineTrades + '/n')
                                            fileException.write('-------------------------------------------------------------------\n')
                                            errorflag = 1
                                            
                                        #-------------------------Initialize option expiry day. End---------------------------
                                        
                                        #-----------------------Initialize strike and option type. Start----------------------
                                        
                                        i_new.strike_price = strike
                                        i_new.call_option = 1
                                        
                                        #-----------------------Initialize strike and option type. End------------------------
                                    
                                #-----------------------------------Call Option. End--------------------------------------
                                
                                #------------------------------------Put Option. Start------------------------------------
                                
                                elif typeContract == 'p':
                                
                                    #--------------------Initializing the strike and the insid. Start---------------------
                                    
                                    strike = (float)(strike)
                                    insid = 'ZAR/FUT/' + und + '/SAFEX/' + (str)(monthYear.upper()) + '/P/' + str((int)(strike)) + '.00'
                                    
                                    #--------------------Initializing the strike and the insid. End-----------------------
                                    
                                    #---Selecting the instrument and relevant positions. If the instument doesn't exist--
                                    #--then create a new instrument based upon the underlying. If the underlying doesn't-
                                    #---------------------exist then write to the exception report.----------------------
                                    
                                    try:
                                    
                                        #-------------------------Selecting the instrument. Start------------------------
                                        
                                        instrument = ael.Instrument[insid]
                                        i_new = instrument.clone()
                                        
                                        key = i_new.insid + portf
                                        if instrumentdic.has_key(key):
                                            PositionPrev = instrumentdic[key]
                                            Position = instrumentdic[key]
                                        else:
                                            PositionPrev = (instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, -1), None, None, ael.Portfolio[portf]) / contsize)
                                            Position = (instrument.position(None, i_new.curr.insid, tradedate.add_banking_day(i_new.curr, 0), None, None, ael.Portfolio[portf]) / contsize)
                                            
                                        #-------------------------Selecting the instrument. End--------------------------
                                        
                                    except:
                                    
                                        #------The relevant instrument does not exist. Create a new instrument with-------
                                        #------the relevant underlying. If the underlying does not exist, then write------
                                        #-----------------------------to the exception file.------------------------------
                                        
                                        try:
                                        
                                            #------------------Selecting the relevant underlying. Start-------------------
                                            
                                            i_new = ael.Instrument.new('Option')
                                            i_new.und_insaddr = ael.Instrument['ZAR/' + und + '/SAFEX/' + monthYear.upper()]
                                            i_new.und_instype = 'Future/Forward'
                                            i_new.insid = insid
                                            i_new.quote_type = 'Per Unit'
                                            key = i_new.insid + portf
                                            PositionPrev = 0
                                            Position = 0
                                            
                                            #------------------Selecting the relevant underlying. End---------------------
                                            
                                        except:
                                        
                                            #--The instrument and underlying does not exist. Write to the exception file.-
                                            
                                            fileException.write('---------------------Underlying does not exist.--------------------\n')
                                            fileException.write(lineTrades + '\n')
                                            fileException.write('-------------------------------------------------------------------\n')
                                            errorflag = 1
                                            
                                    #-------------------------Initialize option expiry day. Start-------------------------
                                    
                                    if not errorflag:
                                        newdate = date.to_string('%y-%b')
                                        if OptionExpityDictionary.has_key(newdate):
                                            newexpday = ael.date_from_string(OptionExpityDictionary[newdate], '%d/%m/%Y')
                                            i_new.exp_day = newexpday
                                            i_new.exp_time = newexpday.to_time()
                                        else:
                                            fileException.write('--------------Error with column Option Expiry (Mapping)------------\n')
                                            fileException.write('------The Expiry Date and Mapping Option Expiry dates differ.------\n')
                                            fileException.write(lineTrades + '/n')
                                            fileException.write('-------------------------------------------------------------------\n')
                                            errorflag = 1
                                            
                                        #-------------------------Initialize option expiry day. End---------------------------
                                        
                                        #-----------------------Initialize strike and option type. Start----------------------
                                        
                                        i_new.strike_price = (float)(strike)
                                        i_new.call_option = 0
                                        
                                        #-----------------------Initialize strike and option type. End------------------------
                                    
                                #------------------------------------Put Option. End--------------------------------------
                                
                                #-------------------------The contract type does not exist. Start-------------------------
                                
                                else:
                                    fileException.write('-----------------------Error with column F/c/p---------------------\n')
                                    fileException.write('-------Unknown character to determine a future or an option.-------\n')
                                    fileException.write(lineTrades + '\n')
                                    fileException.write('-------------------------------------------------------------------\n')
                                    errorflag = 1
                                    
                                #-------------------------The contract type does not exist. End---------------------------
                                
                                #---------------Initialize contact size, paytype and the otc status. Start----------------
                                
                                if not errorflag:
                                    i_new.contr_size = contsize
                                    i_new.paytype = 'Future'
                                    i_new.otc = 0
                                    
                                    #---------------Initialize contact size, paytype and the otc status. End-----------------
                                    
                                    #-----------------------Assigning Valgroup to the instrument. Start----------------------
                                    
                                    valflag = 0
                                    for valgroup in ael.ChoiceList['ValGroup'].members():
                                        if valgroup.entry == 'AgriesSAFEX_' + val:
                                            valflag = 1
                                            i_new.product_chlnbr = valgroup.seqnbr
                                    
                                    if not valflag:
                                        fileException.write('---------------------Error with column Contract--------------------\n')
                                        fileException.write('-----------------Val Group does not exist in Front.----------------\n')
                                        fileException.write(lineTrades + '\n')
                                        fileException.write('-------------------------------------------------------------------\n')
                                        errorflag = 1
                                        
                                    #-----------------------Assigning Valgroup to the instrument. End------------------------
                                    
                                    #---------------------Update the positions in the dictionary. Start----------------------
                                    
                                    if not errorflag:
                                        if instrumentdic.has_key(key):
                                            instrumentdic[key] = instrumentdic[key] + (factor*(float)(nbrContract))
                                        else:
                                            instrumentdic[key] = PositionPrev + (factor*(float)(nbrContract))
                                        
                                        #-----------------------Update the positions in the dictionary. End----------------------
                                        
                                        #---------------------Only non zero positions will be booked. Start----------------------
                                        
                                        if PositionPrev + (factor*(float)(nbrContract)) != Position:
                                            
                                            #--------------------------Committing the instrument. Start--------------------------
                                            
                                            try:
                                                i_new.commit()
                                            except:
                                                fileException.write('------------------Instrument could not be saved.-------------------\n')
                                                fileException.write(lineTrades + '\n')
                                                fileException.write('-------------------------------------------------------------------\n')
                                                errorflag = 1
                                                
                                            ael.poll()
                                            
                                            #--------------------------Committing the instrument. End----------------------------
                                            
                                            #---------------Create trade with all the relevant information. Start----------------
                                            
                                            if not errorflag:
                                                t_new = ael.Trade.new(i_new)
                                                
                                                t_new.quantity = (PositionPrev + (factor * (float)(nbrContract))) - Position
                                                t_new.price = (float)(price)
                                                t_new.prfnbr = portf
                                                t_new.status = 'FO Confirmed'
                                                t_new.counterparty_ptynbr = ael.Party.read('ptyid2="SAFEX"')
                                                t_new.acquirer_ptynbr = ael.Party['Agris Desk']
                                                t_new.text1 = 'Ael booked ' + (str)(dealdate)
                                                t_new.optkey1_chlnbr = ael.ChoiceList.read('list="TradArea" and entry="SAFX"') 
                                                
                                                date1 = dealdate.to_string('%d/%m/%Y')
                                                date2 = ael.date_from_string(date1, '%d/%m/%Y')
                                                t_new.value_day = date2
                                                t_new.time = date2.to_time()
                                                t_new.acquire_day = date2
                                                
                                                #-----------------------------Committing the trade. Start----------------------------
                                                
                                                try:
                                                    t_new.commit()
                                                except:
                                                    fileException.write('------------------Instrument could not be saved.-------------------\n')
                                                    fileException.write(lineTrades + '\n')
                                                    fileException.write('-------------------------------------------------------------------\n')
                                                    errorflag = 1
                                                    
                                                #-----------------------------Committing the trade. End------------------------------
                                                
                                                #---------------Create trade with all the relevant information. End------------------
                                                
                                        #----------------------Only non zero positions will be booked. End-----------------------
            
            #--------------------------Reading the next line in the Trade file. Start--------------------------
            
            lineTrades = fileTrades.readline()
            
            #--------------------------Reading the next line in the Trade file. End----------------------------
        
        #-------------------------------Close the mapping and trade files. Start-------------------------------
        
        filePortfolio.close()
        fileTrades.close()
        
        #-------------------------------Close the mapping and trade files. End---------------------------------
        
    #-------------------Final response. Determine if the booking was successful or not. Start------------------
    
    if openFileFlag or errorflag:
        fileException.close()
        result = 'An error occured during excecution. An email will be sent to the relevant people.'
    else:
        result = 'All entries, with no errors, were booked successfuly.'
        fileException.write(result)
    
    #-------------------Final response. Determine if the booking was successful or not. End--------------------
    
    #----------------------Close the exception file and email this exception file. Start-----------------------
    
    fileException.close()
    
    sendMail(exceptionFilename, dealdate)
    
    #----------------------Close the exception file and email this exception file. Start-----------------------
    
    print result
    return result

def getExceptionFile(location, dealDate):
    date = dealDate.to_string('%Y%m%d')
    version = 1
    
    filename = location + '/Exception_' + date + '_' + str(version) + '.txt'
    file = openFile(filename, filename)
    
    while file != 'Error':
        file.close()
        version = version + 1
        filename = location + '/Exception_' + date + '_' + str(version) + '.txt'
        file = openFile(filename, filename)
    
    return filename

def openFile(filename,exceptionFilename,*rest):
    try:
        file = open(filename, 'r')
    except:
        if filename != exceptionFilename:
            exception = open(exceptionFilename, 'w')
            exception.write('Error opening file: ' + filename + '. Please check if the file exist or that the file is not corrupted.\n')
            exception.close()
            
        file = 'Error'
    
    return file

def sendMail(file,date,*rest):
    from smtplib import SMTP
    from MimeWriter import MimeWriter
    try:
      from cStringIO import StringIO
    except ImportError:
      from StringIO import StringIO
    from email.Utils import COMMASPACE
    
    files_to_attach = []
    files_to_attach.append(file)
    
    send_to = []
    send_to.append('heinrich.cronje@absa.co.za')
    send_to.append('PCGCommodities@corpexchange01.absa.co.za')
    
    send_from = 'heinrich.cronje@absa.co.za'
    
    tempfile = StringIO()
    mw = MimeWriter(tempfile)
    mw.addheader('to', COMMASPACE.join(send_to) )
    mw.addheader('from', send_from)
    mw.addheader('subject', 'SAAGRI_SAXEF_Physical_Trades Result ' + date.to_string())
    mw.startmultipartbody('mixed')
    for filename in files_to_attach:
      sw = mw.nextpart()
      f = sw.startbody('application/x-python')
      f.write(open(filename).read())
    mw.lastpart()
    
    message = tempfile.getvalue()
    SMTP('v036eml004001:25').sendmail(send_from, send_to, message)
