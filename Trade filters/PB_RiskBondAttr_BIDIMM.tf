<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_BIDIMM_CR', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Bond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CD', ')')
]
</query>
</FTradeFilter>
