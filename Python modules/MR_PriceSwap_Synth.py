
'''
Purpose                 :[Market Risk feed files],[To model a Price Swap as an asian option in order to get the correct average value (float leg) and a swap fixed leg]
Department and Desk     :[IT],[MR]
Requester:              :Jacqueline Calitz
Developer               :Heinrich Cronje
CR Number               :XXXXXX

Date           CR               Requestor          Developer          Change
----------------------------------------------------------------------------------------
2020-09-11     CHG0128302	Garth Saunders	   Heinrich Cronje    https://absa.atlassian.net/browse/CMRI-776
'''


import ael, string, acm, PositionFile, MR_MainFunctions
import csv
InsL = []


# OPENFILE ##########################################################################################################
    
def OpenFile(temp,FileDir,Filename,PositionName,*rest):
    
    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    
    outfile             =  open(filename, 'w')
    outfileP            =  open(PositionFilename, 'w')
    
    outfile.close()
    outfileP.close()
    
    del InsL[:]
    InsL[:] = []
    
    return filename

# OPENFILE ##########################################################################################################

def writeCSVRow(_headers, _dataSet, _csvPtr):
    _out = []

    # Populating the tuple for the output
    for _col in tuple(_headers.split()):
        _out.append(_dataSet[_col] if _col in _dataSet else '')

    _csvPtr.writerow(_out)

# WRITE - FILE ######################################################################################################

def Write(i,FileDir,Filename,PositionName,*rest):

    filename            = FileDir + Filename
    PositionFilename    = FileDir + PositionName
    insaddr = i.insaddr
    Instrument = acm.FInstrument[insaddr]
            
    # Defining the fields
    columnsHeaders='''BASFLAG HeaderName OBJECT TYPE NAME IDENTIFIER CurrencyCAL CurrencyDAYC CurrencyPERD CurrencyUNIT 
    CostOfCarryCAL CostOfCarryDAYC CostOfCarryPERD CostOfCarryVAL TheoModelXREF MarketModelXREF FairValueModelXREF 
    '''
    
    columnsHeadersUnderlying='''BASFLAG HeaderName ATTRIBUTE OBJECT ComponentWghtVAL 
    '''

    columnsHeadersComponents='''BASFLAG HeaderName ATTRIBUTE OBJECT UndrFinEntitisXREF 
    '''    

    if (insaddr) not in InsL:
        InsL.append(insaddr)
        
        # Data initialisation
        data={}
        uData={}        # Underlying data
        cData={}        # Component data
        
        #Base record
        data['BASFLAG']       = 'BAS'
        data['HeaderName']    = 'Synthetic'
        data['OBJECT']        = 'Synthetic InstrumentSPEC'
        data['TYPE']          = 'Synthetic InstrumentSPEC'
        data['NAME']          = MR_MainFunctions.NameFix(i.insid)
        data['IDENTIFIER']    = 'insaddr_'+ str(insaddr)
        data['CurrencyUNIT']  = Instrument.Currency().Name()
        data['TheoModelXREF'] = 'Basket Instrument'
      
        # Writing the CSV file
        with open (filename, 'ab') as csvfile:
            csvwriter = csv.writer(csvfile)
            writeCSVRow(columnsHeaders, data, csvwriter)
            
            #Rollover record            
            uData['BASFLAG']          = 'rm_ro'
            uData['HeaderName']	      = 'Synthetic : Component Weights'
            uData['ATTRIBUTE']	      = 'Component Weights'
            uData['OBJECT']           = 'Synthetic InstrumentSPEC'
            
            for l in i.legs():
                if l.type == 'Float':
                    if l.payleg:
                        uData['ComponentWghtVAL']  =	-1
                    else:
                        uData['ComponentWghtVAL']  =	1
                                            
            writeCSVRow(columnsHeadersUnderlying, uData, csvwriter)
                                
            cData['BASFLAG']            = 'rm_ro'
            cData['HeaderName']         = 'Synthetic : Underlying Financial Entities'
            cData['ATTRIBUTE']          = 'Underlying Financial Entities'
            cData['OBJECT']             = 'Synthetic InstrumentSPEC'           
            cData['UndrFinEntitisXREF'] = 'insaddr_'+ str(insaddr)+'_1'
            writeCSVRow(columnsHeadersComponents, cData, csvwriter)
                       
            for l in i.legs():
                if l.type == 'Fixed':
                    if l.payleg:
                        uData['ComponentWghtVAL']  =	-1
                    else:
                        uData['ComponentWghtVAL']  =	1
                       
            writeCSVRow(columnsHeadersUnderlying, uData, csvwriter)
                                
            cData['UndrFinEntitisXREF'] = 'insaddr_'+ str(insaddr)+'_2'          
            writeCSVRow(columnsHeadersComponents, cData, csvwriter)

        csvfile.close()

        for trades in i.trades():
            if MR_MainFunctions.ValidTradeNo(trades) == 0:
                if MR_MainFunctions.IsExcludedPortfolio(trades) == False:
                    PositionFile.CreatePosition(trades, PositionFilename)

    return i.insid

# WRITE - FILE ######################################################################################################
