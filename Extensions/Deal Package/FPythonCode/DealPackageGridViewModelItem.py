import acm

'''********************************************************'''
class ModelRow(object):
    def __init__(self, rowItems):
        self._rowItems = rowItems
    
    def RowItems(self):
        return self._rowItems
        
    def Visible(self, dp):
        return True
            
    def RowHight(self, dp):
        return 18
        
    def IsColumnHeaderRow(self, dp):
        return False
        
'''********************************************************'''
class ModelItem(object):
    def ToolTip(self, dp):
        return ''
        
    def GetValue(self, dp):
        pass
        
    def SetValue(self, dp, value):
        pass
        
    def ReadOnly(self, dp):
        return True
 
    def ToolTip(self, dp):
        return None
        
    def Formatter(self, dp):
        return None
        
    def ChoiceListSource(self, dp):
        return None
        
    def IsCalculatedValue(self, dp):
        return False

    def IsCalculationSimulated(self, dp):
        return False

    def GetCalculationColumnName(self, dp):
        return None
     
    def UseBoldFont(self, dp):
        return False

    def UseItalicFont(self, dp):
        return False
        
    def Alignment(self, dp):
        return 'MiddleRight'
 
    def BackColor(self, dp):
        return None
    
    def OnDoubleClick(self, dp):
        pass 
        
    def OnDeleteKeyDown(self, dp):
        pass
    
