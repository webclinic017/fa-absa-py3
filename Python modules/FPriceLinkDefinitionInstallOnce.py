import ael
import acm

def setProtectionOnTextObject(user, module):
    user.protection = "W:R,O:R,G:R,U:RWD"
    ownerName = acm.UserName()
    user.owner_usrnbr = acm.FUser[ownerName].Oid()
    try:
        user.commit()
        acm.Log("Protection set for %s." %module)
    except Exception, e:
        acm.Log("Fail to set protection on %s! %s"%(module, e)) 

def addChoiceListValue(key,val,descr='',sortO=0):
    newcl = acm.FChoiceList()
    newcl.List = key
    newcl.Name = val
    if descr: newcl.Description(descr)
    if sortO: newcl.SortOrder(sortO)
    try:
        newcl.Commit()
    except Exception, e:
            print e

def addChoiceListType(choiceListType, listofchoicelist):   
    for choicelist in range(len(listofchoicelist)):
        choiceListDISTYPE = acm.FChoiceList.Select("list=%s"%choiceListType)
        if not choiceListDISTYPE:
            addChoiceListValue(choiceListType,listofchoicelist[choicelist])
        else:
            clval = acm.FChoiceList.Select("list='%s' and name='%s'" %(choiceListType, listofchoicelist[choicelist]))
            if not clval:
                addChoiceListValue(choiceListType,listofchoicelist[choicelist])
                
def main():
    # define local variables#
    service_types = []
    semantic_types = []
    choicelist_types = []
    # Set Protection on Scripts#
    users = ael.TextObject.select()

    for user in users:
        user = user.clone()
        if user.name == "FPriceLinkDefinitionInstallOnce":
            setProtectionOnTextObject(user, user.name)
        elif user.name == "FPriceDefinitionValidation":
            setProtectionOnTextObject(user, user.name)
        elif user.name == "FPriceDistributorValidation":
            setProtectionOnTextObject(user, user.name)
        elif user.name == "FPriceLinkDefinitionValidation":
            setProtectionOnTextObject(user, user.name)
        elif user.name == "PriceLinkDefinitionUpgrade":
            setProtectionOnTextObject(user, user.name)
    
    # Create the service and semantic choice lists#
    service_types.append('IDN_SELECTFEED')
    semantic_types.append('ILS')
    semantic_types.append('BSF')
    semantic_types.append('RSF')
    choicelist_types.append('PriceServices')
    choicelist_types.append('PriceSemantics')
    
    addChoiceListType('PriceServices', service_types)
    addChoiceListType('PriceSemantics', semantic_types)
    addChoiceListType('MASTER', choicelist_types)

#call main function    
main()