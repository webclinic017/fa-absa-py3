import ael

def CDate(i,D,*rest):

 

            

   

    Month = D.to_string('%m')

    Year = D.to_string('%Y')
    
    Day = D.to_string('%d')

    YMD =  Year +  Month  + Day

    return YMD
    
def MinDate(i,D,*rest):
    d = '9999-01-01'
    for l in i.legs():
        if l.start_day < d:
            d = l.start_day
            
            Month = d.to_string('%m')

            Year = d.to_string('%Y')
    
            Day = d.to_string('%d')

            YMD =  Year +  Month  + Day    
        
    return YMD


def FXONbr(t,*rest):
    TNbr = t.trdnbr
    A = 'FXO'
    
    Output = A + str(TNbr)
    return Output    

def FXONbrB(t,*rest):
    TNbr = t.trdnbr
    A = 'FXO'
    B = 'B'
    Output = A + str(TNbr) + B
    return Output    



def EInst(t,*rest):
    
    Ins=  t.insaddr.insid
    
    T = t.trdnbr
    
    
    output = Ins + str(T)
    return output


def EqtPar(t,*rest):

    
    
    Und = t.insaddr.und_insaddr.insaddr
    Trdno = str(t.trdnbr)
    
    
    output = str(Und) + Trdno
    
    
    return output

def EqtLeg(t,lg,*rest):

    Ins = str(t.insaddr.insaddr)
    
    Trdno = str(t.trdnbr)
    z = ''
    legs = t.insaddr.legs()
    for l in legs:
        p = l.payleg
        if l.legnbr == lg:
            if p == 1:
                z = '1'
            else:
                z = '2'
        
    
    Output = Ins+Trdno+z
    
    return Output
    
