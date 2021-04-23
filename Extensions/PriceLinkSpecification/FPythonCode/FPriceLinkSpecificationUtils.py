""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/price_link_specification/etc/FPriceLinkSpecificationUtils.py"
import acm

SYMBOL_PLUSMINUS = chr(177)

class ButtonOptions:
    OKAY   = "Button1"
    CANCEL = "Button2"

def ValidateTime(timeValue):
    if not timeValue:
        return

    if timeValue == '-1':
        return

    value = timeValue.replace('.', ':')
    if len(value.split(':')) > 2:
        raise ValueError('Please enter time in valid format!')

    value = value.replace(':', '')
    if value.startswith('-'):
        raise ValueError('Please enter only positive values!')

    if not value.isdigit():
        raise ValueError('Please enter only positive integer values!')

    if len(value) > 4:
        raise ValueError('Please enter time in valid format!')

    value = int(value)
    HH = int(value)/100
    MM = int(value)%100
    if HH > 23 or MM > 59:
        raise ValueError('Time should be less than or equal to 23:59!')

def TimeToInt(timeValue):
    """converts time in integer format and returns -1 if blank"""
    if not timeValue:
        return -1

    if timeValue == '-1':
        return -1

    value = timeValue.replace('.', ':').split(":")
    if len(value) == 2:
        value = int(value[0])*60 + int(value[1])
    else:
        value = value[0].zfill(4)
        value = int(value[:2])*60 + int(value[2:])
    return value

def ValidateStartTime(startTime):
    try:
        ValidateTime(startTime)
    except ValueError as e:
        msg = 'Invalid Start Time. \n'
        e.args = (msg + str(e.args[0]),)
        raise

def ValidateStopTime(stopTime):
    try:
        ValidateTime(stopTime)
    except ValueError as e:
        msg = 'Invalid Stop Time. \n'
        e.args = (msg + str(e.args[0]),)
        raise

def isfloat(value):
  try:
    float(value)
    return True
  except ValueError:
    return False

def ValidateUpdateInterval(updateInterval):
    if not updateInterval:
        return

    if updateInterval != '-1':
        if not isfloat(updateInterval):
            message = "Invalid Update Interval, please enter time in sec or in millisecond (e.g. 0.001). \n" \
                    + "Enter decimal value or '-1' to use default from price distributor!"
            raise ValueError(message)

def ValidateAdditionAddend(additionAddend):
    if not additionAddend:
        return

    try:
        float(additionAddend)
    except ValueError as e:
        raise ValueError("Invalid entry, enter only integer or float value in Addition Addend!")

def ValidateMultiplicationFactor(multiplicationFactor):
    if not multiplicationFactor:
        return

    try:
        float(multiplicationFactor)
    except ValueError as e:
        raise ValueError("Invalid entry, enter only integer or float value in Multiplication Factor!")

def IntToTime(time_val):
    """returns time in proper display format"""
    if(-1 == time_val):
        return ""
    hours = minutes = time_hm = ""
    hours = str(int(time_val)/60)
    hours = hours.zfill(2)
    minutes = str(int(time_val)%60)
    minutes = minutes.zfill(2)
    time_hm = hours + ":" + minutes
    return time_hm

def ValidateUTCTime(timeValue):
    sign = +1
    value = timeValue
    if timeValue.startswith(('-', '+')):
        value = timeValue[1:]
        if timeValue.startswith('-'):
            sign = -1

    message = "%sHH:MM '%s' in UTC Offset is invalid, " % (SYMBOL_PLUSMINUS, timeValue)\
        + 'Please enter a valid time in the range -12:00 to +13:00, where MM is less than 59'

    value = value.replace('.', ':')
    if len(value.split(':')) > 2:
        raise ValueError(message)

    value = value.replace(':', '')
    if not value.isdigit():
        raise ValueError('Please enter integer value for UTC Offset!')

    if len(value) > 4:
        raise ValueError(message)

    value = int(value)
    HH = int(value)/100
    HH = sign * HH
    MM = int(value)%100

    if not( -12 <= HH <= 13):
        raise ValueError(message)

    if HH in (-12, 13) and MM > 0:
        raise ValueError(message)
    elif MM > 59:
        raise ValueError(message)


def UTCTimeToInt(timeValue):
    sign = '+'
    value = timeValue
    if timeValue[0] in ('-', '+'):
        sign = timeValue[0]
        value = timeValue[1:]

    value = value.replace('.', ':').split(":")
    if len(value) == 2:
        value = int(value[0].zfill(4))*100 + int(value[1].zfill(2))
    else:
        value = value[0].zfill(4)
        value = int(value[:2])*100 + int(value[2:])

    if sign == '-':
        value = value * -1

    return value

def IntToUTCTime(time_val):
    """returns time in proper display format"""
    sign = ''
    time_val = str(time_val)
    if '-' in time_val:
        sign = '-'
        time_val = time_val.replace('-', '')
    hours = minutes = time_hm = ""
    hours = str(int(time_val)/100)
    hours = hours.zfill(2)
    minutes = str(int(time_val)%100)
    minutes = minutes.zfill(2)
    time_hm = sign + hours + ":" + minutes
    return time_hm

def BinaryToDecimal(number):
    binarylist = list(number)
    no = len(binarylist)
    no = no -1
    diginum = 0
    i = 0
    while no > -1:
        if binarylist[no] == '1':
            kj = 2**i
            diginum = diginum + kj
        no = no -1
        i = i +1
    return diginum

def DecimalToBinary(number, numdigits):
    base = 2
    binary_list = []
    digits = [0 for i in range(numdigits)]
    for i in range(numdigits):
        number, digits[i] = divmod(number, base)
    for i in reversed(digits):
        binary_list.append(i)
    return binary_list

def NegativeToBlank(value):
    if value == -1:
        value = ""
    return value

def ZeroToBlank(value):
    if value == 0:
        value = ""
    return value

def OneToBlank(value):
    if value == 1:
        value = ""
    return value

def NoneToBlank(value):
    if value == 'None':
        value = ""
    return value

def BlankToNone(value):
    if value == '':
        value = None
    return value

def ValidateBooleanValue(value):
    if value in ('', None):
        value = 'None'
    return value