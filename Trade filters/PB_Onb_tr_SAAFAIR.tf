<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_SAAFAIR_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_CFD_SAAFAIR', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_SAAFAIR_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
