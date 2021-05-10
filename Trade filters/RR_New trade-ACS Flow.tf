<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '40725 ACS EQ_Cash_Facilitation', ''),
('Or', '', 'Portfolio', 'equal to', '40741 ACS_FLOW', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Portfolio', 'not equal to', 'SS_OTC', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Execution time', 'less than', '1d', ''),
('And', '', 'Execution time', 'greater than', '0d', '')
]
</query>
</FTradeFilter>
