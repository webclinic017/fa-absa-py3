<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Single Stock Trading', ''),
('Or', '', 'Portfolio', 'equal to', '46052 Book Build', ''),
('Or', '', 'Portfolio', 'equal to', 'Small Cap SSO', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', '')
]
</query>
</FTradeFilter>
