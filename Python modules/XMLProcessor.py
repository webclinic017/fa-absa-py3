from xml.etree.ElementTree import Element, SubElement, dump, XML, tostring, ElementTree, parse, fromstring

class XMLProcessor:
    def __init__(self, xml_text):
        self.xml_text = xml_text
        
    def getNodeByAttributeValue(self, node_name, attribute, attribute_value):
        xml_tree_object = ElementTree(fromstring(self.xml_text))
        elements = xml_tree_object.findall(node_name)
        value = None
        for element in elements:
            if element.attrib[attribute] == attribute_value:
                return element
                
    def getNodeValueFromElement(self, element, path):
        path = path.split('/')
        length = len(path)
        value = None 
        for node in element.getchildren():
            if node.tag == path[0]:
                value = node.find(path[length-1]).text
                return value
        
        
    def getNodeValue(self, path):
        path = path.split('/')
        length = len(path)
        xml_tree_object = ElementTree(fromstring(self.xml_text))
        element = xml_tree_object.find(path[0])
        value = None 
        for node in element.getchildren():
            if node.tag == path[length-1]:
                value = node.text
        return value
    
    def getAttributeValueFromElement(self, element, attribute):
        #element = element.find(path)
        attribute_value = element.get(attribute)
        return attribute_value
    
    def getAttributeValue(self, path, attribute):
        xml_tree_object = ElementTree(fromstring(self.xml_text))
        element = xml_tree_object.find(path)
        attribute_value = element.get(attribute)
        return attribute_value
