import xml.dom.minidom as xml
import acm

class SecureConfigReader():

    def __init__(self, configName):
    
        arenaDataServer = acm.FDhDatabase['ADM'].ADSNameAndPort().lower()
        
        configuration = acm.GetDefaultValueFromName(acm.GetDefaultContext(), acm.FObject, configName)

        domXml = xml.parseString(configuration)

        host = domXml.getElementsByTagName('Host')
        
        print('CAL Process running with dataserver:%s'%arenaDataServer)
        
        self.elements = [e for e in host if e.getAttribute('Name') == arenaDataServer]
        
        
    def getElementValue(self, elementName):
        
        for element in self.elements:
            if len(element.getElementsByTagName(elementName)) > 0:
                return element.getElementsByTagName(elementName)[0].childNodes[0].data
            else :
                print('No such tag:"%s"'%elementName)
            
#secureConfigReader = SecureConfigReader('CALConfigSettings')

#print(secureConfigReader.getElementValue('OutputPat'))
