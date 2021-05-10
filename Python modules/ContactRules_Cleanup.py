import ael

def Party(temp,PartyID,*rest):

    p_clone = ael.Party[PartyID].clone()
    p_contacts = p_clone.contacts()


    for c in p_contacts:

        ContactRule = c.rules()
     
        for cr in ContactRule:
            ChoiceList = cr.event_chlnbr
            if not ChoiceList:
                cr.delete()

    p_clone.commit()
    ael.poll()
    return str(PartyID)
