#  SAGEN_str_funcitons : AEL module for string functions
#  Aaeda Salejee        2005-04-06
#  Hienrich Cronje      2007-04-17 Added function Substring
#  Kim Madeley          2011-11-26 Added CFR_str for the CFR project - used in la_curr- CR  C000000837458
#  Willie van der Bank  2012-07-05 Added error checking to get_CP_Portfolio CHNG0000302724

import ael, string, time


# splits a string into a list by the 'delimiter' and returns the 'index'    #
# member of the list.	    	    	    	    	    	    	    #
#   	    	    	    	    	    	    	    	    	    #
# used in the Tri-Optima query to extract the float ref index and rolling   #
# period from the float ref 'ZAR-JIBAR-3M' to get ['ZAR', 'JIBAR', '3M']    #

def split_string(temp, st, delimiter, index, *rest):
    list = st.split(delimiter)
    if index < len(list):
    	return list[index]
    else:
    	return 'Index out of range'


def getPartyENUM(temp, id, *rest):
    p = ael.Party[id]
    return ael.enum_from_string('PartyType', p.type)
    
    
def getInstypeENUM(temp, ins, *rest):
    try:
        i = ael.Instrument[ins]
        return ael.enum_from_string('InsType', i.instype)
    except:
        return 0


def concat(temp, str1, str2, str3, *rest):

    return str(str1) + str(str2) + str(str3)


def uppercase(temp, str1, *rest):
    return string.upper(str1)


def Safex_str(temp, st, *rest):
    st1 = split_string(1, st, '_', 0)
    st2 = split_string(1, st, '_', 1)
    st3 = split_string(1, st2, '/', 3)
    #print st, st2, last, d*/
    d = st2.rstrip(st3)
    d = d.rstrip('/')
    year = split_string(1, d, '/', 0).lstrip('20') + split_string(1, d, '/', 1) + split_string(1, d, '/', 2)
    #print year
    if len(year) == 5:
        year = '0' + year 
    final = 'SF_' + year + '/' + st3
    return final


def Substring (temp, st, start, num, *rest):
    if start > len(st):
        print('Starting Position to big')
        return 'Starting Position to big'
    elif num > len(st):
        return st
    else:
        return st[start:num]
 
 
#Build a list of all the exotic dates connected to an instrument
def Exotic_Build_Date_String(Instr,*rest):

    DateList = []
    
    #Get a list of all the dates in the events table    
    MonitorDates = Instr.exotic_events()
    
    #Get a distinct list of all the barrier dates in the events list 
    for dates in MonitorDates:
        if dates.type == 'Barrier date':
            if DateList.__contains__(dates.date) == 1:
                pass
            else:
                DateList.append(dates.date)
    
    #Sort the list in ascending order
    DateList.sort()
    
    DateLstStr = ''
    
    #Build the string with all the dates
    if DateList:
        for date in DateList:
            if date == DateList[0]:
                DateLstStr = DateLstStr + (str)(date)
            else:
                DateLstStr = DateLstStr + ',' + (str)(date)
        return DateLstStr
    else:
        return DateLstStr


def get_CP_Portfolio(t, *rest):
    if t.get_mirror_trade():
        y = t.get_mirror_trade().prfnbr.prfid
        return y
    else:
        return ''


def CFR_str(temp, st, *rest):
    st1 = st
    s = st1
    s = s.replace('2', '4')
    final = s
    return final
