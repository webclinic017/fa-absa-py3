<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3456</protection>
<query>
[('', '(', 'Portfolio', 'equal to', '9806', ''),
('Or', '', 'Portfolio', 'equal to', '41186', ''),
('Or', '', 'Portfolio', 'equal to', '40808 Prime Services Misdeals', ''),
('Or', '', 'Portfolio', 'equal to', 'PRIME BROKER', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS Cash Equities Trading', ''),
('Or', '', 'Portfolio', 'equal to', 'ACS Prime Risk', ''),
('Or', '', 'Portfolio', 'equal to', '40659_Syndicate trades', ''),
('Or', '', 'Portfolio', 'equal to', '9399', ''),
('Or', '', 'Portfolio', 'equal to', '0057', ''),
('Or', '', 'Portfolio', 'equal to', '9923', ''),
('Or', '', 'Portfolio', 'equal to', '0522 CC', ')'),
('And', '(', 'Instrument.Type', 'equal to', 'Stock', ''),
('Or', '', 'Instrument.Type', 'equal to', 'ETF', ')'),
('And', '', 'Instrument.Currency', 'equal to', 'ZAR', ''),
('And', '(', 'Status', 'not equal to', 'Simulated', ')'),
('And', '(', 'Portfolio', 'not equal to', 'Barcap DMA Brokerage', ''),
('And', '', 'Portfolio', 'not equal to', '248179', ''),
('And', '', 'Portfolio', 'not equal to', 'Nigeria Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Kenya Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Ghana Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'GSE Newgold', ''),
('And', '', 'Portfolio', 'not equal to', 'NSE Newgold', ''),
('And', '', 'Portfolio', 'not equal to', '332171 JSE_NewPlat', ''),
('And', '', 'Portfolio', 'not equal to', 'BSE NewGold', ''),
('And', '', 'Portfolio', 'not equal to', 'RSP Autocalls', ''),
('And', '', 'Portfolio', 'not equal to', 'Absa Life Brokerage', ''),
('And', '', 'Portfolio', 'not equal to', 'EQ_Funds', ''),
('And', '', 'Portfolio', 'not equal to', '333252 - Albaraka', ''),
('And', '', 'Portfolio', 'not equal to', 'Plexus Brokerage', ''),
('And', '', 'Portfolio', 'not equal to', 'Mauritius Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Zambia Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Botswana Equities', ''),
('And', '', 'Portfolio', 'not equal to', 'Listed LEIPs', ''),
('And', '', 'Portfolio', 'not equal to', 'MSE NewGold', ''),
('And', '', 'Portfolio', 'not equal to', 'MSE_NewPlat', ''),
('And', '', 'Portfolio', 'not equal to', '340083 JSE_NewPalladium', ''),
('And', '', 'Portfolio', 'not like', '309%', ''),
('And', '', 'Portfolio', 'not equal to', 'Sygnia Life Financials', ''),
('And', '', 'Portfolio', 'not equal to', 'Access Notes', ')'),
('And', '(', 'Instrument', 'not equal to', 'ZAR/GFI/CFD/SPECFIN', ''),
('And', '', 'Instrument', 'not equal to', 'ZAR/NHM/CFD/SPECFIN', ')')
]
</query>
</FTradeFilter>
