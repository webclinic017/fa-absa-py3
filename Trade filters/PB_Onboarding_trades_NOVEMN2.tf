<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_NOVEMN2_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK_FV_NOVEMN2', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_NOVEMN2_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
