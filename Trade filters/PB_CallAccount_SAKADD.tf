<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'PB_CALLACCNT_SAKADD', ''),
('Or', '', 'Portfolio', 'equal to', 'PB_CAT_B_SAKADD_CR', ')'),
('And', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
('And', '(', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ')'),
('And', '', 'Counterparty', 'equal to', 'KADD CAPITAL PTY LTD OBO KADD VALIDUS S', '')
]
</query>
</FTradeFilter>
