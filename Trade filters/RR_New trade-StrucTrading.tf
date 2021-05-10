<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '', 'Portfolio', 'equal to', '0522 CC', ''),
('And', '', 'Portfolio', 'not equal to', 'Africa Structures', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Execution time', 'less than', '1d', ''),
('And', '', 'Portfolio', 'not equal to', 'Eq_SA_Dividends', ''),
('And', '', 'Execution time', 'greater than', '0d', '')
]
</query>
</FTradeFilter>
