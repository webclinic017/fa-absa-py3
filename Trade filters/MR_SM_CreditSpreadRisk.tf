<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Instrument.Expiry day', 'greater than', '0d', ')'),
('And', '(', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '(', 'Portfolio', 'equal to', 'SECONDARY MARKETS BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'SECONDARY MARKETS TRADING', ')')
]
</query>
</FTradeFilter>
