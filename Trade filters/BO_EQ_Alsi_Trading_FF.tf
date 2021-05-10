<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'Alsi Trading', ''),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')'),
('And', '', 'Instrument.Type', 'equal to', 'Future/Forward', '')
]
</query>
</FTradeFilter>
