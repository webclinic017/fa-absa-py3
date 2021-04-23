import acm

t1 = acm.FTrade[72759537]
t1.OptionalKey('')
t1.Commit()
print(t1.OptionalKey())

t2 = acm.FTrade[72759538]
t2.OptionalKey('')
t2.Commit()
print(t2.OptionalKey())

t1 = acm.FTrade[72759806]
t1.OptionalKey('')
t1.Commit()
print(t1.OptionalKey())

t2 = acm.FTrade[72759807]
t2.OptionalKey('')
t2.Commit()
print(t2.OptionalKey())
