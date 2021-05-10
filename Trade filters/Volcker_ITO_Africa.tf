<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'AFRICA BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'AFRICA TRADING', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Reserved', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
