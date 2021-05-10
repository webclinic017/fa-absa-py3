<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_ABAXFIT_CR', ''),
('And', '', 'Portfolio', 'not equal to', 'PB_YIELDX_ABAXFIT_CR', ''),
('And', '', 'Portfolio', 'not equal to', 'PB_FULLYFUNDED_ABAXFIT_CR', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'BuySellback', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ''),
('And', '', 'Status', 'not equal to', 'Void', '')
]
</query>
</FTradeFilter>
