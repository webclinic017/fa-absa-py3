<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'MAN_Swap_2', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '-1d', ''),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')')
]
</query>
</FTradeFilter>
