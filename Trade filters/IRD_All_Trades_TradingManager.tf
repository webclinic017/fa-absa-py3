<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATSU4</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Swap Flow', ''),
('Or', '', 'Portfolio', 'equal to', 'CPI', ''),
('Or', '', 'Portfolio', 'equal to', 'PRIME', ''),
('Or', '', 'Portfolio', 'equal to', 'MAN_Swap_2', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_IRP', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Risk', ''),
('Or', '', 'Portfolio', 'equal to', 'LTFX_BASIS_RV', ''),
('Or', '', 'Portfolio', 'equal to', 'MAN_Swap', ''),
('Or', '', 'Portfolio', 'equal to', 'LTFX', ')'),
('And', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ')')
]
</query>
</FTradeFilter>
