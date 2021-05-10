<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'SECONDARY MARKETS TRADING', ''),
('And', '', 'Portfolio', 'not equal to', 'Struct Notes Banking', ''),
('And', '', 'Portfolio', 'not equal to', 'PM Portfolio Management', ''),
('And', '', 'Portfolio', 'not equal to', 'PRIME SERVICES TRADING', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')')
]
</query>
</FTradeFilter>
