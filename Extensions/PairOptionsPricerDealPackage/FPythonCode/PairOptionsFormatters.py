import acm
import math
from FXOptionPricerExtensionPoint import INCREASED_PRECISION
from PairOptionsUtil import GetSingleValue, IsIterable
from DealPackageDevKit import ParseFloat



def GetInstrumentPair(instr1, curr2):
    instrPair = acm.FInstrumentPair['%s/%s' % (instr1.Name(), curr2.Name())]
    if not instrPair:
        instrPair = acm.FInstrumentPair['%s/%s' % (curr2.Name(), instr1.Name())]
    return instrPair

def GetNumOfDecimalsFromPointValue(instrPair, inverse):
    pointValue = 0.0001
    try:
        pointValue = instrPair.PointValueInverse() if inverse else instrPair.PointValue() 
    except Exception:
        pass
    numOfDecimals = int(-math.log10(pointValue))
    return numOfDecimals

def GetNumOfDecimalsFromRoundingSpec(curr):
    numOfDecimals = 2
    try:
        rs = curr.RoundingSpecification()
        # TODO: Change the below to fetch the Roundings from the RS directly instead
        roundings = acm.FRounding.Select('roundingSpec = "%s"' % rs.Name())
        if len(roundings) > 0:
            for rounding in roundings:
                if rounding.Attribute() == 'Premium':
                    numOfDecimals = rounding.Decimals()
                    break
    except Exception:
        pass
    return numOfDecimals

def TheorPriceFormatterCBImpl(attrName, attrUnit):
    formatter = acm.Get('formats/VeryDetailedPrice').Clone()  
    formatter.NumDecimals(2)
    if not attrUnit:
        formatter.NumDecimals(4)
    return formatter

def GetFXSpotForwardFormatter(instr1, curr2, inverse):
    formatter = acm.Get('formats/FXRate').Clone()
    instrPair = GetInstrumentPair(instr1, curr2)
    numOfDecimals = GetNumOfDecimalsFromPointValue(instrPair, inverse) + INCREASED_PRECISION
    formatter.NumDecimals(numOfDecimals)
    return formatter

class FXRateFormatter(object):
    def __init__(self, instr, curr, inverse):
        self.instr = instr
        self.curr = curr
        self.inverse = inverse
        
    def CompoundFormatting(self):
        ''' This formatter returns true to format strings as '1.1/1.2' '''
        return True
    
    def GetFormatter(self):
        return GetFXSpotForwardFormatter(self.instr, self.curr, self.inverse)
        
    def Format(self, value):
        splittedValue = value.split('/') if isinstance(value, str) else value if IsIterable(value) else [value]
        return  '/'.join(map(self.GetFormatter().Format, splittedValue))
        
    def Parse(self, value):
        formatter = self.GetFormatter()
        return formatter.Parse(value)
        

class FXRateInverseFormatter(FXRateFormatter):
    def Format(self, value):
        if self.inverse:
            splittedValue = value.split('/') if isinstance(value, str) else value if IsIterable(value) else [value]
            return  '/'.join([self.GetFormatter().Format(1.0 / ParseFloat(v)) for v in splittedValue])
        return super(FXRateInverseFormatter, self).Format(value)
        
    def Parse(self, value):
        parsedValue = super(FXRateInverseFormatter, self).Parse(value)
        if self.inverse and value:
            parsedValue = 1.0 / ParseFloat(value)
        return parsedValue
     
class FXPointsFormatter(FXRateFormatter):
    def GetFormatter(self):
        formatter = acm.Get('formats/VeryDetailedPrice').Clone()
        formatter.NumDecimals(2) # Forward points always set to 2 decimals
        return formatter

class StrikeFormatter:
    def __init__(self, instr1, curr2, inverse):
        self.instrPair = GetInstrumentPair(instr1, curr2)
        self.inverse = inverse
    
    def Format(self, value):
        # Going from the db to the GUI
        numOfDecimals = GetNumOfDecimalsFromPointValue(self.instrPair, self.inverse)
        value = '{:.{}f}'.format(value, numOfDecimals)
        return value
        
    def Parse(self, value):
        # Going from the GUI to the db
        # TODO: Anything needed here? 
        return value
        
class AmountFormatter:
    def __init__(self, curr):
        self.curr = curr
    
    def Format(self, value):
        # Going from the db to the GUI
        formatter = acm.Get('formats/Imprecise').Clone()
        formatter.NumDecimals = GetNumOfDecimalsFromRoundingSpec(self.curr)
        if isinstance(value, (int, long, float)):
            value = abs(value)
        return formatter.Format(value)
        
    def Parse(self, value):
        # Going from the GUI to the db
        formatter = acm.Get('formats/Imprecise').Clone()
        if formatter:
            value = formatter.Parse(value)
        return value


class SingleValueFormatter:
    def __init__(self, buySell = None):
        self._buySell = buySell

    def CompoundFormatting(self):
        ''' This formatter returns true to format strings as '1.1/1.2' '''
        return True

    def Format(self, value):
        splittedValue = value.split('/') if isinstance(value, str) else list(value) if IsIterable(value) else [value]
        value = GetSingleValue(splittedValue, self._buySell)
        return str(value)
        
    def Parse(self, value):
        return value


class SingleValueIfAllEqualFormatter:
    def CompoundFormatting(self):
        ''' This formatter returns true to format strings as '1.1/1.2' '''
        return True

    def Format(self, value):
        splittedValue = value.split('/') if isinstance(value, str) else list(value) if IsIterable(value) else [value]
        value = splittedValue[0]
        for val in splittedValue:
            if val != value:
                value = ""
                break
        return str(value)
        
    def Parse(self, value):
        return value

class HideValueFormatter:

    def Format(self, value):
        return ''
        
    def Parse(self, value):
        return value

