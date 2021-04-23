'''----------------------------------------------------------------------------------------------------------------------------------
# Purpose                       :  Odyssey recon. Grouped at Portfolio, Counterparty, Instrument Name
# Department and Desk           :  PCG
# Requester                     :  Diana Rodrigues
# Developer                     :  Bhavnisha Sarawan
# CR Number                     :  C892102
----------------------------------------------------------------------------------------------------------------------------------'''




import acm, time

context = acm.GetDefaultContext()
calc_space = acm.Calculations().CreateCalculationSpace(context, 'FPortfolioSheet')

    
ael_gui_parameters = {'hideExtracControls' : True,
                      'windowCaption' : 'Odyssey Extract'}
                      
ael_variables = [ ['Path', 'Path', 'string', None, '', 0],
                  ['Filename', 'Filename', 'string', None, 'Odyssey.csv', 0],
                  ['Portfolio', 'Portfolio', 'FPhysicalPortfolio', acm.FPhysicalPortfolio.Select(''), 'Equities Desk', 1]]
    
    
    

def getCalc(ml, outfile):
    node = calc_space.InsertItem(ml)
    portfolioGrouper = acm.FAttributeGrouper('Trade.Portfolio')
    CPGrouper = acm.FAttributeGrouper('Trade.Counterparty')
    InsGrouper = acm.FAttributeGrouper('Instrument.Name')
    node.ApplyGrouper(acm.FChainedGrouper([portfolioGrouper, CPGrouper, InsGrouper]))
    calc_space.Refresh()
    if node.NumberOfChildren():
        portfolioIter = node.Iterator().Clone().FirstChild()
    
        while portfolioIter:
            portfolio = portfolioIter.Tree().Item().StringKey()
            CounterpartyIter = portfolioIter.Clone().FirstChild()

            while CounterpartyIter:
                CP= CounterpartyIter.Tree().Item().StringKey()
                InsIter = CounterpartyIter.Clone().FirstChild()
                    
                while InsIter:
                    Ins = InsIter.Tree().Item().StringKey()
                    InstrumentsIter = InsIter.Clone().FirstChild()
                        
                    while InstrumentsIter:
                        InstrumentType = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Instrument Type').Value()
                        UnderlyingType = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Underlying Type').Value()
                        
                        try:
                            CashEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Portfolio Cash End').Value().Number()
                        except:
                            CashEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Portfolio Cash End').Value()
                        
                        try:
                            PosValEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Pos Val End').Value().Number()
                        except:
                            PosValEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Pos Val End').Value()
                        
                        try:
                            NegValEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Neg Val End').Value().Number()
                        except:
                            NegValEnd = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Neg Val End').Value()
                            
                        try:
                            AccInt = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Portfolio Accrued Interest').Value().Number()
                        except:
                            AccInt = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Portfolio Accrued Interest').Value()
                        
                        try:
                            CurrentNominal = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Current Nominal').Value().Number()
                        except:
                            CurrentNominal = calc_space.CreateCalculation(InstrumentsIter.Tree(), 'Current Nominal').Value()


                        outfile.write('%s,%s,%s,%s,%s,%s,%s,%s,%s,%s\n' % (portfolio, Ins, InstrumentType, UnderlyingType, CP, CashEnd, PosValEnd, NegValEnd, AccInt, CurrentNominal))
                        InstrumentsIter = InstrumentsIter.NextSibling()
                    InsIter = InsIter.NextSibling()
                CounterpartyIter = CounterpartyIter.NextSibling()
                     
            portfolioIter =portfolioIter.NextSibling()
    

def ael_main(parameter, *rest):
    count = 0
    tm = time.clock()
    header = 'Portfolio,Instrument ID,Instrument Type, Underlying Type, Counterparty, Cash End, Pos Val End, Neg Val End, Accrued Interest, Current Nominal \n'
    
    outputPath = parameter['Path']
    outputName = parameter['Filename']
    portfolio = parameter['Portfolio']
    
    fileName = outputPath + outputName
    
    outfile=  open(fileName, 'w')
    outfile.write(header)
    
    getCalc(portfolio, outfile)

    
    outfile.close()
    print 'Output Complete', time.clock() - tm
    print 'Wrote secondary output to::: ' + fileName
