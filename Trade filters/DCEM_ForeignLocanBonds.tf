<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Instrument.Type', 'equal to', 'Bond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Bill', ''),
('Or', '', 'Instrument.Type', 'equal to', 'BuySellback', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ')'),
('Or', '(', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'Bond', ')'),
('Or', '(', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'ETF', ')'),
('Or', '(', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'Bond', ')'),
('Or', '(', 'Instrument.Type', 'equal to', 'Repo/Reverse', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'FRN', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ')')
]
</query>
</FTradeFilter>
