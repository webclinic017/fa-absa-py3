#-----------------------------------------------------------------------------------------------------------------
#  Developer           : Tshepo Mabena
#  Purpose             : This module updates additional info's by reading the xml response message from Midas on
#                        the server. This serves as confirmation of the message received. The module is run by the
#                        windows service.
#  Department and Desk : Fx Desk
#  Requester           : Justin Nichols
#  CR Number           : CR 431665, CR 458129
#-----------------------------------------------------------------------------------------------------------------

import acm, amb, os, ael, sys, time, shutil
from FBDPCommon     import is_acm_object, acm_to_ael
from Midas_AddInfos import setAdditionalInfo, otherTrade

timeFormat = '%Y/%m/%d %H:%M:%S'
              
def Read_Message(msg, file_name):
    
    FA_ID        = msg.mbf_find_object('FA_ID').mbf_get_value()
    MIDAS_ID     = msg.mbf_find_object('MIDAS_ID').mbf_get_value()
    MIDAS_STATUS = msg.mbf_find_object('STATUS').mbf_get_value()
       
    findTrdnbr = FA_ID.find('_BTB')
       
    if findTrdnbr != -1:
        FA_ID = FA_ID[:findTrdnbr]
        ret   = 0
    else:
        FA_ID 
        ret   = 1
    
    t = acm.FTrade[int(FA_ID)]
    
    if ret == 1:
        Dict = {'Midas_ID':MIDAS_ID ,'Midas_Status':MIDAS_STATUS}
    else:    
        Dict = {'Midas_ID_BTB':MIDAS_ID ,'Midas_Status_BTB':MIDAS_STATUS}
  
    for addinfo in Dict.keys():
        
        try:
            if addinfo == 'Midas_ID' and Dict[addinfo] == '' or addinfo == 'Midas_ID_BTB' and Dict[addinfo] == '':
                Dict[addinfo] = 'NO MIDAS ID'
            
            # Fx Spot/Forward
            if t.TradeProcess() in (4096, 8192):  
                
                setAdditionalInfo(acm_to_ael(t), addinfo, Dict[addinfo])
                
            # Fx Swap    
            elif t.TradeProcess() in (16384, 32768):  
            
                trade = ael.Trade[int(t.Name())]
                
                setAdditionalInfo(trade, addinfo, Dict[addinfo])
                        
        except Exception, e:
            print e
  
def ProcessTradeXML(file_name):
   
    XMLMessage = file(file_name).read()
    Msg_Buffer = amb.mbf_create_buffer_from_data(XMLMessage)
    Midas_MSG  = Msg_Buffer.mbf_read()
    
    if Midas_MSG:
        Midas_MSG = Read_Message(Midas_MSG, file_name)
    
        # Moves response xml messages from midas into the archive folder 
        Source = "C:/MIDAS_INBOX"   
        Destination = "C:/MIDAS_ARCHIVE" + '/'+ ael.date_today().to_string('%Y.%m.%d')
        
        try: 
            if os.path.exists(Destination):
                Destination
            else:
                os.mkdir(Destination)
                
            shutil.move(file_name, Destination) 
           
        except Exception, e:
                print e   
  
def start():
 
    acm.Log('Startng additional info update at ' + time.strftime(timeFormat))

    while True:   
        try:
            rootdir = 'C:/MIDAS_INBOX/'
            for subdir, dirs, files in os.walk(rootdir):
                for file in files:
                    Outpath = rootdir + file
                    if os.path.isfile(Outpath):
                        ProcessTradeXML(Outpath)
        except Exception, e:
            print e
        time.sleep(15.0)

