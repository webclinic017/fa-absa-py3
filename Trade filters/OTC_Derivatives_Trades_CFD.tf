<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Counterparty.Type', 'equal to', 'Counterparty', ''),
('Or', '', 'Counterparty.Type', 'equal to', 'Client', ')'),
('And', '', 'Execution time', 'greater equal', '02/28/2011 04:00:00 PM', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '(', 'Instrument.Type', 'equal to', 'CFD', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ')'),
('And', '', 'Portfolio', 'equal to', 'ABSA CAPITAL', '')
]
</query>
</FTradeFilter>
