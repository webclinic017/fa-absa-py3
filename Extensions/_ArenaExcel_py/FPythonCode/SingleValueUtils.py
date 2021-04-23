""" Compiled: 2020-09-18 10:38:52 """

#__src_file__ = "extensions/ArenaExcel/etc/SingleValueUtils.py"
import acm
import Contracts_Tk_Messages_TkEnumerations as TkEnum

from datetime import datetime


def ToUnicode(inputString):
    return unicode(inputString, 'cp1251')

def FromUnicode(inputString):
    return inputString.encode('ascii', 'ignore')
    
def Unpack(args, index):
    try:
        return FromUnicode(args[index])
    except IndexError:
        return None
        
        
class PaceVariant(object):
    
    @classmethod
    def Value(cls, variant):
        value_ = cls._Value(variant)
        if variant.type == TkEnum.PVT_DATETIME:
            return AcmVariant.DateTimeFromMs(value_)
        elif variant.type in (TkEnum.PVT_STRING, TkEnum.PVT_DATEPERIOD):
            return AcmVariant.AsString(value_)
        return value_
        
    @classmethod
    def _Value(cls, variant):
        fieldName = PaceVariantFieldConversion.FieldName(variant.type)
        return getattr(variant, fieldName)     
        

class AcmVariant(object):

    EPOCH = datetime(1970, 1, 1)
    SECONDS_IN_DAY = 24 * 3600
    DATE_FORMAT = '%Y-%m-%d %H:%M:%S'
    DATE_LENGTH = len(EPOCH.strftime(DATE_FORMAT))
    
    @classmethod
    def Value(cls, variant, domain=None):
        domain = domain or cls.ToDomain(variant)
        if domain is acm.FObject:
            return cls.ToUnicode(variant.StringKey())
        if domain is datetime:
            return cls.MsFromEpoch(variant)
        if domain is float:
            return float(variant)
        if domain is int:
            return int(variant)
        if domain is bool:
            return bool(variant)
        return variant
        
    @classmethod
    def ToDomain(cls, variant):
        if cls.IsDateTime(variant):
            return datetime
        if hasattr(variant, 'IsKindOf'):
            if variant.IsKindOf(acm.FReal):
                return float
            if variant.IsKindOf(acm.FBoolean):
                return bool
            if variant.IsKindOf(acm.FNumber):
                return int
            return acm.FObject
        return type(variant)
            
    @classmethod
    def DateTimeFromMs(cls, ms):       
        return datetime.fromtimestamp(ms/1000).strftime(cls.DATE_FORMAT)
            
    @classmethod
    def MsFromEpoch(cls, variant):       
        td = datetime.strptime(variant, cls.DATE_FORMAT) - cls.EPOCH
        return 1000 * (td.seconds + td.days * cls.SECONDS_IN_DAY)
            
    @classmethod
    def IsDateTime(cls, variant):
        try:
            return bool(isinstance(variant, basestring) and 
                len(variant) == cls.DATE_LENGTH and
                variant[4] == '-' and
                variant[7] == '-' and
                variant[13] == ':' and
                variant[16] == ':')
        except (TypeError, ValueError):
            return False
    
    @staticmethod
    def ToUnicode(inputString):
        return unicode(str(inputString), 'latin-1', 'replace')
    
    @staticmethod
    def AsString(variant):
        return str(variant).strip() or None
        

class PaceVariantFieldConversion(object):
    
    VARIANT_FIELD_MAP = {
        TkEnum.PVT_DATEPERIOD: 'dateperiodValue',
        TkEnum.PVT_DATETIME: 'datetimeValue',
        TkEnum.PVT_INT32: 'int32Value',
        TkEnum.PVT_INT64: 'int64Value',
        TkEnum.PVT_DOUBLE: 'doubleValue',
        TkEnum.PVT_BOOL: 'boolValue',        
        TkEnum.PVT_STRING: 'stringValue',
        TkEnum.PVT_NONE: 'stringValue'        
    }
    
    @classmethod
    def FieldName(cls, variant):
        return cls.VARIANT_FIELD_MAP.get(variant)

class PaceVariantConversion(object):

    DEFAULT_TYPE = TkEnum.PVT_STRING
    NONE = TkEnum.PVT_NONE
    
    DOMAIN_TO_TYPE_MAP = {
        type(None): TkEnum.PVT_NONE,
        int: TkEnum.PVT_INT64,
        float: TkEnum.PVT_DOUBLE,
        str: TkEnum.PVT_STRING,
        bool: TkEnum.PVT_BOOL,
        datetime: TkEnum.PVT_DATETIME,
        acm.FObject: TkEnum.PVT_STRING
    }
    
    @classmethod
    def ToPaceType(cls, variant, domain=None):
        domain = domain or AcmVariant.ToDomain(variant)
        return cls.DOMAIN_TO_TYPE_MAP.get(domain, cls.DEFAULT_TYPE)
