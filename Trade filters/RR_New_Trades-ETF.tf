<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '2264 CC', ''),
('And', '', 'Portfolio', 'not equal to', 'Africa Structures', ''),
('And', '', 'Portfolio', 'not equal to', 'NewFunds GOVI ETF', ''),
('And', '', 'Portfolio', 'not equal to', 'NewFunds ILBI ETF', ''),
('And', '', 'Portfolio', 'not equal to', 'NewFunds Tradable Money Market Index ET', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Execution time', 'less than', '1d', ''),
('And', '', 'Execution time', 'greater than', '0d', '')
]
</query>
</FTradeFilter>
