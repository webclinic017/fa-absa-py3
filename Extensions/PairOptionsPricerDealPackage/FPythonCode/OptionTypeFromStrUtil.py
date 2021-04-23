import acm

def OrderedDict(*keyValuePairs):
    d = acm.FOrderedDictionary()
    for key, value in keyValuePairs:
        d.AtPut(key, value)
    return d
    
mappingDict = { #VANILLA
                'VE':   OrderedDict(('baseType', 'Vanilla'),
                                    ('exerciseType', 'European')),
                'VA':   OrderedDict(('baseType', 'Vanilla'),
                                    ('exerciseType', 'American')),
                #BARRIER
                'DI':   OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Down & In')),
                'DO':   OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Down & Out')),
                'UI':   OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Up & In')),
                'UO':   OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Up & Out')),
                'DKI':  OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Double In')),
                'DKO':  OrderedDict(('baseType', 'Barrier'),
                                    ('barrierTypeForeign', 'Double Out')),
                #DIGITAL EUROPEAN
                'DE':   OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Vanilla')),
                'DEDI': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Down & In')),
                'DEDO': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Down & Out')),
                'DEUI': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Up & In')),
                'DEUO': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Up & Out')),
                'DEDKI': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Double In')),
                'DEDKO': OrderedDict(('baseType', 'Digital European'),
                                    ('digitalEuropeanTypeForeign', 'Double Out')),
                #DIGITAL AMERICAN
                'NT':   OrderedDict(('baseType', 'Digital American'),
                                    ('digitalAmericanTypeForeign', 'No Touch')),
                'OT':   OrderedDict(('baseType', 'Digital American'),
                                    ('digitalAmericanTypeForeign', 'One Touch')),
                'DNT':  OrderedDict(('baseType', 'Digital American'),
                                    ('digitalAmericanTypeForeign', 'Double No Touch')),
                'DOT':  OrderedDict(('baseType', 'Digital American'),
                                    ('digitalAmericanTypeForeign', 'Double One Touch')),
        }
        
menuDict = {}
for shortCut, setDict in mappingDict.items():
    menu = menuDict
    for menuNbr, menuItem in enumerate(setDict):
        menu = menu.setdefault(menuItem, {}).setdefault(setDict[menuItem], {} if menuNbr != len(setDict)-1 else shortCut)

def TransformToOptionTypeFromStr(inputStr):
    mapping = inputStr
    if mapping and isinstance(mapping, str):
          mapping = mapping.upper()
    return mappingDict.get(mapping, mapping)
