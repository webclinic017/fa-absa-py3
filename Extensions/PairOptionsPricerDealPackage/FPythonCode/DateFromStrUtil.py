import acm
import re
import datetime
from traitlets import AttributeException

def AdjustToFirstValidYear(date):
    try:
        today = datetime.datetime.strptime(acm.Time().DateToday(), '%Y-%m-%d').date()
        date = date.replace(year=today.year)
        if today > date:
            date = date.replace(year=date.year + 1)
        return date
    except Exception as e:
        print (e)
    
def splitStr(inputStr):
    inputStr = inputStr.replace(' ', '')
    split = re.split('(\d+)', inputStr)
    for s in split:
        if s == '':
            split.remove(s)
    return split
    
def transformToDate(dateStr, dateFormat):
    date = None
    try:
        date = datetime.datetime.strptime(dateStr, dateFormat).date()
    except:
        pass
    return date

def toDate(inputStr):
    date = inputStr 
    split = splitStr(inputStr)
    formattedStr = ' '.join(split)
    if len(split) == 3:
        date = transformToDate(formattedStr, '%d %b %y')
        if date is None:
            date = transformToDate(formattedStr, '%d %b %Y')
        if date is None:
            date = transformToDate(formattedStr, '%d %B %y')
        if date is None:
            date = transformToDate(formattedStr, '%d %B %Y')   
    elif len(split) == 2:
        date = transformToDate(formattedStr, '%d %b')
        if date is None:
            date = transformToDate(formattedStr, '%d %B')
        date = AdjustToFirstValidYear(date)
    return date
    
def stringToDate(inputStr, attrName):
    date = None
    try:
        date = toDate(inputStr)
        if isinstance(date, datetime.date):
            date = str(date)
    except:
        pass
    return date

def InputIsValidDate(inputStr):
    validDate = True
    try:
        acm.GetDomain('datetime').ParseObject(inputStr)
    except:
        validDate = acm.Time().PeriodSymbolToDate(inputStr) != ''
        if validDate:
            #We might be a period - but could also be, e.g. 12maj, since the parser will treat this as 12m date period
            validDate = len(splitStr(inputStr)[1]) < 2
    return validDate
    
def TransformExpiryInputStrToDate(inputStr, attrName):
    date = inputStr
    if not InputIsValidDate(inputStr):
        date = stringToDate(inputStr, attrName)
        
        if date is None:
            raise AttributeException(attrName, " value " + inputStr + " not valid in domain date")
    return date
    
