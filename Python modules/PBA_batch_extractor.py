"""
Project: Prime Brokerage Africa (PBA)
Department: Prime Services
Requester: Francois Henrion
Developer: Ondrej Bahounek, Lester Williams
CR Number: 3506685 (Initial Deployment)

Description:
    This script duplicate trades in Prime Broking portfolio.
    Run as a batch.
    Books trades into fund's stock reporting portfolio.
    Sets original trade's text1 from "PB_Agency_Uploaded" to "PB_Agency_Processed"
    and contracts to a new trade.
 
Prerequisites:
    Run csv uploader
    User must confirm Agency1 trade:
        - set status to FO Confirmed
        - move it to Agency2 portoflio
        - set Acquirer
                    
Result:
    New trade booked in fund's reporting portfolio with BO status.

History:
Date       CR Number Who                    What
"""

import acm
import ast
import at_addInfo
from PBA_csv_uploader import COMMISSION_TEXT as COMMISSION_TEXT_OLD

COMMISSION_TEXT = "Commission"

# Portfolio to select from
FROM_AGENCY_PORTFOLIO_ID = "PBA_CR_LIVE"
STOCK_PORTF_TEMPLATE = "PBA_CE_FF_%(alias)s_CR"

   
def get_PBA_agency2_trades():
    """Get all trades that need to be extracted.
    
    Trades for all PBA clients which:
        -- are in Agency2 portfolio
        -- have FO Confirmed status
        -- text1 indicatiting that trade was not processed by this script yet
    """
    
    portfs = acm.FPhysicalPortfolio.Select('name like "PBA_*_Agency2_CR"')
    all_trades = []
    for p in portfs:
        trades = acm.FTrade.Select('status="FO Confirmed" and portfolio="%s" and text1="PBA_Agency_Uploaded"' %p.Name())
        all_trades.extend(trades)
    return all_trades

def clone_PBA_trades():
    """Book reporting trades.
    
    These will be clones of Agency trades.
    Same properties:
        time
    New properties:
        quantity, price
    Amended properties:
        portfolio, status
    """
    
    pba_trades  = get_PBA_agency2_trades()
    print("Extractor: Trades found: {0}".format(len(pba_trades)))
    
    trade_oids = [trd.Oid() for trd in pba_trades]

    for trd in trade_oids:
        
        trade = acm.FTrade[trd]
        clone = trade.Clone()
        
        print("")
        print("Extracting Agency trade:", trade.Oid())
        
        dct = ast.literal_eval(trade.Text2())
        qty = float(dct.get('Qty')) if dct.get('Qty') else 0
        prc =  float(dct.get('Prc')) if dct.get('Prc') else 0
        clone.Quantity(qty)
        clone.Price(prc)
        clone.Premium(qty * prc)
        if qty > 0:
            clone.Premium(-clone.Premium())
        
        alias = trade.Portfolio().AdditionalInfo().PS_ClientFundName()        
        clone.Portfolio(acm.FPhysicalPortfolio[STOCK_PORTF_TEMPLATE % {'alias':alias}])
        clone.Status('BO Confirmed')
        clone.ContractTrdnbr(trade.Oid())
        clone.Text1('')
        clone.Text2('')
        clone.Commit()
        print("Reporting trade created: {0}".format(clone.Oid()))
            
        add_payments(clone, trade)
        set_addinfo(clone, trade)

        # Change flag so the original trade is not processed again
        trade.Text1('PBA_Agency_Processed')
        trade.ContractTrdnbr(clone.Oid())
        trade.Commit()

def add_payments(clone, origtrade):
    
    payments = {}
    for payment in clone.Payments():
        payments[payment.Text()] = payment
        
    payment_commission = payments[COMMISSION_TEXT_OLD]
    commission = origtrade.AdditionalInfo().Broker_Commission()
    if not commission:
        commission = 0
    payment_commission.Amount(-float(commission))
    payment_commission.Text(COMMISSION_TEXT)
    
    fees = origtrade.AdditionalInfo().Fees()
    if not fees:
        fees = 0
    if not payments.has_key("Fees"):
        payment_fee = acm.FPayment()
    else:
        payment_fee = payments["Fees"]
    payment_fee.Amount(-float(fees))
    payment_fee.Text("Fees")
    payment_fee.Currency(origtrade.Instrument().Currency())
    payment_fee.Type("Cash")
    payment_fee.Party(payment_commission.Party())
    payment_fee.PayDay(origtrade.AcquireDay())
    payment_fee.ValidFrom(origtrade.TradeTime())
    clone.Payments().Add(payment_fee)
    clone.Commit()
    print("Trade {0}: Commission Payment added (value = {1})".format(
        clone.Oid(), payment_commission.Amount()))
    print("Trade {0}: Fees Payment added (value = {1})".format(
        clone.Oid(), payment_fee.Amount()))
        
def set_addinfo(clone, origtrade):

    at_addInfo.save(clone, "Gross Price", origtrade.AdditionalInfo().Gross_Price())
    at_addInfo.save(clone, "Country", origtrade.AdditionalInfo().Country())
    at_addInfo.save(clone, "Gross Consideration", origtrade.AdditionalInfo().Gross_Consideration())
    at_addInfo.save(clone, "Broker Commission", origtrade.AdditionalInfo().Broker_Commission())
    at_addInfo.save(clone, "Fees", origtrade.AdditionalInfo().Fees())
    at_addInfo.save(clone, "PB_Fully_Funded", origtrade.AdditionalInfo().PB_Fully_Funded())
    print("Trade {0}: Additional Info added".format(clone.Oid()))

def main():
    print("")
    print("Extractor: Started")
    print("")
    clone_PBA_trades()
    print("")
    print("Extractor: Completed successfully")
    
main()