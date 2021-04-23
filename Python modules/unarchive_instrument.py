ins = ['USD/C/MUR/P/36.03']

for i in ins:
    instrument = acm.FInstrument[i]
    if instrument.ArchiveStatus() == 1:
        instrument.ArchiveStatus(0)
        instrument.Commit()
        print(instrument.Name(), instrument.Oid())
