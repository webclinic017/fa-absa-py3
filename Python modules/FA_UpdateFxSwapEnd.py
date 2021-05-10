import acm

ins1=acm.FInstrument['AUD-USD/FXS/GEN/ON/OPT']
for leg in ins1.Legs():
    leg.EndPeriodCount(-1)
    leg.Commit()

ins2=acm.FInstrument['AUD-USD/FXS/GEN/TN/OPT']
for leg in ins2.Legs():
    leg.EndPeriodCount(0)
    leg.Commit()

ins3=acm.FInstrument['USD-CAD/FXS/GEN/ON']
for leg in ins3.Legs():
    leg.EndPeriodCount(-1)
    leg.Commit()

ins4=acm.FInstrument['USD-CAD/FXS/GEN/TN']
for leg in ins4.Legs():
    leg.EndPeriodCount(0)
    leg.Commit()
