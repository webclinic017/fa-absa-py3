import ael

qt = ael.Quotation['Per Unit']
ol = ael.Instrument.select('instype = "Option"')

for o in ol:
    #print o.insid
    if o.strike_quotation_seqnbr == None and o.und_instype=='Curr':
        try:
            oc = o.clone()
            oc.strike_quotation_seqnbr = qt
            oc.commit()
            print(o.insid, '- fixed')
        except:
            print(o.insid, '- could not fix')

