import ael, acm
from string import zfill
from zak_funcs import write_file

albi = acm.FInstrument['ZAR/ALBI_TEST']

def get_albi_spot():
    ap = acm.GetCalculatedValueFromString(albi, "Standard", 'object:*"theor"', acm.CreateEBTag()).Value()
    
    data.append(['ALBI SPOT', albi.Name(), albi.Instrument().Isin(), '', '', '', ap])

def get_bond_info():
    for i in albi.InstrumentMaps():
        data.append(['BOND YIELDS', i.Instrument().Name(), i.Instrument().Isin(), '', '', i.Weight(), i.Instrument().used_price()])
        
def get_repo_point():
    yc_list = [acm.FYieldCurve['ZAR_Bond_Repo_Cash'], acm.FYieldCurve['ZAR_Bond_repo_157'], acm.FYieldCurve['ZAR_Bond_repo_ALBI'], acm.FYieldCurve['ZAR_Bond_repo_GC']]
    
    for yc in yc_list:
        for b in yc.Benchmarks():
            data.append(['REPO POINTS', b.Name(), '', b.ExpiryPeriod(), '', '', b.used_price()])

def get_vol_points():
    vol = acm.FVolatilityStructure['Bond_Options']
    for p in vol.Points():
            vol_data.append(['VOL POINTS', p.Benchmark().Underlying().Name(), '', p.Benchmark().ExpiryPeriod(), p.ConvertedStrike(), '', p.Volatility()*100])

data = []
vol_data = []
data.append(['DATA TYPE', 'INSTRUMENT', 'ISIN', 'MATURITY', 'STRIKE', 'WEIGHT', 'VALUE'])
get_albi_spot()
get_bond_info()
get_repo_point()
get_vol_points()

vol_data.sort(lambda x, y: cmp(x[4], y[4]))
vol_data.sort(lambda x, y: cmp(zfill(x[3], 3), zfill(y[3], 3)))
vol_data.sort(lambda x, y: cmp(x[1], y[1]))

data.extend(vol_data)

write_file(r"C:\temp\ALBI_VOL_DATA.txt", data)
