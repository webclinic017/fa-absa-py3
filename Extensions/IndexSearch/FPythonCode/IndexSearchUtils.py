
import acm




def log(message):
    if acm.IsUnicodeEnabled() :
        message = message.encode('utf-8')
    else:
        message = message.encode('latin-1')

    log_category = 'pace task - IndexSearch'

    if acm.LogStatus(log_category):
        acm.LogAll(message)

def get_encoding(encoding = None) :
    if not encoding :
        if acm.IsUnicodeEnabled() :
            encoding = 'utf-8'
        else:
            encoding = 'latin-1'

    return encoding

def unicode_decode(s, encoding = None) :
    try :
        if not isinstance(s, basestring):
            s = str(s)
        encoding = get_encoding(encoding)
        s = s.decode(encoding)
    except Exception as er:
        print (er, s)

    return s


def unicode_encode(s, encoding = None) :
    try :
        if not isinstance(s, basestring):
            s = str(s)
        encoding = get_encoding(encoding)
        s = s.encode(encoding)
    except Exception as er:
        print (er, s)

    return s


def safe_name(obj) :
    name = ''
    if obj and hasattr(obj, 'Name'):
        name = str(obj.Name())

    return name
