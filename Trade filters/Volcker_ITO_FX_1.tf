<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'FOREIGN EXCHANGE TRADING', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Reserved', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '(', 'Instrument.Type', 'not equal to', 'Curr', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ')'),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
