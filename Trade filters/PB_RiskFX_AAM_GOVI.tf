<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_AAM_GOVI_CR', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ')'),
('And', '(', 'Instrument.Underlying type', 'equal to', 'Bond', ''),
('Or', '', 'Instrument.Underlying type', 'equal to', 'Curr', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '-1m', '')
]
</query>
</FTradeFilter>
