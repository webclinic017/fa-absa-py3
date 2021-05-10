
import acm


def listChoices(listName):
    query = 'name = '
    query += listName
    
    collection = acm.FChoiceList.Select(query)
    
    if collection.Size() < 1 :
        return ['None']
        
    list = collection.At(0)
        
    arr = list.Choices()
    arr = arr.SortByProperty('StringKey', True)

    return arr

def listChoicesWithEmpty(listName):
    choices = listChoices(listName)
    choices.Add("")
    return choices

def getClearingLocations():
    return listChoicesWithEmpty("Clearing Location")
    
