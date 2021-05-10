<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'TREASURY ONE', ''),
('Or', '', 'Portfolio', 'equal to', 'Allocation', ''),
('Or', '', 'Portfolio', 'equal to', 'Capital Markets Funding', ''),
('Or', '', 'Portfolio', 'equal to', 'Commercial Fixed Assets', ''),
('Or', '', 'Portfolio', 'equal to', 'Fixed rate risk hedge', ''),
('Or', '', 'Portfolio', 'equal to', 'GT FX Hedging', ''),
('Or', '', 'Portfolio', 'equal to', 'GT Securitizations', ''),
('Or', '', 'Portfolio', 'equal to', 'Liquid Assets', ''),
('Or', '', 'Portfolio', 'equal to', 'Margin Compression', ''),
('Or', '', 'Portfolio', 'equal to', 'R&amp;C Deposits', ''),
('Or', '', 'Portfolio', 'equal to', 'R&amp;C Variable Assets and Liabilities', ''),
('Or', '', 'Portfolio', 'equal to', 'Residual Economic Risk', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM EFV Fund', ''),
('Or', '', 'Portfolio', 'equal to', 'Structural products &amp; equity', ')'),
('And', '', 'Portfolio', 'not like', 'Simulate%', ''),
('And', '', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', '')
]
</query>
</FTradeFilter>
