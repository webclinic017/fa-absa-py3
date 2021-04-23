import ael, string, math, SAGEN_str_functions

def RP(temp, l, *rest):
    return l.rolling_period.count.__self__

def ResetPeriod(temp, l, *rest):
    return l.reset_period.count.__self__
    
def ResetIndex(temp, l, *rest):
    if l.type == 'Float':
        list = string.split(l.float_rate.insid, '-')
        return list[0] + '-' + list[1]
    else:
        return ''

def DifferenceRoll(temp, trade, *rest):
    
    s1 = trade.insaddr.legs()[0].rolling_period.count.__self__
    s2 = trade.insaddr.legs()[1].rolling_period.count.__self__
    x1 =len(s1)-1
    unit1 =  s1[x1]
    num1 = s1[0:x1]
    x2 =len(s2)-1
    unit2 =  s2[x2]
    num2 = s2[0:x2]
    if unit1 == unit2:
        diff = int(num1) - int(num2)
    else:
        diff = -1
    return diff
    

def RPUpper(temp, l, *rest):
    X = l.rolling_period.count.__self__
   
    
    U = SAGEN_str_functions.uppercase(1, X) 
    
    return U


    
#t = ael.Trade[1172185]
#print DifferenceRoll(3,t)
