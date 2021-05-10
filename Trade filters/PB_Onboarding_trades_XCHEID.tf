<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_XCHEID_FINANCING', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_RISK_FV_XCHEID', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_PSWAP_XCHEID_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')')
]
</query>
</FTradeFilter>
