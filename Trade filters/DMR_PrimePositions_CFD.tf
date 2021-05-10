<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Prime Optimize (Compound)', ''),
('Or', '', 'Portfolio', 'equal to', 'EQ_CFD', ''),
('Or', '', 'Portfolio', 'equal to', 'BARCAP_CFD', ''),
('Or', '', 'Portfolio', 'equal to', 'CS_PSwap', ')'),
('And', '', 'Portfolio', 'not equal to', '41012_CFD_ZERO', ''),
('And', '', 'Instrument.Type', 'equal to', 'CFD', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', '')
]
</query>
</FTradeFilter>
