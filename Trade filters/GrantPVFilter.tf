<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Value day', 'equal to', '-1d', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '(', 'Acquirer', 'equal to', 'NLD DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'IRD DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'MONEY MARKET DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'REPO DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'STRUCT NOTES DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'CREDIT DERIVATIVES DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'CREDIT DERIVATIVES DESK NONCSA', ''),
('Or', '', 'Acquirer', 'equal to', 'PRIME SERVICES DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'AFRICA DESK', ''),
('Or', '', 'Acquirer', 'equal to', 'Agris Desk', ''),
('Or', '', 'Acquirer', 'equal to', 'Metals Desk', ''),
('Or', '', 'Acquirer', 'equal to', 'Gold Desk', ''),
('Or', '', 'Acquirer', 'equal to', 'EQ Derivatives Desk', ''),
('Or', '', 'Acquirer', 'equal to', 'IRD DESK NONCSA', ')')
]
</query>
</FTradeFilter>
