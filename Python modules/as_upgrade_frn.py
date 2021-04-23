#  Code to update the FRN cashflows' nominal factor to correct the Theor prices
import ael

#4474 cashflows needs to be updated
count = 0

list = ael.Instrument.select('instype = FRN')

for i in list:
    for leg in i.legs():
        for cf in leg.cash_flows():
            if cf.type == 'Float Rate' and cf.nominal_factor == 0:
                ncf = cf.clone()
                ncf.nominal_factor = 1
                ncf.float_rate_factor = 0
                ncf.spread = 0
                #both rate and float_rate_offset is already 0
                
                try:
                    ncf.commit()
                except:
                    print(i.insid, ncf.cfwnbr, ' did not commit')
                
                count = count + 1

print(count, ' cashflows updated')
