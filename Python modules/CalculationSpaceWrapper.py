import acm
'''-------------------------------------------------------------------------------------------------------------
Wraps the Calculation API, supports creation/recreation of calculation spaces
and GC handeling when using the calculation space API. The calculation space/
calculation space collection are cleared when ever the "CalculationSpace"
or "CalculationSpaceCollection" access methods have been called more times than 
GC collect frequency is set too.         
Suitable to use when running scripts using the calculation API, excuted 
not a collection of e.g. big portfolios.


M.KLIMKE TODO
Add a list of simulation that have been done and then run through the list in the a desctructor

-------------------------------------------------------------------------------------------------------------'''

class CSCalcSpaceWrapper:
    def __init__(self, calculationSheet, collectFrequency = 500):
        self.collectFrequency           = collectFrequency
        self.nbrOfCalculations          = 0
        self.calculationSheet           = calculationSheet
        self.calculationSpaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
        self.calculationSpace           = acm.FCalculationSpace(self.calculationSheet)
        
    def CalculationSpace(self):
        self.PerformGCCollection()
        return self.calculationSpace 
        
    def CalculationSpaceCollection(self):
        self.PerformGCCollection()
        return self.calculationSpaceCollection 
    
    def PerformGCCollection(self):
        self.nbrOfCalculations += 1
        if( self.nbrOfCalculations % self.collectFrequency ) == 0:
            try:
                self.calculationSpaceCollection.Clear()
                self.calculationSpace.Clear()
                self.calculationSpaceCollection = acm.Calculations().CreateStandardCalculationsSpaceCollection()
                self.calculationSpace = acm.FCalculationSpace(self.calculationSheet)
                acm.Memory().GcWorldStoppedCollect()
                print("Garbage collection performed and new Calculation Space Collection created")
            except Exception, errMsg:
                print("Garbage collection and/or Construction of new calculation space collection faild, exception", errMsg)
    
    def CreateCalculation(self, anObject, column):
        try: 
            return self.CalculationSpace().CreateCalculation( anObject, column )
        except Exception, errMsg:
            print("Creation of calculation faild", errMsg)  
#------------------------------------------------------------------------
