
import acm

def GetTreatmentLinks(ai):
    treatmentLinks = acm.FTreatmentLink.Select("accountingInstruction = %d" % ai.Oid()).AsArray()
    return treatmentLinks

def GetTAccountLinks(ai):
    taccountLinks = list()
    jvds = ai.JournalValueDefinitions()
    for jvd in jvds:
        taccountLinks.extend(jvd.TAccountAllocationLinks())
    return taccountLinks

def RemoveObjects(objects):
    for obj in objects:
        RemoveObject(obj)

def RemoveObject(obj):
    acm.Log("Deleting %s %d" % (obj.ClassName(), obj.Oid()))
    obj.Delete()

def SetMappingPointers(mapping):
    prevMapping = mapping.Previous()
    nextMapping = mapping.Next()
    if(prevMapping):
        prevMapping.Next(nextMapping)
        prevMapping.Commit()
    if(nextMapping):
        nextMapping.Previous(prevMapping)
        nextMapping.Commit()

def RemoveMappings(mappings):
    mappingList = list()
    mappingList.extend(mappings)
    for mapping in mappingList:
        RemoveMapping(mapping)

def RemoveMapping(mapping):
    SetMappingPointers(mapping)
    RemoveMappings(mapping.Children().AsArray())
    RemoveObject(mapping)

def RemoveAccountingInstructionMappings(treatmentLinks):
    mappings = list()
    for treatmentLink in treatmentLinks:
        mappings.extend(treatmentLink.AccountingInstructionMappings().AsArray())
    RemoveMappings(mappings)

def RemoveTAccountMappings(treatmentLinks):
    mappings = list()
    for treatmentLink in treatmentLinks:
        mappings.extend(acm.FTAccountMapping.Select("treatmentLink = %d" % treatmentLink.Oid()).AsArray())
    RemoveMappings(mappings)

def RemoveAIReferences(ai):
    treatmentLinks = GetTreatmentLinks(ai)
    taccountLinks = GetTAccountLinks(ai)
    RemoveTAccountMappings(treatmentLinks)
    RemoveObjects(taccountLinks)
    RemoveAccountingInstructionMappings(treatmentLinks)
    RemoveObjects(treatmentLinks)

def HasJournalReferences(ai):
    journals = acm.FJournalInformation.Select("accountingInstruction=" + ai.Name())
    if len(journals) > 0:
        return True
    return False

def OpenWarningDialog(ai):
    func=acm.GetFunction('msgBox', 3)
    msgstr = "There are journals connected to '%s'.\n" % (ai.Name())
    msgstr += "Do you still want to remove all references to \'%s\' from the assignment tree?\n\n" % (ai.Name())
    msgstr += "Note: References between existing journals and '%s' will NOT be removed." % (ai.Name())
    selVal = func("Remove Accounting Instruction References", msgstr, 4)
    if(selVal == 6):
        RemoveAIReferences(ai)


def OpenContinueDialog(ai):
    func=acm.GetFunction('msgBox', 3)
    msgstr = "This operation will remove all references to \'%s\' from the assignment tree.\n\n" % (ai.Name())
    msgstr += "Do you want to continue?"
    selVal = func("Remove Accounting Instruction References", msgstr, 4)
    if(selVal == 6):
        RemoveAIReferences(ai)


def OpenDialog(eii):
    ai = eii.ExtensionObject()[0]
    if HasJournalReferences(ai):
        OpenWarningDialog(ai)
    else:
        OpenContinueDialog(ai)

