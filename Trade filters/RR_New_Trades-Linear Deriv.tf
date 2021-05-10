<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Delta One Trading', ''),
('Or', '', 'Portfolio', 'equal to', 'Index Arbitrage', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Execution time', 'less than', '1d', ''),
('And', '', 'Execution time', 'greater than', '0d', '')
]
</query>
</FTradeFilter>
