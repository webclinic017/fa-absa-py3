<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>0</protection>
<query>
[('', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Option', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Portfolio Swap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CFD', ''),
('Or', '', 'Instrument.Type', 'equal to', 'ETF', ''),
('Or', '', 'Instrument.Type', 'equal to', 'TotalReturnSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'VarianceSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Warrant', ')'),
('And', '(', 'Portfolio', 'equal to', 'EQUITIES TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS RTM Equities', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS Flow', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS Facilitation', ')'),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('Or', '', 'Status', 'not equal to', 'Confirmed Void', ''),
('Or', '', 'Status', 'not equal to', 'Terminated', ''),
('Or', '', 'Status', 'not equal to', 'Simulated', ')')
]
</query>
</FTradeFilter>
