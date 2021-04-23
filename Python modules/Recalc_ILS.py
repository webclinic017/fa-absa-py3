import ael
def calc_initial_indx():
    ins = ael.Instrument.select('instype = "IndexLinkedSwap"')
    indx_val = ael.Instrument['SACPI'].cpi_reference(ael.date_today())
    yc = ael.YieldCurve['ZAR-CPI']
    for i in ins:
        for l in i.legs():
            if l.nominal_scaling == 'CPI' or l.nominal_scaling == 'CPI Fixing In Arrears':
                if i.add_info('Index_Date'):
                    if ael.date_today() <= ael.date(i.add_info('Index_Date')):
                        lc = l.clone()
                        df = yc.yc_rate(ael.date_today(), ael.date(i.add_info('Index_Date')), None, 'Act/365', 'Discount')
                        lc.initial_index_value = indx_val / df
                        lc.commit()
    
calc_initial_indx()
