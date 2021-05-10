import acm
from at_time import *

market_names = [
('WMR LDN 11:00AM', 'Europe/London', 1100),
('WMR LDN 16:00PM', 'Europe/London', 1600),
('WMR NYK 10:00AM', 'America/New_York', 1000)
]

for name, time_zone, cutoff_time in market_names:
    
    market = acm.FParty[name]
    market.Type('MtM Market')
    market.TimeZone(time_zone)
    market.InternalCutOff(cutoff_time)
    market.ExternalCutOff(cutoff_time)
    market.Commit()
