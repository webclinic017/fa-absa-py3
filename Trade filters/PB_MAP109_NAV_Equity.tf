<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_MAP109_CR', ''),
('And', '(', 'Instrument.Underlying type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', ')'),
('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CFD', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
