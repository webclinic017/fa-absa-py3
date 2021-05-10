<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_SAXO_PRINCIPAL', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_GPP_PRINCIPAL', ''),
('Or', '', 'Portfolio', 'equal to', 'Prime optimize', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK_FV_INTERMED_EUROCLEAR', ''),
('Or', '', 'Portfolio', 'equal to', 'ETF Trading', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_SAXO', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_GPP', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK', ')'),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')')
]
</query>
</FTradeFilter>
