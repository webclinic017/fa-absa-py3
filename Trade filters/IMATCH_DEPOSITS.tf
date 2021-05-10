<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3520</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '47274_CFD_ZERO', ''),
('Or', '', 'Portfolio', 'equal to', '47332_CFD_ZERO', ')'),
('And', '', 'Execution time', 'greater than', '-3d', ''),
('And', '', 'Execution time', 'less than', '0d', '')
]
</query>
</FTradeFilter>
