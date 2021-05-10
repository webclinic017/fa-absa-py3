'''-----------------------------------------------------------------------------
PROJECT                 :  Markets Message Gateway
PURPOSE                 :  Wraps messages for the Markets Message Gateway
DEPATMENT AND DESK      :  
REQUESTER               :  
DEVELOPER               :  Francois Truter
CR NUMBER               :  XXXXXX
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date       Change no Developer                 Description
--------------------------------------------------------------------------------
2011-03-25 XXXXXX    Francois Truter           Initial Implementation
'''

from xml.etree import ElementTree
from xml.dom.minidom import Document
import time
import acm

class GatewayMessageType:
    New = 'NEW'
    Amend = 'AMEND'
    
class GatewayMessageFormat:
    Swift = 'SWIFT'
    Xml = 'XML'

class GatewayMessage:

    @staticmethod
    def _addNode(doc, parent, name, text = None):
        node = doc.createElement(name)
        parent.appendChild(node)
        if text:
            textNode = doc.createTextNode(str(text))
            node.appendChild(textNode)
        
        return node
    
    def __init__(self, sourceSystem, timeStamp, swiftCode, uniqueRef, subSystemId, subSystemUser, swiftType, msgType, msgFormat, msgDetails):
        doc = Document()
        
        NAMESPACE = 'GateWaySchema'
        root = doc.createElementNS(NAMESPACE, 'GateWayMessage'); 
        root.setAttribute('xmlns', NAMESPACE) 
        doc.appendChild(root)
        
        GatewayMessage._addNode(doc, root, 'SourceSystem', sourceSystem)
        GatewayMessage._addNode(doc, root, 'TimeStamp', timeStamp)
        GatewayMessage._addNode(doc, root, 'SwiftCode', swiftCode)
        GatewayMessage._addNode(doc, root, 'UniqueRef', uniqueRef)
        GatewayMessage._addNode(doc, root, 'SubSystemID', subSystemId)
        GatewayMessage._addNode(doc, root, 'SubSystemUser', subSystemUser)
        GatewayMessage._addNode(doc, root, 'SwiftType', swiftType)
        GatewayMessage._addNode(doc, root, 'MsgType', msgType)
        GatewayMessage._addNode(doc, root, 'MsgFormat', msgFormat)
        GatewayMessage._addNode(doc, root, 'MsgDetails', msgDetails)
        
        self._doc = doc
    
    def __str__(self):
        return self._doc.toxml('UTF-8')
        
class FrontGatewayMessage(GatewayMessage):
    
    def __init__(self, swiftCode, uniqueRef, subSystemId, swiftType, msgType, msgFormat, msgDetails):
        sourceSystem = 'FrontArena'
        timeStamp = time.strftime('%Y-%m-%d %H:%M:%S')
        subSystemUser = acm.User().Name()
        GatewayMessage.__init__(self, sourceSystem, timeStamp, swiftCode, uniqueRef, subSystemId, subSystemUser, swiftType, msgType, msgFormat, msgDetails)
