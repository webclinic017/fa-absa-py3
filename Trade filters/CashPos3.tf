<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>EXTRACT</owner>
<protection>3072</protection>
<query>
[('', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'greater equal', '-6m', ''),
('And', '', 'Time', 'less than', '-4m', '')
]
</query>
</FTradeFilter>
