import acm, ael

COMMIT = True

instruments = acm.FInstrument.Select('insType="%s"' % 'TotalReturnSwap')
divSwapCounter = 1
priceTypeCounter  = 1
initialPriceTypeCounter = 1

doNotDeletePaymentsFor =['ZAR/TRS/MPCDIVSWAP110317#2', 'ZAR/BRK/EQSWAP/TFG/USD/08JUL11_25OCT11']

def deletePayment(i):
    if i.Name() in doNotDeletePaymentsFor:
        return
    for t in i.Trades():
        for p in t.Payments():
            if p.Type() == 'Internal Fee':
                print "[I] Delete Payment: %s, %s, %s" % (p.Type(), p.Text(), p.Amount())
                if COMMIT:
                    p.Delete()


class DivSwap():

    def __init__(self):
        pass
        
    def isDivSwap(self, i):
        test1 = False
        test2 = False

        for l in i.Legs():
            if  (l.LegType() == 'Total Return') and l.NominalScaling() == 'None' and l.InitialIndexValue() == 100.0:
                test1 = True
            if  (l.LegType() in  ['Fixed', 'Float']) and l.NominalScaling() == 'None':
                test2 = True
        if test1 and test2:
            return True
        else:
            return False
        
    def fixDivSwap(self, i):
        global divSwapCounter
        deletePayment(i)
        print "[I] (* %s *) %s type Dividend Swap" % (divSwapCounter, i.Name())

        #if skipInstrument(i):
        #    return

        divSwapCounter += 1

        if self.isDivSwap(i):
            for l in i.Legs():
                deleteListCf = []
                deleteListRe = []
                if l.LegType() == 'Total Return' and l.NominalScaling() == 'None': 
                    print "[I] Index Type set to: \'Price\'"
                    print "[I] Initial Index Value set to: 1"
                    if COMMIT:
                        l.NominalScaling('Price')
                        l.InitialIndexValue(1)
                        l.Commit()

                #Collect what should be deleted on the dividend leg
                if l.NominalScaling() == 'Dividend':
                    for cf in l.CashFlows():
                        if not i.IsExpired():
                            if l.PassingType() == 'CashFlow Payday':
                                i.RegenerateDividendCashFlows(cf.StartDate(), cf.EndDate())
                        #Delete all cash flows of type Fixed Amount on the dividend leg
                        if cf.CashFlowType() in ('Fixed Amount', 'Redemption Amount', 'Call Fixed Rate'):
                            if not (i.IsExpired() and cf.CashFlowType() == 'Fixed Amount'):
                                deleteListCf.append(cf)
                                print "[I] Delete Cash Flow \'%s\' [%s]: %s" % (cf.CashFlowType(), cf.Oid(), cf.FixedAmount())
                        elif cf.CashFlowType() == 'Dividend':
                            for r in cf.Resets():
                                if r.ResetType() == 'Nominal Scaling':
                                    deleteListRe.append(r)
                                    print "[I] Delete Reset \'%s\' [%s] on Cash Flow \'%s\' [%s] " % (r.ResetType(), r.Oid(), cf.CashFlowType(), cf.Oid())
                        else:
                            print "[E] Unknown Cash Flow type \'%s\' [%s]" % (cf.CashFlowType(), cf.Oid())
                            
                #Delete Cash Flows 
                for cf in deleteListCf:
                    if COMMIT:
                        cf.Delete()
                        
                #Delete Resets        
                for r in deleteListRe:
                    if COMMIT:
                        r.Delete()

        #Total Return Cash Flow needs a Nominal Scaling reset otherwise:
        #No reset of type Nominal Scaling found for instrument: ZAR/TRS/LEWDIVSWAP110317#13, leg number 616814, cash flow number 7584346.
        resetDict = {}
        cfAddReset = None
        for l in i.Legs():
            if l.LegType() == 'Total Return':
                for cf in l.CashFlows():
                    if cf.CashFlowType() == 'Total Return':
                        cfAddReset = cf
                        for r in cf.Resets():
                            if r.ResetType() == 'Return':
                                resetDict[r.Day()] = r
                            elif r.ResetType() == 'Nominal Scaling':
                                print "[E] Reset of type \'Nominal Scaling\' does already exist"
                                return 
                                
        keys = resetDict.keys()
        keys.sort()
        rClone = resetDict[str(keys[0])].Clone()
        rClone.Day()
        rClone.StartDate()
        rClone.EndDate()
        rClone.FixingValue(1.0)
        rClone.ResetType('Nominal Scaling')
        if COMMIT:
            rClone.Commit()
            print "[I] Adding Reset: \'Nominal Scaling\': %s, %s, %s, %s on Cash Flow \'%s\' [%s]" % (rClone.Day(), rClone.StartDate(), rClone.EndDate(), 1.0, cfAddReset.CashFlowType(), cfAddReset.Oid())
            
        print "[I] ----------------------------------------"

class NoDiv():

    def __init__(self):
        pass
    
    def isNoDiv2(self, i):

        eqUnderlying = False
        
        for l in i.Legs():
            if l.LegType() == 'Total Return':
                if l.FloatPriceReference().InsType() in ('Stock', 'EquityIndex'):
                    eqUnderlying = True
        
        if eqUnderlying:
            hasDiv = False
            for l in i.Legs():
                for cf in l.CashFlows():
                    if cf.CashFlowType() == 'Dividend':
                        hasDiv = True
            if hasDiv:
                return False
            else:
                if i.IsExpired():
                    return True
                else:
                    return False

        else:
            return True

    def isNoDiv(self, i):
        noDiv = True
        for l in i.Legs():
            for cf in l.CashFlows():
                if cf.CashFlowType() == 'Dividend':
                    noDiv = False    
        return noDiv


class Price():

    def __init__(self):
        pass   

    def isCashFlowZero(cf):
        space = acm.FCalculationMethods().CreateStandardCalculationsSpaceCollection()
        proj = cf.Calculation().Nominal(acm.Calculations().CreateStandardCalculationsSpaceCollection(), t)
        if round(proj.Number(), 6) != 0.0:
            return True
        else:
            return False
    
    def isPrice(self, i):

        indexRef = None
        floatRef = None
            
        for l in i.Legs():
            if l.LegType() == 'Total Return':
                if l.IndexRef() and l.IndexRef().Name() and l.NominalScaling() == 'Price':
                    indexRef = l.IndexRef().Name()
                if l.FloatRateReference() and l.FloatRateReference().Name():
                    floatRef = l.FloatRateReference().Name()

        if indexRef == floatRef:
            return True
        return False

    def fixIndexTypePrice(self, i):
        global priceTypeCounter
        print "[I] (* %s *) %s type Price" % (priceTypeCounter, i.Name())
        deletePayment(i)
        priceTypeCounter += 1

        #if skipInstrument(i):
        #    return

        for l in i.Legs():
            deleteListCf = []
            deleteListRe = []
            #Collect what should be deleted on the dividend leg
            if l.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                for cf in l.CashFlows():
                    if not i.IsExpired():
                        if l.PassingType() == 'CashFlow Payday':
                            i.RegenerateDividendCashFlows(cf.StartDate(), cf.EndDate())
                    #Delete all cash flows of type Fixed Amount on the dividend leg
                    if cf.CashFlowType() in ('Fixed Amount', 'Redemption Amount', 'Call Fixed Rate'):
                        if not (i.IsExpired() and cf.CashFlowType() == 'Fixed Amount'):
                            deleteListCf.append(cf)
                            print "[I] Delete Cash Flow \'%s\' [%s]: %s" % (cf.CashFlowType(), cf.Oid(), cf.FixedAmount())
                    elif cf.CashFlowType() == 'Dividend':
                        for r in cf.Resets():
                            if r.ResetType() == 'Nominal Scaling':
                                deleteListRe.append(r)
                                print "[I] Delete Reset \'%s\' [%s] on Cash Flow \'%s\' [%s] " % (r.ResetType(), r.Oid(), cf.CashFlowType(), cf.Oid())
                    else:
                        print "[E] Unknown Cash Flow type \'%s\' [%s]" % (cf.CashFlowType(), cf.Oid())
        
            #Delete Cash Flows 
            for cf in deleteListCf:
                if COMMIT:
                    cf.Delete()
                    
            #Delete Resets        
            for r in deleteListRe:
                if COMMIT:
                    r.Delete()
        print "[I] ----------------------------------------"

class InitialPrice():

    def __init__(self):
        pass   


    def runResetFixing(self, acm_reset_array):

        import FBDPString
        reload(FBDPString)
        import FBDPCommon
        reload(FBDPCommon)
        try:
            import FBDPHook
            reload(FBDPHook)
        except:
            pass
        import FFixPerform
        reload(FFixPerform)
        # Only used for Op Man Fixing (1 = do not commit changes)
        dictionary = {}
        dictionary['GetOpManFixingRates_DoNotCommit'] = True
        dictionary["resets"] = acm_reset_array
        dictionary["extend_oe"] = False

        logme = FBDPString.logme
        ScriptName = "Fixing"

        logme.setLogmeVar("", # ScriptName
                          0,  # LogMode
                          0,  # LogToConsole
                          0,  # LogToFile
                          "", # LogFile
                          0,  # SendReportByMail
                          "", # MailList
                          "") # ReportMessageType

        FFixPerform.fix(dictionary)

    def isInitialPrice(self, i):

        indexRef = None
        floatRef = None
        nominalScaling = None
        for l in i.Legs():
            if l.LegType() == 'Total Return':
                if l.IndexRef() and l.IndexRef().Name():
                    indexRef = l.IndexRef().Name()
                    nominalScaling = l.NominalScaling()
                if l.FloatRateReference() and l.FloatRateReference().Name():
                    floatRef = l.FloatRateReference().Name()
        if indexRef != floatRef or nominalScaling == 'Initial Price':
            return True
        return False
       
    def fixInitialPrice(self, i):
    

        global initialPriceTypeCounter
        print "\n[I] (* %s *) %s type Initial Price" % (initialPriceTypeCounter, i.Name())
        initialPriceTypeCounter += 1
        for l in i.Legs():
            deleteListCf = []
            if l.NominalScaling() in ('Dividend', 'Dividend Initial Price'):
                for cf in l.CashFlows():
                    #Delete all cash flows of type Fixed Amount on the dividend leg
                    if cf.CashFlowType() in ('Fixed Amount', 'Redemption Amount', 'Call Fixed Rate'):
                        if not (i.IsExpired() and cf.CashFlowType() == 'Fixed Amount'):
                            deleteListCf.append(cf)
                            print "[I] Delete Cash Flow \'%s\' [%s]: %s" % (cf.CashFlowType(), cf.Oid(), cf.FixedAmount())

            #Delete Cash Flows 
            for cf in deleteListCf:
                if COMMIT:
                    cf.Delete() 
                    
                
        for l in i.Legs():
            if l.LegType() == 'Total Return':
                indexRef = l.IndexRef().Name()
                print "[I] Getting infdex ref %s" % (indexRef)
    
    
        for l in i.Legs():
            if l.NominalScaling() in ("Dividend", "Dividend Initial Price"):
                l.FloatPriceReference(indexRef )
                l.NominalScaling("Dividend Initial Price")
                if COMMIT:
                    l.Commit()

        iStartDate = i.StartDate()
        for l in i.Legs():
            for cf in l.CashFlows():
                if cf.CashFlowType() == 'Dividend':
                    for r in cf.Resets():
                        if r.ResetType()  in ('Nominal Scaling', 'Dividend Scaling'):
                            print "[I] Adjusting reset [%s] to %s, %s, %s" % (r.Oid(), iStartDate, iStartDate, cf.EndDate())
                            if COMMIT: 
                                r.ResetType('Dividend Scaling')
                                r.Day(iStartDate)
                                r.StartDate(iStartDate)
                                r.EndDate(cf.EndDate())
                                r.Commit()
            
            
 
        """
        for l in i.Legs():
            for cf in l.CashFlows():
                if cf.CashFlowType() == 'Dividend':
                    for r in cf.Resets():
                        print "[I] Changing Reset Type on [%s] %s, %s, %s from \'%s\' to \'Dividend Scaling\'" % (r.Oid(),r.StartDate(),r.EndDate(),r.Day(),r.ResetType())
                        r.ResetType('Dividend Scaling')
                        if COMMIT:
                            r.Commit() 
        
        """
      	  
        
        # Set fixings of type Dividend Scaling
        acm_reset_array = []
        for l in i.Legs():
            for cf in l.CashFlows():
                if cf.CashFlowType() == 'Dividend':
                    for r in cf.Resets():
                        print "[I] Fixing reset [%s] %s, %s, %s" % (r.Oid(), r.StartDate(), r.EndDate(), r.Day())
                        acm_reset_array.append(r)
        
     
        print "[I] Fixing Resets..." 
        if COMMIT:
              self.runResetFixing(acm_reset_array)
        print "[I] Done..." 
        
        # Set Initial Index value
        value = None
        for l in i.Legs():    
            for cf in l.CashFlows():
                if not i.IsExpired():
                    if l.PassingType() == 'CashFlow Payday':
                        i.RegenerateDividendCashFlows(cf.StartDate(), cf.EndDate())
                for r in cf.Resets():
                    if r.ResetType() == 'Dividend Scaling':
                        value =  r.FixingValue()
        oldInitIndexValues = []
        if value:
            for l in i.Legs():
                #if l.LegType() == 'Total Return':
                if l.NominalScaling() in ("Dividend", "Dividend Initial Price"):
                    oldInitIndexValues.append(l.InitialIndexValue())
                    if COMMIT:
                        l.InitialIndexValue(value)
                        l.Commit() 
            print "[I] Setting Initial Index Values: %s -> %s" % (oldInitIndexValues, value)
        else:          
            print "[E] Invalid Initial Index Value: %s" % (value)
            for l in i.Legs(): 
                fixingValue = l.InitialIndexValue()
                for cf in l.CashFlows():
                    for r in cf.Resets():
                        if r.ResetType() == 'Dividend Scaling':
                            if COMMIT:
                                r.FixingValue(fixingValue)
                                r.Commit()
                            print "[I] Setting Fixing Value: %s" % (fixingValue)
                            
c1 = 0
c2 = 0
c3 = 0
c4 = 0
c5 = 0

c1l = []
c2l = []
c3l = []
c4l = []
c5l = []

divSwap = DivSwap()
noDiv = NoDiv()
price = Price()
initialPrice = InitialPrice()

for i in acm.FInstrument.Select('insType="%s"' % 'TotalReturnSwap'):

    if noDiv.isNoDiv(i):    
        c1 = c1 + 1
        c1l.append(i)
    elif price.isPrice(i):
        c2 = c2 + 1
        c2l.append(i)
    elif divSwap.isDivSwap(i):    
        c3 = c3 + 1
        c3l.append(i)
    elif initialPrice.isInitialPrice(i):
        c4 = c4 + 1
        c4l.append(i)
    else:
        c5 = c5 + 1
        c5l.append(i)
        
print "No Div:     %s" % c1
print "Price:      %s" % c2
print "Div Swap:   %s" % c3
print "Init Price: %s" % c4
print "Other:      %s" % c5

ael_variables = []

def ael_main(dict):

    for i in c1l:     
        if noDiv.isNoDiv(i):
            deletePayment(i)    
            for l in i.Legs():
                if l.LegType() == 'Total Return':
                    if l.FloatPriceReference() and l.FloatPriceReference().InsType() in ('Stock', 'EquityIndex'):
                        if divSwap.isDivSwap(i):
                            divSwap.fixDivSwap(i)

    print "[I] ############################################# "

    for i in c2l:
        if price.isPrice(i):
            price.fixIndexTypePrice(i)

    print "[I] ############################################# "

    for i in c3l:   
        if divSwap.isDivSwap(i):
            divSwap.fixDivSwap(i) 
            
    print "[I] ############################################# "

    for i in c4l:   
        if initialPrice.isInitialPrice(i):
            initialPrice.fixInitialPrice(i)
            
    print "[I] ############################################# "
     
    for i in c5l:
        print "[E] Type not known %s" % (i.Name())
