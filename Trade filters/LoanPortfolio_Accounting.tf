<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PRIMARY MARKETS BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'PM Portfolio Management', ''),
('Or', '', 'Portfolio', 'equal to', 'PM Corp', ')'),
('And', '(', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ')')
]
</query>
</FTradeFilter>
