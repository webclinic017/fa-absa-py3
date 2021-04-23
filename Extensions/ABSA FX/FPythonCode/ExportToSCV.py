import acm
'''================================================================================================
================================================================================================'''
def RowInterator(activeSheet, iterator, infile):
    if iterator.HasChildren() == True:
        childIter = iterator.FirstChild()
        while childIter:
            Row = childIter.Tree().Item()
            columnIterator = activeSheet.GridColumnIterator().First()
            line = str(Row.AsSymbol()) + ','
            while columnIterator:
                value = activeSheet.GetCell(childIter, columnIterator).FormattedValue()
                value = value.replace(',', '')
                line = line + value + ','
                columnIterator = columnIterator.Next()
            infile.write(line + "\n")    
            RowInterator(activeSheet, childIter, infile) 
            childIter = childIter.NextSibling()
'''================================================================================================
================================================================================================'''
def Run(invokationInfo): #FExtensionInvokationInfo
    import os
    desktopFile = os.path.expanduser("~/Desktop/tradeview.csv")
    #desktopFile = "C://temp//tradeview %s.csv " % acm.Time.TimeNow().replace(':','') 
    #activeSheet =  invokationInfo.ExtensionObject().GetUtilityView('TradeViewer')
    activeSheet =  invokationInfo.ExtensionObject().ActiveSheet()
    
    if activeSheet != None:
        iterator =  activeSheet.RowTreeIterator(True)
        FileHeader = ',' 
        columnIterator = activeSheet.GridColumnIterator().First()
        while columnIterator:
            FileHeader = FileHeader + columnIterator.GridColumn().ColumnId() + ','
            columnIterator = columnIterator.Next()
        
        with open(desktopFile, 'w') as infile:
            infile.write(FileHeader + "\n")   
            RowInterator(activeSheet, iterator, infile)

        from subprocess import Popen
        p = Popen(desktopFile, shell=True)
        
        #acm.UX().Dialogs().MessageBoxInformation(invokationInfo.ExtensionObject().Shell(), "Written CSV File to %s" % desktopFile)
    else:
        acm.UX().Dialogs().MessageBoxInformation(invokationInfo.ExtensionObject().Shell(), "The utility on works with Trade Viewer")
'''================================================================================================
================================================================================================'''




