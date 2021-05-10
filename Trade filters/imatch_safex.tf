<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3520</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '9196', ''),
('Or', '', 'Portfolio', 'equal to', 'PETE_FX_Spot_SAFEX_Options', ''),
('Or', '', 'Portfolio', 'equal to', 'PETE_FX_Spot_SAFEX_Futures', ''),
('Or', '', 'Portfolio', 'equal to', '9399', ''),
('Or', '', 'Portfolio', 'equal to', '9806', ''),
('Or', '', 'Portfolio', 'equal to', '9923', ')'),
('And', '', 'Counterparty', 'equal to', 'JSE CLEAR', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '-5d', '')
]
</query>
</FTradeFilter>
