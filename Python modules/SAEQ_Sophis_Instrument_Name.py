import ael, string, math, SAGEN_str_functions

 

 

 

 

def real_round(number, dec):

    r = round(number, dec)

    if dec == 0:

        return str(int(r))

    else:

        str_dec = str(r - math.floor(r))

        zeros = dec + 2 - len(str_dec)

        return str(r) + zeros * '0' 

        

 

 

def InsName(i,request,*rest):

 

            

   

    Month = i.exp_day.to_string('%m')

    Year = i.exp_day.to_string('%y')

    MY =  Month + '/' + Year

    Strike = real_round(i.strike_price, 0)

    if request == 'Output':
        Und1 = i.und_insaddr.und_insaddr
    elif request == 'Ins3':
        Und1 = i.und_insaddr

    

    if i.call_option == 0:

        OType = 'P'

    else:

        OType = 'C'

    

    if Und1.instype == 'Stock':

        

        Ins1 = SAGEN_str_functions.split_string(1, Und1.insid, '/', 1) 
        Ins = SAGEN_str_functions.split_string(1, Ins1, '2', 0) + '0'
        Ins3 = SAGEN_str_functions.split_string(1, Ins1, '2', 0)
      

    else:

 

        if string.find(i.insid, 'ALSI') != -1:

            Ins = 'ALSI'
            Ins3 = 'ALSI'
    

        elif string.find(i.insid, 'DTOP') != -1:

            Ins = 'DTOP'
            Ins3 = 'DTOP'
    

        else:

    

            Ins = 'Not'
            Ins3 = 'Not'
 

    Output =  Ins + ' ' + MY + ' ' + OType + ' ' + Strike

            
    if request == 'Output':
        return Output
    elif request == 'Ins3':
        return Ins3
