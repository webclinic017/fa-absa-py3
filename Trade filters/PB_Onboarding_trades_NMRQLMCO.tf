<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_NMRQLMCO_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK_FV_NMRQLMCO', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_NMRQLMCO_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
