<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'GK_FI Composite', ''),
('Or', '', 'Portfolio', 'equal to', 'SPW_Risk', ''),
('Or', '', 'Portfolio', 'equal to', 'GK_IRD Composite', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', '')
]
</query>
</FTradeFilter>
