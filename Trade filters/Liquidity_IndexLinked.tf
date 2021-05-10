<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'ABSA CAPITAL', ''),
('And', '', 'Instrument.Expiry day', 'greater than', '-10d', ''),
('And', '(', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')'),
('And', '', 'Counterparty.Type', 'not equal to', 'Intern Dept', '')
]
</query>
</FTradeFilter>
