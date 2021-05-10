<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_RISK_FV_INTERMED_OAKHAVEN', ''),
('And', '', 'Acquirer', 'equal to', 'PRIME SERVICES DESK', ''),
('And', '(', 'Instrument.Type', 'equal to', 'IndexLinkedSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Swap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRA', ')'),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', '')
]
</query>
</FTradeFilter>
