import acm

TODAY = acm.Time().DateNow()

class DateEnum:
    Unselected = 'None'
    Custom = 'Custom Date'
    Yesterday = 'Yesterday'
    Today = 'Today'
    Tomorrow = 'Tomorrow'

class DateParameter:

    DATE_DICT = {
        DateEnum.Unselected: None,
        DateEnum.Custom: None,
        DateEnum.Yesterday: acm.Time().DateAddDelta(TODAY, 0, 0, -1),
        DateEnum.Today: TODAY,
        DateEnum.Tomorrow: acm.Time().DateAddDelta(TODAY, 0, 0, 1)
    }
    
    DATE_DISPLAY = DATE_DICT.keys()
    DATE_DISPLAY.sort()
    
    @staticmethod
    def _toAcmDate(aelDate):
        if aelDate:
            [y, m, d] = aelDate.to_ymd()
            return acm.Time().DateFromYMD(y, m, d)
        else:
            return None
    
    @staticmethod
    def AddParameter(aelVariables, position, variableName, displayName, default, mandatory, description):
        if not default:
            dafault = DateEnum.Unselected
            
        customVariableName = 'CUSTOM' + variableName
        customDisplayName = 'Custom ' + displayName
        
        obj = DateParameter(aelVariables, variableName, customVariableName, customDisplayName, mandatory)
        
        #Variable Name, Display Name, Type, Candidate Values, Default, Mandatory, Multiple, Description, Input Hook, Enabled
        dateParameter = [variableName, displayName, 'string', DateParameter.DATE_DISPLAY, default, mandatory, False, description, obj._callBack, 1]
        customDateParemeter = [customVariableName, customDisplayName, 'date', None, None, False, False, "Custom date for parameter '%s'" % displayName, None, 1]
        
        aelVariables.insert(position, dateParameter)
        aelVariables.insert(position + 1, customDateParemeter)
        
        return obj
    
    def __init__(self, aelVariables, variableName, customVariableName, customDisplayName, mandatory):
        self._aelVariables = aelVariables
        self._variableName = variableName
        self._customVariableName = customVariableName
        self._customDisplayName = customDisplayName
        self._mandatory = mandatory
        
    def _callBack(self, index, fieldValues):
        self._aelVariables[index + 1][9] = (fieldValues[index] == DateEnum.Custom)
        return fieldValues
         
    def GetAcmDate(self, parameters):
        date = parameters[self._variableName]
        if date == DateEnum.Custom:
            customDate = parameters[self._customVariableName]
            if not customDate and self._mandatory:
                raise Exception('%s is mandatory, please supply a valid date' % self._customDisplayName)
                
            return DateParameter._toAcmDate(customDate)
        else:
            if date == DateEnum.Unselected and self._mandatory:
                raise Exception('%s is mandatory, please supply a valid date' % self._customDisplayName)
                
            if date not in DateParameter.DATE_DICT:
                raise Exception('Invalid date: %s' % date)
            
            return DateParameter.DATE_DICT[date]
