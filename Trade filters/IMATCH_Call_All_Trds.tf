<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3520</protection>
<query>
[('', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
('And', '', 'Acquirer', 'equal to', 'Funding Desk', ''),
('And', '', 'Portfolio', 'like', 'Call_%', ''),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')'),
('And', '', 'Instrument.Currency', 'equal to', 'ZAR', ''),
('And', '', 'Instrument.Open End Status', 'equal to', 'Open End', '')
]
</query>
</FTradeFilter>
