import acm
        

'''******************************'''
class DefaultValGroup(object):
    def __init__(self, valGroup):
        try:
            if valGroup == "":
                valGroup = None
            elif isinstance(valGroup, str):
                valGroup = acm.FChoiceList[valGroup]
            elif hasattr(valGroup, 'StringKey'):
                valGroup = valGroup if valGroup.IsKindOf(acm.FChoiceList) else None 
        except:
            valGroup = None
        
        self._valGroup = valGroup
        
    def ValuationGroup(self):
        return self._valGroup
