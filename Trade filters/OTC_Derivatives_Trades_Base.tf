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
('And', '(', 'Instrument.Type', 'equal to', 'BuySellback', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Cap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Combination', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CreditDefaultSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CurrSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'EquityIndex', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Floor', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRA', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Repo/Reverse', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Swap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'VarianceSwap', ')'),
('And', '', 'Portfolio', 'equal to', 'ABSA CAPITAL', '')
]
</query>
</FTradeFilter>
