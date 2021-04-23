import ael

#scopeName is portfolio name
scopeName = '40428'

#tradeCreateCutOffDateTime is report date for the trades
tradeCreateCutOffDateTime = '2016-08-22'

dataSelection = ael.asql(r'''SELECT t.trdnbr
                                     from 
                                     Trade t,
                                     Portfolio p 
                                     WHERE t.prfnbr = p.prfnbr and p.prfid = '%s' and t.status not in (1 , 7) and t.creat_time <= '%s'
                             ''' %(scopeName, tradeCreateCutOffDateTime))
print(dataSelection)
