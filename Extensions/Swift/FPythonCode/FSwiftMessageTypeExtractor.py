""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/swift/etc/FSwiftMessageTypeExtractor.py"
from FOperationsExceptions import WrapperException 
import FOperationsDocumentService as DocumentMod

class ExtractorException(WrapperException):
    def __init__(self, message, innerException = None):
        super(ExtractorException, self).__init__(message, innerException)

class FSwiftMessageTypeExtractor():
    def __init__(self, documentService):
        self.__documentService = documentService

    def Extract(self, documentId):
        try:
            documentInfo = self.__documentService.GetDocumentInfo(documentId)
            treatmentEvent = documentInfo['TreatmentEvent']
            # ConvertSWIFTMTXXXToInt implements similar workaround 
            if treatmentEvent.find("SWIFT_MT_") != -1:
                if treatmentEvent.find("SWIFT_MT_192_FOR_199") != -1:                
                    return 192
                elif treatmentEvent.find("SWIFT_MT_292_FOR_299") != -1:
                    return 292                    
                else:        
                    return int(treatmentEvent.strip("SWIFT_MT_")[-3:])
            else:
                raise ExtractorException('Could not extract message type for document %d: treatmentEvent contains unexpected data.' % documentId)
        except KeyError as e:
            raise ExtractorException('Could not extract message type for document %d: treatmentEvent not found.' % documentId, e)     
        except DocumentMod.DocumentServiceException as e:
            raise ExtractorException('Could not extract message type for document %d:' % documentId, e)

