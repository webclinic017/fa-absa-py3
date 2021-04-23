import acm

'''
************************************************************************************
script to update incorrect MONEY MARKET and PRIME SERVICES SSIs 
'''

def task1():
    parties = {'MONEY MARKET': acm.FParty['Money Market Desk'],
                'PRIME SERVICES': acm.FParty['PRIME SERVICES DESK']}

    SSIs = [SSI.Oid() for SSI in acm.FSettleInstruction.Select('') if SSI.FromParty() and SSI.FromParty().Name() in ('MONEY MARKET', 'PRIME SERVICES')]
    print('Total number of incorrect SSIs:', len(SSIs))

    #print acm.FSettleInstruction[SSIs[0]]
    #SSIs = [SSIs[0]]

    for ssi in SSIs:
        _SSI = acm.FSettleInstruction[ssi]
        print('Updating:', _SSI.Party().Name() + ' (' + _SSI.Name() + ': ' + _SSI.FromParty().Name() + ')')
        try:
            _SSI.FromParty(parties[_SSI.FromParty().Name()])
            #_SSI.Enabled('True')
            _SSI.Commit()
        except Exception, e:
            print('Error:', e)

    SSIs = [SSI.Oid() for SSI in acm.FSettleInstruction.Select('') if SSI.FromParty() and SSI.FromParty().Name() in ('MONEY MARKET', 'PRIME SERVICES')]
    print('Total number of incorrect SSIs after update:', len(SSIs))

'''
************************************************************************************
script to delete From Party SSIs on acquirers
'''

def task2():
    allSSIs = []

    acquirers = [p for p in acm.FParty.Select('') if p.Type() == 'Intern Dept']

    #acquirers = [acm.FParty['IRD DESK']]
    #print len(acquirers)

    for p in acquirers:
        SSIs = p.SettleInstructions()
        for ssi in SSIs:
            if ssi.FromParty() and ssi.FromParty().Type() == 'Intern Dept':
                allSSIs.append(ssi.Oid())
        
    print('Total number if SSIs to be deleted:', len(allSSIs))

    for ssi in allSSIs:
        SSI = acm.FSettleInstruction[ssi]
        print('Deleting %s on %s' %(SSI.Name(), SSI.Party().Name()))
        try:
            SSI.Delete()
        except Exception, e:
            print(e)

'''
************************************************************************************
FIS SSI upgrade script
'''

def task3():
    print(acm.FAelTask['FSettlementUpgradeSettleInstructions'].Execute())

'''
************************************************************************************
'''

ael_variables = []

def ael_main(parameters):
    print('Starting...')
    task1()
    task2()
    task3()
    print('Done!!!')
    print('This module can now be deleted.')
