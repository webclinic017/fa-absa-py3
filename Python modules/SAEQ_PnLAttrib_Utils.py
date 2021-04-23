import ael, acm

def concat(i, s1, s2, *rest):
    return s1 + s2
    
def getFairForward(instr, *rest):
    adfl = 'object:*"%s"' % ("fairForward")
    context = "Standard"

    tag = acm.CreateEBTag()

    acm_ins = acm.FInstrument[instr.insid]
    eval = acm.GetCalculatedValueFromString(acm_ins, context, adfl, tag)

    if eval != None:
        tmpReturn = (str)(eval.Value())
    else:
        tmpReturn = (str)(0)
   
    return tmpReturn

#eg. print getFairForward(ael.Instrument["ZAR/ALSI/AUG08/15000"])
