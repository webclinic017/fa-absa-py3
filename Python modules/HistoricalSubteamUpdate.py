'''
Once off run for the load of historical trades with default subteams
'''

import ael, acm

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
        user = acm.FUser[salesPerson]
        if user:
            return str(user.add_info('Default-SC-Sub-Team'))
        
        return ''
    except Exception, e:
        print e
        return ''



def __defaultSubTeamHook(t, salesPeople):
    SUBTEAM = 'SalesCreditSubTeam'
    t_clone = ael.Trade[t.Oid()].clone()
    
    i = 0    
    for salesPerson in salesPeople:
        i += 1
        hasValue = str(t.add_info(SUBTEAM + str(i)))
        if salesPerson != '' and hasValue == '':            
            __defaultSalesCreditAddInfo(t_clone, SUBTEAM + str(i), __getDefaultSubTeam(salesPerson))
            
    hasValue = str(t.add_info('Broker Status'))
    if hasValue == '':
        __defaultSalesCreditAddInfo(t_clone, 'Broker Status', 'Broker Trade with Direct Input')


def GetSalesData(Date, TradeDateFrom):
    TradeFrom = acm.Time().AsDate(TradeDateFrom)        
    if Date:
        Date = ael.date(Date)
        LastBankingDay = acm.Time().AsDate(Date)
    else:
        Date = ael.date_today()
        LastBankingDay = acm.Time().AsDate(Date)                

    trades = acm.FTrade.Select("updateTime >= '%s' and createTime >= '%s' and status <> 'Void' and status <> 'Simulated' and status <> 'FO Sales'" %(LastBankingDay, TradeFrom))
    tradesII = [t for t in trades if t.SalesPerson() != None or t.add_info('Sales_Person2') != '' or \
                t.add_info('Sales_Person3') != '' or t.add_info('Sales_Person4') != '' or t.add_info('Sales_Person5') != '']

    print '%i trades need to be processed during this run' %(len(tradesII))    
    
    for t in tradesII:        
        writerecord = False
        if t.SalesPerson()!= None:
            writerecord = True
        if not writerecord:
            for i in range(2, 7):
                field = 'Sales_Person' + str(i)
                if t.add_info(field) != '':
                    writerecord = True
                    break

        if writerecord:
            Sales_Person1 = ''                
            try:
                Sales_Person1 = t.SalesPerson().Name()
            except:
                Sales_Person1 = ''                    
            Sales_Person1 = str(Sales_Person1)                    
            Sales_Person2 = str(t.add_info('Sales_Person2'))
            Sales_Person3 = str(t.add_info('Sales_Person3'))
            Sales_Person4 = str(t.add_info('Sales_Person4'))
            Sales_Person5 = str(t.add_info('Sales_Person5'))
            
            #this makes more sense not to have it in validation slowing the entire system down
            #we update the trade as we get it in - only if it doesnt already have a value assigned to the relevant field 
            #for the default subteam value
            try:
                print 'Processing trade: ', t.Oid()
                __defaultSubTeamHook(t, [Sales_Person1, Sales_Person2, Sales_Person3, Sales_Person4, Sales_Person5])
            except Exception, e:
                print 'ERROR (%s) processing trade: %i' %(e, t.Oid())
    

ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Historical Subteam Update'}
ael_variables = [ ['Created', 'Created on or after date', 'date', None, ael.date_today(), 1],
                  ['Updated', 'Updated on or after date', 'date', None, ael.date_today(), 1]  ]

def ael_main(parameter, *rest):
    try:
        createDate = ael.date(parameter['Created'])
    except Exception, e:
        ael.log('Error parsing Create date input:' + str(e))
        raise

    try:
        updateDate = ael.date(parameter['Updated'])
    except Exception, e:
        ael.log('Error parsing Update date input:' + str(e))
        raise
    
    GetSalesData(updateDate, createDate)
