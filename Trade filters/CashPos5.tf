<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>EXTRACT</owner>
<protection>3072</protection>
<query>
[('', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'greater equal', '-2m', ''),
('And', '', 'Time', 'less than', '-1m', '')
]
</query>
</FTradeFilter>
