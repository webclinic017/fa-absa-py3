<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>0</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'EQUITIES TRADING', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ')'),
('Or', '(', 'Instrument.Type', 'equal to', 'VarianceSwap', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ')'),
('And', '(', 'Status', 'not equal to', 'Reserved', ''),
('Or', '', 'Status', 'not equal to', 'Simulated', ''),
('Or', '', 'Status', 'not equal to', 'Terminated', ''),
('Or', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('Or', '', 'Status', 'not equal to', 'Void', ')')
]
</query>
</FTradeFilter>
