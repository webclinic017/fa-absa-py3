<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_CORINCIS2_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_CFD_CORINCIS2', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_CORINCIS2_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
