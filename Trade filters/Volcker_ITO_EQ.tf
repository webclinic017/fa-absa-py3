<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Reserved', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '(', 'Portfolio', 'equal to', 'EQUITIES TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS Cash Equities Trading', ')'),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
