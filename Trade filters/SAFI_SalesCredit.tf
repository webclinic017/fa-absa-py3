<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Inflation Bonds', ''),
('Or', '', 'Portfolio', 'equal to', 'RC FI', ')'),
('And', '', 'Instrument.Type', 'equal to', 'IndexLinkedBond', ''),
('And', '(', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'FO Confirmed', ')'),
('And', '', 'Aggregate', 'equal to', '0', ''),
('And', '', 'Counterparty', 'not equal to', 'ACQ STRUCT DERIV DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'GFI SOUTH AFRICA PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'CITIBANK NA SOUTH AFRICA BRANCH', ''),
('And', '', 'Counterparty', 'not equal to', 'STANDARD BANK SA', ''),
('And', '', 'Counterparty', 'not equal to', 'AVIOR PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'EQ Derivatives Desk', ''),
('And', '', 'Counterparty', 'not equal to', 'ETP BONDS', ''),
('And', '', 'Counterparty', 'not equal to', 'MERRILL LYNCH SA', ''),
('And', '', 'Counterparty', 'not equal to', 'BARCLAYS BANK PLC', ''),
('And', '', 'Counterparty', 'not equal to', 'FFO SECURITIES PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'ROKOS GLOBAL MACRO MASTER FUND LP', ''),
('And', '', 'Counterparty', 'not equal to', 'CARGILL GLOBAL FUNDING PLC', ''),
('And', '', 'Counterparty', 'not equal to', 'AG INSTITUTIONAL BROKERS PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'PIMCO 3637', ''),
('And', '', 'Counterparty', 'not equal to', 'PHARO GA PHARO TRADING FUND LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'GARBAN SA  PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'IRD DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'SARB', ''),
('And', '', 'Counterparty', 'not equal to', 'REPO DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'TFS SECURITIES PTY LTD', ''),
('And', '', 'Counterparty', 'not equal to', 'TULLETT', ''),
('And', '', 'Counterparty', 'not equal to', 'CREDIT DERIVATIVES DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'BOND DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'PSG FIXED INCOME AND COMMODITIES PTY LT', ''),
('And', '', 'Counterparty', 'not equal to', 'MONEY MARKET DESK', ''),
('And', '', 'Counterparty', 'not equal to', 'STRUCT NOTES DESK', ''),
('And', '', 'Execution time', 'greater equal', '-5d', '')
]
</query>
</FTradeFilter>
