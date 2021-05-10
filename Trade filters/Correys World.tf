<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '', 'Portfolio', 'equal to', '2796', ''),
('Or', '', 'Portfolio', 'equal to', '2795', ''),
('Or', '', 'Portfolio', 'equal to', '2969', ''),
('Or', '', 'Portfolio', 'equal to', '9802', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', '')
]
</query>
</FTradeFilter>
