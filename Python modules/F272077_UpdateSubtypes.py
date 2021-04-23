"""----------------------------------------------------------------------------
MODULE
    F272077_UpdateSubtypes - Module which updates persistent archives to use the new text_object column subtype.

    (c) Copyright 2007 by Front Capital Systems AB. All rights reserved.

DESCRIPTION
    #
    #   Valid when upgrading to PRIME 4.0 from any earlier version

----------------------------------------------------------------------------"""

import acm

def UpdateQueryFolders():
    queryFolders = acm.FStoredASQLQuery.Select('')

    for storedQuery in queryFolders:
        storedQuery.AutoUser(False)
        print(storedQuery.Name())
        query = storedQuery.Query()
        if query:
            queryClass = query.QueryClass()
            if len( queryClass ):
                storedQuery.SubType( queryClass )
                storedQuery.Commit()
    

def UpgradeSheetTemplates():
    sheetTemplates = acm.FTradingSheetTemplate.Select('')
    
    for template in sheetTemplates:
        template.AutoUser(False)
        print(template.Name())
        template.SubType( template.SheetClass() )
        template.Commit()


UpdateQueryFolders()
UpgradeSheetTemplates()
