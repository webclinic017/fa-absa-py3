import ael
i = ael.Instrument['ZAR-SAFEX-ON-DEP']
print(i.used_price())
print(float(i.used_price()))
print(float(i.used_price()) <> i.used_price())
