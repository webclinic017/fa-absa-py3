import acm

original = acm.FTrade[68269504]
original.OptionalKey('')
original.Commit()

t1 = acm.FTrade[68617589]
t1.OptionalKey('0000464574|BBL|000320005F')
t1.Commit()
print(t1.OptionalKey())
