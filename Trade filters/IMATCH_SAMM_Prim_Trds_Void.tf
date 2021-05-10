<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3520</protection>
<query>
[('', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Void', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ')'),
('And', '', 'Acquirer', 'equal to', 'Funding Desk', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Portfolio', 'not equal to', 'MM_Graveyard', ''),
('And', '', 'Instrument.Open End Status', 'not equal to', 'Open End', '')
]
</query>
</FTradeFilter>
