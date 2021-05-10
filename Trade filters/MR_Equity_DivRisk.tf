<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>0</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'EQUITIES TRADING', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('Or', '', 'Instrument.Type', 'equal to', 'VarianceSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('Or', '', 'Status', 'not equal to', 'Void', ''),
('Or', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('Or', '', 'Status', 'not equal to', 'Terminated', ''),
('Or', '', 'Status', 'not equal to', 'Reserved', ')')
]
</query>
</FTradeFilter>
