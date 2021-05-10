<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'ABSA CAPITAL', ''),
('And', '', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Value day', 'greater equal', '01/01/2017', ''),
('And', '', 'Value day', 'less than', '02/01/2017', ''),
('And', '(', 'Portfolio', 'not equal to', 'PRIME BROKER', ')'),
('And', '(', 'Status', 'not equal to', 'Reserved', ''),
('Or', '', 'Status', 'not equal to', 'Confirmed Void', ')')
]
</query>
</FTradeFilter>
