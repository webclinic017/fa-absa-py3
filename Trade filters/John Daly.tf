<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'LTFX_Composite', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '', 'Instrument.Expiry day', 'not equal to', '0d', '')
]
</query>
</FTradeFilter>
