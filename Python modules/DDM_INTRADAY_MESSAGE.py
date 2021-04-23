'''----------------------------------------------------------------------------------------------------------
MODULE                  :       DDM_INTRADAY_MESSAGE
PROJECT                 :       (Pegasus) Data Distribution Model - ATS
PURPOSE                 :       This module defines a intraday message for report generation 
                                
DEPARTMENT AND DESK     :       PCG Change
REQUASTER               :       Pegasus Project
DEVELOPER               :       Heinrich Momberg/Heinrich Cronje
CR NUMBER               :       TBA
-------------------------------------------------------------------------------------------------------------
'''
from AMBA_Helper_Functions import AMBA_Helper_Functions as ambaUtils

class DDM_INTRADAY_MESSAGE():

    #local members
    source = None
    type = None
    time = None
    txNbr = 0
    tradeNumber = 0
    instrumentAddress = 0
    
    #********************************************************************************************************
    # Class Constructor
    #******************************************************************************************************** 
    def __init__(self, msg):
        try:
            #Fetch the source attribute on the message
            self.source = ambaUtils.get_AMBA_Object_Value(msg, 'SOURCE')
            if not self.source:
                raise Exception('SOURCE tag not found')
                
            #Fetch the type attribute on the message
            self.type = ambaUtils.get_AMBA_Object_Value(msg, 'TYPE')
            if not self.type:
                raise Exception('TYPE tag not found')
               
            #Fetch the type attribute on the message
            self.txNbr = ambaUtils.get_AMBA_Object_Value(msg, 'TXNBR')
             
            #Fetch the time attribute on the message
            self.time = ambaUtils.get_AMBA_Object_Value(msg, 'TIME')
            if not self.time:
                raise Exception('TIME tag not found')
                
            
            #Fetch the trade tag
            tradeTag = ambaUtils.object_by_name(msg, ['', '!', '+'], 'TRADE')
            if tradeTag:
                self.instrumentAddress = ambaUtils.get_AMBA_Object_Value(tradeTag, 'INSADDR')
                self.tradeNumber = ambaUtils.get_AMBA_Object_Value(tradeTag, 'TRDNBR')
                        
            #Fetch the instrument tag
            instrumentTag = ambaUtils.object_by_name(msg, ['', '!', '+'], 'INSTRUMENT')
            if instrumentTag:
                self.instrumentAddress = ambaUtils.get_AMBA_Object_Value(instrumentTag, 'INSADDR')
                self.tradeNumber = 0
                
         
                
           
            
        except Exception, e:
            raise Exception('Could not create the intraday message. %s' % str(e))
