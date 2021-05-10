<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>0</protection>
<query>
[('', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', ')'),
('And', '(', 'Portfolio', 'equal to', 'SECONDARY MARKETS TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'ABSA CAPITAL SECURITIES', ')'),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('Or', '', 'Status', 'not equal to', 'Simulated', ''),
('Or', '', 'Status', 'not equal to', 'Terminated', ''),
('Or', '', 'Status', 'not equal to', 'Confirmed Void', ')')
]
</query>
</FTradeFilter>
