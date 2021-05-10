<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Value day', 'less than', '0d', ''),
('And', '(', 'Execution time', 'greater equal', '0d', ''),
('And', '', 'Execution time', 'less than', '1d', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')'),
('And', '(', 'Trader.Group', 'not equal to', 'Integration Process', ''),
('And', '', 'Trader.Group', 'not equal to', 'System Processes', ''),
('And', '', 'Trader', 'not equal to', 'STRAUSD', ')')
]
</query>
</FTradeFilter>
