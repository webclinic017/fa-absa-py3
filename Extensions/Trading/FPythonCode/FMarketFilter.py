
import acm

def GetFormatter(self, property):
    return acm.PropertyBinder.FindFormatter(self.Class(), property, None)
    
    
def Format(self, property, value):
    return GetFormatter(self, property).Format(value)
    
    
def Parse(self, property, string):
    try:
        return GetFormatter(self, property).Parse(string)
    except:
        return None
    
    
def GetFromDateTimeString(self):
    if self.FromDatePeriod():
        return Format(self, 'FromDatePeriod', self.FromDatePeriod())
    return Format(self, 'FromDateTime', self.FromDateTime())
    

def GetToDateTimeString(self):
    if self.ToDatePeriod():
        return Format(self, 'ToDatePeriod', self.ToDatePeriod())
    return Format(self, 'ToDateTime', self.ToDateTime())


def SetFromDateTimeString(self, fromDateTimeString):
    period = Parse(self, 'FromDatePeriod', fromDateTimeString)
    if period:
        self.FromDatePeriod(period)
    else:
        self.FromDateTime(Parse(self, 'FromDateTime', fromDateTimeString))


def SetToDateTimeString(self, toDateTimeString):
    period = Parse(self, 'ToDatePeriod', toDateTimeString)
    if period:
        self.ToDatePeriod(period)
    else:
        self.ToDateTime(Parse(self, 'ToDateTime', toDateTimeString))
