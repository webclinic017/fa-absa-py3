'''
Delete entries of PriceDefinition table
for the migration to the price entitlements hub
as part of upgrade to 2018.4
'''


import acm

pds = acm.FPriceDefinition.Select('')
tuple_pds =[]
print(len(pds), 'Before')

for pd in pds:
    if pd.Data0():
        print(pd.Oid(), 'will be deleted')
        tuple_pds.append(pd.Oid())

tuple_pds = tuple(tuple_pds)
        
for tpd in tuple_pds:
    p = acm.FPriceDefinition[tpd]
    p.Delete()


print(len(pds), 'After')
