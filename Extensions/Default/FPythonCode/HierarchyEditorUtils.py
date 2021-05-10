import acm

class SettingsKeys :
    Bold = 'Bold'
    Visible = 'Visible'
    Color = 'Color'

class Settings:
    def __init__(self, choice, bold, visible, color) :
        self.m_choice = choice
        self.m_bold = bold
        self.m_visible = visible
        self.m_color = color

def SettingsFromChoice(choice, parameter) :
    name = str(choice.Name())
    bold = parameter.At(name + SettingsKeys.Bold, acm.FSymbol('No')) == acm.FSymbol('Yes')
    visible = parameter.At(name + SettingsKeys.Visible, acm.FSymbol('Yes')) == acm.FSymbol('Yes')
    color = parameter.At(name + SettingsKeys.Color, None)
        
    if color :
        colors = str(color).split(' ')
        if colors and len(colors) == 3:
            r = int(colors[0][1:])                           
            g = int(colors[1][1:])                           
            b = int(colors[2][1:])                           
            color = acm.UX().Colors().Create(r, g, b)

    return Settings(choice, bold, visible, color)

def ParameterFromName(parameterName) :
    extensions = acm.GetDefaultContext().GetAllExtensions('FParameterGUIDefinition', 'FObject', True, True)

    for ext in extensions :
        if ext.Name() == acm.FSymbol(parameterName) :
            return ext

    return acm.FParameterGUIDefinition()


def CopyIcon(iconName, newIconName) :
    if not acm.UX().IconFromName(newIconName) :
        icon = acm.UX().IconFromName(iconName)
        icon.Name(newIconName)
        icon.RegisterIcon()
        
def BoolToString(value) :
    if value:
        return 'True'

    return 'False'


def GetEnumValueAsString(dataGroupName, dataEnumValue) :
    enumerator = None
    
    if dataGroupName == 'Standard' :
        enumerator = acm.FEnumeration['enum(B92StandardType)']
    elif dataGroupName == 'Enum' :
        enumerator = acm.FEnumeration['enum(B92EnumType)']
    elif dataGroupName == 'RecordRef' :
        enumerator = acm.FEnumeration['enum(B92RecordType)']

    enumName = None
    if enumerator :
        enumName = enumerator.Enumerator(dataEnumValue)

    return enumName
    
def CommitObject(obj, shell) :
    ret = False
    try :
        obj.Commit()
        ret = True
    except RuntimeError as ex:
        acm.UX().Dialogs().MessageBoxInformation(shell, ex.message)
    except:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'Unable commit object ' + obj.StringKey())

    return ret

def DeleteObject(obj, shell) :
    ret = False
    try :
        obj.Delete()
        ret = True
    except RuntimeError as ex:
        acm.UX().Dialogs().MessageBoxInformation(shell, ex.message)
    except:
        acm.UX().Dialogs().MessageBoxInformation(shell, 'Unable delete object ' + obj.StringKey())

    return ret

