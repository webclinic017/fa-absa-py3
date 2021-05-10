<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3508</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'Terminated', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')'),
('And', '(', 'Portfolio', 'equal to', 'Swap Flow', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Risk_2', ''),
('Or', '', 'Portfolio', 'equal to', 'MAN_Swap', ''),
('Or', '', 'Portfolio', 'equal to', 'STIRT - FRA Trading', ''),
('Or', '', 'Portfolio', 'equal to', 'MAN_Swap_2', ''),
('Or', '', 'Portfolio', 'equal to', 'CD_DCRM_CRB_NONCSA', ''),
('Or', '', 'Portfolio', 'equal to', 'MAN_Swap', ''),
('Or', '', 'Portfolio', 'equal to', 'CPI', ''),
('Or', '', 'Portfolio', 'equal to', 'PRIME', ''),
('Or', '', 'Portfolio', 'equal to', 'PRIME_2', ''),
('Or', '', 'Portfolio', 'equal to', 'CPI_2', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_IRP_STRUCT', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_IRP', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_IRP', ''),
('Or', '', 'Portfolio', 'equal to', 'LEHMAN BANKRUPTCY', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_PRIME', ''),
('Or', '', 'Portfolio', 'equal to', 'RAJ - FRA Trading', ''),
('Or', '', 'Portfolio', 'equal to', 'ERM_CPI', ''),
('Or', '', 'Portfolio', 'equal to', 'PT_FI_OPTIONS', ''),
('Or', '', 'Portfolio', 'equal to', 'PT_IRS', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Risk_6', ''),
('Or', '', 'Instrument.Type', 'equal to', 'CurrSwap', ''),
('Or', '', 'Instrument.Type', 'equal to', 'Swap', ''),
('Or', '', 'Portfolio', 'equal to', 'GK_SWAPS', ''),
('Or', '', 'Portfolio', 'equal to', 'RAJ - ED Futs', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap_Futures', ''),
('Or', '', 'Portfolio', 'equal to', 'Swap Risk', ')'),
('And', '(', 'Instrument.Type', 'not equal to', 'IndexLinkedBond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ')'),
('And', '', 'Counterparty', 'like', '%TRANSNET%', '')
]
</query>
</FTradeFilter>
