<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATSU3</owner>
<protection>3072</protection>
<query>
[('', '(', 'Instrument', 'equal to', 'ZAR/ACL/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/ANG/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/BGA/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/BIL/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/BTI/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/BVT/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/CFR/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/FSR/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/GFI/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/HAR/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/IMP/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/INL/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/INP/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/ITU/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/LON/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/MTN/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/OML/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/RMH/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/SAB/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/SBK/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/SOL/CFD', ''),
('Or', '', 'Instrument', 'equal to', 'ZAR/TKG/CFD', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'CFD', ')'),
('And', '(', 'Portfolio', 'equal to', '47274_CFD_ZERO', ')')
]
</query>
</FTradeFilter>
