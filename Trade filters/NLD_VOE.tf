<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATSU7</owner>
<protection>3508</protection>
<query>
[('', '', 'Acquirer', 'equal to', 'Non Linear Derivatives', ''),
('And', '', 'Portfolio', 'equal to', 'VOE', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')'),
('And', '', 'Instrument.Underlying type', 'not equal to', 'Commodity', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Commodity', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '03/31/2005', '')
]
</query>
</FTradeFilter>
