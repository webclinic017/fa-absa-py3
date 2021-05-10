<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Instrument.Type', 'equal to', 'Bond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
('Or', '', 'Instrument.Type', 'equal to', 'FRN', ''),
('Or', '', 'Instrument.Type', 'equal to', 'BuySellback', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Repo/Reverse', ')'),
('And', '', 'Status', 'equal to', 'FO Confirmed', ''),
('And', '(', 'Counterparty', 'equal to', 'DRA TRANSAKSIES', ''),
('Or', '', 'Counterparty', 'equal to', 'REPO DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'PRIME SERVICES DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'ALCO DESK ISSUER', ''),
('Or', '', 'Counterparty', 'equal to', 'MONEY MARKET DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'STRUCT NOTES DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'NLD DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'CREDIT DERIVATIVES DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'BOND DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'IRD DESK', ''),
('Or', '', 'Counterparty', 'equal to', 'CM FUNDING', ''),
('Or', '', 'Counterparty', 'equal to', 'CM Spot Trading', ''),
('Or', '', 'Counterparty', 'equal to', 'Capital Market Desk', ''),
('Or', '', 'Counterparty', 'equal to', 'EQ Derivatives Desk', ''),
('Or', '(', 'Counterparty.Type', 'equal to', 'Intern Dept', ''),
('And', '', 'Text1', 'equal to', 'Booked cm_BuySellBackProcess', ')'),
('And', '', 'Time', 'greater equal', '-2m', ')'),
('And', '', 'Portfolio', 'not equal to', 'PB_CR_LIVE', ''),
('And', '', 'Portfolio', 'not equal to', 'Abacas_S1_CP', ''),
('And', '', 'Portfolio', 'not equal to', 'Commisioner Street No. 4', ''),
('And', '', 'Instrument.Currency', 'equal to', 'ZAR', '')
]
</query>
</FTradeFilter>
