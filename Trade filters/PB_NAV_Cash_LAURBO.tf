<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'PB_CALLACCNT_LAURBO', ''),
('And', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ')'),
('And', '', 'Counterparty', 'equal to', 'BLUE OCEAN LAURIUM LONG SHORT EN COMMAN', '')
]
</query>
</FTradeFilter>
