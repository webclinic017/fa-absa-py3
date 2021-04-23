
import acm

def SupportedMethods():
    methods=['2nd Shortest', 'Closest', 'Following', 'Preceding', 'Shortest', 'Following Exclusive']
    return methods
def DeleteItem(item):
    if None!=item:
        item.Delete()
def RemoveListItems(choiceList):
    choices=choiceList.Choices()
    while len(choices)>0:
        c=choices.First()
        c.Delete()
        
def CreateListItem(masterListName, name):
    listItem=acm.FChoiceList()
    listItem.List(masterListName)
    listItem.Name(name)
    listItem.Commit()

def AddItems(choiceList, methods):
    if None !=choiceList:
        masterName=choiceList.Name()
        for m in methods:
            CreateListItem(masterName, m)


def CreateChoiceList(methods=None):
    masterListName='Underlying Future Method'
    masterChoiceList=acm.FChoiceList[masterListName]
    
    #If choice list exists then clear all choices, otherwise create the ChoiceList
    if None!=masterChoiceList:
        RemoveListItems(masterChoiceList)
    else:
        CreateListItem('MASTER', masterListName)
        masterChoiceList=acm.FChoiceList[masterListName]
    #Add all supplied methods to the choice list, if no methods are supplied then add all supported core methods
    if None==methods:
        methods=SupportedMethods()
    
    AddItems(masterChoiceList, methods)
    
