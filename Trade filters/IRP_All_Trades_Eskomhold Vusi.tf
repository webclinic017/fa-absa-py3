<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'FxSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Swap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CurrSwap', ')'),
('And', '(', 'Counterparty', 'equal to', 'ESKOM HOLDINGS SOC LTD ALL DEBT', ''),
('Or', '', 'Counterparty', 'equal to', 'ESKOM HOLDINGS SOC LTD', ''),
('Or', '', 'Counterparty', 'equal to', 'DENEL VEHICLE SYSTEMS PTY LTD', ''),
('Or', '', 'Counterparty', 'equal to', 'COMMISSIONER STREET NO 4', ''),
('Or', '', 'Counterparty', 'equal to', 'GROWTHPOINT PROPERTIES LTD', ''),
('Or', '', 'Counterparty', 'equal to', 'UNICREDIT BANK AG', ''),
('Or', '', 'Counterparty', 'equal to', 'TRANSNET SOC LIMITED', ')')
]
</query>
</FTradeFilter>
