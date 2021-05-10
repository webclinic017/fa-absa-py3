<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATSU4</owner>
<protection>3508</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')'),
('And', '(', 'Portfolio', 'equal to', 'Swap Flow', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Flow Struct', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Flow NonCSA', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_IRP', ')'),
('And', '', 'Trade number', 'less equal', '1700000', ''),
('And', '', 'Trade number', 'greater than', '1500000', '')
]
</query>
</FTradeFilter>
