<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '0522 CC', ''),
('And', '', 'Portfolio', 'not equal to', 'Cisca Fund Linked Notes', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Underlying type', 'equal to', 'EquityIndex', '')
]
</query>
</FTradeFilter>
