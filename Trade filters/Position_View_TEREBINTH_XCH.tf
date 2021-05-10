<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_XCHEID_CR', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_XCHEIDJK_CR', ''),
('Or', '', 'Trade number', 'equal to', '68616489', ')'),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
