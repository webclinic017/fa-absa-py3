import acm
import ael

def deleteTradeFilter():
    tf = ael.TradeFilter['']
    if tf:
        try:
            tf.delete()
            print('Trade Filter deleted')
        except Exception, err:
            print('Trade Filter did not delete ', err)

def deleteInstruments():
    '''Instruments of the following types must have an underlying:
    Option, Warrant, Future/Forward, BuySellback, Convertible,
    Collateral, SecurityLoan, Repo/Reverse
    In the reported instruments this is not the case and that may
    cause problems for clients using the data.
     insaddr      insid                                   
     ------------ --------------------------------------- 
       429678 ZAR/IRS/080813/091113/P/10.88           
       429682 ZAR/IRS/080813/091113/P/10.88/#1        
       430129 ZAR/IRS/080813/091113/R/10.88           
       430131 ZAR/IRS/080813/091113/P/10.88/#3        
       468987 ZAR/IRS/100309/120312/R/8.00            
       520231 ZAR/FRA/100304/100608/B/7.24            
       520237 ZAR/FRA/100304/100608/B/7.24/#1    
    '''
    insNames =  ['ZAR/IRS/080813/091113/P/10.88',
    'ZAR/IRS/080813/091113/P/10.88/#1',
    'ZAR/IRS/080813/091113/R/10.88',
    'ZAR/IRS/080813/091113/P/10.88/#3',
    'ZAR/IRS/100309/120312/R/8.00',
    'ZAR/FRA/100304/100608/B/7.24',
    'ZAR/FRA/100304/100608/B/7.24/#1']
    
    for insName in insNames:
        ins = acm.FInstrument[insName]
        if ins:
            if ins.UnderlyingType() == 'Swap':
                if ins.OptionType() == 'Receiver':
                    ins.OptionType('Payer')
                ins.Underlying(acm.FInstrument['ZAR/IRS/F-JI/081113-091113/10.88'])
            else:
                ins.Underlying(acm.FInstrument['ZAR/FRA/JI/100308-100608/7.24'])
            try:
                ins.Commit()
                print('Instrument %s committed' %(insName))
            except Exception, err:
                print('Instrument %s did not commit %s' %(insName, err))

def deleteAddinfos():
    '''AdditionalInfo must have a recaddr
    In the reported additional infos this is not the case and that may
    cause problems for clients using the data.
     valnbr       addinf_specnbr value                                   recaddr      
     ------------ -------------- --------------------------------------- ------------ 
           153826            102 Unprinted                                       NULL 
          1260985            454 No                                              NULL 
           285803            491 ELOI                                            NULL 
           283834            494 803851                                          NULL 
          1007242            536 6.9                                             NULL 
          1075972            543 Invers                                          NULL 
          1075973            544 Currency2                                       NULL 
          1075975            545 No                                              NULL 
          1075974            546 No                                              NULL 
          1627296            548 Yes                                             NULL 
    '''
    addInfoNbrs = [153826,
    1260985,
    285803,
    283834,
    1007242,
    1075972,
    1075973,
    1075975,
    1075974,
    1627296]
    
    for addInfoNbr in addInfoNbrs:
        addInfo = acm.FAdditionalInfo[addInfoNbr]
        if addInfo:
            try:
                addInfo.Delete()
                print(addInfoNbr, ' additional info deleted')
            except Exception, err:
                print(addInfoNbr, 'AddInfo did not delete', err)


def setExoticType():
    '''Instruments with exotic_type = other must have a corresponding
    entry in the exotic table.
    In the reported instruments this is not the case and that may
    cause problems for clients using the data.
     insaddr      instype     insid                                   exotic_type 
     ------------ ----------- --------------------------------------- ----------- 
           667249           4 17534-L001_DKO/ZAR-USD/C/7.05/7.5/10010          16
    '''
    ins = acm.FInstrument['17534-L001_DKO/ZAR-USD/C/7.05/7.5/10010']
    ins.ExoticType('None')
    try:
        ins.Commit()
        print('Set exotic type to ', ins.ExoticType())
    except Exception, err:
        print('Exotic type did not commit', err)


deleteTradeFilter()
deleteInstruments()    
deleteAddinfos()
setExoticType()

