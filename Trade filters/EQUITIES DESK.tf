<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'EQUITIES BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'EQUITIES TRADING', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', '')
]
</query>
</FTradeFilter>
