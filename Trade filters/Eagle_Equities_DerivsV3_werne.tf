<?xml version='1.0' encoding='ISO-8859-1'?>
<FTradeFilter>
<owner>ATS</owner>
<protection>3504</protection>
<query>
[('', '(', 'Status', 'equal to', 'FO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO Confirmed', ''),
('Or', '', 'Status', 'equal to', 'BO-BO Confirmed', ')'),
('And', '', 'Counterparty.Type', 'not equal to', 'Intern Dept', ''),
('And', '(', 'Counterparty', 'not equal to', 'JSE CLEAR', ''),
('And', '', 'Counterparty', 'not equal to', 'JSE SECURITIES EXCHANGE SOUTH AFRICA', ''),
('And', '', 'Counterparty', 'not equal to', 'ABSA BANK LTD AIB', ''),
('And', '', 'Counterparty', 'not equal to', 'JSE', ''),
('And', '', 'Counterparty', 'not equal to', 'ABSA BANK LIMITED', ''),
('And', '', 'Counterparty', 'not equal to', 'ABSA BANK LTD', ')'),
('And', '(', 'Portfolio', 'equal to', '0522 CC', ''),
('Or', '', 'Portfolio', 'equal to', '4533', ''),
('Or', '', 'Portfolio', 'equal to', '9923', ''),
('Or', '', 'Portfolio', 'equal to', '2264 CC', ''),
('Or', '', 'Portfolio', 'equal to', '0524 CC', ''),
('Or', '', 'Portfolio', 'equal to', '3016 CC', ')'),
('And', '', 'Instrument.Type', 'not equal to', 'CFD', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CD', ''),
('And', '', 'Instrument.Type', 'not equal to', 'IndexLinkedBond', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Deposit', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Zero', ''),
('And', '', 'Instrument.Type', 'not equal to', 'SecurityLoan', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Curr', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Swap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Stock', ''),
('And', '', 'Instrument.Type', 'not equal to', 'EquityIndex', ''),
('And', '', 'Instrument.Type', 'not equal to', 'FRN', ''),
('And', '', 'Instrument.Type', 'not equal to', 'PriceSwap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CurrSwap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Combination', ''),
('And', '', 'Instrument.Type', 'not equal to', 'ETF', ''),
('And', '', 'Instrument.Type', 'not equal to', 'IndexLinkedSwap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'CreditDefaultSwap', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Repo/Reverse', ''),
('And', '', 'Instrument.Type', 'not equal to', 'Bond', ''),
('And', '', 'Instrument.Underlying type', 'not equal to', 'ETF', ''),
('And', '', 'Instrument.Underlying type', 'not equal to', 'Commodity', ''),
('And', '', 'Instrument.Expiry day', 'greater equal', '0d', ''),
('And', '', 'Instrument.Underlying type', 'not equal to', 'Commodity Index', '')
]
</query>
</FTradeFilter>
