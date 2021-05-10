""" Compiled: 2020-09-18 10:38:50 """

#__src_file__ = "extensions/cva/adaptiv_xva/./etc/AAComposer.py"
class Composable(object):
    def __init__(self, value):
        self.value = str(value)

    def __str__(self):
        return self.compose();       
            
    def compose(self):
        return self.value  


# abstract class
class ComposableContainer(Composable):
    
    def __init__(self):
        raise NotImplementedError("Not implemented")
                 
    # Customized copy method to implement one-level deep copy method instead of
    # Python's copy.copy() (shallow copy) or copy.deepcopy() (recursive deep copy)
    def clone(self):
        raise NotImplementedError("Not implemented")
    
    
class ComposableList(ComposableContainer):
    def __init__(self, left, right, separator, data = None):
        self.left = left
        self.right = right
        self.separator = separator
        if data:
            self.data = data
        else:
            self.data = []
            
    def __str__(self):
        return self.compose();     
                
    def clone(self):
        return ComposableList(str(self.left), str(self.right), str(self.separator), self.data[:])

    def __getitem__(self, index):
        return self.data[index]
    
    def append(self, newItem):
        self.data.append(newItem)
        
    def extend(self, newList):
        self.data.extend(newList)
        
    def compose(self):
        return self.left + (self.separator).join([composable.__str__() for composable in self.data]) + self.right
    
    def clear(self):
        self.data[:] = []
    
    def is_empty(self):
        return len(self.data) == 0        

class ComposablePairList(ComposableContainer):
    def __init__(self, left, right, separator, assigner, data = None):
        self.left = left
        self.right = right
        self.separator = separator
        self.assigner = assigner
        if data:
            self.data = data
        else:
            self.data = []
    
    def __str__(self):
        return self.compose();     
    
    def clone(self):
        return ComposablePairList(str(self.left), str(self.right), str(self.separator), str(self.assigner),  self.data[:])
    
    def __getitem__(self, wantedKey):
        for (key, value) in self.data:
            if key == wantedKey:
                return value
        raise Exception("Could not find key '%s'" % key)
    
    def __setitem__(self, key, newItem):
        self.data.append( (key, newItem) )
        
    def compose(self):
        return self.left + (self.separator).join("%s=%s" % (keyValPair[0], keyValPair[1]) for keyValPair in self.data) + self.right
    
    def clear(self):
        self.data[:] = []
        
        
# Custom composable containers

class CashFlowList(ComposableList):
    def __init__(self, data = None):
        super(CashFlowList, self).__init__("[", "]", "", data)


class ResetList(ComposableList):
    def __init__(self, data = None):
        super(ResetList, self).__init__("[", "]", ",", data)
        
        
class PairList(ComposablePairList):
    def __init__(self, data = None):
        super(PairList, self).__init__("", "", ",", "=", data)
      
  
class CashFlowDataDictionary(ComposablePairList):
    def __init__(self, data = None):
        super(CashFlowDataDictionary, self).__init__("[", "]", ",", "=", data)


class ComposablePriceFactorList(PairList):
    price_factors = [ 'InterestRate', 'SurvivalProb', 'DiscountRate', 
                      'FxRate', 'InterestRateVol', 'InterestYieldVol', 
                      'FXVol', 'InflationRate', 'PriceIndex', 'EquityPriceVol',
                      'CommodityPriceVol',  'EquityPrice', 'CommodityPrice', 'DividendRate',
                      'SeasonalFactor', 'ReferencePrice', 'ForwardPrice', 'ForwardPriceSample',
                      'FuturesPrice', 'ConvenienceYield', 'ReferenceVol', 'ForwardPriceVol', 'Correlation']
                      
    def __init__(self, data = None):
        super(ComposablePriceFactorList, self).__init__(data)                      

    def getAssigner(self, key):
        if '=' in key:
            return ""

        if key in self.price_factors:
            return "."
        else:
            return self.assigner            
    
    def compose(self):
        return self.left + (self.separator).join("%s%s%s" % (keyValPair[0], self.getAssigner(keyValPair[0]), keyValPair[1]) for keyValPair in self.data) + self.right
