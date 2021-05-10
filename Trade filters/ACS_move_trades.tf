<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '', 'Portfolio', 'equal to', 'ACS Cash Equities Agency', ''),
('And', '', 'Portfolio', 'like', '%-TRD', ''),
('And', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ')'),
('And', '', 'Additional Info.XtpTradeType', 'equal to', 'XTP_OD_MOVE', '')
]
</query>
</FTradeFilter>
