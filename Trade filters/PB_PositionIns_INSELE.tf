<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_RISK_FV_INTERMED_OAKHAVEN', ''),
('Or', '', 'Trade number', 'equal to', '102944931', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
