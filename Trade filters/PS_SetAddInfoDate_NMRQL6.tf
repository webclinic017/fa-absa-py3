<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_NMRQL6_CR', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_COLL_NMRQL6_CR', ')'),
('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Void', ')')
]
</query>
</FTradeFilter>
