'''
Willie van der bank
This module is part of the previous settlement solution and is not used anymore
'''

import acm

def GenerateVostro(temp, forDate, *rest):
    try:
        print '1', forDate
        outfile = open('F:\VostroFields.txt', 'w')
        outfile.write('AccName,ValueDate,Amount,Ref,AccNum,OurAcc\n')
                
        query = 'status = "Manual Match" and valueDay = %s' % (forDate)        
        set = acm.FSettlement.Select(query)

        for s in set:
            if s.add_info('SWIFT_MessageType') == 'VOSTRO':
                
                AccName = s.CounterpartyName()
                ValueDate = s.ValueDay()
                Amount = abs(s.Amount())
                Ref = str(s.Trade().Instrument().InsType()) + '_' + str(s.Trade().Oid())
                AccNum = s.CounterpartyAccount()
                
                findSpace = AccNum.find(' ')
                if findSpace == -1:
                    AccNum = (str)(AccNum)
                else:
                    AccNum = (str)(AccNum[findSpace+1:])
                        
                OurAcc = s.AcquirerAccount()
                
                findSpace = OurAcc.find(' ')
                if findSpace == -1:
                    OurAcc = (str)(OurAcc)
                else:
                    OurAcc = (str)(OurAcc[findSpace+1:])        
                
                
                outfile.write('%s,%s,%s,%s,%s,%s\n' %(AccName, ValueDate, Amount, Ref, AccNum, OurAcc))

        outfile.close()
        return 'Success'
    except:
        return 'Failed'

#print GenerateVostro(None, acm.Time().DateNow())
