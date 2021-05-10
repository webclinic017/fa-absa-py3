'''
Implementation of Murabaha uploader in Python -- object generator
which creates instrument and trade objects and provides a generator
to feed processor. 

Project:    Murabaha Uploader
Department: Markets Structuring
Requester:  Gisella Nicola Bascelli
Developer:  Peter Fabian
CR Number:  CHNG0001979991


HISTORY
=============================================================================================
Date        CR number       Developer       Description
---------------------------------------------------------------------------------------------
2014-08-14  CHNG0002267615  Nico Louw   Changed fwd_deposit method to only book one FRN/depo
                                        instead of two, and corrected error when getting the next 
                                        order number for an instrument.
                                        
---------------------------------------------------------------------------------------------

'''
import acm, ael
import xlrd
import Structured_murabaha_instrument
import Structured_murabaha_trade
import Structured_murabaha_data_prvdr

class MurabahaInstrumentNameStore(object):
    """ Purpose: When the instruments are created, we want them to have unique names
        so we need to see if there are any similar instruments in Front
        plus we need to count the instruments in current upload.
        Since the data providers and individual instruments are represented by 
        individual classes, we need a place to store the info above ins/data 
        providers level.
    """
    def __init__(self):
        self._ins_names_count = {}
    
    def next_ord_no_for_ins(self, base_name):
        """ First try to find the base_name in Front Arena. 
            If it does not exist, return 0 (and the resulting
            name can be created without #N at the end).
            
            If the base name already exists in Front, 
            start searching until we find N such that
            base_name#N does not exist and we return N.
            
            This search in Front is done only the first time the script runs,
            as we store the N in a dict and increment each time
            this function is called with the same base_name.
            
            We assume that if there is no ins with base_name
            or base_name#(N-1) in Front, there also won't be any base_name#N
            instruments.
        """
        if base_name not in self._ins_names_count:
            ins = acm.FInstrument[base_name]
            if not ins:
                self._ins_names_count[base_name] = 2
                return 0
            
            ord_ = 2
            while ins:
                ins = acm.FInstrument[base_name + "#%s" % ord_]
                ord_ += 1
            
            self._ins_names_count[base_name] = ord_ - 1
            
        current_ord_no = self._ins_names_count[base_name]
        # add +1 to prepare for the next instrument with same base name 
        self._ins_names_count[base_name] += 1
        # return the original value before the bump 
        return current_ord_no
        

class MurabahaGenerator(object):
    """ Provide a generator of objects based on input Excel file
        
        Murabaha transaction consists of the following obejcts:
        1. OTC Forward hedge -- instrument + trade
        2. If the user chooses to hedge,
            i) Fwd Deposit + trade 
            ii) Swap + trade
            iii) Internal Deposit + trade
        3. If the user chooses to create one, create a Zero Coupon Bond + trade
    """
    def __init__(self, file_name, ins_name_storage, logger):
        self.excel_book = xlrd.open_workbook(file_name)
        self.logger = logger
        # fetch metadata from Excel file -- which instruments and 
        # trades to create
        self.metadata = Structured_murabaha_data_prvdr.MurabahaMetaDataProvider(self.excel_book)
        
        # Ordered list of created instruments and trades
        # used also to cross reference objects later, etc.
        self.instruments = []
        self.trades = []
        
        self.ins_name_storage = ins_name_storage
    
    def otc_fwd_hedge(self):
        """ Create OTC Future/Forward hedge instrument and trade
        """
        data_provider = Structured_murabaha_data_prvdr.FwdHedgeExcelDataProvider(self.excel_book)
        instr = Structured_murabaha_instrument.FwdHedge(data_provider, self.ins_name_storage, self.logger)
        instr.acm_ins.RegisterInStorage()
        trade = Structured_murabaha_trade.FwdHedgeTrade(data_provider, instr, self.logger)
        return ([instr], [trade])
        
    def fwd_deposit(self, column):
        """ Create Fwd deposit instrument and trade inside Funding Desk
        """
        data_provider = Structured_murabaha_data_prvdr.FwdDepositExcelDataProvider(self.excel_book, column)
        instr = Structured_murabaha_instrument.FwdDeposit(data_provider, self.ins_name_storage, self.logger)
        trade_fund_desk = Structured_murabaha_trade.FwdDepositTradeFundingDesk(data_provider, instr, self.logger)
        return ([instr], [trade_fund_desk])
    
    def murabaha_swap(self, column):
        """ Create Swap instrument and trade
        """
        data_provider = Structured_murabaha_data_prvdr.MurabahaSwapExcelDataProvider(self.excel_book, column)
        instr = Structured_murabaha_instrument.MurabahaSwap(data_provider, self.ins_name_storage, self.logger)
        trade = Structured_murabaha_trade.MurabahaSwapTrade(data_provider, instr, self.logger)
        return ([instr], [trade])
    
    def internal_deposit(self, column):
        """ Create OTC Future/Forward hedge instrument and trade
        """
        data_provider = Structured_murabaha_data_prvdr.InternalDepositExcelDataProvider(self.excel_book, column)
        instr = Structured_murabaha_instrument.InternalDeposit(data_provider, self.ins_name_storage, self.logger)
        trade = Structured_murabaha_trade.InternalDepositTrade(data_provider, instr, self.logger)
        return ([instr], [trade])
    
    def client_deposit(self, column):
        """ Create Client Deposit instrument and trade
        """
        data_provider = Structured_murabaha_data_prvdr.InternalDepositExcelDataProvider(self.excel_book, column)
        instr = Structured_murabaha_instrument.ClientDeposit(data_provider, self.ins_name_storage, self.logger)
        trade = Structured_murabaha_trade.ABSADepositTrade(data_provider, instr, self.logger)
             
        return ([instr], [trade])
        
    
    def _create_objects(self):
        """ Create all the internal objects according to spec from Excel file
            and populate lists of instruments and trades so they can 
            generate the final list of objects
        """
        fwd_hedge_inss, fwd_hedge_trds = self.otc_fwd_hedge()
        self.instruments.extend(fwd_hedge_inss)
        self.trades.extend(fwd_hedge_trds)
        
        column = self.metadata.hedge_start_column
        for hedge in self.metadata.hedge_flags():
            if hedge:
                fwd_deposit_inss, fwd_deposit_trds = self.fwd_deposit(column)
                self.instruments.extend(fwd_deposit_inss)
                self.trades.extend(fwd_deposit_trds)
                
                swap_inss, swap_trds = self.murabaha_swap(column)
                self.instruments.extend(swap_inss)
                self.trades.extend(swap_trds)
                
                internal_deposit_inss, internal_deposit_trds = self.internal_deposit(column)
                self.instruments.extend(internal_deposit_inss)
                self.trades.extend(internal_deposit_trds)
            
            column += 1
        
        column = self.metadata.zcb_start_column
        for zcb in self.metadata.zcb_flags():
            if zcb:
                zcb_inss, zcb_trds = self.client_deposit(column)
                self.instruments.extend(zcb_inss)
                self.trades.extend(zcb_trds)
                  
            column += 1
        
    def get_list_of_objects(self):
        """ Return generator of objects to be created
        """
        self._create_objects()
        
        for ins in self.instruments:
            yield ins

        for trd in self.trades:
            yield trd
