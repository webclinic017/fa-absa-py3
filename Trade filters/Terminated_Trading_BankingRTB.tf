<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'SECONDARY MARKETS BANKING', ''),
('Or', '', 'Portfolio', 'equal to', 'GROUP TREASURY', ''),
('Or', '', 'Portfolio', 'equal to', 'SECONDARY MARKETS TRADING', ')'),
('And', '', 'Status', 'equal to', 'Terminated', '')
]
</query>
</FTradeFilter>
