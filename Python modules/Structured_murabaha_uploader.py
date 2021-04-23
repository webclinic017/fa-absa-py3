'''
Implementation of Murabaha uploader in Python -- entry point

Project:    Murabaha Uploader
Department: Markets Structuring
Requester:  Gisella Nicola Bascelli
Developer:  Peter Fabian
CR Number:  CHNG0001979991


HISTORY
===============================================================================
Date        CR number   Developer       Description
-------------------------------------------------------------------------------

-------------------------------------------------------------------------------

'''

import acm
import FRunScriptGUI
from at_feed_processing import FeedProcessor
import at_choice
import at
import at_calculation_space
import Structured_murabaha_instrument
import Structured_murabaha_trade
import Structured_murabaha_obj_gen
import csv

output_trades = []

class MurabahaUploader(FeedProcessor):
    """ Implementation of Murabaha transaction in Python.
        
        Subclass of at_feed_processor which creates several instruments
        and trades based on the input Excel config file  
    """
    def __init__(self, input_file, output_file, open_created_trades):
        super(MurabahaUploader, self).__init__()
        # input file containing all the info for the upload
        self.input_file = input_file
        # output is written to this file
        self.output_file = output_file
        # flag -- open new trades after they have been created 
        self.open_created_trades = open_created_trades
        
    class Log(object):
        """ A small wrapper around at_feed_processor's logging ability
        
            Adds just one feature -- logging levels
        """
        INFO = 1
        DEBUG = 2
        TRACE = 3
        def __init__(self, log_level = 1):
            self._log_level = log_level
            self._log_fn = FeedProcessor._log
            
        def log(self, msg, msg_level = 1):
            if msg_level <= self._log_level:
                self._log_fn(msg)
    
    def _load(self):
        """ Load information from input file to internal data structures
        """
        self._full_path = self.input_file
        self._logger = self.Log(self.Log.INFO)
        ins_name_storage = Structured_murabaha_obj_gen.MurabahaInstrumentNameStore()
        self.records = Structured_murabaha_obj_gen.MurabahaGenerator(self._full_path, ins_name_storage, self._logger)
    
    def _generate_records(self):
        """ Generate and prepare objects for processing in _process method
        """
        return self.records.get_list_of_objects()
    
    def _process_object(self, object_, dry_run):
        object_.get_variable_data()
        
        if not dry_run:
            self._logger.log("Committing object %s" % (object_.__class__.__name__))
            object_.commit()
    
    def _report_created_objects(self, dry_run):
        """ Print basic info about created objects to console 
        """
        if dry_run:
            return
        
        for trd in self.records.trades:
            self._logger.log("%s Trade %s created on Instrument %s" % 
                             (trd.identifier(), trd.acm_trd.Name(), 
                              trd.acm_trd.Instrument().Name())
                             )
            if self.open_created_trades:
                acm.StartApplication("Stock", trd.acm_trd)
    
    def _create_output_file(self, dry_run, swap_trades):
        """ Create output csv file which contains Ids of created
            instruments and trades plus PV for swaps
            
            As we don't have a python lib to support writing 
            the info back to original Excel file, a separate 
            csv file is craeted.
        """
        if dry_run:
            try:
                f = open(self.output_file, 'wb')
            except Exception as e:
                self._logger.log("Could not create output file %s: %s" 
                                 % (self.output_file, e))
            return
        
        field_names = ["Note", "Instrument", "Trade", "PV"]
        rowdicts = []
        try:
            for trd in self.records.trades:
                rowdicts.append({
                       "Note"       : trd.identifier(),
                       "Instrument" : trd.acm_trd.Instrument().Name(),
                       "Trade"      : trd.acm_trd.Oid(),
                       "PV"         : at_calculation_space.calculate_value("FTradeSheet", trd.acm_trd, "Present Value").Number() 
                                        if trd.identifier() == Structured_murabaha_trade.MurabahaSwapTrade.identifier() else ""
                       })
            
            
            for trd in output_trades:
                rowdicts.append({
                       "Note"       : "Payment Swap",
                       "Instrument" : trd.Instrument().Name(),
                       "Trade"      : trd.Oid(),
                       "PV"         : at_calculation_space.calculate_value("FTradeSheet", trd, "Present Value").Number()                                       
                       })
                       
            with open(self.output_file, 'wb') as f:
                writer = csv.DictWriter(f, field_names)
                # write header
                writer.writerow(dict([(fn, fn) for fn in field_names]))
                # write data
                writer.writerows(rowdicts)
            self._logger.log("Output file created at %s" % (self.output_file))
        except IOError as e:
            self._logger.log("Could not create output file %s, redirecting to console" % (self.output_file))
            self._logger.log("====="*20)
            print(";".join(field_names))
            for row in rowdicts:
                ordered_row = []
                for fn in field_names:
                    ordered_row.append(row[fn])
                print(";".join([str(value) for value in ordered_row]))
            self._logger.log("====="*20)
            
    
    # TODO: where to put these three functions?
    def _amend_YourRef(self):
        """ Set YourRef attribute for swap trades to their mirrors
            
            YourRef is a string and since we don't know the trade numbers
            before the transaction is committed we can only set this
            after the transaction
        """
        swap_trades = [trd for trd in self.records.trades 
                       if trd.identifier() == Structured_murabaha_trade.MurabahaSwapTrade.identifier()]
        for trade in swap_trades:
            mirror_trd = trade.acm_trd.MirrorTrade()
            trade.acm_trd.YourRef(mirror_trd.Oid())
            mirror_trd.YourRef(trade.acm_trd.Oid())
            trade.acm_trd.Commit()
            mirror_trd.Commit()
            
    def _amend_AddInfo(self):
        """ Change the add info for mirror trades of forward deposits
        
            Since the mirror is only created when the trade
            is committed at the end of the transaction, the add info 
            can only be amended afterwards
        """
        self._logger.log("Amending add info on mirrors of deposits")
        fwd_deposit_trades = [trd for trd in self.records.trades 
                              if trd.ins.identifier() == Structured_murabaha_instrument.FwdDeposit.identifier()]
        for trade in fwd_deposit_trades:
            self._logger.log("\tTrade %s" % (trade.acm_trd.MirrorTrade().Oid()))
            at.addInfo.save_or_delete(trade.acm_trd.MirrorTrade(), "Funding Instype", "CL Roll-up")
    
    def _amend_TrxTrade(self):
        """ Set TrxTrade for Fwd hedge, fwd deposits, swaps and zeroes to fwd hedge trade
            
            Front Arena doesn't handle trx ref correctly in 
            a transaction -- need to fix it here...
        """
        self._logger.log("Setting transaction reference for trades")
        fwd_hedge = [trd for trd in self.records.trades 
                     if trd.identifier() == Structured_murabaha_trade.FwdHedgeTrade.identifier()][0]
                     
        trades = [trd for trd in self.records.trades 
                  if (trd.ins.identifier() == Structured_murabaha_instrument.FwdDeposit.identifier()
                      or trd.identifier() in (
                            Structured_murabaha_trade.MurabahaSwapTrade.identifier(), 
                            Structured_murabaha_trade.ABSADepositTrade.identifier(),
                            Structured_murabaha_trade.InternalDepositTrade.identifier()
                            )
                      )
                      ]
        trades.append(fwd_hedge)
        
        for trade in trades:
            trade.acm_trd.TrxTrade(fwd_hedge.acm_trd)
            self._logger.log("\tTrade %s" % (trade.acm_trd.Oid()))
            trade.acm_trd.Commit()
            
    def _create_deposit_payment(self):
        trades = [trd for trd in self.records.trades 
                    if trd.ins.identifier() == Structured_murabaha_trade.ABSADepositTrade.identifier()]
        
                
        for trade in trades:
            acm_trade = trade.acm_trd
            
            external_trade = acm_trade 
            
            payment = acm.FPayment()
        
            payment.Trade(external_trade)
            payment.Party(external_trade.Acquirer ())
            payment.Type('Premium')
            payment.Amount(-1*external_trade.Quantity()*1000000)
            payment.Currency(external_trade.Currency())
            payment.PayDay(external_trade.ValueDay())
            payment.ValidFrom(acm.Time.DateToday())
            payment.Text('fwd prem')
            
            try:            
                payment.Commit()
                external_trade.Commit() 
            except Exception as e:
                print('Error: Cannot create payment :', e)
    
    def _create_fwd_hedge_payments(self):
    
        fwd_hedge = [trd for trd in self.records.trades 
                         if trd.identifier() == Structured_murabaha_trade.FwdHedgeTrade.identifier()][0]
        
        trades = [trd for trd in self.records.trades 
                            if trd.ins.identifier() == Structured_murabaha_trade.ABSADepositTrade.identifier()]  
        
        swap_instrument = acm.FSwap['AIB_DAY1_FEE_CAPTURE']
        now = acm.Time.DateToday()
        
        for trade in trades:
            
            acm_trade = trade.acm_trd
            
            swap_trade = acm.FTrade()
            swap_trade.RegisterInStorage()
            swap_trade.Instrument(swap_instrument)
            swap_trade.Acquirer(acm.FParty['ACQ STRUCT DERIV DESK'])
            swap_trade.Nominal(1)
            swap_trade.Portfolio(acm.FPhysicalPortfolio['ST Islamic Hedges'])
            swap_trade.Currency(swap_instrument.Currency())
            swap_trade.Counterparty(acm.FParty['ABSA BANK LTD AIB'])          
            swap_trade.TradeTime(now)
            swap_trade.AcquireDay(now)
            swap_trade.ValueDay(now)
            swap_trade.Status('Simulated')
            swap_trade.Trader(acm.User())
            swap_trade.TrxTrade(fwd_hedge.acm_trd)
            swap_trade.Commit()
            
            payment_inflow = acm.FPayment()
            payment_inflow.Trade(swap_trade)
            payment_inflow.Party(swap_trade.Acquirer())
            payment_inflow.Type('Cash')
            payment_inflow.Amount(acm_trade.Quantity()*1000000)
            payment_inflow.Currency(acm_trade.Currency())
            payment_inflow.PayDay(acm_trade.ValueDay())
            payment_inflow.ValidFrom(acm_trade.TradeTime())
            payment_inflow.Text('internal move to AC')
            
            payment_outflow = acm.FPayment()
            payment_outflow.Trade(swap_trade)
            payment_outflow.Party(acm_trade.Counterparty())
            payment_outflow.Type('Cash')
            payment_outflow.Amount(acm_trade.Text2())
            payment_outflow.Currency(acm_trade.Currency())
            payment_outflow.PayDay(acm_trade.TradeTime())
            payment_outflow.ValidFrom(acm_trade.TradeTime())
            payment_outflow.Text('AIB T0 Cash')
            
            try:            
                payment_inflow.Commit()
                payment_outflow.Commit()
                swap_trade.Commit()
                output_trades.append(swap_trade)
            except Exception as e:
                print('Error: Cannot create payment :', e)            
    
        
    def _update_query_folder(self):
        """ Create/Replace existing 'Shariah hedges' query folder
            with a query folder which selects swaps created in the current 
            upload.
            
            Side note: couldn't figure out how to amend trade filter 
            from python code (even when using FMatrix, etc.)
        """
        swap_trdnbrs = [trd.acm_trd.Oid() for trd in self.records.trades 
                        if (trd.identifier() == Structured_murabaha_trade.MurabahaSwapTrade.identifier())
                      ]
        qf_name = 'Shariah hedges'
        qf = acm.FStoredASQLQuery[qf_name]
        if not qf:
            qf = acm.FStoredASQLQuery()
            qf.Name(qf_name)
            
        query = acm.CreateFASQLQuery('FTrade', 'OR')
        for trdnbr in swap_trdnbrs:
            query.AddAttrNode('Oid', 'EQUAL', trdnbr)
        
        qf.Query(query)
        qf.Commit()
        self._logger.log("Query Folder '%s' updated" % qf_name)
    
    def _generate_deposit_cashflows(self):
        """ Generate resets and correct cash flow properties.
            
            Deposit instruments are created without the resets by default
            for some reason, running this in post process fixes the problem.
        """
        self._logger.log("Generating deposit cashflows")
        deposits = [ins.acm_ins for ins in self.records.instruments 
                     if ins.acm_ins.InsType() == "Deposit"]
        for deposit in deposits:
            self._logger.log("\tDeposit %s" % (deposit.Name()))
            for leg in deposit.Legs():
                leg.GenerateCashFlows(None)
    
    def _post_process(self, dry_run):
        """ Perform work that can't be done in the transaction together with the 
            creation of the objects as it requires db ids of the objects
        """
        if dry_run:
            return
        
        acm.BeginTransaction()
        try:
            # amend YourRef references for swaps 
            self._amend_YourRef()
            # amend add info for mirrors of Fwd deposits
            self._amend_AddInfo()
            # set trans ref for fwd deposits, swaps and zero coupon bonds
            self._amend_TrxTrade()
            # update trade filter with currrent swaps
            self._update_query_folder()
            # genrate cash flows and resets for deposits
            self._generate_deposit_cashflows()
            # create additional payment for client deposit
            self._create_deposit_payment()
            # create additional payments for the forward trade
            self._create_fwd_hedge_payments()
            acm.CommitTransaction()
        except Exception as e:
            self._logger.log(e)
            acm.AbortTransaction()
            raise
        
    def _process(self, dry_run):
        self._logger.log("Processing " + self._full_path)
        acm.BeginTransaction()
        try:
            for record in self._generate_records():
                self._process_object(record, dry_run)
            acm.CommitTransaction()
        except Exception as ex:
            self._logger.log(ex)
            self.errors.append(ex)
            acm.AbortTransaction()
            raise
    
        self._post_process(dry_run)
        self._create_output_file(dry_run, output_trades)
        # this might fail because sometimes opening created trades
        # results in runtime error/Front crashing miserably,
        # so run it as a last item here
        self._report_created_objects(dry_run)
    
    def _finish(self):
        self._logger.log("Upload finished successfully")
        
        
ratesFileSelection = FRunScriptGUI.InputFileSelection("")
ratesFileSelection.SelectedFile(r'y:\Jhb\Official\Structured Trading Sales\UAT\Murabaha Upload Trades.xls')

ael_variables = MurabahaUploader.ael_variables()
ael_variables.add("input_file", label='Input File',
    default=ratesFileSelection, cls=ratesFileSelection, multiple=True)
ael_variables.add("output_file", label='Output File',
    default=r'c:\temp\Murabaha Uploaded Trades.csv', cls='string')
ael_variables.add("open_created_trades", label='Open Created Trades',
    default=False, cls='bool', collection=(True, False))

def ael_main(params):
    hm = MurabahaUploader(str(params['input_file'].SelectedFile()), params['output_file'], params['open_created_trades'])
    hm.process(params['dry_run'])


# params = {
#           "input_file"          : r'c:\Users\fabianpe\AppData\Roaming\Microsoft\Structured Trading Sales\UAT\Murabaha Upload Trades.xls',
#           "output_file"         : r'c:\temp\Murabaha Uploaded Trades.csv',
#           "open_created_trades" : False,
#           "dry_run"             : False,
#           }
#ael_main(params)
