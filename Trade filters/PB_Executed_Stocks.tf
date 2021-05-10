<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_CR_LIVE', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'ETF', ')'),
('And', '', 'Execution time', 'greater than', '0d', ''),
('And', '', 'Execution time', 'less than', '1d', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')')
]
</query>
</FTradeFilter>
