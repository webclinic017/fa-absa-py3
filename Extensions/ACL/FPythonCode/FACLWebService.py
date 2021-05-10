""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/FACL/ACL/./etc/FACLWebService.py"
import acm
import FACLArMLResponse

class FACLWebService:
    def __init__(self, armlServiceUrl, maxMsgBufSize):
        import facl
        self.armlService = facl.ArMLService(armlServiceUrl, maxMsgBufSize)

    def ProcessCookedArMLRequest(self, arml):
        return FACLArMLResponse.FACLArMLResponse(self.armlService.process_arml_request(arml))

    def ProcessRawArMLRequest(self, arml):
        return self.armlService.process_arml_request(arml)
