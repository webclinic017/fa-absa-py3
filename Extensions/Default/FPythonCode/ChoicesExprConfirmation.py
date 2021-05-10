
import acm
import ael
from ChoicesExprCommon import listChoices, listChoicesWithEmpty


def getSettleCategories():
    return listChoicesWithEmpty("Settle Category")

def getDepartments():
    dep = acm.FInternalDepartment.Select('')
    dep = dep.SortByProperty('StringKey', True)
    return dep

def getDocuments():
    return listChoices('Standard Document')

def getEvents():
    return listChoices('Event')

def getInsTypes():
    arr = acm.FEnumeration['enum(InsType)'].Enumerators()
    arr = arr.Sort()
    return [type for type in  arr if type and checkInsType(type)]

def getProducts():
    return listChoices('Product Type')

def getTemplates():
    return listChoices('Conf Template')
