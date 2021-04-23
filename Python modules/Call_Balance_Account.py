import acm
import Call_Balance

def TradeFiletrList():

    TradeFilterList = []
    for tf in acm.FTradeSelection.Select(''):
        TradeFilterList.append(str(tf.Name()))
    TradeFilterList.sort()
    
    return TradeFilterList
    
ael_variables =[['tradeFilter', 'TradeFilter', 'string', TradeFiletrList(), None, 1],
                ['FileName', 'File Name', 'string', None, 'CallBalanceOverride.TAB', 1],
                ['OutputPath', 'Output Path', 'string', None, '/services/frontnt/Task/', 1]]
                 
def ael_main(ael_dict):

    TradeFilter = acm.FTradeSelection[ael_dict['tradeFilter']].Trades()
    
    filePath = ael_dict['OutputPath'] + ael_dict['FileName']
        
    file        = open(filePath, 'w')  
  
    Heading =  'TrdNbr' + '\t' + 'Margin_Call_Balance'  
    file.writelines(Heading + "\n")
    
    for t in TradeFilter:
    
        p           = t.Portfolio().Name()
        port        = acm.FPhysicalPortfolio[p]
        portAddInfo = port.add_info('PSClientCallAcc')
        
        trdNo       = acm.FInstrument[portAddInfo].Trades()[0]
                
        try:
            Line    =  str(t.Name()) + '\t' + str(Call_Balance.get_CallBalance(trdNo))
            file.writelines(Line + "\n")
        except:
            print 'Coul not write to file'
            
    file.close()
    print 'Wrote secondary output to::' + filePath 
