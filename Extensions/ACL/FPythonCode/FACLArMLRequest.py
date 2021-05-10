""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLArMLRequest.py"
from xml.etree.ElementTree import fromstring

class FACLArMLRequest:
    
    def __init__(self, armlString):
        self._namespace = '{http://www.sungard.com/Adaptiv/Crs/Schema}'
        self._parseRequest(fromstring(armlString))

    def RequestID(self):
        return self._requestID

    def Action(self):
        return self._action
    
    def Flags(self):
        return self._flags

    def AdminType(self):
        return self._adminType
        
    def _parseRequest(self, armlDocument):
        self._requestID = self._extractRequestID(armlDocument)
        self._action = self._extractAction(armlDocument)
        self._flags = self._extractFlags(armlDocument)
        self._adminType = self._extractAdminType(armlDocument)

    def _extractRequestID(self, armlDocument):
        path = './/{0}RequestID'.format(self._namespace)
        return armlDocument.find(path).text
    
    def _extractAction(self, armlDocument):
        path = './/{0}Action'.format(self._namespace)
        return armlDocument.find(path).text
    
    def _extractFlags(self, armlDocument):
        path = './/{0}ActionFlags/{0}Flag'.format(self._namespace)
        matches = armlDocument.findall(path)
        return [match.text for match in matches]

    def _extractAdminType(self, armlDocument):
        path = './/{0}AdminHeader/{0}Type'.format(self._namespace)
        match = armlDocument.find(path)
        if match is None:
            return None
        else:
            return match.text
