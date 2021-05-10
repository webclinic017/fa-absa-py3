<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_BIDGLOBL_CR', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_COLL_BIDGLOBL_CR', ')'),
('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Void', ')')
]
</query>
</FTradeFilter>
