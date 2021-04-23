'''
# Python module created for the upload of SDS ID's from Midbase/BarCap into Front Arena
#2008-04-23

Purpose:    Add check to see if party exists
            Put the commits on the updates in a transaction blcok so the version number goes up by 1 only
Department: IT, IT
Requester:  Heinrich Cronje, Matthew Berry
Developer:  Jaysen Naicker, Jaysen Naicker
CR Number:  480986 (04/11/2010), 516748 (06/12/2010)
'''

import ael, string

#Main
def ael_main(ael_dict):

    FileLocation = ael_dict["FileLocation"]

    Upload_SDS(1, FileLocation)

ael_variables = [('FileLocation', 'FileLocation', 'string', None, '//services/frontnt/BackOffice/Atlas-End-Of-Day/', 1)]


def Upload_SDS(temp,FileLocation,*rest):

    print FileLocation
    try:
        SDSFile = open(FileLocation, 'r')
    except:
        print 'SDS file does not exist'
        return
        
    line = SDSFile.readline()
    line = SDSFile.readline()
    records = []
    fail_list = []
    count = 0
    
    CP_spec = ael.AdditionalInfoSpec["BarCap_SMS_CP_SDSID"]
    LE_spec = ael.AdditionalInfoSpec["BarCap_SMS_LE_SDSID"]
    Eagle_Incl_spec = ael.AdditionalInfoSpec["BarCap_Eagle_Incl"]
    Eagle_SDS_spec = ael.AdditionalInfoSpec["BarCap_Eagle_SDSID"]
        
    while line:
        CP_AddInfo=0
        LE_AddInfo=0
        Incl_AddInfo=0
        Eagle_SDS_AddInfo=0
        
        #Insert the records into the list
        records = line.rstrip().split('|')
        
        #Assign the first party to a temp variable
        number = records[0]
        
        #Get the associated party
        FAParty = ael.Party[(int)(number)]
        
        if FAParty:

            #Clone the party entity
            try:
                party_clone = FAParty.clone()
            
                #Get all the additional info attributes against the party
                AIS = party_clone.additional_infos()
                a_CP = None
                a_LE = None
                a_Inc = None
                a_Eagle_SDS = None
                
                for ai in AIS:
                    if ai.addinf_specnbr.field_name == 'BarCap_SMS_CP_SDSID':
                        a_CP = ai
            
                    if ai.addinf_specnbr.field_name == 'BarCap_SMS_LE_SDSID':
                        a_LE = ai
                        
                    if ai.addinf_specnbr.field_name == 'BarCap_Eagle_Incl':
                        a_Inc = ai
            
                    if ai.addinf_specnbr.field_name == 'BarCap_Eagle_SDSID':
                        a_Eagle_SDS = ai
            
            
            
                #Assign the Additional info for all counterparties
                if len(records)>1 and records[1]:
                    if a_CP == None:
                        CP_AddInfo = ael.AdditionalInfo.new(party_clone)
                        CP_AddInfo.addinf_specnbr = CP_spec
                        CP_AddInfo.value = records[1]
                    elif records[1] != a_CP.value:
                        CP_AddInfo = a_CP.clone()
                        CP_AddInfo.value = records[1]
                elif a_CP:
                    a_CP.delete()


                #Assign the Additional info for all Legal Entities

                if len(records)>2 and records[2]:
                    if a_LE == None:
                        LE_AddInfo = ael.AdditionalInfo.new(party_clone)
                        LE_AddInfo.addinf_specnbr = LE_spec
                        LE_AddInfo.value = records[2]
                    elif records[2] != a_LE.value:
                        LE_AddInfo = a_LE.clone()
                        LE_AddInfo.value = records[2]
                elif a_LE:
                    a_LE.delete()

                #Assign the Additional info for all include flags
                if len(records)>3 and records[3] == '1':
                    if a_Inc == None:
                        Incl_AddInfo = ael.AdditionalInfo.new(party_clone)
                        Incl_AddInfo.addinf_specnbr = Eagle_Incl_spec
                        Incl_AddInfo.value = 'Yes'
                    elif a_Inc.value != 'Yes':
                        Incl_AddInfo = a_Inc.clone()
                        Incl_AddInfo.value = 'Yes'
                else:
                    if a_Inc == None:
                        Incl_AddInfo = ael.AdditionalInfo.new(party_clone)
                        Incl_AddInfo.addinf_specnbr = Eagle_Incl_spec
                        Incl_AddInfo.value = 'No'
                    elif a_Inc.value != 'No':
                        Incl_AddInfo = a_Inc.clone()
                        Incl_AddInfo.value = 'No'

                #Assign the Additional info for all Eagle SDS flags
                if len(records)>4 and records[4]:
                    if a_Eagle_SDS == None:
                        Eagle_SDS_AddInfo = ael.AdditionalInfo.new(party_clone)
                        Eagle_SDS_AddInfo.addinf_specnbr = Eagle_SDS_spec
                        Eagle_SDS_AddInfo.value = records[4]
   
                    elif records[4] != a_Eagle_SDS.value:
                        Eagle_SDS_AddInfo = a_Eagle_SDS.clone()
                        Eagle_SDS_AddInfo.value = records[4]

                elif a_Eagle_SDS:
                    a_Eagle_SDS.delete()
                
                try:
                    ael.begin_transaction()
                    if CP_AddInfo:
                        CP_AddInfo.commit()
                    if LE_AddInfo:
                        LE_AddInfo.commit()
                    if Incl_AddInfo:
                        Incl_AddInfo.commit()
                    if Eagle_SDS_AddInfo:
                        Eagle_SDS_AddInfo.commit()
                    ael.commit_transaction()
                except:
                    ael.abort_transaction()

                line = SDSFile.readline()
            
            except Exception, e:
                print e, line
                line = SDSFile.readline()
        else:
            line = SDSFile.readline()
            

    SDSFile.close()
