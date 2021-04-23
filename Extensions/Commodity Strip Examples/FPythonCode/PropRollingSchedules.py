
from __future__ import print_function
import acm

def ThirdFuture(futures, valDate):
    futures.SortByProperty("ExpiryDate")
    comb_consts = []
    from_date = "1980-01-01"
    to_date = from_date
    for j in range(1, futures.Size() + 1):
        if j < 3:
            try:
                comb_consts.append(acm.CombinationConstituent.CreateTransientConstituent(futures[j-1], from_date, to_date, 0.0, 1))
            except Exception as e:
                print (e)
        else:
            to_date = futures[j-3].ExpiryDateOnly()
            try:
                comb_consts.append(acm.CombinationConstituent.CreateTransientConstituent(futures[j-1], from_date, to_date, 1.0, 1))
            except Exception as e:
                print (e)
            from_date = to_date
    return comb_consts
      

      
