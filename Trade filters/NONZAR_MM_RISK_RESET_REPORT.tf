<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '(', 'Portfolio', 'not like', 'Call%', ''),
('And', '', 'Portfolio', 'not like', '%unallocated%', ''),
('And', '', 'Portfolio', 'not like', '%pace%', ')'),
('And', '(', 'Portfolio', 'equal to', '3012', ''),
('Or', '', 'Portfolio', 'equal to', '4811', ''),
('Or', '', 'Portfolio', 'equal to', '4812', ''),
('Or', '', 'Portfolio', 'equal to', '4813', ''),
('Or', '', 'Portfolio', 'equal to', '9336', ')')
]
</query>
</FTradeFilter>
