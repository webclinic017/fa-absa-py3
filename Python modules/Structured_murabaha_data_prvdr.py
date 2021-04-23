'''
Implementation of Murabaha uploader in Python -- Excel data provider
which provides input data to trades and instruments created by 
generator.

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
import xlrd
import datetime


class MurabahaExcelDataProvider(object):
    """ Parent for Excel data provider, contains basic universal functions
        for reading data using xlrd.
    """
    def __init__(self, excel_workbook):
        self.excel_book = excel_workbook
        self.trade_upload_sheet = self.excel_book.sheet_by_name('Trade Upload')
        self.trade_details_sheet = self.excel_book.sheet_by_name('Trade Details')
    
    def _cell_val(self, cell, expected_type=None):
        """ Convert data from Excel to Python format:
            - dates to Python date/datetime
            - boolean cells to Python bool
            - strings are stripped and converted from utf to regular str 
            - for empty cells return None
        """
        if expected_type and cell.ctype != expected_type:
            raise ValueError("Incorrect cell format")
        
        if cell.ctype == xlrd.XL_CELL_DATE:
            datetuple = xlrd.xldate_as_tuple(cell.value, self.excel_book.datemode)
            if datetuple[3:] == (0, 0, 0):
                return datetime.date(datetuple[0], datetuple[1], datetuple[2])
            return datetime.date(datetuple[0], datetuple[1], datetuple[2], datetuple[3], datetuple[4], datetuple[5])
        if cell.ctype == xlrd.XL_CELL_EMPTY:
            return None
        if cell.ctype == xlrd.XL_CELL_BOOLEAN:
            return cell.value == 1
        if cell.ctype == xlrd.XL_CELL_TEXT:
            return str(cell.value).strip()
        # this is not really needed, but better be explicit
        if cell.ctype == xlrd.XL_CELL_NUMBER:
            return cell.value
            
        return cell.value
    
    def _get_val(self, sheet, row, col, exc_msg, expected_type):
        try:
            val = self._cell_val(sheet.cell(row, col), expected_type)
            if val:
                return val
            else:
                raise ValueError("Error in row %s column %s: " % (row+1, col+1) + exc_msg)
        except Exception as e:
            raise ValueError("Error in row %s column %s: " % (row+1, col+1) + exc_msg)


class MurabahaMetaDataProvider(MurabahaExcelDataProvider):
    """ Provide information about which instruments and trades to create.
        This info is read from the top section of the Excel workbook
    """
    def __init__(self, excel_workbook):
        super(MurabahaMetaDataProvider, self).__init__(excel_workbook)
        # count from 0
        self.hedge_start_column = 3 
        self.zcb_start_column = 3
        
    def hedge_flags(self):
        values = self.trade_upload_sheet.row(3)
        # ignore first three columns + convert to bool
        flags = [self._cell_val(cell).upper() in ("YES", "TRUE") 
                 for cell in values[self.hedge_start_column:]]
        return flags
        
    def zcb_flags(self):
        values = self.trade_upload_sheet.row(4)
        # ignore first three columns + convert to bool
        flags = [self._cell_val(cell).upper() in ("YES", "TRUE") 
                 for cell in values[self.zcb_start_column:]]
        return flags
    
    
class FwdHedgeExcelDataProvider(MurabahaExcelDataProvider):
    def __init__(self, excel_workbook):
        super(FwdHedgeExcelDataProvider, self).__init__(excel_workbook)

    def client_name(self):
        return self._get_val(self.trade_upload_sheet, 1, 3, 
                             "Client name for Future/Forward not valid",
                             xlrd.XL_CELL_TEXT)
    
    def underlying(self):
        return self._get_val(self.trade_upload_sheet, 15, 3, 
                             "Underlying for Future/Forward not valid",
                             xlrd.XL_CELL_TEXT)
        
    def expiry_day(self):
        return self._get_val(self.trade_upload_sheet, 16, 3, 
                             "Expiry for Future/Forward not valid",
                             xlrd.XL_CELL_DATE)
    
    def counterparty(self):
        return self._get_val(self.trade_upload_sheet, 17, 3, 
                             "Counterparty for Future/Forward not valid",
                             xlrd.XL_CELL_TEXT)
        
    def quantity(self):
        return self._get_val(self.trade_upload_sheet, 18, 3, 
                             "Quantity for Future/Forward not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def price(self):
        return self._get_val(self.trade_upload_sheet, 19, 3, 
                             "Price for Future/Forward not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def trade_date(self):
        return self._get_val(self.trade_upload_sheet, 20, 3, 
                             "Trade Date for Future/Forward not valid",
                             xlrd.XL_CELL_DATE)
        
    def settlement_type(self):
        settleTypeLookup = {
            1: "Cash",
            2: "Physical Delivery",
        }
        # first get the dropdown value
        settleType = int(self._get_val(self.trade_details_sheet, 15, 2, 
                                       "Fwd settlement type not valid",
                                       xlrd.XL_CELL_NUMBER))
        # translate this to settlement type
        if settleTypeLookup[settleType]:
            return settleTypeLookup[settleType]
        else:
            raise ValueError("Fwd settlement type not found")
    
    def acquire_day(self):
        return self._get_val(self.trade_upload_sheet, 20, 3, 
                             "Acquire Day not found",
                             xlrd.XL_CELL_DATE)


class FwdDepositExcelDataProvider(MurabahaExcelDataProvider):
    def __init__(self, excel_workbook, column):
        super(FwdDepositExcelDataProvider, self).__init__(excel_workbook)
        self._column = column
    
    def spread(self):
        return self._get_val(self.trade_upload_sheet, 33, self._column, 
                             "Spread for fwd deposit not valid",
                             xlrd.XL_CELL_NUMBER)
        
    def start_day(self):
        return self._get_val(self.trade_upload_sheet, 28, self._column, 
                             "Start date for fwd deposit not valid",
                             xlrd.XL_CELL_DATE)
        
    def end_day(self):
        return self._get_val(self.trade_upload_sheet, 29, self._column, 
                             "End date for fwd deposit not valid",
                             xlrd.XL_CELL_DATE)
        
    def deposit_term(self):
        return self._get_val(self.trade_upload_sheet, 30, self._column, 
                             "Deposit term for fwd deposit not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def client_name(self):
        return self._get_val(self.trade_upload_sheet, 1, 3, 
                             "Client name for fwd deposit not valid",
                             xlrd.XL_CELL_TEXT)

    def trade_time(self):
        return self._get_val(self.trade_upload_sheet, 8, 3, 
                             "Trade time for fwd deposit not valid",
                             xlrd.XL_CELL_DATE)
    
    def acquire_day(self):
        return self.start_day()
    
    def premium(self):
        return self._get_val(self.trade_upload_sheet, 31, self._column, 
                             "Premium for fwd deposit not valid",
                             xlrd.XL_CELL_NUMBER)


class MurabahaSwapExcelDataProvider(MurabahaExcelDataProvider):
    def __init__(self, excel_workbook, column):
        super(MurabahaSwapExcelDataProvider, self).__init__(excel_workbook)
        self._column = column
    
    def client_name(self):
        return self._get_val(self.trade_upload_sheet, 1, 3, 
                             "Client name for swap not valid",
                             xlrd.XL_CELL_TEXT)
        
    def spread(self):
        return self._get_val(self.trade_upload_sheet, 33, self._column, 
                             "Spread for swap not valid",
                             xlrd.XL_CELL_NUMBER)
        
    def start_day(self):
        return self._get_val(self.trade_upload_sheet, 28, self._column, 
                             "Start date for swap not valid",
                             xlrd.XL_CELL_DATE)
        
    def end_day(self):
        return self._get_val(self.trade_upload_sheet, 29, self._column, 
                             "End date for swap not valid",
                             xlrd.XL_CELL_DATE)
        
    def deposit_term(self):
        return self._get_val(self.trade_upload_sheet, 30, self._column, 
                             "Deposit term for swap not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def fixed_rate(self):
        return self._get_val(self.trade_upload_sheet, 34, self._column, 
                             "Fixed rate for swap not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def deposit_amount(self):
        return self._get_val(self.trade_upload_sheet, 31, self._column, 
                             "Qty for swap not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def acquire_day(self):
        return self.start_day()
    
    def trade_time(self):
        return self._get_val(self.trade_upload_sheet, 8, 3, 
                             "Trade time for swap not valid",
                             xlrd.XL_CELL_DATE)


class InternalDepositExcelDataProvider(MurabahaExcelDataProvider):
    def __init__(self, excel_workbook, column):
        super(InternalDepositExcelDataProvider, self).__init__(excel_workbook)
        self._column = column
    
    def client_name(self):
        return self._get_val(self.trade_upload_sheet, 1, 3, 
                             "Client name for internal deposit not valid",
                             xlrd.XL_CELL_TEXT)
                             
    def counterparty(self):
        return self._get_val(self.trade_upload_sheet, 48, self._column, 
                             "Counterparty for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_TEXT)
        
    def start_day(self):
        return self._get_val(self.trade_upload_sheet, 28, self._column, 
                             "Start date for internal deposit not valid",
                             xlrd.XL_CELL_DATE)    
        
    def end_day(self):
        return self._get_val(self.trade_upload_sheet, 29, self._column, 
                             "End date for internal deposit not valid",
                             xlrd.XL_CELL_DATE)
        
    def deposit_term(self):
        return self._get_val(self.trade_upload_sheet, 30, self._column, 
                             "Deposit term for internal deposit not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def fixed_rate(self):
        return self._get_val(self.trade_upload_sheet, 34, self._column, 
                             "Fixed rate for internal deposit not valid",
                             xlrd.XL_CELL_NUMBER)
        
    def input_insid(self):
        return self._get_val(self.trade_upload_sheet, 27, self._column, 
                             "Input insid for internal deposit not valid",
                             xlrd.XL_CELL_TEXT)
    
    def premium(self):
        return self._get_val(self.trade_upload_sheet, 31, self._column, 
                             "Premium for internal deposit not valid",
                             xlrd.XL_CELL_NUMBER)
                             
    def _zero_bond_premium(self):
        return self._get_val(self.trade_upload_sheet, 54, self._column, 
                             "Premium for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def cash(self):
        return self._get_val(self.trade_upload_sheet, 31, self._column, 
                             "Premium for internal deposit not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def price(self):
        return self._get_val(self.trade_upload_sheet, 34, self._column, 
                             "Price for internal deposit not valid",
                             xlrd.XL_CELL_NUMBER)

    def acquire_day(self):
        return self.start_day()
    
    def trade_time(self):
        return self._get_val(self.trade_upload_sheet, 8, 3, 
                             "Trade time for internal deposit not valid",
                             xlrd.XL_CELL_DATE)


class ZeroBondExcelDataProvider(MurabahaExcelDataProvider):
    def __init__(self, excel_workbook, column):
        super(ZeroBondExcelDataProvider, self).__init__(excel_workbook)
        self._column = column
    
    def client_name(self):
        return self._get_val(self.trade_upload_sheet, 1, 3, 
                             "Client name for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_TEXT)
        
    def start_day(self):
        return self._get_val(self.trade_upload_sheet, 46, self._column, 
                             "Start date for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_DATE)
        
    def end_day(self):
        return self._get_val(self.trade_upload_sheet, 47, self._column, 
                             "End date for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_DATE)
                
    def input_insid(self):
        return self._get_val(self.trade_upload_sheet, 45, self._column, 
                             "Input insid for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_TEXT)
    
    def counterparty(self):
        return self._get_val(self.trade_upload_sheet, 48, self._column, 
                             "Counterparty for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_TEXT)
    
    def premium(self):
        return self._get_val(self.trade_upload_sheet, 51, self._column, 
                             "Premium for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def quantity(self):
        return self._get_val(self.trade_upload_sheet, 49, self._column, 
                             "Quantity for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_NUMBER)
    
    def acquire_day(self):
        return self._get_val(self.trade_upload_sheet, 50, self._column, 
                             "Acquire day for Zero Coupon Bond not valid",
                             xlrd.XL_CELL_DATE)

