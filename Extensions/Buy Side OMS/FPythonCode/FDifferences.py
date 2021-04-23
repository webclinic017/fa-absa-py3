""" Compiled: 2020-09-18 10:38:51 """

#__src_file__ = "extensions/BuySideOMS/./etc/FDifferences.py"
"""
"""


def CapitalizeFirst(text):
    text = str(text)
    return ''.join((text[0].upper(), text[1:]))
    
def DifferencesBetween(left, right):
    for diff in left.Difference(right).Differences():
        attr = diff.AssociationKey()
        attrValue = diff.AssociationValue().AssociationValue()
        yield attr, attrValue
        
def Attributes(obj):
    # pylint: disable-msg=W0612
    attributes = {}
    newObj = obj.Class().BasicNew(None)
    if newObj is None:
        raise TypeError('Can\'t compare differences for object of type %s' %obj.ClassName())
    for attr, attrValue in DifferencesBetween(newObj, obj):
        acmattr = obj.Class().GetAttribute(attr)
        if acmattr.IsUnique() is False or acmattr.IsOptionallyUnique() is True:
            methodName = CapitalizeFirst(attr)
            if hasattr(obj, methodName):
                attributes[methodName] = getattr(obj, methodName)()
    return attributes
    
def AdditionalInfoAttributes(obj):
    attributes = {}
    newObj = obj.Class().BasicNew(None)
    if newObj is None:
        raise TypeError('Can\'t compare differences for object of type %s' %obj.ClassName())
    try:
        for attr, attrValue in DifferencesBetween(newObj.AdditionalInfo(), obj.AdditionalInfo()):
            attrChain = ''.join(('AdditionalInfo.', CapitalizeFirst(attr))) 
            attributes[attrChain] = attrValue
        return attributes
    except AttributeError:
        return dict()
    
def PositionAttributes(obj):
    attributes = {}
    attributes.update(Attributes(obj))
    attributes.update(AdditionalInfoAttributes(obj))
    return attributes
    
def PositionAttributesFormatted(obj):
    attributes = {}
    for attr, attrValue in PositionAttributes(obj).items():
        try:
            attrValue = attrValue.StringKey()
        except AttributeError:
            pass
        attributes[attr] = attrValue
    return attributes
