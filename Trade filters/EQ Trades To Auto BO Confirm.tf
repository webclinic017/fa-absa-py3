<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Sales', ')'),
('And', '', 'Portfolio', 'not equal to', 'Allocate_Pfolio_Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Call_9806', ''),
('And', '(', 'Portfolio', 'equal to', 'ABSA CAPITAL SECURITIES', ''),
('Or', '', 'Portfolio', 'equal to', 'Equities Desk', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'ETF', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Stock', ')'),
('And', '', 'Instrument.Currency', 'equal to', 'ZAR', '')
]
</query>
</FTradeFilter>
