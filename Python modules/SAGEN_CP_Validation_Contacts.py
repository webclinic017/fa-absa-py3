import ael

def name(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            for cr in c.rules():
                if cr.event_chlnbr.entry == 'Money Market' and cr.instype == 'Deposit' and cr.curr.insid == 'ZAR':
                    if c.fullname != 'MM/Dep/Z/' + c.attention:
                        return 1
    return 0
                
def attention(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.attention:
                return 1
            else:
                return 0

def address2none(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.address and c.address2:
                return 1
            else:
                return 0

def addresszip(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.address and not c.zipcode:
                return 1
            else:
                return 0

def ziplength(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.address and c.zipcode:
                if len(c.zipcode) != 4:
                    return 1
                else:
                    return 0
            else:
                return 0

def zipspecialchar(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.address and c.zipcode:
                if not c.zipcode.isdigit():
                    return 1
                else:
                    return 0
            else:
                return 0
    
def faxandaddress(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.fax and not c.address:
                return 1
            else:
                return 0

def city(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.address and not c.city:
                return 1
            else:
               return 0

def country(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.address and not c.country:
                return 1
            else:
                return 0

def tellength(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.telephone:
                if len(c.telephone) != 12:
                    return 1
                else:
                    return 0
            else:
                return 0
                
def teldialingcode(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.telephone:
                if c.telephone[0:3] != '+27':
                    return 1
                else:
                    return 0
            else:
                return 0
                
def telspecialchar(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.telephone:
                if not c.telephone[1:].isdigit():
                    return 1
                else:
                    return 0
            else:
                return 0

def faxlength(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.fax:
                if len(c.fax) != 12:
                    return 1
                else:
                    return 0
            else:
                return 0
                
def faxdialingcode(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.fax:
                if c.fax[0:3] != '+27':
                    return 1
                else:
                    return 0
            else:
                return 0
                
def faxspecialchar(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.fax:
                if not c.fax[1:].isdigit():
                    return 1
                else:
                    return 0
            else:
                return 0

def emailoneatsign(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.email:
                count = 0
                i = 0
                while i < len(c.email):
                    if c.email[i] == '@':
                        count = count + 1
                    i = i + 1
                if count == 0:
                    return 1
                else:
                    return 0
            else:
                return 0

def emailcharbeforeat(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.email:
                if c.email[0] == '@':
                    return 1
                else:
                    return 0
            else:
                return 0

def emailfullafterat(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.email:
                i = 0
                count = 0
                while i < len(c.email):
                    if c.email[i] == '@':
                        j = i
                        while j < len(c.email):
                            if c.email[j] == '.':
                                count = count + 1
                            j = j + 1
                        if count == 0:
                            return 1
                            break
                        else:
                            return 0
                            break
                    i = i + 1
            return 0

def emailendfullstop(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.email:
                if c.email[len(c.email) - 1] == '.':
                    return 1
                else:
                    return 0
            else:
                return 0

def emailendatsign(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.email:
                if c.email[len(c.email) - 1] == '@':
                    return 1
                else:
                    return 0
            else:
                return 0

def commfreqemail(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.email:
                return 1
            else:
                return 0

def commfreqfax(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.fax:
                return 1
            else:
                return 0

def commfreqemailfax(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.fax or not c.email:
                return 1
            else:
                return 0

def commfreqprint(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.address or not c.zipcode:
                return 1
            else:
                return 0

def commfreqprintfax(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.fax or not c.address or not c.zipcode:
                return 1
            else:
                return 0

def commfreqprintemail(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.email or not c.address or not c.zipcode:
                return 1
            else:
                return 0

def commfreqall(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if not c.fax or not c.email or not c.address or not c.zipcode:
                return 1
            else:
                return 0

def commfreqdaily(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.add_info('Comm Type - Daily') == 'All':
                return commfreqall(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Email':
                return commfreqemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Email, Print':
                return commfreqprintemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Fax':
                return commfreqfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Fax, Email':
                return commfreqemailfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Fax, Print':
                return commfreqprintfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Daily') == 'Print':
                return commfreqprint(temp, ptynbr, seqnbr)
            else:
                return 0

def commfreqmonthly(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.add_info('Comm Type - Monthly') == 'All':
                return commfreqall(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Email':
                return commfreqemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Email, Print':
                return commfreqprintemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Fax':
                return commfreqfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Fax, Email':
                return commfreqemailfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Fax, Print':
                return commfreqprintfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Monthly') == 'Print':
                return commfreqprint(temp, ptynbr, seqnbr)
            else:
                return 0

def commfreqweekly(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            if c.add_info('Comm Type - Weekly') == 'All':
                return commfreqall(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Email':
                return commfreqemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Email, Print':
                return commfreqprintemail(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Fax':
                return commfreqfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Fax, Email':
                return commfreqemailfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Fax, Print':
                return commfreqprintfax(temp, ptynbr, seqnbr)
            elif c.add_info('Comm Type - Weekly') == 'Print':
                return commfreqprint(temp, ptynbr, seqnbr)
            else:
                return 0

def andsignaddress(temp,ptynbr,seqnbr,*rest):
    p = ael.Party[ptynbr]
    for c in p.contacts():
        if c.seqnbr == seqnbr:
            i = 0
            error = 0
            if c.address:
                while i < len(c.address):
                    if c.address[i] == '&':
                        error = 1
                    i = i + 1
            if error:
                return 1
            else:
                return 0
