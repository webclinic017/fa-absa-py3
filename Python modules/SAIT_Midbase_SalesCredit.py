'''
Purpose                 :SalesCredit Feed,, Updated to use ACM Date,Updated To Correct String Conversion, Updated To Handle exceptions 
			 Add new additional info fields, choice list and new fields to the feed to Midbase. Handle Commas in sales credit
			 Six new attributes added for sales subteam and broker status
			 Trade tickets updated with default values for six additional fields if they need to be and no value exists on trade ticket
			 Added check for status - excluded Simualted and Void
			 Changes to send the Far leg trade number with the near leg sales credit details for FX Swaps
Department and Desk     :IT
Requester:              :Daniel Simoes, Daniel Simoes, Daniel/Jerome,Jerome, Jerome, Jerome
Developer               :Henk Nel,Ickin Vural, Jaysen Naicker,Ickin Vural, Anwar Banoo, Anwar Banoo,Ickin Vural, Bhavnisha Sarawan, Bhavnisha Sarawan
CR Number               :C000000469235,C000000470674,C000000476513,C000000482069, 506836,C000000508688,C000000510464, C591849, C602184, C000000620427, C880865, C892048
'''

import ael, acm

def __createFile(fileName):
    try:
        outfile = open(fileName, 'w')
        outfile.close()
        return True
    except Exception, e:
        print 'Error creating output file %s: %s' %(fileName, e)
        return False
        

def __writeHeaders(fileName):
    outfile = open(fileName, 'a')

    TrdNbr              = 'TrdNbr'
    Sales_Person1       = 'Sales_Person1'
    Sales_Person2       = 'Sales_Person2'
    Sales_Person3       = 'Sales_Person3'
    Sales_Person4       = 'Sales_Person4'
    Sales_Person5       = 'Sales_Person5'
    Sales_Credit1       = 'Sales_Credit1'       
    Sales_Credit2       = 'Sales_Credit2' 
    Sales_Credit3       = 'Sales_Credit3' 
    Sales_Credit4       = 'Sales_Credit4' 
    Sales_Credit5       = 'Sales_Credit5' 
    ValueAddCredits     = 'ValueAddCredits'          
    ValueAddCredits2    = 'ValueAddCredits2'                
    ValueAddCredits3    = 'ValueAddCredits3'                
    ValueAddCredits4    = 'ValueAddCredits4'                
    ValueAddCredits5    = 'ValueAddCredits5'                
    Shadow_Revenue_Type = 'Shadow_Revenue_Type'
    RWA_Counterparty    = 'RWA_Counterparty'
    Relationship_Party  = 'Relationship_Party'
    Country             = 'Country'
    Portfolio           = 'Portfolio'
    Repday              = 'Repday'
    BrokerStatus        = 'BrokerStatus'
    Sales_SubTeam1      = 'Sales_SubTeam1'
    Sales_SubTeam2      = 'Sales_SubTeam2'
    Sales_SubTeam3      = 'Sales_SubTeam3'
    Sales_SubTeam4      = 'Sales_SubTeam4'
    Sales_SubTeam5      = 'Sales_SubTeam5'

    outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(TrdNbr, Sales_Person1, Sales_Credit1,\
                   Sales_Person2, Sales_Credit2, Sales_Person3, Sales_Credit3, Sales_Person4, Sales_Credit4, Sales_Person5, Sales_Credit5, ValueAddCredits,\
                   ValueAddCredits2, ValueAddCredits3, ValueAddCredits4, ValueAddCredits5, Shadow_Revenue_Type, RWA_Counterparty, Relationship_Party,
                   Country, Portfolio, Repday, BrokerStatus, Sales_SubTeam1, Sales_SubTeam2, Sales_SubTeam3, Sales_SubTeam4, Sales_SubTeam5))

    outfile.close()
        

def __defaultSalesCreditAddInfo(entity, fieldName, defaultValue):

    def __createAddInfo():
        ai = ael.AdditionalInfo.new(entity)
        ai.addinf_specnbr = aisp
        ai.value = defaultValue
        ai.commit()
    
    try:
        if defaultValue:
            #have to handle the case where the GUI assigns two blank likes to the inputs for the sales credit add infos.
            try:
                addInfoField = entity.add_info(fieldName)
            except Exception, e:
                print '%s is an invalid entry: ' %(fieldName), e
                addInfoField = None
                
            if not addInfoField or addInfoField == '':
                aisp = ael.AdditionalInfoSpec[fieldName]
                if aisp:                    
                    aiList = ael.AdditionalInfo.select('addinf_specnbr = %i' %aisp.specnbr)    
                    myTrade = [ai for ai in aiList if ai.recaddr == entity.trdnbr]
                        
                    if myTrade:
                        ais = entity.additional_infos()
                        falsePositive = True
                        for ai in ais:
                            if ai.addinf_specnbr.specnbr == aisp.specnbr:                            
                                ai.value = defaultValue
                                falsePositive = False
                                continue
                                
                        if falsePositive:
                            __createAddInfo()
                    else:
                        __createAddInfo()
    except Exception, e:
        print e

                
def __getDefaultSubTeam(salesPerson):
    try:
        user = ael.User[salesPerson]
        if user:
            return str(user.add_info('Default-SC-Sub-Team'))
        
        return ''
    except Exception, e:
        print e
        return ''



def __defaultSubTeamHook(t, salesPeople):
    SUBTEAM = 'SalesCreditSubTeam'
    t_clone = t.clone()
    
    i = 0    
    for salesPerson in salesPeople:
        i += 1
        hasValue = str(t.add_info(SUBTEAM + str(i)))
        if salesPerson != '' and hasValue == '':            
            __defaultSalesCreditAddInfo(t_clone, SUBTEAM + str(i), __getDefaultSubTeam(salesPerson))
            
    hasValue = str(t.add_info('Broker Status'))
    if hasValue == '':
        __defaultSalesCreditAddInfo(t_clone, 'Broker Status', 'No Broker')
    ael.poll()


def GetSalesData(temp, FileName, Directory, Date, TradeDateFrom, *rest):
    fileName = Directory + FileName
    if __createFile(fileName):
        __writeHeaders(fileName)
    
        TradeFrom = acm.Time().AsDate(TradeDateFrom)        
        if Date:
            Date = ael.date(Date)
            LastBankingDay = acm.Time().AsDate(Date)
        else:
            Date = ael.date_today()
            LastBankingDay = acm.Time().AsDate(Date)                

        trades = acm.FTrade.Select("updateTime >= '%s' and createTime >= '%s'" %(LastBankingDay, TradeFrom))

        for value in trades:
            outfile = open(fileName, 'a')
            t = ael.Trade[value.Oid()]
            writerecord = False
            if t.status not in ('Simulated', 'Void') and t.trade_process != (16384):
                if t.sales_person_usrnbr != None:
                    writerecord = True
                if not writerecord:
                    for i in range(2, 7):
                        field = 'Sales_Person' + str(i)
                        if t.add_info(field) != '':
                            writerecord = True
                            break
                   

            if writerecord:
                TrdNbr                      =      str(t.trdnbr)
                
                if t.trade_process == 32768:
                    t = t.connected_trdnbr
                
                Sales_Person1               =      ''                
                try:
                    Sales_Person1           =      t.sales_person_usrnbr.userid
                except:
                    Sales_Person1           =      ''                    
                Sales_Person1               =     str(Sales_Person1)                    
                Sales_Person2               =     str(t.add_info('Sales_Person2'))
                Sales_Person3               =     str(t.add_info('Sales_Person3'))
                Sales_Person4               =     str(t.add_info('Sales_Person4'))
                Sales_Person5               =     str(t.add_info('Sales_Person5'))
                
                Sales_Credit1               =     ''                
                try:
                    Sales_Credit1           =     str(t.sales_credit).replace(',', '')
                except:
                    Sales_Credit1           =     ''
                    
                Sales_Credit1               =     str(Sales_Credit1)                    
                Sales_Credit2               =     str(t.add_info('Sales_Credit2').replace(',', ''))
                Sales_Credit3               =     str(t.add_info('Sales_Credit3').replace(',', ''))
                Sales_Credit4               =     str(t.add_info('Sales_Credit4').replace(',', ''))
                Sales_Credit5               =     str(t.add_info('Sales_Credit5').replace(',', ''))

                ValueAddCredits             =     str(t.add_info('ValueAddCredits').replace(',', ''))
                ValueAddCredits2            =     str(t.add_info('ValueAddCredits2').replace(',', ''))
                ValueAddCredits3            =     str(t.add_info('ValueAddCredits3').replace(',', ''))
                ValueAddCredits4            =     str(t.add_info('ValueAddCredits4').replace(',', ''))
                ValueAddCredits5            =     str(t.add_info('ValueAddCredits5').replace(',', ''))


                if str(t.add_info('Shadow_Revenue_Type')) == '':
                    Shadow_Revenue_Type     =     'Auto'
                else:
                    Shadow_Revenue_Type     =     str(t.add_info('Shadow_Revenue_Type'))
                    
                if str(t.add_info('RWA_Counterparty')) == '':
                    RWA_Counterparty        =     str(t.counterparty_ptynbr.ptyid)
                else:
                    RWA_Counterparty        =     str(t.add_info('RWA_Counterparty'))
                    
                if str(t.add_info('Relationship_Party')) == '':
                    Relationship_Party      =     str(t.counterparty_ptynbr.ptyid)
                else:
                    Relationship_Party      =     str(t.add_info('Relationship_Party'))

                Country                     =     str(t.add_info('Country'))
                
                Portfolio                   =     ''
                
                try:
                    Portfolio                   =     str(t.prfnbr.prfid)
                except:
                    Portfolio                   =     ''
                
                Repday                      =     LastBankingDay
                
                if ((not t.add_info('Broker Status')) or (str(t.add_info('Broker Status')) == '')):
                    BrokerStatus     =     'No Broker'
                    
                else:
                    BrokerStatus     =     str(t.add_info('Broker Status'))
                   
                
                #this makes more sense not to have it in validation slowing the entire system down
                #we update the trade as we get it in - only if it doesnt already have a value assigned to the relevant field 
                #for the default subteam value
                __defaultSubTeamHook(t, [Sales_Person1, Sales_Person2, Sales_Person3, Sales_Person4, Sales_Person5])
                
                Sales_SubTeam1 = str(t.add_info('SalesCreditSubTeam1'))
                Sales_SubTeam2 = str(t.add_info('SalesCreditSubTeam2'))
                Sales_SubTeam3 = str(t.add_info('SalesCreditSubTeam3'))
                Sales_SubTeam4 = str(t.add_info('SalesCreditSubTeam4'))
                Sales_SubTeam5 = str(t.add_info('SalesCreditSubTeam5'))
                
                outfile.write('%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n'%(TrdNbr, Sales_Person1,\
                              Sales_Credit1, Sales_Person2, Sales_Credit2, Sales_Person3, Sales_Credit3, Sales_Person4, Sales_Credit4, Sales_Person5,\
                              Sales_Credit5, ValueAddCredits, ValueAddCredits2, ValueAddCredits3, ValueAddCredits4, ValueAddCredits5, Shadow_Revenue_Type,\
                              RWA_Counterparty, Relationship_Party, Country, Portfolio, Repday, BrokerStatus, Sales_SubTeam1, Sales_SubTeam2, Sales_SubTeam3, Sales_SubTeam4, Sales_SubTeam5))

            outfile.close()
        return fileName
    else:
        return 'Failed to create file'
