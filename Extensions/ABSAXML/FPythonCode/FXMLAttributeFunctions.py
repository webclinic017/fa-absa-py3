
import re
import acm
from array import array
from ABSAFOperationsXML import ABSAFOperationsXML
from ABSADataContainer import ABSADataContainer

class FXMLAttributeFunctions(object): 
    
    def __init__(self, dom):
        self.data = ABSAFOperationsXML.ToXml(dom)
        self.token = '#FA#'
        self.pattern = re.compile('(\w+)="#FA#(.*?)"', re.LOCALE) #make the \w match word characters for this locale

    def process_attributes(self):
        a1 = array('c', self.data)
        offset = 0
        token_length = len(self.token)
        
        for m in re.finditer(self.pattern, self.data):
            result = getattr(self, m.group(2), None)
            if result:
                result_output = result()
                output = array('c', "%s=\"%s\"" % (m.group(1), result_output))
                a1[m.start() + offset:m.end() + offset] = output
                offset += len(result_output) - len(m.group(2)) - token_length
        
        return ABSAFOperationsXML.CreateXMLMiniDom(a1.tostring())
    
    
    def get_TRXnbr(self):         #define lots of these
        return str(ABSADataContainer.GetTRXNumber())
