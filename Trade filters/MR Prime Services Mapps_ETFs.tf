<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Mapps Growth 41129', ''),
('Or', '', 'Portfolio', 'equal to', 'Mapps Protector 41137', ')'),
('And', '', 'Instrument.Type', 'equal to', 'ETF', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', '')
]
</query>
</FTradeFilter>