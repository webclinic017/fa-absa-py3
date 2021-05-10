<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3520</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '9399', ''),
('Or', '', 'Portfolio', 'equal to', '9806', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ')')
]
</query>
</FTradeFilter>
