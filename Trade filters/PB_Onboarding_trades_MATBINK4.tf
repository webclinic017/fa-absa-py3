<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_MATBINK4_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK_FV_MATBINK4', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_MATBINK4_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
