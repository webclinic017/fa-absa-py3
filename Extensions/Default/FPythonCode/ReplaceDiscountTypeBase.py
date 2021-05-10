
import acm
import FUxUtils

def DiscTypeCriteria(anObject, types):
    if not anObject:
        return False
    val = anObject.Value()
    return val in types

def getDiscountingTypeChoicesAndEmpty():
    discountingTypes = [""]
    discountingTypes.extend( acm.FChoiceList.Select("list = 'DiscType'").SortByProperty("Name") )
    return discountingTypes
    
def ReplaceDiscountingType( discountingType, replaceWhat, replaceWith ):
    if discountingType == replaceWhat:
        return replaceWith
    return discountingType
    
def show( shell, params ):
    parametersDef = 'discountingTypeIn,Discounting Type In;discountingTypeOut,Discounting Type Out'
    return FUxUtils.ShowNamedParametersDlg(shell, params, parametersDef )

def main( parameters, dictExtra, riskFactorGroup ):
    namedParameters = FUxUtils.UnpackNamedParameters(parameters)
    
    criteria = []
    params = []
    for i in namedParameters:
        iParams = []
        dtOut = None
        dtIn = None
        if i.Parameter('discountingTypeOut') != "":
            dtOut = acm.FChoiceList.Select("list = 'DiscType' and name = '" + str(i.Parameter('discountingTypeOut')) + "'").First()
        if i.Parameter('discountingTypeIn') != "":
            dtIn = acm.FChoiceList.Select("list = 'DiscType' and name = '" + str(i.Parameter('discountingTypeIn')) + "'").First()
        criteria.append( dtIn )
        iParams = [ dtIn, dtOut ]
        itemName = i.Name() != "" and i.Name() or (str(i.Parameter('discountingTypeIn')) + "->" + str(i.Parameter('discountingTypeOut')))
        params.append( [iParams, itemName] )

    func = acm.GetFunction('discTypeCriteria', 2)
    args = [None, criteria]
    shiftVector = acm.CreateShiftVector( 'replaceDiscountingType', riskFactorGroup, func.CreateCall( args ) )
    for iParam in params:
        shiftVector.AddShiftItem( iParam[0], iParam[1] )

    return shiftVector 
