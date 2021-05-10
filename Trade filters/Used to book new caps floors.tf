<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Instrument.Type', 'equal to', 'Cap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Floor', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '(', 'Portfolio', 'equal to', 'Swap Risk', ''),
('Or', '', 'Portfolio', 'equal to', 'NLDO', ')'),
('And', '', 'Instrument.Currency', 'equal to', 'ZAR', ''),
('And', '', 'Instrument', 'not like', '%_2y', '')
]
</query>
</FTradeFilter>
