<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Economic Funding', ''),
('Or', '', 'Portfolio', 'equal to', 'GT Accounting Mismatch', ''),
('Or', '', 'Portfolio', 'equal to', 'CME Funding', ''),
('Or', '', 'Portfolio', 'equal to', 'Retail Fixed Assets', ''),
('Or', '', 'Portfolio', 'equal to', 'Wholesale Funding', ''),
('Or', '', 'Portfolio', 'equal to', 'Wholesale Funding (non ZAR)', ''),
('Or', '', 'Portfolio', 'like', 'Simulate%', ')'),
('And', '', 'Portfolio', 'not equal to', 'ERM EFV Fund', ''),
('And', '', 'Portfolio', 'not equal to', 'UNKNOWN', ''),
('And', '', 'Portfolio', 'not equal to', 'UNKNOWN', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', '')
]
</query>
</FTradeFilter>
