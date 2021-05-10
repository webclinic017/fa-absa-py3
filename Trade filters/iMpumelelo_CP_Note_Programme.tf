<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'IB iMpumelelo Accrual', ''),
('Or', '', 'Portfolio', 'equal to', 'Impume1_LREC', ''),
('Or', '', 'Portfolio', 'equal to', 'IB iMpumelelo FV', ''),
('Or', '', 'Portfolio', 'equal to', 'IB iMpumelelo AFS', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')'),
('And', '(', 'Instrument.Open End Status', 'not equal to', 'Open End', ''),
('And', '', 'Instrument.Open End Status', 'not equal to', 'Terminated', ')')
]
</query>
</FTradeFilter>
