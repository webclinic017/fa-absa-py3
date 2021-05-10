import ael

def TelLength(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.telephone:
        if len(p.telephone) != 12:
            return 1
        else:
            return 0
    else:
        return 0

def TelDialingCode(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.telephone:
        if p.telephone[0:3] != '+27':
            return 1
        else:
            return 0
    else:
        return 0

def TelSpecialChar(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.telephone:
        if not p.telephone[1:].isdigit():
            return 1
        else:
            return 0
    else:
        return 0

def FaxLength(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.fax:
        if len(p.fax) != 12:
            return 1
        else:
            return 0
    else:
        return 0

def FaxDialingCode(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.fax:
        if p.fax[0:3] != '+27':
            return 1
        else:
            return 0
    else:
        return 0

def FaxSpecialChar(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.fax:
        if not p.fax[1:].isdigit():
            return 1
        else:
            return 0
    else:
        return 0

def ZipLength(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.address and p.zipcode:
        if len(p.zipcode) != 4:
            return 1
        else:
            return 0
    else:
        return 0

def ZipSpecialChar(temp,ptynbr,*rest):
    p = ael.Party[ptynbr]
    if p.address and p.zipcode:
        if not p.zipcode.isdigit():
            return 1
        else:
            return 0
    else:
        return 0

def EmailOneAtSign(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.email:
        count = 0
        i = 0
        while i < len(p.email):
            if p.email[i] == '@':
                count = count + 1
            i = i + 1
        if count == 0:
            return 1
        else:
            return 0
    else:
        return 0

def EmailCharBeforeAt(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.email:
        if p.email[0] == '@':
            return 1
        else:
            return 0
    else:
        return 0

def EmailFullAfterAt(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.email:
        i = 0
        count = 0
        while i < len(p.email):
            if p.email[i] == '@':
                j = i
                while j < len(p.email):
                    if p.email[j] == '.':
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

def EmailEndFullstop(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.email:
        if p.email[len(p.email) - 1] == '.':
            return 1
        else:
            return 0
    else:
        return 0

def EmailEndAtSign(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.email:
        if p.email[len(p.email) - 1] == '@':
            return 1
        else:
            return 0
    else:
        return 0


def Fullname(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if not p.fullname:
        return 1
    else:
        return 0

#def Attention(temp,ptynbr,*rest):
#    p = ael.Party[(int)(ptynbr)]
#    if not p.attention:
#        return 1
#    else:
#        return 0

def Address(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if not p.address and not p.address2:
        return 1        #No Address
    elif not p.address and p.address2:
        return 2        #Address 1 Missing
    else:
        return 0

def AddressZip(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if (p.address and not p.zipcode) or (not p.address and p.zipcode) or (not p.address and p.address2 and not p.zipcode):
        return 1        #I there is an address there must be a zipcode
    else:
        return 0
        
#def Address1Missing(temp,ptynbr,*rest):
#    p = ael.Party[(int)(ptynbr)]
#    if not p.address and p.address2:
#        return 1
#    else:
#        return 0

def City(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.address and not p.city:
        return 1
    else:
       return 0

def Country(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.address and not p.country:
        return 1
    else:
        return 0

def FaxAndEmail(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if not p.fax and not p.email:
        return 1
    else:
        return 0

def BisStatus(temp,ptynbr,*rest):
    p = ael.Party[(int)(ptynbr)]
    if p.bis_status != 'Other':
        return 1
    else:
        return 0
