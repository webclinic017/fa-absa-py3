<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'LTFX', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Curr', ''),
('And', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')')
]
</query>
</FTradeFilter>
