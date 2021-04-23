import acm

for aisName in ['ET_EcnInstance', 'ET_EcnTradeId']:
    ais = acm.FAdditionalInfoSpec[aisName]
    if not ais:
        print('Creating...' + aisName)
        ais = acm.FAdditionalInfoSpec()
        ais.FieldName = aisName
        description = aisName
        excType = 'String'
        grpS = 'Standard'
        typ = acm.FEnumeration['enum(B92StandardType)'].Enumeration(excType.capitalize())
        ais.DataTypeGroup(acm.FEnumeration['enum(B92DataGroup)'].Enumeration(grpS))
        ais.DataTypeType(typ)
        ais.Description = description
        ais.RecType('Trade')
        ais.SubRecMask1(64)
        #print ais
        ais.Commit()
        print('..create done.')        
    else:
        print(aisName + ' already exists!')
        
    
