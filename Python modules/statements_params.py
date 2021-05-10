"""-----------------------------------------------------------------------------
PURPOSE              :  Client Valuation Statements Automation
                        Parameters used in the solution.
DESK                 :  PCG Collateral
DEVELOPER            :  Libor Svoboda
--------------------------------------------------------------------------------

HISTORY
================================================================================
Date        Change no      Developer           Description
--------------------------------------------------------------------------------
2019-02-14  CHG1001362755  Libor Svoboda       Initial Implementation (FEC)
2019-06-14  CHG1001881233  Libor Svoboda       Update FEC layout
2020-06-03  CHG0103217     Libor Svoboda       Add SBL client statements
"""
import os
import acm


STATE_CHART = acm.FStateChart['Statements']

REPORTING_CURR = acm.FCurrency['ZAR']

SBL_FINDER_MAPPING = {
    acm.FParty['SLL SPECIALISED PS FINDER']: 'Specialised Portfolio Services',
    acm.FParty['SLL AG CAPITAL FINDER']: 'AG CAPITAL',
    acm.FParty['SLL OPTIMIZE FIN SERVICE FINDER']: 'Optimize Financial Services (Pty) Limit',
    acm.FParty['SLL AXON ORG FINDER']: 'Axon/ORG',
}

DATE_PATTERN_VALUES = '%d/%m/%Y'
DATE_PATTERN_DOCS = '%d %B %Y'
DATE_PATTERN_MONTH = '%B %Y'

LIVE_TRADE_PERIOD_DEFAULT = 10 # number of days
LIVE_TRADE_PERIOD_SBL = 60 # number of days

FPARAMS = ('StatementsProd' 
           if acm.FDhDatabase['ADM'].InstanceName() in ('Production', 'DR') 
           else 'StatementsTest')

OUTPUT_DIR_PARAM = 'OutputRoot'
PREVIEW_DIR_PARAM = 'PreviewRoot'

ABSA_ADDRESS_PARAM = 'AbsaAddress'
ABSA_WEB_PARAM = 'AbsaWeb'
ABSA_VAT_NBR_PARAM = 'AbsaVatNbr'

VALUATIONS_TEL_PARAM = 'ValuationsTel'

SBL_ACC_NAME_PARAM = 'SBLAccountName'
SBL_BANK_PARAM = 'SBLBankName'
SBL_ACC_NUM_PARAM = 'SBLAccountNumber'
SBL_BRANCH_PARAM = 'SBLBranchCode'
SBL_SWIFT_PARAM = 'SBLSwift'
SBL_DIV_ACC_NAME_PARAM = 'SBLDivAccountName'
SBL_DIV_ACC_NUM_PARAM = 'SBLDivAccountNumber'
SBL_DIV_BRANCH_PARAM = 'SBLDivBranchCode'

SBL_OPS_TEL_PARAM = 'SBLOpsTel'
SBL_OPS_EMAIL_PARAM = 'SBLOpsEmail'

SBL_COLL_TEL_PARAM = 'SBLCollTel'
SBL_COLL_EMAIL_PARAM = 'SBLCollEmail'


DISCLAIMER_VALUATIONS = '''This document has been prepared by Absa Bank Limited (registration number 1986/004794/06) ("Absa"), for information purposes only. This document is provided to you and at your specific request.
Any information herein is indicative, is subject to change, is not intended to be an offer or solicitation for the purchase, sale, assignment, settlement or termination of any financial instrument, and is provided for reference purposes only. This information is not intended as an indicative price or quotation, and does not imply that a market exists for any financial instrument discussed herein; it does not therefore reflect hedging and transaction costs, credit considerations, market liquidity or bid-offer spreads. Absa does not represent that any value(s) in this document directly correlate with values which could actually be achieved now or in the future. Absa does not make any representation or warranty, neither does it guarantee the adequacy, accuracy, correctness or completeness of information which is contained in this document and which is stated to have been obtained from or is based upon trade and statistical services or other third party sources. Any data on past performance, modelling or back-testing contained herein is no indication as to future performance. No representation is made in respect of the assumptions or the accuracy or completeness of any modelling or back-testing. All opinions and estimates are given as of the date hereof and are subject to change. The value of any investment may fluctuate as a result of market changes. The information in this document is not intended to predict actual results and no assurances are given with respect thereto. This document represents our view as at the date hereof and subject to the limited scope of the assumptions and methodology set forth herein. This document has not been prepared in accordance with the standards and practice of any professional body in any jurisdiction and does not, and is not intended to, constitute an accounting, legal or tax opinion from Absa.
This document is not intended to be legally binding. Neither you nor your affiliates or advisers or any other person may rely on the information contained herein. Absa does not, through this document or the views expressed herein, owe or accept any responsibility or liability to you or your affiliates or your advisers or any other person, whether in contract or in tort or howsoever otherwise arising, including the use of this document in the preparation of your own financial books and records, and shall have no responsibility or liability to you or your affiliates or advisers or any other person for any loss or damage suffered or costs or expenses incurred (whether direct or consequential) by any person arising out of or in connection with the provision of this document to you, howsoever loss or damage is caused or costs or expenses are incurred. Absa, its affiliates and the individuals associated therewith may (in various capacities) have positions or deal in transactions or securities (or related derivatives) identical or similar to those described herein.
Absa Bank Limited is a registered bank in South Africa. Copyright in this document is proprietary to Absa Bank Limited and is confidential, and no part hereof may be reproduced, distributed or transmitted without the prior written permission of Absa Bank Limited.
Absa Bank Limited is an authorised Financial Services and Registered Credit Provider, NCRCP7.
'''
DISCLAIMER_SBL_MARGIN_CALL = '''All Securities Lending Transactions between yourself and ABSA Bank Limited ("ABSA") shall be promptly confirmed by ABSA by Confirmation exchanged electronically. Unless you object to the terms and of the Securities Lending Transaction contained in the Confirmation within 24 hours of receipt thereof, the terms of such Confirmation shall be deemed correct and accepted absent manifest error. Furthermore, please note that this confirmation is electronically generated and requires no signature by ABSA.
'''
DISCLAIMER_SBL_DIVIDEND_NOTIFICATION = '''Corporate and Investment Banking - Securities Borrowing & Lending Operations Team
The Securities Borrowing & Lending Operations Team of Absa Corporate and Investment Banking, a division of Absa Bank Limited, with company registration number: 1986/004794/06 (ABSA) has prepared this
document, for information purposes only. ABSA provides this document to you at your specific request. Any information in this document is indicative, subject to change, not intended to be an offer
or solicitation for the purchase, sale, assignment, settlement or termination of any financial instrument or product, and is provided for reference purposes only. This information is not intended as an
indicative price or quotation, and does not imply that a market exists for any financial instrument or product discussed herein; it does not therefore reflect hedging and transaction costs, credit
considerations, market liquidity or bid and offer spreads.
ABSA does not represent that any value(s) in this document directly correlate with current or future values. In respect of information which is stated to have been obtained from or is based on trade
and statistical services or other third-party sources, ABSA does not make any representation or give any warranty in respect of, the adequacy, accuracy, correctness or completeness of such
information contained or referenced in this document. Any data or information based on past financial returns, modelling or back-testing contained in this document is no indication as to any future
financial returns. ABSA makes no representations in respect of the assumptions or the accuracy or completeness of any modelling or back-testing. All opinions and estimates are given by ABSA as
of the date hereof and are subject to change. The value of any financial Instrument or product or any investment may fluctuate as a result of market changes. The information in this document is
not intended to predict actual results and no assurances are given with respect thereto. Where ABSA expresses a view in this document, such view is expressed as at the date hereof and subject
to the limited scope of the assumptions and methodology set out herein. This document has not been prepared in accordance with the standards and practice of any professional body in any
jurisdiction and does not, and is not intended to, constitute an accounting, legal or tax opinion or any other form of professional advice from ABSA. This document is not intended to be legally
binding. Neither the recipient nor its affiliates or advisers or any other third person may rely on the information contained herein. ABSA does not, through this document or the views expressed
herein, owe or accept any responsibility or liability to the recipient or its affiliates or advisers or any other third person who receives this document, whether in contract or in delict (tort) or howsoever
otherwise arising, including, without limitation, the use of the information contained in this document in the preparation of any financial statements and records. ABSA disclaims any ,liability to the
recipient or its affiliates or advisers or any other third person receiving this document for any loss or damage suffered or costs or expenses incurred (whether direct, indirect or consequential) by
any one arising out of or in connection with the provision of this document, howsoever such loss or damage is caused or costs or expenses are incurred.
ABSA, its affiliates and the individuals associated therewith may (in various capacities) have positions or deal in transactions or securities (or related derivative instruments) identical or similar to
those described herein, and therefore the recipient of this document may be exposed to potential conflicts of interest, although policies and procedures have been implemented which seek to
resolve any conflicts of interest fairly.
Absa Bank Limited is a licensed Financial Services Provider and a registered Credit Provider (with registration number: NCRCP7) in the Republic of South Africa (all rights reserved). Copyright in
this document is owned by Absa Bank Limited and is confidential, and no part hereof may be reproduced, distributed or transmitted without the prior written permission of Absa Bank Limited.
'''


XSLT_NAME_DEFAULT = 'XMLReportStatements'
XSLT_NAME_SBL = 'XMLReportStatementsSBL'
XSLT_NAME_WIDE = 'XMLReportStatementsWide'

VALID_SBL_STATUS = (
    'FO Confirmed',
    'BO Confirmed',
    'BO-BO Confirmed',
)


EMAIL_UNDELIVERED = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style type="text/css">
a:link
    {color:blue;
    text-decoration:underline;
    text-underline:single;
}
</style>
</head>

<body style="font-size:12px; font-family:Verdana; line-height:20px">

<p>%s</p>

</body></html>
"""

EMAIL_CLIENT_VALUATIONS = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style type="text/css">
a:link
    {color:gray;
    text-decoration:none;
}
</style>
</head>

<body style="font-size:12px; font-family:Verdana; line-height:20px; color:gray">

<p><b>Dear Valued Customer</b></p>

<p>Attached is your %s as at %s.</p>

<p>Absa was authorised as an Over the counter Derivatives Provider on 1 September 2020 and is accordingly required to comply with the Conduct Standard for Authorised OTC Derivative Providers (published under the Financial Markets Act 19 of 2012) (&quot<b>the Conduct Standard</b>&quot).  In terms of the Conduct Standard, Absa is required to send portfolio data to you to enable the identification, at an early stage, of any discrepancies in material terms of non-centrally cleared OTC derivative transactions, including valuations.  Hence we are sending you Valuation Statement to enable Absa to perform portfolio reconciliation with you.  Please let us know if there is any discrepancy in any material term of the OTC derivatives transactions and valuations in the Valuation Statement and we will endeavor to resolve such discrepancies as soon as possible.</p>

<p>If you are not the correct person to be receiving this portfolio data, please send us the correct contact details. Should you have any queries or concerns related to this email, other than the raising of discrepancies, please contact your relevant relationship manager at Absa.</p>

<p>Yours sincerely,</p>

<p>Absa | Client Valuations Post Trade Services<br>+27 11 895 7444<br>xraClientValuations1@absa.africa</p>

</body></html>
"""

EMAIL_CLIENT_SBL = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style type="text/css">
a:link
    {color:gray;
    text-decoration:none;
}
</style>
</head>

<body style="font-size:12px; font-family:Verdana; line-height:20px; color:gray">

<p><b>Dear Valued Customer</b></p>

<p>Attached is your %s.</p>

</body></html>
"""

EMAIL_CLIENT_SBL_COLL = """<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml">
<head>
<style type="text/css">
a:link
    {color:gray;
    text-decoration:none;
}
</style>
</head>

<body style="font-size:12px; font-family:Verdana; line-height:20px; color:gray">

<p>Good day,</p>

<p>Please find attached %s.</p>

<p>Please confirm if in agreement.</p>

<p>SBL Collateral Management Team<br>Hotline: +27102454223<br>xraeqdcollateralmana@absa.africa</p>

<p>Escalation :       Shaun du Plessis - +27117727560</p>

</body></html>
"""
