<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Portfolio', 'equal to', 'Non Zar Repo', ''),
('Or', '', 'Portfolio', 'equal to', 'CD_UNSECFIN_ACCRUAL', ''),
('Or', '', 'Portfolio', 'equal to', 'CD_CorpCDS_Basis', ''),
('Or', '', 'Portfolio', 'equal to', 'CD_COLLATERAL', ')'),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '', 'Instrument.Expiry day', 'greater equal', '-2d', ''),
('And', '', 'Counterparty.Type', 'not equal to', 'Intern Dept', ''),
('And', '(', 'Instrument.Type', 'equal to', 'Repo/Reverse', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Deposit', ''),
('Or', '', 'Instrument.Type', 'equal to', 'BuySellback', ')')
]
</query>
</FTradeFilter>
