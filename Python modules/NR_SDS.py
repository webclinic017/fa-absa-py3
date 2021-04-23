# Python module created for the upload of SDS ID's from Midbase/BarCap into Front Arena
#2008-04-23

import ael, string

#Main
def ael_main(ael_dict):

    FileLoc = ael_dict["FileLocation"]
    Upload_SDS(FileLoc)

ael_variables = [('FileLocation', 'FileLocation', 'string', None, '//services/frontnt/BackOffice/Atlas-End-Of-Day/', 1)]   


def Upload_SDS(FileLocation,*rest):

    try:
    
        SDSFile = open(FileLocation, 'r')
    except:
        print 'SDS file does not exist'
        
        
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
        
            #Insert the records into the list
            records = line.rstrip().split('|')
            
            #Assign the first party to a temp variable
            number = records[0]
            
            
            #Get the associated party
            FAParty = ael.Party[(int)(number)]
        
            #Clone the party entity
            try:
                party_clone = FAParty.clone()
            
                #Get all the additional info attributes against the party
                AIS = FAParty.additional_infos()
                CP_flag = 'no'
                LE_flag = 'no'
                Inc_Flag = 'no'
                Eagle_SDS_Flag = 'no'
                
                
                for ai in AIS:
                    if ai.addinf_specnbr.field_name == 'BarCap_SMS_CP_SDSID':
                        CP_flag = 'Yes'
                        a_CP = ai
            
                    if ai.addinf_specnbr.field_name == 'BarCap_SMS_LE_SDSID':
                        LE_flag = 'yes'
                        a_LE = ai
                        
                    if ai.addinf_specnbr.field_name == 'BarCap_Eagle_Incl':
                        Inc_Flag = 'Yes'
                        a_Inc = ai
            
                    if ai.addinf_specnbr.field_name == 'BarCap_Eagle_SDSID':
                        Eagle_SDS_Flag = 'yes'
                        a_Eagle_SDS = ai
            
            
            
                #Assign the Additional info for all counterparties
                if CP_flag == 'no':
                    CP_AddInfo = ael.AdditionalInfo.new(party_clone)
                    CP_AddInfo.addinf_specnbr = CP_spec
                    
                    if records[1] != '':
                        CP_AddInfo.value = records[1]
                    else:
                        CP_AddInfo.value = ' '
                else:
                    CP_AddInfo = a_CP.clone()
                    
                    if records[1] != '':
                        CP_AddInfo.value = records[1]
                    else:
                        CP_AddInfo.value = ' '
            
                #Assign the Additional info for all Legal Entities
                if LE_flag == 'no':
                    LE_AddInfo = ael.AdditionalInfo.new(party_clone)
                    LE_AddInfo.addinf_specnbr = LE_spec
                    
                    if records[2] != '':
                        LE_AddInfo.value = records[2]
                    else:
                        LE_AddInfo.value = ' '
                else:
                    LE_AddInfo = a_LE.clone()
                    
                    if records[2] != '':
                        LE_AddInfo.value = records[2]
                    else:
                        LE_AddInfo.value = ' '
                    
                #Assign the Additional info for all include flags
                if Inc_Flag == 'no':
                    Incl_AddInfo = ael.AdditionalInfo.new(party_clone)
                    Incl_AddInfo.addinf_specnbr = Eagle_Incl_spec
                    
                    if records[3] == '1':
                        Incl_AddInfo.value = 'Yes'
                    else:
                        Incl_AddInfo.value = 'No'
                else:
                    Incl_AddInfo = a_Inc.clone()
                    
                    if records[3] == '1':
                        Incl_AddInfo.value = 'Yes'
                    else:
                        Incl_AddInfo.value = 'No'
            
                #Assign the Additional info for all Eagle SDS flags
                if Eagle_SDS_Flag == 'no':
                    Eagle_SDS_AddInfo = ael.AdditionalInfo.new(party_clone)
                    Eagle_SDS_AddInfo.addinf_specnbr = Eagle_SDS_spec
                    
                    if records[4] != '':
                        Eagle_SDS_AddInfo.value = records[4]
                    else:
                        Eagle_SDS_AddInfo.value = ' '
                else:
                    Eagle_SDS_AddInfo = a_Eagle_SDS.clone()
                    
                    if records[4] != '':
                        Eagle_SDS_AddInfo.value = records[4]
                    else:
                        Eagle_SDS_AddInfo.value = ' '
            
                CP_AddInfo.commit()
                LE_AddInfo.commit()
                Incl_AddInfo.commit()
                Eagle_SDS_AddInfo.commit()
                
                count = count + 1
            
                line = SDSFile.readline()
        
            except:
                line = SDSFile.readline()
                    
        SDSFile.close()
