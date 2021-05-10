<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'STIRT - FRA FLO', ''),
('Or', '', 'Portfolio', 'equal to', 'STIRT - FRA FLO LCH', ''),
('Or', '', 'Portfolio', 'equal to', 'STIRT - FRA FLO_LCH', ''),
('Or', '', 'Portfolio', 'equal to', 'STIRT - Bonds FLO', ''),
('Or', '', 'Portfolio', 'equal to', 'STIRT - ED Futures FLO', ''),
('Or', '', 'Portfolio', 'equal to', 'MIDAS_FLO', ''),
('Or', '', 'Portfolio', 'equal to', 'FLO', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '(', 'Value day', 'less than', '0d', ''),
('And', '', 'Instrument.Expiry day', 'less than', '0d', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', '')
]
</query>
</FTradeFilter>
