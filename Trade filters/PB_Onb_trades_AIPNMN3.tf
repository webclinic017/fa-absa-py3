<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_AIPNMN3_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_CFD_AIPNMN3', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_AIPNMN3_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
