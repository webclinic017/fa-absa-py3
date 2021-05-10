<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Acquirer', 'equal to', 'TWC DT', ''),
('Or', '', 'Acquirer', 'equal to', 'TWC NON RECOURSE RECEIVABLES', ''),
('Or', '', 'Acquirer', 'equal to', 'TWC SF', ')'),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Instrument.Currency', 'equal to', 'ZAR', ')'),
('And', '(', 'Portfolio', 'equal to', 'Supplier Finance Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Supplier Finance ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'STCF ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Trade Loans Refi Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'NRRF ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'NRRF Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Vanilla Open Account Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'FI Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Doc Trade Vanilla ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Doc Trade Vanilla Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Islamic Trade Loans ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'STCF Non ZAR', ''),
('Or', '', 'Portfolio', 'equal to', 'Vanilla Open Account ZAR', ')')
]
</query>
</FTradeFilter>
