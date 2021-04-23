import acm
import ael  

createdAddInfos = {}

def changeAddInfoAel(entity, fieldName, value, commit=True):
    '''
    set the add info and creates it if needed
    '''
    
    spec = ael.AdditionalInfoSpec[fieldName]
    set = False
    
    if type(value) == type('str') and len(value)>39:
        print 'Shortening value from %s to 39 characters' % value
        value = value[0:39]
        
    if commit:
        entity = entity.clone()
    
    aiToSet = None
    for add_info in entity.additional_infos():
        if add_info.addinf_specnbr == spec:
            aiToSet = add_info
            break
            
    if not aiToSet:
        if entity.record_type == 'Trade':
            if (entity.trdnbr, spec.specnbr) in createdAddInfos:
                #print 'updating add info that was created in the same transaction'
                aiToSet = createdAddInfos[(entity.trdnbr, spec.specnbr)]
                
    if aiToSet:
        aiToSet.value = value
        set = True
        
    if not set:
        #print 'Create new add info "%s" with value "%s" for trade %s'%(fieldName, value,entity.trdnbr)
            
        add_info = ael.AdditionalInfo.new(entity)
        add_info.addinf_specnbr = spec.specnbr
        add_info.value = value
        if entity.record_type == 'Trade':
            #update dict to be able to catch duplicate updates within one transaction
            createdAddInfos[(entity.trdnbr, spec.specnbr)] = add_info
        
    if commit:
        entity.commit()


settlements =[3472361,
3472240,
3472238,
3472239,
3472284,
3472243,
3472242,
3472326,
3383871,
3472287,
3472441,
3472234,
3474303,
3474312,
3472329,
3472248,
3474289,
3474293,
3474290,
3474291,
3474313,
3474292,
3474314,
3510608,
3474294,
3474295,
3474315,
3474316,
3474317,
3474287,
3474296,
3474307,
3474310,
3472417,
3474300,
3474299,
3473187,
3474301,
3474311,
3474302,
3474298,
3474318,
3474304,
3474319,
3472416,
3474320,
3474321,
3474322,
3474306,
3474305,
3474297,
3474288,
3481200,
3474308,
3474323,
3474309,
3472231,
3509609,
3510911,
3472285,
3482578,
3510502,
3474142,
3472229,
3472290,
3474143,
3504551,
3500404,
3500305,
3472433,
3472421,
3474357,
3472338,
3472327,
3472304,
3472476,
3472419,
3472449,
3472283,
3515447,
3472420,
3472292,
3472237,
3472718,
3472236,
3472244,
3472418,
3494707,
3472444,
3519073,
3472341,
3472328,
3510144,
3472247,
3472235,
3494222,
3472442,
3481124,
3472457,
3472455,
3472456,
3516895,
3513313,
3472428,
3472291
]


total = len(settlements)
print 'This will processing {0} number of settlements'.format(total)
count = 1

try:
    for settlement in settlements:
        print 'Processing {0}/{1}'.format(count, len(settlements))
        s = acm.FSettlement[settlement]

        clone = s.Clone()
        clone.Status('Authorised')
        clone.ValueDay(acm.Time.DateToday())
        s.Apply(clone)
        changeAddInfoAel(ael.Settlement[settlement], 'Authorise Debit', 'Yes')
        changeAddInfoAel(ael.Settlement[settlement], 'Call_Confirmation', 'Auto Int Payment')		
        s.Commit()
        print 'settlement {0} status = {1}'.format(settlement, s.Status())

        clone = s.Clone()
        clone.Status('Released')
        s.Apply(clone)
        s.Commit()
        print 'settlement {0} status = {1}'.format(settlement, s.Status())
        print ''
        count+=1
except Exception, e:
    print '{0}. Error on settlement {1}'.format(str(e), settlement)
    pass

