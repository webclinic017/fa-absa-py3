""" Compiled: 2020-09-18 10:38:56 """

#__src_file__ = "extensions/RegulatoryInfo/etc/ChoicesExprRegInfoAddInfo.py"

import acm
import traceback
from contextlib import contextmanager


@contextmanager
def TryExcept():
    try:
        yield None
    except Exception as e:
        print(Exception, e)
        print(traceback.format_exc())
        raise e
        

def finalPriceTypes():
    with TryExcept():
        return acm.FChoiceList.Select('list="FinalPriceType"')


def transactionTypes():
    with TryExcept():
        return acm.FChoiceList.Select('list="TransactionType"')
        
        
def executingEntities():
    with TryExcept():
        return acm.FParty.Select('type = "Market"')


def reportingEntities():
    with TryExcept():
        brokers = acm.FParty.Select('type="Broker"')
        counterparties = acm.FParty.Select('type="Counterparty"')
        internalDepartments = acm.FParty.Select('type="Intern Dept"')
        parties = acm.FSortedCollection()
        parties.AddAll(brokers)
        parties.AddAll(counterparties)
        parties.AddAll(internalDepartments)
        return acm.FIndexedPopulator(parties)


def venues():
    with TryExcept():
        return acm.FParty.Select('type = "Market"')
    
    
    

