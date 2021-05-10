<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_MATFI_CR', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_COLL_MATFI_CR', ')'),
('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Void', ')')
]
</query>
</FTradeFilter>
