<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'SECONDARY MARKETS TRADING', ''),
('Or', '', 'Portfolio', 'equal to', 'SECONDARY MARKETS BANKING', ')'),
('And', '', 'Instrument.Type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Commodity', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Option', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Warrant', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Curr', ''),
('And', '', 'Instrument.Type', 'not equal to', 'EquityIndex', ''),
('And', '', 'Instrument.Type', 'not equal to', 'BondIndex', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Portfolio Swap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'RateIndex', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Repo/Reverse', ''),
('And', '', 'Instrument.Type', 'not equal to', 'BuySellback', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CFD', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Commodity Index', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Instrument.Expiry day', 'greater than', '0d', '')
]
</query>
</FTradeFilter>
