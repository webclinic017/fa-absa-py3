'''----------------------------------------------------------------------------------------------------------
MODULE                  :       CBFETR_Message_Processing
PROJECT                 :       Cross Border Foreign Exchange Transaction Reporting
PURPOSE                 :       This module contains classes to process the incomming portfolio message as well
                                as the amendment of a field on an outgoing message.
DEPARTMENT AND DESK     :       Operations
REQUASTER               :       CBFETR Project
DEVELOPER               :       Heinrich Cronje
CR NUMBER               :       235281
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-02-22      235281          Heinrich Cronje                 Initial Implementation
2013-08-17      CHNG0001209844  Heinrich Cronje                 BOPCUS 3 Upgrade

-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

    CBFETR_AMBA_Message_Process :       This class will get the Portfolio ID and the Date of the incoming AMBA message.
    
    CBFETR_AMBA_Message_Amend   :       This class will amend a specified field on an AMBA message to a specified value.
'''

import acm
from AMBA_Helper_Functions import AMBA_Helper_Functions as AMBA_Utils

class CBFETR_AMBA_Message_Process():
    def __init__(self, message):
        self.AMBA_Message = message
        self.AMBA_Date = ''
        self.AMBA_Request_Id = None
        self.AMBA_Request_Type = None
        self.AMBA_Scope_Name = None

    def __del__(self):
        self.AMBA_Message = None
        self.AMBA_Date = None
        self.AMBA_Request_Id = None
        self.AMBA_Request_Type = None
        self.AMBA_Scope_Name = None

    def process_AMBA_Message(self):
        self.AMBA_Request_Id = AMBA_Utils.get_AMBA_Object_Value(self.AMBA_Message, 'REQUEST_ID')

        if not self.AMBA_Request_Id:
            raise Exception('No REQUEST_ID exist on the incomming AMBA Message.')
            
        dataTag = AMBA_Utils.object_by_name(self.AMBA_Message, [''], 'DATA')
        
        if not dataTag:
            raise Exception('No DATA Tag exist on the incomming AMBA Message.')
            
        portfolioTag = AMBA_Utils.object_by_name(dataTag, [''], 'PORTFOLIO')

        if portfolioTag:
            try:
                self.AMBA_Date = AMBA_Utils.get_AMBA_Object_Value(portfolioTag, 'DATE').strip()
                self.AMBA_Request_Type = 'PORTFOLIO_TRADES'
                self.AMBA_Scope_Name = AMBA_Utils.get_AMBA_Object_Value(portfolioTag, 'PRFID').strip()
            except:
                raise Exception('Data tags are missing on the incomming AMBA Message.')
        
        if not portfolioTag:
            instrumentTag = AMBA_Utils.object_by_name(dataTag, [''], 'INSTRUMENT')
            
            if instrumentTag:
                try:
                    self.AMBA_Scope_Name = AMBA_Utils.get_AMBA_Object_Value(instrumentTag, 'INSID').strip()
                    self.AMBA_Date = AMBA_Utils.get_AMBA_Object_Value(instrumentTag, 'DATE').strip()
                    self.AMBA_Request_Type = 'INSTRUMENT_TRADES'
                except:
                    raise Exception('Data tags are missing on the incomming AMBA Message.')
            
            if not instrumentTag:
                tradeTag = AMBA_Utils.object_by_name(dataTag, [''], 'TRADE')
                try:
                    self.AMBA_Scope_Name = AMBA_Utils.get_AMBA_Object_Value(tradeTag, 'TRDNBR').strip()
                    self.AMBA_Date = AMBA_Utils.get_AMBA_Object_Value(tradeTag, 'DATE').strip()
                    self.AMBA_Request_Type = 'SINGLE_TRADE'
                except:
                    raise Exception('Data tags are missing on the incomming AMBA Message.')
            
        if not (self.AMBA_Request_Type):
            raise Exception('There are data missing from the incoming AMBA Message.')

class CBFETR_AMBA_Message_Amend():
    def __init__(self, message, nodeList, field, value):
        self.AMBA_Message = message
        self.AMBA_Node_List = nodeList
        self.AMBA_Field = field
        self.AMBA_Value = value
        self.amend_AMBA_Message()
    
    def get_nodes(self, AMBA_Node_List, nextNode):
        list = acm.FArray()
        for node in AMBA_Node_List:
            for objects in AMBA_Utils.objects_by_name(node, [''], nextNode):
                list.Add(objects)
        return list
    
    def amend_AMBA_Message(self):
        new_msg = self.AMBA_Message
        AMBA_Node_List = [new_msg]
        for nodeLevel in self.AMBA_Node_List:
            AMBA_Node_List = self.get_nodes(AMBA_Node_List, nodeLevel)
        
        if AMBA_Node_List:
            for node in AMBA_Node_List:
                node.mbf_find_object(self.AMBA_Field, 'MBFE_BEGINNING')
                node.mbf_replace_string(self.AMBA_Field, self.AMBA_Value)

        self.AMBA_Message = new_msg
