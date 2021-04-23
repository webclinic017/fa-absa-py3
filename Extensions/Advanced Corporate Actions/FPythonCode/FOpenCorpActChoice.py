""" Compiled: 2020-09-18 10:38:49 """

#__src_file__ = "extensions/advanced_corporate_actions/./etc/FOpenCorpActChoice.py"
"""----------------------------------------------------------------------------
MODULE
    FOpenCorpActChoice - GUI Module to open to a corporate action 
    Choice definition.

DESCRIPTION
----------------------------------------------------------------------------"""

import acm

infoSpecs = acm.FAdditionalInfoSpec.Select("recType=CorpActChoice")

def run_main(d, choice, CreateBusinessProcess = 0):
    if d['Name'] != None:
        choice.Name = d['Name']
    choice.IsDefault = d['IsDefault']
    choice.CorpAction = d['CorpAction']
   
    existedAddInfoSpec = []
    addinfo = choice.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        existedAddInfoSpec.append(name)
        if name in list(d.keys()):
            i.FieldValue(d[name])
    
    choice.Commit()
    addinfo = choice.AddInfos()
    for i in addinfo:
        spec = i.AddInf()
        name = spec.FieldName()
        if name in list(d.keys()) and name not in existedAddInfoSpec:
            existedAddInfoSpec.append(name)
            i.FieldValue(d[name])
            i.Commit()

    for spec in infoSpecs:
        name = spec.Name()
        if name in existedAddInfoSpec:
            continue
        if name in list(d.keys()) and d[name]:
            newAddInfo = acm.FAdditionalInfo()
            newAddInfo.AddInf(spec)
            newAddInfo.Parent(choice)
            newAddInfo.FieldValue(d[name])
            newAddInfo.Commit()
