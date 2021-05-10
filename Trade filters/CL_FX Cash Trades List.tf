<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '(', 'Counterparty', 'equal to', 'AFRICA DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'SPOT DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'SHADBAR', ''),
('Or', '', 'Counterparty', 'equal to', 'RAND SPOT DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'EQUITY DERIVATIVES', ''),
('Or', '', 'Counterparty', 'equal to', 'IRD DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'Metals Desk', ''),
('Or', '', 'Counterparty', 'equal to', 'NLD DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'MIDAS DUAL KEY', ''),
('Or', '', 'Counterparty', 'equal to', 'Gold Desk', ''),
('Or', '', 'Counterparty', 'equal to', 'FX SPOT', ''),
('Or', '', 'Counterparty', 'equal to', 'FX FORWARD', ''),
('Or', '', 'Counterparty', 'equal to', 'FORWARDS DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'FMAINTENANCE', ''),
('Or', '', 'Counterparty', 'equal to', 'CREDIT DERIVATIVES DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'EQ Derivatives Desk', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Curr', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Combination', ')'),
('And', '(', 'Execution time', 'less equal', '0d', ''),
('And', '', 'Value day', 'greater equal', '-1d', ')')
]
</query>
</FTradeFilter>
