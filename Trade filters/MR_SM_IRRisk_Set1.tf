<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Instrument.Expiry day', 'greater than', '0d', ')'),
('And', '(', 'Status', 'not equal to', 'Confirmed Void', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '(', 'Portfolio', 'equal to', 'COMMODITIES TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'EQUITIES TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'FOREIGN EXCHANGE TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'MONEY MARKET TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'SYNDICATE TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'PRIME SERVICES TRADING', ')'),
('And', '(', 'Instrument.Type', 'not equal to', 'IndexLinkedBond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'IndexLinkedSwap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'TotalReturnSwap', ')')
]
</query>
</FTradeFilter>
