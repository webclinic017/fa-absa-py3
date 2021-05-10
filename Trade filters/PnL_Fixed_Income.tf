<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'FIXED INCOME BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'FIXED INCOME TRADING', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')')
]
</query>
</FTradeFilter>
