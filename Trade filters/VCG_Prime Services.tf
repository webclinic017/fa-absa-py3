<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Prime Services Desk', ''),
('Or', '', 'Portfolio', 'equal to', '41111', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS RTM Prime - Prime Broking', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS RTM Prime Services', ')'),
('And', '', 'Portfolio', 'not equal to', 'SBL Prop_Accrued', ''),
('And', '', 'Portfolio', 'not equal to', 'Prime Services Accrued', ''),
('And', '', 'Portfolio', 'not equal to', '2456', ''),
('And', '', 'Portfolio', 'not equal to', 'PB_FINANCING', ''),
('And', '', 'Instrument.Issuer (party)', 'not equal to', 'ABSA BANK LTD', ''),
('And', '', 'Instrument.Type', 'not equal to', 'IndexLinkedBond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Expiry day', 'greater than', '0d', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Simulated', '')
]
</query>
</FTradeFilter>
