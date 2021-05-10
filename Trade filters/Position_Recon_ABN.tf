<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3072</protection>
<query>
[('', '(', 'Status', 'not equal to', 'Simulated', ''),
('And', '', 'Status', 'not equal to', 'Void', ''),
('And', '', 'Status', 'not equal to', 'Terminated', ')'),
('And', '', 'Value day', 'less equal', '0d', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '', 'Portfolio', 'equal to', 'ABSA BANK LTD', ''),
('And', '', 'Instrument.Extern ID 1', 'like', '%ABN%', ''),
('And', '', 'Counterparty.Type', 'not equal to', 'Intern Dept', ''),
('And', '', 'Counterparty', 'not equal to', 'BARCLAYS BANK PLC', ''),
('And', '(', 'Instrument', 'not like', '%PASSTHROUGH%', ''),
('And', '', 'Instrument', 'not like', '%PASS-THROUGH%', ''),
('And', '', 'Instrument', 'not like', ' %PASSTH%', ''),
('And', '', 'Instrument', 'not like', '%LOAN%\t', ')'),
('And', '(', 'Instrument.Extern ID 2', 'not like', '%PASSTHROUGH%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%PASS-THROUGH%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%PASSTH%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%LOAN%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%unlisted%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%Unlisted%', ''),
('And', '', 'Instrument.Extern ID 2', 'not like', '%UNLISTED%', ')')
]
</query>
</FTradeFilter>
