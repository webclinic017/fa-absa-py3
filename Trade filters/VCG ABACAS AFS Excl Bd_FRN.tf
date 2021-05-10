<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Abacas_S1_AFS', ''),
('Or', '', 'Portfolio', 'equal to', 'AFS_Abacas_Entity', ''),
('Or', '', 'Portfolio', 'equal to', 'BESA Investments_AFS', ')'),
('And', '(', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'IndexLinkedBond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'FRN', ')'),
('And', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', '')
]
</query>
</FTradeFilter>
