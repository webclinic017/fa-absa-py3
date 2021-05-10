import acm

class ValueInvoker():
    def __init__(self, source, block):
        self.m_source = source
        self.m_block  = block
        
        if not self.Invoke():
            source.AddDependent(self)
    
    def Invoke(self):
        if not self.m_source:
            return False
            
        value = self.m_source.Value()
        
        if self.m_source.IsValuePending():
            return False
        
        self.m_block(value)
        
        return True
            
    def ServerUpdate(self, sender, aspect, parameter):
        if sender == self.m_source:
            if self.Invoke():
                self.m_source.RemoveDependent(self)
                self.m_source = None
  
