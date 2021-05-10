<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_MAP210B_CR', ''),
('And', '(', 'Instrument.Type', 'equal to', 'CFD', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CFD', ''),
('Or', '', 'Instrument.Type', 'equal to', 'BuySellback', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Bond', ')')
]
</query>
</FTradeFilter>
