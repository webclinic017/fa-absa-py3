<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_APCAP_CR', ''),
('Or', '', 'Trade number', 'equal to', '130502070', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>