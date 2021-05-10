<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_LARM3LP_CR', ''),
('Or', '', 'Trade number', 'equal to', '59482456', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
