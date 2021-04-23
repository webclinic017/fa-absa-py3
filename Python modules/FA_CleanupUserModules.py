#
# Script removes Extension Attributes, Column Definitions and Python code from the user extension modules.
#
import acm
import sys

users= acm.FUser.Select("userGroup<>'Integration Process' and userGroup<>'System Processes' and userGroup<>'ADMIN_STO'")
count = 0;
usersArray = users.AsArray()
atsu1=acm.FUser['ATSU1']
usersArray.Add(atsu1)

for user in usersArray:
    extModule = acm.FExtensionModule[user.Name()]
    if extModule:
        #print >>sys.stderr, extModule.Name()
        extAttributes=acm.FClass["FExtensionAttribute"]
        extension = extModule.GetAllExtensions(extAttributes)
        extModule.RemoveExtension(extension)
        colDefinition=acm.FClass["FColumnDefinition"]
        extension = extModule.GetAllExtensions(colDefinition)
        extModule.RemoveExtension(extension)
        pythonCode=acm.FClass["FPythonCode"]
        extension = extModule.GetAllExtensions(pythonCode)
        extModule.RemoveExtension(extension)
        
        extModule.Commit()
        count=count+1
        
print("Number of the user modules updated: ", count, file=sys.stderr)


