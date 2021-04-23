import ael, time, SAGEN_str_functions

def time_to_string(temp,*rest):

    Hour = time.strftime('%H')
    Minute = time.strftime('%M')
    Seconds = time.strftime('%S')
    
    if Hour > '0' and Hour < '10':
        Hour = '0' + Hour
        #print Hour
    elif Minute > '0' and Minute < '10':
        Minute = '0' + Minute
        #print Minute
    elif Seconds > '0' and Seconds < '10':
        Seconds = Seconds
        #print Seconds
    #else:
        #print Hour + Minute + Seconds
    return Hour + Minute + Seconds + '00'


def build_rate_string(temp,rate,*rest):

    if rate != '0':
        Whole = SAGEN_str_functions.split_string(1, rate, '.', 0)
        Decimal = SAGEN_str_functions.split_string(1, rate, '.', 1)
        
        if len(Whole) == 1:
            Whole = '00' + Whole
        elif len(Whole) == 2:
            Whole = '0' + Whole
        else:
            Whole
        
        if  len(Decimal) == 1:
            Decimal = Decimal + '000'
        elif len(Decimal) == 2:
            Decimal = Decimal + '00'
        elif len(Decimal) == 3:
            Decimal = Decimal + '0'
        else:
            Decimal
    else:
        Whole = '000'
        Decimal = '0000'
    
    
    return Whole + Decimal

