import ael

try:
     fr = open('C:\\CounterpartiesToRestore\Front_Party_Filtered_List.csv')
except:
     print 'Input file could not be opened'

try:
    fo = open('C:\\CounterpartiesToRestore\Counterparty_Detail_Restored.csv', 'w')
except:
    print 'Output file could not be opened'


Line = fr.readline()
Line = fr.readline()
List = []

while Line:
    
    List = Line.split(',')
    
    NewP = ael.Party.new()

    NewP.creat_time = ael.date_from_string(List[0][0:10]).to_time()
    NewP.creat_usrnbr = ael.User[(int)(List[1])]
    NewP.updat_time = ael.date_from_string(List[2][0:10]).to_time()
    NewP.updat_usrnbr = ael.User[(int)(List[3])]
#    NewP.protection = List[4]
    NewP.owner_usrnbr = ael.User[(int)(List[5])]
#    NewP.four_eye_on = List[6]
    NewP.authorizer_usrnbr = ael.User[(int)(List[7])]
#    NewP.version_id = (int)(List[8])
#    NewP.ptynbr = int(List[9])
    NewP.ptyid = List[10]
#    NewP.red_code = List[11]
    NewP.parent_ptynbr = ael.Party[(int)(List[12])]
    NewP.guarantor_ptynbr = ael.Party[(int)(List[13])]
    NewP.type = List[14]
    NewP.fullname = List[15]
#    NewP.fullname2 = List[16]
    NewP.attention = List[17]
    NewP.address = List[18]
    NewP.address2 = List[19]
    NewP.zipcode = List[20]
    NewP.city = List[21]
    NewP.country = List[22]
    NewP.telephone = List[23]
#    NewP.fax = List[24]
#    NewP.telex = List[25]
#    NewP.swift = List[26]
#    NewP.contact1 = List[27]
#    NewP.contact2 = List[28]
#    NewP.free1 = List[29]
#    NewP.free2 = List[30]
#    NewP.free3 = List[31]
#    NewP.free4 = List[32]
#    NewP.free5 = List[33]
    NewP.bis_status = List[34]
#    NewP.business_status_chlnbr = (int)(List[35])
    NewP.relation_chlnbr = ael.ChoiceList[(int)(List[36])]
#    NewP.legal_form_chlnbr = (int)(List[37])
    NewP.document_type_chlnbr = ael.ChoiceList[(int)(List[38])]
#    NewP.document_date = ael.date_from_string(List[39][0:10]).to_time()
    NewP.rating_agency_chlnbr = ael.ChoiceList[(int)(List[40])]
    NewP.rating_chlnbr = ael.ChoiceList[(int)(List[41])]
#    NewP.rating_date = ael.date_from_string(List[42][0:10]).to_time()
    NewP.user_rating_chlnbr = ael.ChoiceList[(int)(List[43])]
#    NewP.isda_member = List[44]
#    NewP.group_limit = List[45]
#    NewP.hostid = List[46]
#    NewP.netting = List[47]
#    NewP.free1_chlnbr = (int)(List[48])
#    NewP.free2_chlnbr = (int)(List[49])
#    NewP.free3_chlnbr = (int)(List[50])
#    NewP.free4_chlnbr = (int)(List[51])
#    NewP.ptyid2 = List[52]
#    NewP.rating1_chlnbr = (int)(List[53])
#    NewP.rating2_chlnbr = (int)(List[54])
#    NewP.rating3_chlnbr = (int)(List[55])
    NewP.risk_country_chlnbr = ael.ChoiceList[(int)(List[56])]
    NewP.issuer = 0
#    NewP.url = List[58]
#    NewP.free5_chlnbr = (int)(List[59])
    NewP.bankruptcy = 0
    NewP.obl_acceleration = 0
    NewP.obl_default = 0
    NewP.restructuring = 0
    NewP.repudiation = 0
    NewP.failure_to_pay = 0
    NewP.notify_receipt = 0
    NewP.internal_cutoff = 0
    NewP.external_cutoff = 0
#    NewP.time_zone = List[69]
    NewP.correspondent_bank = 0
#    NewP.email = List[71]
#    NewP.consolidate_chlnbr = (int)(List[72])
    NewP.price_access_control = 0
    NewP.not_trading = 0
    
    try:
        NewP.commit()
        ael.poll()
        print List[10], ' - CREATED'
        fo.write((str)(NewP.ptynbr) + ',' + List[10] + ',' + 'CREATED SUCCESSFULLY' + '\n')
    except:
        print List[10], ' - NOT CREATED'
        fo.write('' + ',' + List[10] + ',''NOT CREATED' + '\n')
    
    Line = fr.readline()

  
fr.close()
fo.close()

