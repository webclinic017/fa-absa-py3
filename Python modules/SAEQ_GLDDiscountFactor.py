import ael, math

factor = float(1/(1-0.004))
start = ael.date('2004-11-01')
end = ael.date_today()
period = float(start.days_between(end))
power = float((period)/365)

DiscountFactor = str(round(math.pow(factor, -power), 4))

ins = ael.Instrument['ZAR/GLD']
c_clone=ins.clone()
for a in ins.additional_infos():
    if a.addinf_specnbr.field_name == 'DiscountFactor':
        val = a.value
        ai = a.clone()
        ai.value = DiscountFactor
	try:
            ai.commit()
	except:
            pass
		
try:
    c_clone.commit()
except:
    pass	
