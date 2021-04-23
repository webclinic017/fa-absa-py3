

import acm
import traceback

defaultGUI = acm.FBusinessLogicGUIDefault()

def Decorate(object):
    return acm.FBusinessLogicDecorator.WrapObject(object, defaultGUI)

def allEnumValuesExcludeNone( enumValues ):
    return [e for e in enumValues.Enumerators() if (e != 'None')]  


def listChoices(listName):
    query = 'name = '
    query += listName
    
    collection = acm.FChoiceList.Select(query)
    
    if collection.Size() < 1 :
        list=acm.FArray()
        list.Add('None')
        return list
        
    list = collection.At(0)
        
    arr = list.Choices().AsArray()

    return arr
    
def listChoicesWithEmpty(listName):
    choices = listChoices(listName)
    choices.Add("")
    return choices

def getTimeZones():
    return acm.Time.TimeZones()


# the tryExceptDecorator should be used as soon as PRIME can handle calls from extensionAttributes to decorated python functions, SPR 370407
def tryExceptDecorator(func):
        def tryExcept(*args, **kwargs):
            try:
                func(*args, **kwargs)
            except Exception as e:
                print (Exception, e)
                print (traceback.format_exc())
                print ("Arguments were: %s, %s" % (args, kwargs))
        return tryExcept
