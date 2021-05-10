""" Compiled: 2015-09-23 14:33:50 """

import acm

from FOrderValidationCalculationMessages import Definition, Result, ResultKey


def createDefinitionMessage(portfolio, positionColumnIds,
                            portfolioColumnIds, orderCalculations=True):
    definition = Definition()
    definition.portfolio_oid = portfolio.Oid()
    
    if orderCalculations:
        definition.active_orders = True
    
    if positionColumnIds:
        definition.position_column_id.extend(positionColumnIds)

    if portfolioColumnIds:    
        definition.portfolio_column_id.extend(portfolioColumnIds)
    
    return definition

def createKeyAndResultMessage(rowObject, calculations, orderInfo, definition):
    resultKey = ResultKey()
    if rowObject.IsKindOf(acm.FInstrument):
        resultKey.instrument_oid = rowObject.Oid()
        result = createInstrumentResultMessage(calculations, orderInfo, definition)
    else:
        resultKey.portfolio_oid = rowObject.Oid()
        result = createPortfolioResultMessage(calculations, definition)
        
    return resultKey, result

def createInstrumentResultMessage(calculations, orderInfo, definition):
    result = Result()
    
    for columnId in definition.position_column_id:
        pbVariant = result.position_value.add()
        value = calculations.get(columnId, None)
        toPbVariant(value, pbVariant)

    if definition.active_orders:
        for buyOrSell in [ True, False ]:
            pbVariant = result.order_value.add()
            if orderInfo:
                value = orderInfo.OrderInfo( buyOrSell ).Current()
            else:
                value = 0.0
            toPbVariant(value, pbVariant)
    
    return result
    
def createPortfolioResultMessage(calculations, definition):
    result = Result()

    for columnId in definition.portfolio_column_id:
        pbVariant = result.portfolio_value.add()
        value = calculations.get(columnId, None)
        toPbVariant(value, pbVariant)
    
    return result

def dvToPbDv(dv, pbDv):
    
    if '#' in str(dv):
        pbDv.number = float('nan')
    else:
        pbDv.number = dv.Number()

    unit = dv.Unit()
    if unit:
        pbDv.unit = str(unit)
    datetime = dv.DateTime()
    if datetime:
        pbDv.datetime = datetime
  
def fobjectToPbVariant(fobject, pbVariant):
    if fobject.IsKindOf(acm.FDenominatedValue):
        dvToPbDv(fobject, pbVariant.dv_value)
    elif fobject.IsKindOf(acm.FDenominatedBasket) or fobject.IsKindOf(acm.FDenominatedValueArray):
        if len(fobject) == 1:
            dvToPbDv(fobject[0], pbVariant.dv_value)
    elif fobject.IsKindOf(acm.FSymbol):
        pbVariant.string_value = str(fobject)
    elif fobject.IsKindOf(acm.FException):
        pbVariant.exception_value = str(fobject.Message())

def toPbVariant(value, pbVariant):
    if value is None:
        return
    elif hasattr(value, 'IsKindOf'):
        fobjectToPbVariant(value, pbVariant)
    elif isinstance(value, bool):
        pbVarint.bool_value = value
    elif isinstance(value, int):
        pbVariant.int32_value = value
    elif isinstance(value, float):
        pbVariant.double_value = value
    elif isinstance(value, str):
        pbVariant.string_value = value
    elif isinstance(value, Exception):
        pbVariant.exception_value = str( value )

def fromPbDv(pbDv):
    return acm.DenominatedValue(pbDv.number, str(pbDv.unit), str(pbDv.datetime))
    
class PbException(Exception): pass

def fromPbException(exceptionMsg):
    return PbException(str(exceptionMsg))

def singularFieldFromMessage(pbMessage, fields, default=None):
    result = default
    for field in fields:
        if pbMessage.HasField(field[0]):
            result = getattr(pbMessage, field[0])
            if field[1]:
                result = field[1](result)
            break
    return result

def fromUnicode(ustring):
    return str(ustring)
    
def fromInt32(int32):
    return int(int32)

PB_VARIANT_FIELDS = (('double_value', None), ('dv_value', fromPbDv), ('bool_value', None),
               ('int32_value', fromInt32), ('string_value', fromUnicode), ('exception_value', fromPbException))

def fromPbVariant(pbVariant):
    return singularFieldFromMessage(pbVariant, PB_VARIANT_FIELDS)

def fromPbVariants(variants):
    values = []
    for pbVariant in variants:
        values.append(fromPbVariant(pbVariant))
    return values    

def valuesFromResult(result, rowObject):
    if rowObject.IsKindOf(acm.FInstrument):
        return fromPbVariants(result.position_value)
    else:
        return fromPbVariants(result.portfolio_value)

def asFloat(pbVariant):
    try:
        value = float(fromPbVariant(pbVariant))
    except TypeError:
        value = 0.0
    
    return value

def selectIdentity(acmClass):
    def select(oid):
        return acmClass[int(oid)]
    return select
            
RESULT_KEY_FIELDS = (('instrument_oid', selectIdentity(acm.FInstrument)), 
    ('portfolio_oid', selectIdentity(acm.FPhysicalPortfolio)))
 
def objectFromResultKey(resultKey):
    return singularFieldFromMessage(resultKey, RESULT_KEY_FIELDS, None)

