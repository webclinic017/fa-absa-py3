<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_SAASPCV_CR', ''),
('And', '', 'Instrument.Underlying type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Underlying type', 'not equal to', 'EquityIndex', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Future/Forward', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Time', 'less than', '1d', '')
]
</query>
</FTradeFilter>
