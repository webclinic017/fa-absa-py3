<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '9923', ''),
('Or', '', 'Portfolio', 'equal to', '0687', ')'),
('And', '', 'Execution time', 'greater equal', '0d', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '(', 'Counterparty', 'equal to', 'JSE', ''),
('Or', '', 'Counterparty', 'equal to', 'A2X PTY LTD', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'ETF', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Stock', ')')
]
</query>
</FTradeFilter>
