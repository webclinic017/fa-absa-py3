<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '(', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '', 'Counterparty.Type', 'not equal to', 'Intern Dept', ''),
('And', '', 'Portfolio', 'equal to', 'ABSA CAPITAL', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Type', 'not equal to', 'SecurityLoan', ''),
('And', '', 'Instrument.Type', 'not equal to', 'ETF', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Curr', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CFD', ''),
('And', '(', 'Instrument.Type', 'not equal to', 'Future/Forward', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Future/Forward', ''),
('And', '', 'Instrument.Pay type', 'not equal to', 'Future', ')')
]
</query>
</FTradeFilter>
