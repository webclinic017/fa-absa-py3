import acm


p = acm.FParty['ETP BONDS']

print p.Name(), p.Type(), 'before'
p.Type('Counterparty')
p.Commit()

print p.Name(), p.Type(), 'after'
