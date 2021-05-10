<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Instrument.Type', 'equal to', 'CFD', ''),
('And', '', 'Portfolio', 'equal to', 'PB_CR_LIVE', '')
]
</query>
</FTradeFilter>
