<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3492</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_MAZI_CR', ''),
('Or', '', 'Trade number', 'equal to', '65049583', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', '')
]
</query>
</FTradeFilter>