from __future__ import print_function
import acm
import os
import re
import FAptReportUtils as utils
import FAptReportCommon
import FReportParser
import xml.etree.cElementTree as ElementTree
import FAptLauncher
import FLogger

logger = FLogger.FLogger.GetLogger('APT')

class PrimeReportWriter(object):

    MODULE_NAME = 'AMI APT'

    def __init__(self, portfolios=[], trade_filters=[], instruments=[], grouper=None):
        self.trading_sheet = acm.FPortfolioSheet()
        self.portfolios = portfolios
        self.trade_filters = trade_filters
        self.instruments = instruments
        self.grouper = grouper
        self.output = acm.FXmlReportOutput('')
        self.grid = acm.Report.CreateReport("test", self.output)
        self.config = acm.Report.CreateGridConfiguration(False, True)
        self.output.IncludeFormattedData(False)
        self.grid.OpenSheet(self.trading_sheet, self.config)
        self.grid_builder = self.grid.GridBuilder()
        self._insert_contents()
        self._insert_columns()
        self.grid.Generate()
        
    def _get_column_creators(self):
        context = acm.GetDefaultContext()
        module = context.GetModule(self.MODULE_NAME)
        column_extensions = module.GetAllExtensions('FColumnDefinition')
        column_names = acm.FArray().AddAll([column.Name() for column in column_extensions])
        return acm.GetColumnCreators(column_names, context)
        
    def _insert_columns(self):
        column_creators = self._get_column_creators()
        self.grid_builder.ColumnCreators().Clear()
        for index in range(column_creators.Size()):
            self.grid_builder.ColumnCreators().Add(column_creators.At(index))
        
    def _insert_contents(self):
        for item in self.portfolios+self.trade_filters+self.instruments:
            top_node = self.grid_builder.InsertItem(item)
            top_node.ApplyGrouper(self.grouper)
        
    def get_xml(self):
        return self.output.AsString()
    
    def get_parser(self):
        parser = FReportParser.Contents(None, self.get_xml())
        return parser

class AptColumns:
    #COMPOSIOTION COLUMNS
    RECON_ID_TYPE               = 'APT_Compositions_00_AptReconIdType'
    COMP_CURRENCY               = 'APT_Compositions_01_CompositionCurrency'
    COMP_DATE                   = 'APT_Compositions_02_Date'
    COMP_ID_TYPE                = 'APT_Compositions_03_IdType'
    COMP_ID                     = 'APT_Compositions_04_Id'
    ASSET_UNITS                 = 'APT_Compositions_05_Units'
    ASSET_PRICE                 = 'APT_Compositions_06_Price'
    FOREIGN_CURRENCY            = 'APT_Compositions_07_ForeignCurrency'
    DOMESTIC_CURRENCY           = 'APT_Compositions_08_DomesticCurrency'
    ROW_CLASS                   = 'APT_Compositions_09_RowClass'
    FOREIGN_CURRENCY_PRICE      = 'APT_Compositions_10_ForeignCurrencyPrice'
    DOMESTIC_CURRENCY_PRICE     = 'APT_Compositions_11_DomesticCurrencyPrice'
    FOREIGN_CURRENCY_UNITS      = 'APT_Compositions_12_ForeignCurrencyUnits'
    DOMESTIC_CURRENCY_UNITS     = 'APT_Compositions_13_DomesticCurrencyUnits'
    BASE_CURRENCY_PRICE         = 'APT_Compositions_14_BaseCurrencyPrice'
    BASE_CURRENCY_UNITS         = 'APT_Compositions_15_BaseCurrencyUnits'
    CFD_CURR_VALUES             = 'APT_Compositions_16_CfdCurrencyValues'
    CFD_UND_VALUES              = 'APT_Compositions_17_CfdUnderlyingValues'
    CFD_PAYMENTS_CURR           = 'APT_Compositions_18_CfdPaymentsCurrency'
    EXPORT_TYPE                 = 'APT_Compositions_19_AptExportType'
    
    #UNIVERSE COLUMNS

    ASSET_CLASS                 = 'APT_Universe_01_AssetClass'
    ASSET_ID                    = 'APT_Universe_02_Id'
    ASSET_ID_TYPE               = 'APT_Universe_03_IdType'
    MARKET_DATA_DATE            = 'APT_Universe_04_MarketDataDate'
    CURRENCY                    = 'APT_Universe_05_Currency'
    UND_ID_TYPE                 = 'APT_Universe_06_UnderlyingIdType'
    UND_ID                      = 'APT_Universe_07_UnderlyingId'
    PRICE                       = 'APT_Universe_08_Price'
    INITIAL_PRICE               = 'APT_Universe_09_InitialPrice'
    FORWARD_PRICE               = 'APT_Universe_10_ForwardPrice'
    UND_PRICE                   = 'APT_Universe_11_UnderlyingPrice'
    STRIKE                      = 'APT_Universe_12_Strike'
    TYPE                        = 'APT_Universe_13_Type'
    EXERCISE_TYPE               = 'APT_Universe_14_ExerciseType'
    DELTA                       = 'APT_Universe_15_Delta'
    UND_DIV_YIELD               = 'APT_Universe_16_DividendYield'
    RISK_FREE_RATE              = 'APT_Universe_17_RiskFreeRate'
    ISSUER                      = 'APT_Universe_18_Issuer'
    BORROWER_CLASS              = 'APT_Universe_19_BorrowerClass'
    RATING                      = 'APT_Universe_20_CreditRating'
    ISSUE_DATE                  = 'APT_Universe_21_IssueDate'
    REDEMPTION_DATE             = 'APT_Universe_22_RedemptionDate'
    MATURITY                    = 'APT_Universe_23_Maturity'
    EXPIRES                     = 'APT_Universe_24_Expires'
    COUPON_FREQUENCY            = 'APT_Universe_25_CouponFrequency'
    PAYMENT_FREQUENCY           = 'APT_Universe_26_PaymentFrequency'
    SHORT_PAYMENT_FREQUENCY     = 'APT_Universe_27_ShortPaymentFrequency'
    COUPON                      = 'APT_Universe_28_Coupon'
    SPREAD                      = 'APT_Universe_29_FloatingSpread'
    SWAP_RATE                   = 'APT_Universe_30_SwapRate'
    INFLATION_INDEX             = 'APT_Universe_31_InflationIndex'
    EFFECTIVE_DURATION          = 'APT_Universe_32_EffectiveDuration'
    SERVICE_FEE                 = 'APT_Universe_33_ServiceFee'
    MBS_TYPE                    = 'APT_Universe_34_MBSType'
    TERM_LENGTH                 = 'APT_Universe_35_TermLength'
    SWAP_TYPE                   = 'APT_Universe_36_SwapType'
    SWAP_TERM_YRS               = 'APT_Universe_37_SwapTermYrs'
    UND_TYPE                    = 'APT_Universe_38_UnderlyingType'
    IS_BARRIER                  = 'APT_Universe_39_IsBarrier' 
    BARRIER_TYPE                = 'APT_Universe_40_BarrierType'
    BARRIER_DIRECTION           = 'APT_Universe_41_BarrierDirection' 
    BARRIER_VALUE               = 'APT_Universe_42_BarrierValue' 
    IS_DIGITAL                  = 'APT_Universe_43_IsDigital' 
    DIGITAL_PAYOFF              = 'APT_Universe_44_DigitalPayOff' 
    DIGITAL_CASH_AMOUNT         = 'APT_Universe_45_DigitalCashAmount' 
    CALL_CURRENCY               = 'APT_Universe_46_CallCurrency'
    PUT_CURRENCY                = 'APT_Universe_47_PutCurrency'
    RECOVERY_RATE               = 'APT_Universe_48_RecoveryRate'
    INS_TYPE                    = 'APT_Universe_49_InsType'
    UND_CURRENCY                = 'APT_Universe_50_UndCurrency'
    IS_CALLABLE                 = 'APT_Universe_51_IsCallable'
    CALL_SCHEDULE               = 'APT_Universe_52_CallSchedule'
    CALL_AMOUNT                 = 'APT_Universe_53_CallAmount'
    PUT_AMOUNT                  = 'APT_Universe_54_PutAmount'
    UND_RISK_FREE_RATE          = 'APT_Universe_55_UndRiskFreeRate' 
    CONVERSION_START            = 'APT_Universe_56_ConversionStart'
    CONVERSION_END              = 'APT_Universe_57_ConversionEnd'
    CONVERSION_PRICE            = 'APT_Universe_58_ConversionPrice'
    FORCE_CONVERSION            = 'APT_Universe_59_ForceConversion'
    IS_STOCK_TRIGGER            = 'APT_Universe_60_IsStockTrigger'
    STOCK_TRIGGER_SCHEDULE      = 'APT_Universe_64_StockTriggerSchedule'
    CURRENCY_ID_TYPE            = 'APT_Universe_62_CurrencyIdType'
    UND_CLASS                   = 'APT_Universe_63_UnderlyingClass'
    LONG_LEG_PRINCIPAL          = 'APT_Universe_66_LongLegPrincipal'
    SHORT_LEG_PRINCIPAL         = 'APT_Universe_67_ShortLegPrincipal'
    LONG_LEG_CURRENCY           = 'APT_Universe_68_LongLegCurrency'
    SHORT_LEG_CURRENCY          = 'APT_Universe_69_ShortLegCurrency'
    SHORT_LEG_IS_FIXED          = 'APT_Universe_70_ShortLegIsFixed'
    LONG_LEG_IS_FIXED           = 'APT_Universe_71_LongLegIsFixed'
    FIXED_LONG_LEG_DATE         = 'APT_Universe_72_FixedLongLegDate'
    FLOAT_LONG_LEG_DATE         = 'APT_Universe_73_FloatLongLegDate'
    FIXED_LONG_LEG_COUPON       = 'APT_Universe_74_FixedLongLegCoupon'
    FLOAT_LONG_LEG_SPREAD       = 'APT_Universe_75_FloatLongLegSpread'
    FIXED_SHORT_LEG_DATE        = 'APT_Universe_76_FixedShortLegDate'
    FLOAT_SHORT_LEG_DATE        = 'APT_Universe_77_FloatShortLegDate'
    FIXED_SHORT_LEG_COUPON      = 'APT_Universe_78_FixedShortLegCoupon'
    FLOAT_SHORT_LEG_SPREAD      = 'APT_Universe_79_FloatShortLegSpread'
    CURR_SWAP_FX_RATE           = 'APT_Universe_80_CurrSwapFxRate'
    ASSET_NAME                  = 'APT_Universe_81_AssetName'
    IS_FORWARD_START            = 'APT_Universe_82_IsForwardStart'
    INSTRUMENT_START_DATE       = 'APT_Universe_83_InstrumentStartDate'
    DOMESTIC_CURRENCY_ID_TYPE   = 'APT_Compositions_84_DomesticCurrencyIdType'
    FOREIGN_CURRENCY_ID_TYPE    = 'APT_Compositions_85_ForeignCurrencyIdType'
    CURRENCY_FORWARD_BUY_AMOUNT = 'APT_Universe_84_CurrencyForwardBuy'
    CURRENCY_FORWARD_SELL_AMOUNT = 'APT_Universe_85_CurrencyForwardSell'
    CURRENCY_FORWARD_BUY_CURRENCY = 'APT_Universe_86_CurrencyForwardBuyCurr'
    CURRENCY_FORWARD_SELL_CURRENCY = 'APT_Universe_87_CurrencyForwardSellCurr'
    BARRIER_BASE                = 'APT_Universe_88_BarrierBase'
    CURR_DIGITAL_PAYOFF         = 'APT_Universe_89_CurrencyDigitalPayoff'
    CURR_DIGITAL_PAYOFF_AMOUNT  = 'APT_Universe_90_CurrencyDigitalPayoffAmount'
    START_CASH                  = 'APT_Universe_91_StartCash'
    END_CASH                    = 'APT_Universe_92_EndCash'
    CAP                         = 'APT_Universe_93_Cap'
    FLOOR                       = 'APT_Universe_94_Floor'
    FIRST_FLOAT_LEG_TYPE        = 'APT_Universe_95_FirstFloatLegType'
    FIRST_FLOAT_LEG_DATE        = 'APT_Universe_96_FirstFloatLegDate'
    FIRST_FIXED_LEG_DATE        = 'APT_Universe_97_FirstFixedLegDate'
    FIRST_FIXED_LEG_DATE        = 'APT_Universe_97_FirstFixedLegDate'
    PREPAYMENT                  = 'APT_Universe_98_PrePayment'
    CREDIT_SPREAD               = 'APT_Universe_99_CreditSpread'

class AptInstrumentGroupType:
    
    FIXED_INCOME_PRODUCTS       = 'fixedIncomeProducts'
    CONTRACTS_FOR_DIFFERENCE    = 'contractsForDifference'
    FUTURES                     = 'futures'
    FORWARDS                    = 'forwards'
    REPOS                       = 'forwards'
    CREDIT_DEFAULT_SWAPS        = 'creditDefaultSwaps'
    INTEREST_RATE_SWAPS         = 'interestRateSwaps'
    CURRENCY_SWAPS              = 'currencySwaps'
    OPTIONS                     = 'options'
    DERIVATIVES                 = 'derivatives'
    CAPS                        = 'caps'
    FLOORS                      = 'floors'
    REST                        = 'rest'
    
    @classmethod
    def apt_ins_group_type(cls, ins_type):
        if ins_type in ('Bond', 'Convertible', 'FRN', 'Bill', 'MBS/ABS', 'FreeDefCF'): return cls.FIXED_INCOME_PRODUCTS
        elif ins_type == 'Cap': return cls.CAPS
        elif ins_type == 'Floor': return cls.FLOORS
        elif ins_type == 'Repo/Reverse': return cls.REPOS
        elif ins_type == 'Future': return cls.FUTURES
        elif ins_type == 'Forward': return cls.FORWARDS
        elif ins_type == 'CFD': return cls.CONTRACTS_FOR_DIFFERENCE
        elif ins_type == 'CreditDefaultSwap': return cls.CREDIT_DEFAULT_SWAPS
        elif ins_type == 'Swap': return cls.INTEREST_RATE_SWAPS
        elif ins_type == 'CurrSwap': return cls.CURRENCY_SWAPS
        elif ins_type == 'Option': return cls.OPTIONS
        elif ins_type == 'Derivative': return cls.DERIVATIVES
        else: return cls.REST
        
    
class AptXmlWriter(object):
    
    WORKSPACE_TAG       = "workspace"
    ASSETS_TAG          = "assets"
    COMPOSITIONS_TAG    = 'compositions'
    COMPOSITION_TAG     = 'composition'
    WEIGHTS_TAG         = 'weights'
    LINE_TAG            = 'line'
    ENTRY_TAG           = 'entry'
    CREATOR_TAG         = 'APT'
    VERSION_TAG         = '6.1'
    XMLNS_TAG           = r'http://www.apt.com/pro'
    
    def __init__(self, report_contents, params):
        self.params = params
        self.report_name = params.report_name
        self.factor_model = re.sub(' ', '', params.factor_model)
        self.hide_zero_unit_rows = params.hide_zero_unit_rows
        self.hide_zero_price_rows = params.hide_zero_price_rows
        self.path = None
        self.report_contents = report_contents
        self.ins_rows, self.port_rows, self.group_rows = self._get_rows_by_type()
        self.root = ElementTree.Element(self.WORKSPACE_TAG, creator=self.CREATOR_TAG, version=self.VERSION_TAG, xmlns=self.XMLNS_TAG)
        self.assets_elem = None
        self._add_header()
        
    def _get_rows_by_type(self):
        ins_rows = []
        port_rows = []
        group_rows = []
        for row in self.report_contents.get_rows():
            row_class = self._get_raw_data(row, AptColumns.ROW_CLASS)
            if row_class == 'FPortfolioInstrumentAndTrades':
                port_rows.append(row)
            elif row_class == 'FSingleInstrumentAndTrades':
                ins_rows.append(row)
            else:
                group_rows.append(row)
        return ins_rows, port_rows, group_rows
        
    def _exclude_zero_unit_rows(self, row):
        ins_type = self._get_raw_data(row, AptColumns.INS_TYPE)
        if ins_type != 'Fx Rate':
            units = self._get_raw_data(row, AptColumns.ASSET_UNITS)
            if units in ('0', '0.0', '', 'NaN'):
                logger.info("Not valid position found for instrument %s. The instrument will not be included in the report", row.row_label)
                return 1
        return 0
                    
    def _exclude_zero_price_ins_rows(self, row):
        ins_type = self._get_raw_data(row, AptColumns.INS_TYPE)
        und_name = self._get_raw_data(row, AptColumns.UND_ID)
        if ins_type == 'Fx Rate':
            foreign_currency_price = self._get_raw_data(row, AptColumns.FOREIGN_CURRENCY_PRICE)
            domestic_currency_price = self._get_raw_data(row, AptColumns.DOMESTIC_CURRENCY_PRICE)
            if foreign_currency_price in ('', 'NaN', '0.0', 'None', '0') or domestic_currency_price in ('', 'NaN', '0.0', 'None'):
                logger.info("Not valid price found for instrument %s. The instrument will not be included in the report", row.row_label)
                return 1
                
        elif und_name != 'None':
            und_price = self._get_raw_data(row, AptColumns.UND_PRICE)
            comp_price = self._get_raw_data(row, AptColumns.ASSET_PRICE)
            if comp_price in ('', 'NaN', '0.0', 'None', '0'):
                logger.info("Not valid price found for instrument %s. The instrument will not be included in the report", row.row_label)
                return 1
            if  und_price in ('', 'NaN', '0.0', 'None'):
                logger.info("Not valid price found for underlying %s. The instrument will not be included in the report", und_name)
                return 1

            return 0

        else:
            comp_price = self._get_raw_data(row, AptColumns.ASSET_PRICE)
            univ_price = self._get_raw_data(row, AptColumns.PRICE)
            if comp_price in ('', 'NaN', '0.0', 'None', '0') or univ_price in ('', 'NaN', '0.0', 'None'):
                logger.info("Not valid price found for instrument %s. The instrument will not be included in the report", row.row_label)
                return 1

            return 0
        
    
    def write(self, xml=None ):
        try:
            if xml == None:
                xml = self.generate_xml()
            with open(self.path, "w") as file:
                file.write(xml)
            return xml
        except IOError as err:
            logger.error("Failed to write file: %s", str(err))
    
            
    def _add_header(self):
        self.assets_elem = ElementTree.Element(self.ASSETS_TAG)
        self.root.append(self.assets_elem)
        
    def _get_raw_data(self, row, column):
        row_data = row.raw_data.get(column)
        row_label = row.row_label
        asset_class = row.raw_data.get(AptColumns.ASSET_CLASS)
        if asset_class not in ('EQUITY', 'BOND', 'CURRENCY') and column != AptColumns.UND_ID:
            if not row_data:
                logger.error("Failed to read data from column: %s instrument: %s", column, row_label)
            if row_data in ('NaN', 'None'):
                logger.debug("Row: %s; Column: %s has value %s", row_label, column, row_data)
                if asset_class in ('BOND', 'CONVERTIBLE', 'FRN', 'CDS') and column == AptColumns.BORROWER_CLASS:
                    logger.warn("Borrower Classification has value %s for instrument %s. The instrument will be missing in the report", row_data, row_label)
            if self.hide_zero_unit_rows == 'False':
                if column in (AptColumns.ASSET_UNITS) and row_data in ('None'):
                    raise RuntimeError("Cannot generate Apt Report. Value '%s' is not valid for type Units. Column: %s; Row: %s" % (row_data, column, row_label))

            if self.hide_zero_price_rows == 'False':
                if column in (AptColumns.ASSET_PRICE, AptColumns.PRICE, AptColumns.UND_PRICE) and row_data in ('0.0', 'None'):
                    raise RuntimeError("Cannot generate Apt Report. Value '%s' is not valid for type Price. Column: %s; Row: %s" % (row_data, column, row_label))
        return row_data
            
    
    def generate_xml(self):
        raise NotImplementedError()
    
   
class CompositionFileWriter(AptXmlWriter):        

    COMPOSITIONS_TAG    = 'compositions'
    COMPOSITION_TAG     = 'composition'
    SCHEMA_TAG          = 'schema'
    USER_ATTRIBUTE_TAG  = 'userAttribute'
    UNITS_PRICES_TAG    = 'unitsPrices'
    WEIGHTS_TAG         = 'weights'
    LINE_TAG            = 'line'
    JOB_TAG             = 'job'
    PATH                = 'assets/compositions'

    def __init__(self, report_contents, params, instruments):
        AptXmlWriter.__init__(self, report_contents, params)
        self.portfolios = params.portfolios
        self.trade_filters = params.trade_filters
        self.groupers = params.groupers
        self.items_to_remove = [i.Name() for i in instruments]
        self.composition_struct = self._comp_struct(self.port_rows, self.ins_rows)
        self.path = params.composition_file
        self.compositions_elem = None
        self._add_group_elem()
        self._add_job_elem()
    
    def _add_group_elem(self):
        self.compositions_elem  = ElementTree.Element(self.COMPOSITIONS_TAG)
        self.assets_elem.append(self.compositions_elem)
        
    def _add_job_elem(self):
        portfolio_rows = self.port_rows
        for row in portfolio_rows:
            row_id = self._get_raw_data(row, AptColumns.COMP_ID)
            row_date = self._get_raw_data(row, AptColumns.COMP_DATE)
            job_elem = ElementTree.Element(self.JOB_TAG, portfolio= row_id, report=self.report_name, date= row_date, modelName=self.factor_model)
            self.root.append(job_elem)
            
    
    def _comp_struct(self, port_rows, ins_rows):
        comp_struct = {}
        for port_row in port_rows:
            port_id = port_row.row_id
            port_label = port_row.row_label
            if port_label not in self.items_to_remove:
                for ins_row in ins_rows:
                    if ins_row.parent_row_id == port_id:
                        ins_type = self._get_raw_data(ins_row, AptColumns.INS_TYPE)
                        if port_label not in comp_struct:
                            comp_struct[port_label] = [ins_type]
                        else:
                            comp_struct[port_label].append(ins_type)
        return comp_struct
        
    def _remove_empty_subcomposition_elems_from_compositions(self, root):
        compositions_elem = root.find(self.PATH)
        subcompositions_to_remove = []
        for composition_elem in compositions_elem.findall(self.COMPOSITION_TAG):
            unitPrices_elem = composition_elem.find(self.UNITS_PRICES_TAG)
            if not unitPrices_elem.findall(self.LINE_TAG):
                subcompositions_to_remove.append(composition_elem.get('id'))
                compositions_elem.remove(composition_elem)
                
        for job_elem in root.findall(self.JOB_TAG):
            if job_elem.get('portfolio') in subcompositions_to_remove:
                root.remove(job_elem)
        
    def _remove_empty_composition_elems_from_compositions(self, root):
        compositions_elem = root.find(self.PATH)
        for composition_elem in compositions_elem.findall(self.COMPOSITION_TAG):
            if composition_elem.get('id') in self.items_to_remove:
                compositions_elem.remove(composition_elem)
        
        for job_elem in root.findall(self.JOB_TAG):
            if job_elem.get('portfolio') in self.items_to_remove:
                root.remove(job_elem)
           
    def generate_xml(self):     
        comp_writer = None
        comp_writer = SingleElementWriter(self).write_elem()
        try:
            self._remove_empty_composition_elems_from_compositions(self.root)
            self._remove_empty_subcomposition_elems_from_compositions(self.root)
            composition_xml = ElementTree.tostring(self.root)
            logger.debug("Writing Compositions xml file to %s", str(self.path))
            return composition_xml
        except TypeError as err:
            logger.info("Couldn't generate Compositions xml, please see log for details")
            raise TypeError(str(err))

        
class SingleElementWriter(object):

    def __init__(self, writer):
        self.writer = writer
    
    def _write_fx_cash_domestic_currency_elem(self, row, units_elem):
        row_domestic_units = self.writer._get_raw_data(row, AptColumns.DOMESTIC_CURRENCY_UNITS)
        if row_domestic_units not in ('0', '0.0', '', 'NaN', 'None'):
            row_id = self.writer._get_raw_data(row, AptColumns.DOMESTIC_CURRENCY)
            row_idType = self.writer._get_raw_data(row, AptColumns.DOMESTIC_CURRENCY_ID_TYPE)
            row_price = self.writer._get_raw_data(row, AptColumns.DOMESTIC_CURRENCY_PRICE)
            line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_domestic_units, price=row_price)
            units_elem.append(line_elem)
            self._append_user_defined_attributes(row, line_elem)

    def _write_fx_cash_foreign_currency_elem(self, row, units_elem):
        row_foreign_units = self.writer._get_raw_data(row, AptColumns.FOREIGN_CURRENCY_UNITS)
        if row_foreign_units not in ('0', '0.0', '', 'NaN', 'None'):
            row_id = self.writer._get_raw_data(row, AptColumns.FOREIGN_CURRENCY)
            row_idType = self.writer._get_raw_data(row, AptColumns.FOREIGN_CURRENCY_ID_TYPE)
            row_price = self.writer._get_raw_data(row, AptColumns.FOREIGN_CURRENCY_PRICE)
            line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_foreign_units, price=row_price)
            units_elem.append(line_elem)
            self._append_user_defined_attributes(row, line_elem)

    def _write_fx_cash_base_currency_elem(self, row, units_elem):
        row_base_units = self.writer._get_raw_data(row, AptColumns.BASE_CURRENCY_UNITS)
        if row_base_units not in ('0', '0.0', '', 'NaN', 'None'):
            row_id = self.writer._get_raw_data(row, AptColumns.COMP_CURRENCY)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_price = self.writer._get_raw_data(row, AptColumns.BASE_CURRENCY_PRICE)
            line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_base_units, price=row_price)
            units_elem.append(line_elem)
            self._append_user_defined_attributes(row, line_elem)
    
    def _write_fx_cash_comp_elem(self, row, units_elem):    
        self._write_fx_cash_domestic_currency_elem(row, units_elem)
        self._write_fx_cash_foreign_currency_elem(row, units_elem)
        self._write_fx_cash_base_currency_elem(row, units_elem)

    def _write_cdf_cash_comp_elem(self, row, units_elem, row_curr_values, row_payments_curr, pos):
        row_curr_weight = str(1) 
        row_id = row_payments_curr[pos]
        row_idType = 'ISIN'
        row_price = row_curr_values[pos]
        line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_curr_weight, price=row_price)
        units_elem.append(line_elem)
        
    def _write_cdf_und_comp_elem(self, row, units_elem, row_und_values, row_payments_curr, pos):
        row_und_weight = str(1)
        row_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_price = row_und_values[pos]
        line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_und_weight, price=row_price)
        units_elem.append(line_elem)
        
    def _write_cdf_as_und_comp_elem(self, row, units_elem):
        row_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_units = self.writer._get_raw_data(row, AptColumns.ASSET_UNITS)
        row_price = self.writer._get_raw_data(row, AptColumns.ASSET_PRICE)
        if row_units not in ('0', '0.0', '', 'NaN', 'None'):
            line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_units, price=row_price)
            units_elem.append(line_elem)
            
    def _write_cfd_as_synth_comp_element(self, row, units_elem):
        row_und_values = self.writer._get_raw_data(row, AptColumns.CFD_UND_VALUES).split(';')
        row_curr_values = self.writer._get_raw_data(row, AptColumns.CFD_CURR_VALUES).split(';')
        row_payments_curr = self.writer._get_raw_data(row, AptColumns.CFD_PAYMENTS_CURR).split(';')
        for i in range(len(row_und_values)):
            self._write_cdf_cash_comp_elem(row, units_elem, row_curr_values, row_payments_curr, i)
            self._write_cdf_und_comp_elem(row, units_elem, row_curr_values, row_payments_curr, i)

    def _write_cfd_comp_elem(self, row, units_elem):
        export_type = self.writer._get_raw_data(row, AptColumns.EXPORT_TYPE)
        if export_type == '0': #UNDERLYING
            self._write_cdf_as_und_comp_elem(row, units_elem)
        else: #SYNTHETIC
            self._write_cfd_as_synth_comp_element(row, units_elem)
        self._append_user_defined_attributes(row, line_elem)
                
    def _write_cds_comp_elem(self, row, units_elem):
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_units = self.writer._get_raw_data(row, AptColumns.ASSET_UNITS)
            row_price = self.writer._get_raw_data(row, AptColumns.ASSET_PRICE)
            if row_units not in ('0', '0.0', '', 'NaN', 'None'):
                line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_units, price=row_price)
                units_elem.append(line_elem)
                self._append_user_defined_attributes(row, line_elem)
            
    def _write_swap_comp_elem(self, row, units_elem):
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_units = self.writer._get_raw_data(row, AptColumns.ASSET_UNITS)
            row_price = self.writer._get_raw_data(row, AptColumns.ASSET_PRICE)
            if row_units not in ('0', '0.0', '', 'NaN', 'None'):
                line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_units, price=row_price)
                units_elem.append(line_elem)
                self._append_user_defined_attributes(row, line_elem)
                
    def _write_fx_option_comp_elem(self, row, units_elem, ins_type):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_units = self.writer._get_raw_data(row, AptColumns.ASSET_UNITS)
        row_price = self.writer._get_raw_data(row, AptColumns.ASSET_PRICE)
        if row_units not in ('0', '0.0', '', 'NaN', 'None'):
            line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_units, price=row_price)
            units_elem.append(line_elem)
            self._append_user_defined_attributes(row, line_elem)

    def _write_single_comp_elem(self, row, units_elem):
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_units = self.writer._get_raw_data(row, AptColumns.ASSET_UNITS)
            row_price = self.writer._get_raw_data(row, AptColumns.ASSET_PRICE)
            if row_units not in ('0', '0.0', '', 'NaN', 'None'):
                line_elem = ElementTree.Element(self.writer.LINE_TAG, id=row_id, idType=row_idType, units=row_units, price=row_price)
                units_elem.append(line_elem)
                self._append_user_defined_attributes(row, line_elem)

    def _is_chained_grouper(self, grouper):
        return acm.FChainedGrouper == grouper.Class()
        
    def _get_user_attribute_names(self, grouper):
        if not grouper.IsKindOf('FDefaultGrouper'):
            name = str(grouper.Label()).replace(' ', '')
            return [''.join((name[0].lower(), name[1:]))]
        elif grouper.IsKindOf('FSubportfolioGrouper'):
            name = str(grouper.Label())
            return ['subportfolio']
        return []
        
    def _add_user_attribute_elem(self, schema_elem, grpr):
        user_attrs = self._get_user_attribute_names(grpr)
        for user_attr in user_attrs:
            if user_attr in ('subportfolio'):
                self.user_port_attr_list.append(user_attr)
            else: self.user_attr_list.append(user_attr)
            user_attr_elem = ElementTree.Element(self.writer.USER_ATTRIBUTE_TAG, name=user_attr)
            schema_elem.append(user_attr_elem)
        
    def _add_schema_elem(self, composition_elem):
        self.user_attr_list = []
        self.user_port_attr_list = []
        schema_elem = ElementTree.Element(self.writer.SCHEMA_TAG)
        composition_elem.append(schema_elem)
        if self.writer.groupers:
            try:
                grouper = self.writer.groupers[0]
                if not self._is_chained_grouper(grouper):
                    self._add_user_attribute_elem(schema_elem, grouper)
                else:
                    for grpr in grouper.Groupers():
                        self._add_user_attribute_elem(schema_elem, grpr)
            except IndexError:
                pass
                    
    def _append_user_attributes(self, row, line_elem):
        for index, attr in enumerate(self.user_attr_list):
            value = self.attr_list[index]
            line_elem.attrib[attr] = value
            
    def _append_user_port_attributes(self, row, line_elem):
        for index, attr in enumerate(self.user_port_attr_list):
            try:
                value = self.port_attr_list[index+1]
                line_elem.attrib[attr] = value
            except IndexError:
                continue

    def _append_user_defined_attributes(self, row, line_elem):
        self._append_user_attributes(row, line_elem)
        self._append_user_port_attributes(row, line_elem)
            
    def _get_row(self, row_id):
        try:
            row = [row for row in self.writer.group_rows if row.row_id == row_id][0]
            self.attr_list.insert(0, row.row_label)
            return row
        except IndexError:
            try:
                row = [row for row in self.writer.port_rows if row.row_id == row_id][0]
                self.port_attr_list.insert(0, row.row_label)
                return row
            except IndexError:
                return None
            
    def _get_top_row(self, row):
        row_id = row.parent_row_id
        if row_id:
            row = self._get_row(row_id)
            return self._get_top_row(row)
        else: return row.row_id

    def write_elem(self):
        for row in self.writer.port_rows:
            port_id = row.row_id
            port_label = row.row_label
            row_id = self.writer._get_raw_data(row, AptColumns.COMP_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.COMP_ID_TYPE)
            row_currency = self.writer._get_raw_data(row, AptColumns.COMP_CURRENCY)
            row_date = self.writer._get_raw_data(row, AptColumns.COMP_DATE)
            composition_elem = ElementTree.Element(self.writer.COMPOSITION_TAG, id=row_id, idType=row_idType, currency=row_currency, date=row_date)
            self.writer.compositions_elem.append(composition_elem)
            self._add_schema_elem(composition_elem)
            units_elem = ElementTree.Element(self.writer.UNITS_PRICES_TAG)
            composition_elem.append(units_elem)
            for row in self.writer.ins_rows:
                self.attr_list = []
                self.port_attr_list = []
                if self._get_top_row(row) == port_id:
                    if self.writer.hide_zero_price_rows == 'True':
                        if self.writer._exclude_zero_price_ins_rows(row):
                            continue
                    ins_type = self.writer._get_raw_data(row, AptColumns.INS_TYPE)
                    if ins_type == 'Fx Rate':
                        self._write_fx_cash_comp_elem(row, units_elem)
                    elif ins_type == 'CFD':
                        self._write_cfd_comp_elem(row, units_elem)
                    elif ins_type == 'CreditDefaultSwap':
                        self._write_cds_comp_elem(row, units_elem)
                    elif ins_type == 'Swap':
                        self._write_swap_comp_elem(row, units_elem)
                    elif ins_type in ('Option'):
                        und_type = self.writer._get_raw_data(row, AptColumns.UND_TYPE)
                        recon_id_type = self.writer._get_raw_data(row, AptColumns.RECON_ID_TYPE)
                        if und_type == 'Curr':
                            self._write_fx_option_comp_elem(row, units_elem, ins_type)
                        else: self._write_single_comp_elem(row, units_elem)
                    else: self._write_single_comp_elem(row, units_elem)

    def _is_elem_synthetic():
        pass
    

class UniverseFileWriter(AptXmlWriter):

    MARKET_DATA_TAG             = 'marketData'
    USER_DEFINED_DATA_TAG       = 'userDefinedData'
    CREDIT_RATINGS_TAG          = 'creditRatings'
    CREDIT_RATING_TAG           = 'creditRating'
    DERIVATIVES_TAG             = 'derivatives'
    PREPAYMENT_TABLES_TAG       = 'prepaymentTables'
    PREPAYMENT_TABLE_TAG        = 'prepaymentTable'
    PRICES_TAG                  = 'prices'
    PRICE_TAG                   = 'price'
    DELTAS_TAG                  = 'deltas'
    DELTA_TAG                   = 'delta'
    YIELDS_TAG                  = 'yields'
    RISK_FREE_RATE_TAG          = 'riskFreeRate'
    DIV_YIELD_TAG               = 'divYield'
    TIME_SERIES_ASSETS_TAG      = 'timeSeriesAssets'
    
    SUPPORTED_INS_TYPES = [
                           'Bond', 'Commodity', 'Stock', 'Depositary Receipt', 'Fx Rate', 'Future',
                           'Forward', 'Convertible', 'EquityIndex', 'CreditDefaultSwap', 'Bill',
                           'Swap', 'CurrSwap', 'FRN', 'Option', 'Derivative', 'Commodity Index',
                           'Curr', 'Repo/Reverse', 'Cap', 'Floor', 'MBS/ABS', 'FreeDefCF'
                          ]
    
    def __init__(self, report_contents, params):
        AptXmlWriter.__init__(self, report_contents, params)
        self._add_marketData_header()
        self._add_userDefinedData_header()
        self._add_timeSeriesAssets_header()
        self.path = params.universe_file
        self.ins_map = {}  #{ apt_ins_type: [ins1, ins2, ...] } 
        self._init_ins_map()
        self.compositions_elem = None
        self._add_compositions_elem()
        
    def _add_compositions_elem(self):
        self.compositions_elem = ElementTree.Element(self.COMPOSITIONS_TAG)
        self.assets_elem.append(self.compositions_elem)
        
    def _add_marketData_header(self):
        for row in self.port_rows:
            row_date = self._get_raw_data(row, AptColumns.MARKET_DATA_DATE)
            self.marketData_elem = ElementTree.Element(self.MARKET_DATA_TAG, date=row_date)
            self.creditRatings_elem = ElementTree.Element(self.CREDIT_RATINGS_TAG)
            self.deltas_elem = ElementTree.Element(self.DELTAS_TAG)
            self.prices_elem = ElementTree.Element(self.PRICES_TAG)
            self.yields_elem = ElementTree.Element(self.YIELDS_TAG)
            self.marketData_elem.append(self.creditRatings_elem)
            self.marketData_elem.append(self.deltas_elem)
            self.marketData_elem.append(self.prices_elem)
            self.marketData_elem.append(self.yields_elem)
            self.root.append(self.marketData_elem)

    def _add_userDefinedData_header(self):
        for row in self.port_rows:
            self.userDefinedData_elem = ElementTree.Element(self.USER_DEFINED_DATA_TAG)            
            self.prePaymentTables_elem = ElementTree.Element(self.PREPAYMENT_TABLES_TAG)
            self.userDefinedData_elem.append(self.prePaymentTables_elem)
            self.root.append(self.userDefinedData_elem)

    def _add_timeSeriesAssets_header(self):
        self.timeSeriesAssets_elem = ElementTree.Element(self.TIME_SERIES_ASSETS_TAG)
        self.assets_elem.append(self.timeSeriesAssets_elem)
            

    def _write_marketData_element(self, row, id=None):
        marketData_writer = MarketDataElementWriter(self, row)
        marketData_writer.write(id)


    def _write_userDefinedData_element(self, row, id=None):
        userDefined_writer = UserDefinedDataElementWriter(self, row)
        userDefined_writer.write(id)


    def _init_ins_map(self):
        ins_names = []
        for row in self.ins_rows:
            ins_name = str(row.row_label) 
            ins_type = self._get_raw_data(row, AptColumns.INS_TYPE)
            apt_ins_group_type = AptInstrumentGroupType.apt_ins_group_type(ins_type)
            
            if ins_type not in self.SUPPORTED_INS_TYPES:
                continue
            ins_id_type = self._get_raw_data(row, AptColumns.COMP_ID_TYPE)
            if ins_id_type in ('ISIN', 'DATASTREAM'):
                continue
            if self.hide_zero_unit_rows == 'True':
                if self._exclude_zero_unit_rows(row):
                    continue
            if self.hide_zero_price_rows == 'True':
                if self._exclude_zero_price_ins_rows(row):
                    continue

            if not apt_ins_group_type in self.ins_map:
                self.ins_map[apt_ins_group_type] = []
            
            if not ins_name in ins_names:
                self.ins_map[apt_ins_group_type].append(row)
                ins_names.append(ins_name)
                
    
    def _remove_empty_marketData_elems_from_universe(self, root):
        for marketData_elem in root.findall(self.MARKET_DATA_TAG):
            creditRatig_elem = marketData_elem.find(self.CREDIT_RATINGS_TAG+'/'+self.CREDIT_RATING_TAG)
            delta_elem = marketData_elem.find(self.DELTAS_TAG+'/'+self.DELTA_TAG)
            price_elem = marketData_elem.find(self.PRICES_TAG+'/'+self.PRICE_TAG)
            riskFreeRate_elem = marketData_elem.find(self.YIELDS_TAG+'/'+self.RISK_FREE_RATE_TAG)
            divYield_elem = marketData_elem.find(self.YIELDS_TAG+'/'+self.DIV_YIELD_TAG)
            if (creditRatig_elem == None) and (delta_elem == None) and (price_elem == None) and (riskFreeRate_elem == None) and (divYield_elem == None):
                root.remove(marketData_elem)



    def generate_xml(self):
        for apt_ins_group_type, ins_rows in self.ins_map.items():
            asset_element_writer = AssetClassElementWriter.get_element_writer(self, apt_ins_group_type, ins_rows)
            if asset_element_writer:
                asset_element_writer.write_elem()
        try:
            self._remove_empty_marketData_elems_from_universe(self.root)
            universe_xml = ElementTree.tostring(self.root)
            logger.debug("Writing Universe xml file to %s", str(self.path))
            return universe_xml
        except TypeError as err:
            logger.info("Couldn't generate universe xml, please see log for details")
            raise TypeError(str(err))
            

class AssetClassElementWriter(object):

    @classmethod
    def get_element_writer(cls, writer, apt_ins_group_type, ins_rows):
        if apt_ins_group_type == AptInstrumentGroupType.FIXED_INCOME_PRODUCTS:
            return AptFixedIncomeProductsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.CAPS:
            return AptCapsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.FLOORS:
            return AptFloorsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.REPOS:
            return AptReposElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.CONTRACTS_FOR_DIFFERENCE:
            return AptContractsForDifferenceElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.FUTURES:
            return AptFuturesElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.FORWARDS:
            return AptForwardsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.CREDIT_DEFAULT_SWAPS:
            return AptCreditDefaultSwapsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.INTEREST_RATE_SWAPS:
            return AptInterestRateSwapsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.CURRENCY_SWAPS:
            return AptCurrencySwapsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.OPTIONS:
            return AptOptionsElementWriter(writer, ins_rows)
        elif apt_ins_group_type == AptInstrumentGroupType.DERIVATIVES:
            return AptDerivativesElementWriter(writer, ins_rows)
        else:
            return TimeSeriesAssetsWriter(writer, ins_rows)
            
    def write_elem(self):       
        raise NotImplementedError()

class UserDefinedDataElementWriter(object):

    def __init__(self, writer, ins_row):
        self.writer = writer
        self.row = ins_row

    def write(self, id=None):
        row_ins_type = self.writer._get_raw_data(self.row, AptColumns.INS_TYPE)
        if row_ins_type in ('MBS/ABS'):
            row_coupon = self.writer._get_raw_data(self.row, AptColumns.COUPON)
            row_issueDate = self.writer._get_raw_data(self.row, AptColumns.ISSUE_DATE)[:4]
            row_spread = self.writer._get_raw_data(self.row, AptColumns.CREDIT_SPREAD)
            row_mbs_type = self.writer._get_raw_data(self.row, AptColumns.MBS_TYPE)

            prePaymentTable_elem = None
            for t in self.writer.prePaymentTables_elem.findall('prePaymentTable'):
                if t.get("mbsType") == row_mbs_type:
                    prePaymentTable_elem = t
            if not prePaymentTable_elem:
                prePaymentTable_elem = ElementTree.Element(self.writer.PREPAYMENT_TABLE_TAG, mbsType=row_mbs_type)
                self.writer.prePaymentTables_elem.append(prePaymentTable_elem)

            for e in prePaymentTable_elem.findall('entry'):
                if e.get('coupon') == row_coupon and e.get('issue') == row_issue and e.get('spread') == row_spread:
                    if e.get('value') != row_value:
                        print ("WARNING: Different prepayment assumptions mapped to MBSes with same (APT) MBS type, coupon, issue date and spread.")
                    return

            prepayment_name = self.writer._get_raw_data(self.row, AptColumns.PREPAYMENT)
            prepayment = acm.FPrepayment[prepayment_name]
            if prepayment_name and prepayment:
                ins_name = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
                row_value_string = prepayment.PrepaymentValue(acm.FInstrument[ins_name])
                if row_value_string:
                    row_value = "{0:.4f}".format(float(row_value_string))
                    prePaymentTableEntry_elem = ElementTree.Element(self.writer.ENTRY_TAG, coupon=row_coupon, issue=row_issueDate, spread=row_spread, value=row_value)
                    prePaymentTable_elem.append(prePaymentTableEntry_elem)

            if len(prePaymentTable_elem.findall('entry')) == 0:
                self.writer.prePaymentTables_elem.remove(prePaymentTable_elem)                


class MarketDataElementWriter(object):

    CREDIT_RATING_TAG   = 'creditRating'
    DELTA_TAG           = 'delta'
    PRICE_TAG           = 'price'
    RISK_FREE_RATE_TAG  = 'riskFreeRate'
    DIV_YIELD_TAG       = 'divYield'
    

    def __init__(self, writer, ins_row):
        self.writer = writer
        self.row = ins_row
        
    def write(self, id=None):
        ins_type = self.writer._get_raw_data(self.row, AptColumns.INS_TYPE)
        if ins_type in ('Bond', 'CreditDefaultSwap', 'FRN', 'Bill', 'Cap', 'Floor', 'MBS/ABS', 'FreeDefCF'):
            self._creditRating_marketData_element_writer(id)
        elif ins_type in ('Repo/Reverse'):
            self._repo_price_marketData_element_writer()
            self._riskFreeRate_marketData_element_writer()
        elif ins_type in ('Forward'):
            und_type = self.writer._get_raw_data(self.row, AptColumns.UND_TYPE)
            self._riskFreeRate_marketData_element_writer()
            if und_type in ('Curr'):
                self._und_price_marketData_element_writer()
                self._und_riskFreeRate_marketData_element_writer()
            elif und_type not in ('RateIndex'):
                self._und_price_marketData_element_writer()
                self._divYield_marketData_element_writer()
        elif ins_type in ('CFD'):
            self._und_price_marketData_element_writer()
        elif ins_type in ('Convertible'):
            self._und_price_marketData_element_writer()
            self._creditRating_marketData_element_writer()
        elif ins_type in ('CurrSwap'):
            self._currSwap_price_marketData_element_writer()
        elif ins_type in ('Option'):
            und_type = self.writer._get_raw_data(self.row, AptColumns.UND_TYPE)
            if und_type in ('Stock', 'EquityIndex', 'Depositary Receipt', 'Future/Forward'):
                self._riskFreeRate_marketData_element_writer()
                self._divYield_marketData_element_writer()
                self._price_marketData_element_writer()
            if und_type in ('Curr'):
                self._riskFreeRate_marketData_element_writer()
                self._und_riskFreeRate_marketData_element_writer()
                self._price_fx_option_marketData_element_writer()
            self._und_price_marketData_element_writer()
        elif ins_type in ('Derivative'):
            und_type = self.writer._get_raw_data(self.row, AptColumns.UND_TYPE)
            self._delta_marketData_element_writer()
            self._price_marketData_element_writer()
            self._und_price_marketData_element_writer()

    def _creditRating_marketData_element_writer(self, id=None):
        row_id = id or self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID_TYPE)
        row_rating = self.writer._get_raw_data(self.row, AptColumns.RATING)
        creditRating_elem = ElementTree.Element(self.CREDIT_RATING_TAG, id=row_id, idType=row_idType, rating=row_rating)
        self.writer.creditRatings_elem.append(creditRating_elem)
        
    def _currSwap_price_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.SHORT_LEG_CURRENCY)
        row_idType = 'ISIN'
        row_currency = self.writer._get_raw_data(self.row, AptColumns.LONG_LEG_CURRENCY)
        row_price = self.writer._get_raw_data(self.row, AptColumns.CURR_SWAP_FX_RATE)
        price_elem = ElementTree.Element(self.PRICE_TAG, id=row_id, idType=row_idType, currency=row_currency, price=row_price)
        self.writer.prices_elem.append(price_elem)
        
    def _price_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(self.row, AptColumns.CURRENCY)
        row_price = self.writer._get_raw_data(self.row, AptColumns.PRICE)
        price_elem = ElementTree.Element(self.PRICE_TAG, id=row_id, idType=row_idType, currency=row_currency, price=row_price)
        self.writer.prices_elem.append(price_elem)
        
    def _repo_price_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(self.row, AptColumns.CURRENCY)
        row_price = self.writer._get_raw_data(self.row, AptColumns.START_CASH)
        price_elem = ElementTree.Element(self.PRICE_TAG, id=row_id, idType=row_idType, currency=row_currency, price=row_price)
        self.writer.prices_elem.append(price_elem)
        
    def _price_fx_option_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(self.row, AptColumns.CURRENCY)
        units = float(self.writer._get_raw_data(self.row, AptColumns.ASSET_UNITS))
        price = float(self.writer._get_raw_data(self.row, AptColumns.PRICE))
        #if self.writer._get_raw_data(self.row, AptColumns.IS_DIGITAL) in ('True'):
            #row_price = str(price)
        #else: row_price = str(price*units)
        row_price = str(price*units)
        price_elem = ElementTree.Element(self.PRICE_TAG, id=row_id, idType=row_idType, currency=row_currency, price=row_price)
        self.writer.prices_elem.append(price_elem)


    def _und_price_marketData_element_writer(self):
        row_und_id = self.writer._get_raw_data(self.row, AptColumns.UND_ID)
        row_currency = self.writer._get_raw_data(self.row, AptColumns.CURRENCY)
        row_und_idType = self.writer._get_raw_data(self.row, AptColumns.UND_ID_TYPE)
        row_und_price = self.writer._get_raw_data(self.row, AptColumns.UND_PRICE)
        price_elem = ElementTree.Element(self.PRICE_TAG, id=row_und_id, idType=row_und_idType, currency=row_currency, price=row_und_price)
        self.writer.prices_elem.append(price_elem)


    def _riskFreeRate_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.CURRENCY)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.CURRENCY_ID_TYPE)
        row_riskFreeRate = self.writer._get_raw_data(self.row, AptColumns.RISK_FREE_RATE)
        riskFreeRate_elem = ElementTree.Element(self.RISK_FREE_RATE_TAG, id=row_id, idType=row_idType)
        riskFreeRate_elem.attrib['yield'] = row_riskFreeRate
        self.writer.yields_elem.append(riskFreeRate_elem)


    def _und_riskFreeRate_marketData_element_writer(self):
        row_und_id = self.writer._get_raw_data(self.row, AptColumns.UND_CURRENCY)
        row_und_idType = self.writer._get_raw_data(self.row, AptColumns.CURRENCY_ID_TYPE)
        row_und_riskFreeRate = self.writer._get_raw_data(self.row, AptColumns.UND_RISK_FREE_RATE)
        riskFreeRate_elem = ElementTree.Element(self.RISK_FREE_RATE_TAG, id=row_und_id, idType=row_und_idType)
        riskFreeRate_elem.attrib['yield'] = row_und_riskFreeRate
        self.writer.yields_elem.append(riskFreeRate_elem)


    def _divYield_marketData_element_writer(self):
        row_und_id = self.writer._get_raw_data(self.row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(self.row, AptColumns.UND_ID_TYPE)
        row_und_divYield = self.writer._get_raw_data(self.row, AptColumns.UND_DIV_YIELD)
        divYield_elem = ElementTree.Element(self.DIV_YIELD_TAG, id=row_und_id, idType=row_und_idType)
        divYield_elem.attrib['yield'] = row_und_divYield
        self.writer.yields_elem.append(divYield_elem)
        
        
    def _delta_marketData_element_writer(self):
        row_id = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(self.row, AptColumns.ASSET_ID_TYPE)
        row_delta = self.writer._get_raw_data(self.row, AptColumns.DELTA)
        delta_elem = ElementTree.Element(self.DELTA_TAG, id=row_id, idType=row_idType, delta=row_delta)
        self.writer.deltas_elem.append(delta_elem)

        

class AptFixedIncomeProductsElementWriter(AssetClassElementWriter):
    FIXED_INCOME_PRODUCTS_TAG                   = 'fixedIncomeProducts'
    STRUCTURED_FIXED_INCOME_CONTRACT_TAG        = 'structuredFixedIncomeContract'
    FIXED_COUPON_SCHEDULE_TAG                   = 'fixedCouponSchedule'
    CALL_SCHEDULE_TAG                           = 'callSchedule'
    FIXED_COUPON_SCHEDULE_ENTRY_TAG             = 'fixedCouponScheduleEntry'
    OPTION_SCHEDULE_ENTRY_TAG                   = 'optionScheduleEntry'
    FLOATING_SPREAD_SCHEDULE_TAG                = 'floatingSpreadSchedule'
    FLOATING_SPREAD_SCHEDULE_ENTRY_TAG          = 'floatingSpreadScheduleEntry'
    CONVERTIBLE_TAG                             = 'convertible'
    MBS_TAG                                     = 'mortgageBackedSecurity'
    STOCK_TRIGGER_SCHEDULE_TAG                  = 'stockTriggerSchedule'
    STOCK_TRIGGER_SCHEDULE_ENTRY_TAG            = 'stockTriggerScheduleEntry'


    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.fixed_income_products_elem = ElementTree.Element(self.FIXED_INCOME_PRODUCTS_TAG)
        self.writer.assets_elem.append(self.fixed_income_products_elem)
        
    def get_writer_func(self, row):
        if self.writer._get_raw_data(row, AptColumns.INS_TYPE) in ('Bond', 'Bill'):
            return self._write_fixed_coupon_bond_element(row)
        elif self.writer._get_raw_data(row, AptColumns.INS_TYPE) == 'Convertible':
            return self._write_convertible_bond_element(row)
        elif self.writer._get_raw_data(row, AptColumns.INS_TYPE) == 'FRN':
            return self._write_floating_rate_bond_element(row)
        elif self.writer._get_raw_data(row, AptColumns.INS_TYPE) == 'MBS/ABS':
            return self._write_mbs_element(row)
        elif self.writer._get_raw_data(row, AptColumns.INS_TYPE) == 'FreeDefCF':
            return self._write_fixed_to_float_element(row)

    def write_elem(self):
        for row in self.ins_rows:
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)
            
    def _write_fixed_income_products_base_element(self, row, id=None):
        row_id = id or self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_borrowerClass = self.writer._get_raw_data(row, AptColumns.BORROWER_CLASS)
        row_couponFrequency = self.writer._get_raw_data(row, AptColumns.COUPON_FREQUENCY)
        row_redemptionDate = self.writer._get_raw_data(row, AptColumns.REDEMPTION_DATE)
        self.structured_fixed_income_contract_elem = ElementTree.Element(self.STRUCTURED_FIXED_INCOME_CONTRACT_TAG, id=row_id, idType=row_idType, currency=row_currency, borrowerClass=row_borrowerClass, couponFrequency=row_couponFrequency, redemptionDate=row_redemptionDate)
        self.fixed_income_products_elem.append(self.structured_fixed_income_contract_elem)
        
    def _write_callable_schedule_element(self, row):
        callSchedule_elem = ElementTree.Element(self.CALL_SCHEDULE_TAG)
        self.structured_fixed_income_contract_elem.append(callSchedule_elem)
        call_shedule = []
        for i in self.writer._get_raw_data(row, AptColumns.CALL_SCHEDULE).split(';'):
            call_shedule.append((i.split(',')[0], i.split(',')[1]))
        for row_date, row_strike in call_shedule:
            optionScheduleEntry_elem = ElementTree.Element(self.OPTION_SCHEDULE_ENTRY_TAG, date=row_date, strike=row_strike)
            callSchedule_elem.append(optionScheduleEntry_elem)
            
    def _write_fixed_coupon_shedule_entry_element(self, row):
        row_date = self.writer._get_raw_data(row, AptColumns.ISSUE_DATE)
        row_coupon = self.writer._get_raw_data(row, AptColumns.COUPON)
        fixed_coupon_schedule_entry_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_ENTRY_TAG, date=row_date, coupon=row_coupon)
        self.fixed_coupon_schedule_elem.append(fixed_coupon_schedule_entry_elem)
    
    def _write_fixed_coupon_bond_element(self, row, id=None):
        self._write_fixed_income_products_base_element(row, id)
        self.fixed_coupon_schedule_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_TAG)
        self.structured_fixed_income_contract_elem.append(self.fixed_coupon_schedule_elem)
        ins_type = self.writer._get_raw_data(row, AptColumns.INS_TYPE)
        if ins_type not in ('Bill'):
            self._write_fixed_coupon_shedule_entry_element(row)
        if self.writer._get_raw_data(row, AptColumns.IS_CALLABLE) == 'True'and self.writer._get_raw_data(row, AptColumns.CALL_SCHEDULE) != 'None':
            self._write_callable_schedule_element(row)
        self.writer._write_marketData_element(row, id)
        
    def _write_convertible_bond_element(self, row):
        self._write_fixed_income_products_base_element(row)
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_start = self.writer._get_raw_data(row, AptColumns.CONVERSION_START)
        row_end = self.writer._get_raw_data(row, AptColumns.CONVERSION_END)
        row_conversionPrice = self.writer._get_raw_data(row, AptColumns.CONVERSION_PRICE)
        row_forceConversion = self.writer._get_raw_data(row, AptColumns.FORCE_CONVERSION)
        convertible_elem = ElementTree.Element(self.CONVERTIBLE_TAG, underlying=row_und_id, undIdType=row_und_idType, conversionPrice=row_conversionPrice, start=row_start, end=row_end, forceConversion=row_forceConversion)
        self.structured_fixed_income_contract_elem.append(convertible_elem)
        
        if self.writer._get_raw_data(row, AptColumns.IS_CALLABLE) == 'True' and self.writer._get_raw_data(row, AptColumns.CALL_SCHEDULE) != 'None':
            self._write_callable_schedule_element(row)
        
        if self.writer._get_raw_data(row, AptColumns.IS_STOCK_TRIGGER) == 'True':
            stockTriggerSchedule_elem = ElementTree.Element(self.STOCK_TRIGGER_SCHEDULE_TAG)
            convertible_elem.append(stockTriggerSchedule_elem)
            stock_trigger_shedule = []
            stock_trigger_shedule_array = self.writer._get_raw_data(row, AptColumns.STOCK_TRIGGER_SCHEDULE).split(';')
            if stock_trigger_shedule_array:
                for i in stock_trigger_shedule_array:
                    stock_trigger_shedule.append((i.split(',')[0], i.split(',')[1]))
                for row_date, row_triggerLevel in stock_trigger_shedule:
                    stockTriggerScheduleEntry_elem = ElementTree.Element(self.STOCK_TRIGGER_SCHEDULE_ENTRY_TAG, date=row_date, triggerLevel=row_triggerLevel)
                    stockTriggerSchedule_elem.append(stockTriggerScheduleEntry_elem)
        self.writer._write_marketData_element(row)
        
    def _write_floating_rate_bond_element(self, row, id=None, cap=False, floor=False): 
        self._write_fixed_income_products_base_element(row, id)
        floating_spread__schedule_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_TAG)
        self.structured_fixed_income_contract_elem.append(floating_spread__schedule_elem)
        row_date = self.writer._get_raw_data(row, AptColumns.ISSUE_DATE)
        row_spread = self.writer._get_raw_data(row, AptColumns.SPREAD)
        floating_spread_schedule_entry_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_ENTRY_TAG, date=row_date, spread=row_spread)
        if cap: 
            row_cap = self.writer._get_raw_data(row, AptColumns.CAP)
            floating_spread_schedule_entry_elem.attrib['cap'] = row_cap
        elif floor: 
            row_floor = self.writer._get_raw_data(row, AptColumns.FLOOR)
            floating_spread_schedule_entry_elem.attrib['floor'] = row_floor
        floating_spread__schedule_elem.append(floating_spread_schedule_entry_elem)
        self.writer._write_marketData_element(row, id)

    def _write_mbs_element(self, row, id=None):
        row_id = id or self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_borrowerClass = self.writer._get_raw_data(row, AptColumns.BORROWER_CLASS)

        row_coupon = self.writer._get_raw_data(row, AptColumns.COUPON)
        row_couponFrequency = self.writer._get_raw_data(row, AptColumns.COUPON_FREQUENCY)
        row_redemptionDate = self.writer._get_raw_data(row, AptColumns.REDEMPTION_DATE)
        row_issueDate = self.writer._get_raw_data(row, AptColumns.ISSUE_DATE)

        row_serviceFee = self.writer._get_raw_data(row, AptColumns.SERVICE_FEE)
        row_mbsType = self.writer._get_raw_data(row, AptColumns.MBS_TYPE)

        self.mbs_elem = ElementTree.Element(self.MBS_TAG, id=row_id, idType=row_idType, currency=row_currency, borrowerClass=row_borrowerClass, coupon=row_coupon, couponFrequency=row_couponFrequency, issueDate=row_issueDate, redemptionDate=row_redemptionDate, serviceFee=row_serviceFee, mbsType=row_mbsType)
        self.fixed_income_products_elem.append(self.mbs_elem)       
        self.writer._write_marketData_element(row, id)
        self.writer._write_userDefinedData_element(row, id)
        
    def _write_fixed_to_float_element(self, row, id=None, cap=False, floor=False):
        self._write_fixed_income_products_base_element(row, id)
        
        fixed_coupon_schedule_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_TAG)
        self.structured_fixed_income_contract_elem.append(fixed_coupon_schedule_elem)

        row_coupon = self.writer._get_raw_data(row, AptColumns.COUPON)
        leg_date = self.writer._get_raw_data(row, AptColumns.FIRST_FIXED_LEG_DATE)
        fixed_coupon_schedule_entry_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_ENTRY_TAG, date=leg_date, coupon=row_coupon)
        fixed_coupon_schedule_elem.append(fixed_coupon_schedule_entry_elem)

        floating_spread_schedule_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_TAG)
        self.structured_fixed_income_contract_elem.append(floating_spread_schedule_elem)

        row_spread = self.writer._get_raw_data(row, AptColumns.SPREAD)
        leg_date = self.writer._get_raw_data(row, AptColumns.FIRST_FLOAT_LEG_DATE)
        floating_spread_schedule_entry_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_ENTRY_TAG, date=leg_date, spread=row_spread)
        row_float_type = self.writer._get_raw_data(row, AptColumns.FIRST_FLOAT_LEG_TYPE)
        if row_float_type in ('Capped Float', 'Cap', 'Collared Float'):
            row_cap = self.writer._get_raw_data(row, AptColumns.CAP)
            floating_spread_schedule_entry_elem.attrib['cap'] = row_cap
        elif row_float_type in ('Floor', 'Floored Float', 'Collared Float'):
            row_floor = self.writer._get_raw_data(row, AptColumns.FLOOR)
            floating_spread_schedule_entry_elem.attrib['floor'] = row_floor
        elif not row_float_type in ('Float'):
            logger.info('ERROR: Missing supported float leg in Free Defined Cash Flow %s!' % self.writer._get_raw_data(row, AptColumns.ASSET_ID))
            return 
        floating_spread_schedule_elem.append(floating_spread_schedule_entry_elem)

        if self.writer._get_raw_data(row, AptColumns.IS_CALLABLE) == 'True'and self.writer._get_raw_data(row, AptColumns.CALL_SCHEDULE) != 'None':
            self._write_callable_schedule_element(row)

        self.writer._write_marketData_element(row, id)

class AptContractsForDifferenceElementWriter(AssetClassElementWriter):
    
    CONTRACTS_FOR_DIFFERENCE_TAG        = 'contractsForDifference'
    CONTRACT_FOR_DIFFERENCE_TAG         = 'contractForDifference'    
    
    
    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.contractsForDifference_elem = ElementTree.Element(self.CONTRACTS_FOR_DIFFERENCE_TAG)
        self.writer.assets_elem.append(self.contractsForDifference_elem)
        
    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
            row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
            row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
            row_initialPrice = self.writer._get_raw_data(row, AptColumns.INITIAL_PRICE)
            contractForDifference_elem = ElementTree.Element(self.CONTRACT_FOR_DIFFERENCE_TAG, id=row_id, idType=row_idType, underlying=row_und_id, undIdType=row_und_idType, currency=row_currency, initialPrice=row_initialPrice)
            self.contractsForDifference_elem.append(contractForDifference_elem)
            self.writer._write_marketData_element(row)



class AptForwardsElementWriter(AssetClassElementWriter):
    FORWARDS_TAG                = 'forwards'
    FORWARD_TAG                 = 'forward'
    CURRENCY_FORWARD_TAG        = 'currencyForward'
    CURRENCY_FORWARD_BUY_TAG    = 'buy'
    CURRENCY_FORWARD_SELL_TAG   = 'sell'

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.forwards_elem = ElementTree.Element(self.FORWARDS_TAG)
        self.writer.assets_elem.append(self.forwards_elem)
        
    def _write_forward_elem(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_frwd_price = self.writer._get_raw_data(row, AptColumns.FORWARD_PRICE)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        forward_elem = ElementTree.Element(self.FORWARD_TAG, id=row_id, currency=row_currency, underlying=row_und_id, undIdType=row_und_idType, forwardPrice=row_frwd_price, expires=row_expires)
        self.forwards_elem.append(forward_elem)
        self.writer._write_marketData_element(row)
        
    def _write_currency_forward_buy_elem(self, row, currencyForward_elem):
        row_buy_amount = self.writer._get_raw_data(row, AptColumns.CURRENCY_FORWARD_BUY_AMOUNT)
        row_buy_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY_FORWARD_BUY_CURRENCY)
        currencyForwardBuy_elem = ElementTree.Element(self.CURRENCY_FORWARD_BUY_TAG, currency = row_buy_currency, amount=row_buy_amount)
        currencyForward_elem.append(currencyForwardBuy_elem)

    def _write_currency_forward_sell_elem(self, row, currencyForward_elem):
        row_sell_amount = self.writer._get_raw_data(row, AptColumns.CURRENCY_FORWARD_SELL_AMOUNT)
        row_sell_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY_FORWARD_SELL_CURRENCY)
        currencyForwardSell_elem = ElementTree.Element(self.CURRENCY_FORWARD_SELL_TAG, currency = row_sell_currency, amount=row_sell_amount)
        currencyForward_elem.append(currencyForwardSell_elem)
        
    def _write_currency_forward_elem(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_counter = self.writer._get_raw_data(row, AptColumns.CURRENCY_FORWARD_BUY_CURRENCY)
        currencyForward_elem = ElementTree.Element(self.CURRENCY_FORWARD_TAG, id=row_id, expires=row_expires, counter=row_counter)
        self._write_currency_forward_buy_elem(row, currencyForward_elem)
        self._write_currency_forward_sell_elem(row, currencyForward_elem)
        self.forwards_elem.append(currencyForward_elem)
        self.writer._write_marketData_element(row)
        
    def get_writer_func(self, row):
        if self.writer._get_raw_data(row, AptColumns.UND_TYPE) in ('Curr'):
            return self._write_currency_forward_elem(row)
        else:
            return self._write_forward_elem(row)

    def write_elem(self):
        for row in self.ins_rows:
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)
            

class AptReposElementWriter(AssetClassElementWriter):
    FORWARDS_TAG                = 'forwards'
    FORWARD_TAG                 = 'forward'

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.forwards_elem = ElementTree.Element(self.FORWARDS_TAG)
        self.writer.assets_elem.append(self.forwards_elem)
        
    def _write_forward_elem(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_frwd_price = self.writer._get_raw_data(row, AptColumns.END_CASH)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        forward_elem = ElementTree.Element(self.FORWARD_TAG, id=row_id, currency=row_currency, underlying=row_und_id, undIdType=row_und_idType, forwardPrice=row_frwd_price, expires=row_expires)
        self.forwards_elem.append(forward_elem)
        self.writer._write_marketData_element(row)
        
    def get_writer_func(self, row):
        return self._write_forward_elem(row)

    def write_elem(self):
        for row in self.ins_rows:
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)
        

class AptFuturesElementWriter(AssetClassElementWriter):
    FUTURES_TAG                 = 'futures'
    FUTURE_TAG                  = 'future'
    INTEREST_RATE_FUTURE_TAG    = 'interestRateFuture'

    
    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.futures_elem = ElementTree.Element(self.FUTURES_TAG)
        self.writer.assets_elem.append(self.futures_elem)
        
    def _write_future_elem(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        future_elem = ElementTree.Element(self.FUTURE_TAG, id=row_id, idType=row_idType, expires=row_expires, underlying=row_und_id, undIdType=row_und_idType, currency=row_currency)
        self.futures_elem.append(future_elem)
        self.writer._write_marketData_element(row)
        
    def _write_interest_rate_future_elem(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_termLength = self.writer._get_raw_data(row, AptColumns.TERM_LENGTH)
        interest_rate_future_elem = ElementTree.Element(self.INTEREST_RATE_FUTURE_TAG, id=row_id, idType=row_idType, currency=row_currency, expires=row_expires, termLength=row_termLength)
        self.futures_elem.append(interest_rate_future_elem)
        self.writer._write_marketData_element(row)
        
    def get_writer_func(self, row):
        if self.writer._get_raw_data(row, AptColumns.UND_TYPE) in ('RateIndex', 'Bill', 'Deposit'):
            return self._write_interest_rate_future_elem(row)
        else:
            return self._write_future_elem(row)

    def write_elem(self):
        for row in self.ins_rows:
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)           


class AptCreditDefaultSwapsElementWriter(AssetClassElementWriter):
    
    CREDIT_DEFAULT_SWAPS_TAG    = 'creditDefaultSwaps'
    CREDIT_DEFAULT_SWAP_TAG     = 'creditDefaultSwap'

    
    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.creditDefaultSwaps_elem = ElementTree.Element(self.CREDIT_DEFAULT_SWAPS_TAG)
        self.writer.assets_elem.append(self.creditDefaultSwaps_elem)
    
    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
            row_borrowerClass = self.writer._get_raw_data(row, AptColumns.BORROWER_CLASS)
            #row_issuer = self.writer._get_raw_data(row, AptColumns.ISSUER)
            row_maturity = self.writer._get_raw_data(row, AptColumns.MATURITY)
            row_spread = self.writer._get_raw_data(row, AptColumns.SPREAD)
            row_paymentFrequency = self.writer._get_raw_data(row, AptColumns.PAYMENT_FREQUENCY)
            row_recoveryRate = self.writer._get_raw_data(row, AptColumns.RECOVERY_RATE)
            creditDefaultSwap_elem = ElementTree.Element(self.CREDIT_DEFAULT_SWAP_TAG, id=row_id, idType=row_idType, currency=row_currency, borrowerClass=row_borrowerClass, maturity=row_maturity, spread=row_spread, paymentFrequency=row_paymentFrequency, recoveryRate=row_recoveryRate)
            self.creditDefaultSwaps_elem.append(creditDefaultSwap_elem)
            self.writer._write_marketData_element(row)
            

class AptCapsElementWriter(AssetClassElementWriter):

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        
    def _write_comp_cap_element(self, row, row_id, row_ids, row_idType):
        row_visibility = 'CLOSED'
        row_weighting = 'NOTIONAL'
        row_date = self.writer._get_raw_data(row, AptColumns.COMP_DATE)
        row_currency = self.writer._get_raw_data(row, AptColumns.COMP_CURRENCY)
        composition_elem = ElementTree.Element(self.writer.COMPOSITION_TAG, visibility=row_visibility, idType=row_idType, id=row_id, date=row_date, currency=row_currency)
        weights_elem = ElementTree.Element(self.writer.WEIGHTS_TAG)
        self._add_cap_line_elems(weights_elem, row_ids, row_idType)
        composition_elem.append(weights_elem)
        self.writer.compositions_elem.append(composition_elem)
        
    def _add_cap_line_elems(self, weights_elem, row_ids, row_idType):
        row_weights = ['1', '-1']
        for i in range(2):
            line_elem = ElementTree.Element(self.writer.LINE_TAG, idType=row_idType, id=row_ids[i], weight=row_weights[i])
            weights_elem.append(line_elem)
        
    def _write_cap_element(self, row, row_ids):
        fixed_income_products_writer = AptFixedIncomeProductsElementWriter(self.writer, self.ins_rows)
        fixed_income_products_writer._write_floating_rate_bond_element(row, id=row_ids[0])
        fixed_income_products_writer._write_floating_rate_bond_element(row, id=row_ids[1], cap=True)
        
    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_ids = [' '.join((row_id, 'Long')), ' '.join((row_id, 'Short'))]
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            self._write_comp_cap_element(row, row_id, row_ids, row_idType)
            self._write_cap_element(row, row_ids)
            
        
class AptFloorsElementWriter(AssetClassElementWriter):

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        
    def _write_comp_floor_element(self, row, row_id, row_ids, row_idType):
        row_visibility = 'CLOSED'
        row_weighting = 'NOTIONAL'
        row_date = self.writer._get_raw_data(row, AptColumns.COMP_DATE)
        row_currency = self.writer._get_raw_data(row, AptColumns.COMP_CURRENCY)
        composition_elem = ElementTree.Element(self.writer.COMPOSITION_TAG, visibility=row_visibility, idType=row_idType, id=row_id, date=row_date, currency=row_currency)
        weights_elem = ElementTree.Element(self.writer.WEIGHTS_TAG)
        self._add_floor_line_elems(weights_elem, row_ids, row_idType)
        composition_elem.append(weights_elem)
        self.writer.compositions_elem.append(composition_elem)
        
    def _add_floor_line_elems(self, weights_elem, row_ids, row_idType):
        row_weights = ['1', '-1']
        for i in range(2):
            line_elem = ElementTree.Element(self.writer.LINE_TAG, idType=row_idType, id=row_ids[i], weight=row_weights[i])
            weights_elem.append(line_elem)
        
    def _write_floor_element(self, row, row_ids):
        fixed_income_products_writer = AptFixedIncomeProductsElementWriter(self.writer, self.ins_rows)
        fixed_income_products_writer._write_fixed_coupon_bond_element(row, id=row_ids[0])
        fixed_income_products_writer._write_floating_rate_bond_element(row, id=row_ids[1], cap=True)
        
    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_ids = [' '.join((row_id, 'Long')), ' '.join((row_id, 'Short'))]
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            self._write_comp_floor_element(row, row_id, row_ids, row_idType)
            self._write_floor_element(row, row_ids)

            
class AptInterestRateSwapsElementWriter(AssetClassElementWriter):
    
    INTEREST_RATE_SWAPS_TAG      = 'interestRateSwaps'
    INTEREST_RATE_SWAP_TAG       = 'interestRateSwap'
    
    
    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.interestRateSwaps_elem = ElementTree.Element(self.INTEREST_RATE_SWAPS_TAG)
        self.writer.assets_elem.append(self.interestRateSwaps_elem)
        
    def _write_irs_elem(self, _id, _idType, _expires, _currency, _swapRate, _paymentFrequency, _shortPaymentFrequency):
        interestRateSwap_elem = ElementTree.Element(self.INTEREST_RATE_SWAP_TAG, id=_id, idType=_idType, expires=_expires, currency=_currency, swapRate=_swapRate, paymentFrequency=_paymentFrequency, shortPaymentFrequency=_shortPaymentFrequency)
        self.interestRateSwaps_elem.append(interestRateSwap_elem)
        
    def _write_long_irs(self, id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency):
        id = ' '.join((id, 'Long'))
        self._write_irs_elem(id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency)
        
    def _write_short_irs(self, row, id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency):
        id = ' '.join((id, 'Short'))
        expires = self.writer._get_raw_data(row, AptColumns.INSTRUMENT_START_DATE)
        self._write_irs_elem(id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency)
        
    def _add_irs_line_elems(self, weights_elem, row_id, row_idType):
        row_ids = [' '.join((row_id, 'Long')), ' '.join((row_id, 'Short'))]
        row_weights = ['1', '-1']
        for i in range(2):
            line_elem = ElementTree.Element(self.writer.LINE_TAG, idType=row_idType, id=row_ids[i], weight=row_weights[i])
            weights_elem.append(line_elem)
        
    def _write_comp_irs(self, row, row_id, row_idType):
        row_visibility = 'CLOSED'
        row_weighting = 'NOTIONAL'
        row_date = self.writer._get_raw_data(row, AptColumns.COMP_DATE)
        row_currency = self.writer._get_raw_data(row, AptColumns.COMP_CURRENCY)
        composition_elem = ElementTree.Element(self.writer.COMPOSITION_TAG, visibility=row_visibility, idType=row_idType, id=row_id, date=row_date, currency=row_currency)
        weights_elem = ElementTree.Element(self.writer.WEIGHTS_TAG)
        self._add_irs_line_elems(weights_elem, row_id, row_idType)
        composition_elem.append(weights_elem)
        self.writer.compositions_elem.append(composition_elem)
        
    def _write_forward_start_irs_elem(self, row, id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency):
        self._write_long_irs(id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency)
        self._write_short_irs(row, id, idType, expires, currency, swapRate, paymentFrequency, shortPaymentFrequency)
        self._write_comp_irs(row, id, idType)

    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
            row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
            row_swapRate = self.writer._get_raw_data(row, AptColumns.SWAP_RATE)
            row_paymentFrequency = self.writer._get_raw_data(row, AptColumns.PAYMENT_FREQUENCY)
            row_shortPaymentFrequency = self.writer._get_raw_data(row, AptColumns.SHORT_PAYMENT_FREQUENCY)
            is_forward_start = self.writer._get_raw_data(row, AptColumns.IS_FORWARD_START)
            if is_forward_start not in ('true'):
                self._write_irs_elem(row_id, row_idType, row_expires, row_currency, row_swapRate, row_paymentFrequency, row_shortPaymentFrequency)
            else: self._write_forward_start_irs_elem(row, row_id, row_idType, row_expires, row_currency, row_swapRate, row_paymentFrequency, row_shortPaymentFrequency)
            

class AptCurrencySwapsElementWriter(AssetClassElementWriter):
    
    CURRENCY_SWAPS_TAG                  = 'currencySwaps'
    CURRENCY_SWAP_TAG                   = 'currencySwap'
    SHORT_LEG_TAG                       = 'shortLeg'
    LONG_LEG_TAG                        = 'longLeg'
    FIXED_COUPON_SCHEDULE_TAG           = 'fixedCouponSchedule'
    FIXED_COUPON_SCHEDULE_ENTRY_TAG     = 'fixedCouponScheduleEntry'
    FLOATING_SPREAD_SCHEDULE_TAG        = 'floatingSpreadSchedule'
    FLOATING_SPREAD_SCHEDULE_ENTRY_TAG  = 'floatingSpreadScheduleEntry'
    
    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.currencySwaps_elem = ElementTree.Element(self.CURRENCY_SWAPS_TAG)
        self.writer.assets_elem.append(self.currencySwaps_elem)
        
    def write_floatingShortLegSpreadSchedule_elem(self, row, shortLeg_elem):
        floatingSpreadSchedule_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_TAG)
        shortLeg_elem.append(floatingSpreadSchedule_elem)
        row_date = self.writer._get_raw_data(row, AptColumns.FLOAT_SHORT_LEG_DATE)
        row_spread = self.writer._get_raw_data(row, AptColumns.FLOAT_SHORT_LEG_SPREAD)
        floatingSpreadScheduleEntry_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_ENTRY_TAG, date=row_date, spread=row_spread)
        floatingSpreadSchedule_elem.append(floatingSpreadScheduleEntry_elem)
    
    def write_fixedShortLegCouponSchedule_elem(self, row, shortLeg_elem):
        fixedCouponSchedule_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_TAG)
        shortLeg_elem.append(fixedCouponSchedule_elem)
        row_date = self.writer._get_raw_data(row, AptColumns.FIXED_SHORT_LEG_DATE)
        row_coupon = self.writer._get_raw_data(row, AptColumns.FIXED_SHORT_LEG_COUPON)
        fixedCouponScheduleEntry_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_ENTRY_TAG, date=row_date, coupon=row_coupon)
        fixedCouponSchedule_elem.append(fixedCouponScheduleEntry_elem)
        
    def write_floatingLongLegSpreadSchedule_elem(self, row, longLeg_elem):
        floatingSpreadSchedule_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_TAG)
        longLeg_elem.append(floatingSpreadSchedule_elem)
        row_date = self.writer._get_raw_data(row, AptColumns.FLOAT_LONG_LEG_DATE)
        row_spread = self.writer._get_raw_data(row, AptColumns.FLOAT_LONG_LEG_SPREAD)
        floatingSpreadScheduleEntry_elem = ElementTree.Element(self.FLOATING_SPREAD_SCHEDULE_ENTRY_TAG, date=row_date, spread=row_spread)
        floatingSpreadSchedule_elem.append(floatingSpreadScheduleEntry_elem)
    
    def write_fixedLongLegCouponSchedule_elem(self, row, longLeg_elem):
        fixedCouponSchedule_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_TAG)
        longLeg_elem.append(fixedCouponSchedule_elem)
        row_date = self.writer._get_raw_data(row, AptColumns.FIXED_LONG_LEG_DATE)
        row_coupon = self.writer._get_raw_data(row, AptColumns.FIXED_LONG_LEG_COUPON)
        fixedCouponScheduleEntry_elem = ElementTree.Element(self.FIXED_COUPON_SCHEDULE_ENTRY_TAG, date=row_date, coupon=row_coupon)
        fixedCouponSchedule_elem.append(fixedCouponScheduleEntry_elem)
        
    def write_shortLeg_elem(self, row, currencySwap_elem):
        row_principal = self.writer._get_raw_data(row, AptColumns.SHORT_LEG_PRINCIPAL)
        row_currency = self.writer._get_raw_data(row, AptColumns.SHORT_LEG_CURRENCY)
        row_couponFrequency = self.writer._get_raw_data(row, AptColumns.SHORT_PAYMENT_FREQUENCY)
        shortLeg_elem = ElementTree.Element(self.SHORT_LEG_TAG, principal=row_principal, currency=row_currency, couponFrequency=row_couponFrequency)
        shortLegFixed = self.writer._get_raw_data(row, AptColumns.SHORT_LEG_IS_FIXED)
        if shortLegFixed in ('true'):
            self.write_fixedShortLegCouponSchedule_elem(row, shortLeg_elem)
        else: self.write_floatingShortLegSpreadSchedule_elem(row, shortLeg_elem)
        currencySwap_elem.append(shortLeg_elem)
        
    def write_longLeg_elem(self, row, currencySwap_elem):
        row_principal = self.writer._get_raw_data(row, AptColumns.LONG_LEG_PRINCIPAL)
        row_currency = self.writer._get_raw_data(row, AptColumns.LONG_LEG_CURRENCY)
        row_couponFrequency = self.writer._get_raw_data(row, AptColumns.PAYMENT_FREQUENCY)
        longLeg_elem = ElementTree.Element(self.LONG_LEG_TAG, principal=row_principal, currency=row_currency, couponFrequency=row_couponFrequency)
        longLegFixed = self.writer._get_raw_data(row, AptColumns.LONG_LEG_IS_FIXED)
        if longLegFixed in ('true'):
            self.write_fixedLongLegCouponSchedule_elem(row, longLeg_elem)
        else: self.write_floatingLongLegSpreadSchedule_elem(row, longLeg_elem)
        currencySwap_elem.append(longLeg_elem)

    def write_legs_elem(self, row, currencySwap_elem):
        self.write_shortLeg_elem(row, currencySwap_elem)
        self.write_longLeg_elem(row, currencySwap_elem)
    
    def write_elem(self):
        for row in self.ins_rows:
            row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
            row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
            row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
            row_swapRate = self.writer._get_raw_data(row, AptColumns.SWAP_RATE)
            row_paymentFrequency = self.writer._get_raw_data(row, AptColumns.PAYMENT_FREQUENCY)
            row_shortPaymentFrequency = self.writer._get_raw_data(row, AptColumns.SHORT_PAYMENT_FREQUENCY)
            currencySwap_elem = ElementTree.Element(self.CURRENCY_SWAP_TAG, id=row_id, idType=row_idType, expires=row_expires)
            self.write_legs_elem(row, currencySwap_elem)
            self.currencySwaps_elem.append(currencySwap_elem)
            self.writer._write_marketData_element(row)


class AptOptionsElementWriter(AssetClassElementWriter):
    
    OPTIONS_TAG                 = 'options'
    OPTION_TAG                  = 'option'
    CURRENCY_OPTION_TAG         = 'currencyOption'
    UNDERLYING_TAG              = 'underlying'
    STRIKE_TAG                  = 'strike'
    EUROPEAN_TAG                = 'europeanExercise'
    AMERICAN_TAG                = 'americanExercise'
    SWAPTION_TAG                = 'swaption'
    BARRIER_TAG                 = 'barrier'
    DIGITAL_TAG                 = 'digital'
    CURRENCY_OPTION_TAG         = 'currencyOption'
    DIGITAL_CURRENCY_OPTION_TAG = 'digitalCurrencyOption'
    PAYOFF_TAG                  = 'payoff'
    CALL_TAG                    = 'call'
    PUT_TAG                     = 'put '
        

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.options_elem = ElementTree.Element(self.OPTIONS_TAG)
        self.writer.assets_elem.append(self.options_elem)
        self.option_elem = None
    
    def get_writer_func(self, row):
        if self.writer._get_raw_data(row, AptColumns.UND_TYPE) in ('Curr'):
            if self.writer._get_raw_data(row, AptColumns.IS_BARRIER) in ('True'):
                return self._write_currency_barrier_option_element(row)
            elif self.writer._get_raw_data(row, AptColumns.IS_DIGITAL) in ('True'):
                return self._write_currency_digital_option_element(row)
        elif self.writer._get_raw_data(row, AptColumns.UND_TYPE) in ('Swap'):
            return self._write_swaption_element(row)
        elif self.writer._get_raw_data(row, AptColumns.IS_BARRIER) in ('True'):
            return self._write_barrier_option_element(row)
        elif self.writer._get_raw_data(row, AptColumns.IS_DIGITAL) in ('True'):
            return self._write_digital_option_element(row)
    
    def write_elem(self):
        for row in self.ins_rows:
            if self.writer._get_raw_data(row, AptColumns.UND_TYPE) not in ('Curr', 'Swap'):
                self._write_option_element(row)
            elif self.writer._get_raw_data(row, AptColumns.UND_TYPE) in ('Curr') and not        self.writer._get_raw_data(row, AptColumns.IS_DIGITAL) in ('True'):
                self._write_currency_option_element(row)
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)
            self.writer._write_marketData_element(row)
            
    def _write_currency_barrier_option_element(self, row):
        row_barrier_value = self.writer._get_raw_data(row, AptColumns.BARRIER_VALUE)
        row_barrier_direction = self.writer._get_raw_data(row, AptColumns.BARRIER_DIRECTION)
        row_barrier_type = self.writer._get_raw_data(row, AptColumns.BARRIER_TYPE)
        row_barrier_base = self.writer._get_raw_data(row, AptColumns.BARRIER_BASE)
        barrier_elem = ElementTree.Element(self.BARRIER_TAG, barrier=row_barrier_value, direction=row_barrier_direction, type=row_barrier_type, base=row_barrier_base)
        self.currencyOption_elem.append(barrier_elem)
        
    def _write_currency_digital_option_element(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_base = self.writer._get_raw_data(row, AptColumns.CALL_CURRENCY)
        row_counter = self.writer._get_raw_data(row, AptColumns.PUT_CURRENCY)
        row_strike = self.writer._get_raw_data(row, AptColumns.STRIKE)
        digital_currency_option_elem = ElementTree.Element(self.DIGITAL_CURRENCY_OPTION_TAG, id=row_id, expires=row_expires, base=row_base, counter=row_counter, strike=row_strike)
        row_exercise_type = self.writer._get_raw_data(row, AptColumns.EXERCISE_TYPE)
        if row_exercise_type == 'EUROPEAN':
            exercise_elem = ElementTree.Element(self.EUROPEAN_TAG)
            digital_currency_option_elem.append(exercise_elem)
        row_digital_payoff = self.writer._get_raw_data(row, AptColumns.CURR_DIGITAL_PAYOFF_AMOUNT)
        row_digital_currency = self.writer._get_raw_data(row, AptColumns.CURR_DIGITAL_PAYOFF)
        row_direction = None
        digital_elem = ElementTree.Element(self.PAYOFF_TAG, currency=row_digital_currency, amount=row_digital_payoff, direction="UP")
        digital_currency_option_elem.append(digital_elem)
        self.options_elem.append(digital_currency_option_elem)
    
    def _write_currency_option_element(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_callCurrency = self.writer._get_raw_data(row, AptColumns.CALL_CURRENCY)
        row_callAmount = self.writer._get_raw_data(row, AptColumns.CALL_AMOUNT)
        row_putAmount = self.writer._get_raw_data(row, AptColumns.PUT_AMOUNT)
        row_putCurrency = self.writer._get_raw_data(row, AptColumns.PUT_CURRENCY)
        self.currencyOption_elem = ElementTree.Element(self.CURRENCY_OPTION_TAG, id=row_id, idType=row_idType, expires=row_expires)
        call_elem = ElementTree.Element(self.CALL_TAG, currency=row_callCurrency, amount=row_callAmount)
        put_elem = ElementTree.Element(self.PUT_TAG, currency=row_putCurrency, amount=row_putAmount)
        self.currencyOption_elem.append(call_elem)
        self.currencyOption_elem.append(put_elem)
        row_exercise_type = self.writer._get_raw_data(row, AptColumns.EXERCISE_TYPE)
        if row_exercise_type == 'EUROPEAN':
            exercise_elem = ElementTree.Element(self.EUROPEAN_TAG)
        else:
            exercise_elem = ElementTree.Element(self.AMERICAN_TAG)
        self.currencyOption_elem.append(exercise_elem)
        self.options_elem.append(self.currencyOption_elem)
        
    def _write_swaption_element(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        row_swapTermYrs = self.writer._get_raw_data(row, AptColumns.SWAP_TERM_YRS)
        row_swapRate = self.writer._get_raw_data(row, AptColumns.SWAP_RATE)
        row_swapType = self.writer._get_raw_data(row, AptColumns.SWAP_TYPE)
        row_paymentFrequency = self.writer._get_raw_data(row, AptColumns.PAYMENT_FREQUENCY)
        row_shortPaymentFrequency = self.writer._get_raw_data(row, AptColumns.SHORT_PAYMENT_FREQUENCY)
        swaption_elem = ElementTree.Element(self.SWAPTION_TAG, id=row_id, currency=row_currency, expires=row_expires, swapTermYrs=row_swapTermYrs, swapRate=row_swapRate, swapType=row_swapType, paymentFrequency=row_paymentFrequency, shortPaymentFrequency=row_shortPaymentFrequency)
        row_exercise_type = self.writer._get_raw_data(row, AptColumns.EXERCISE_TYPE)
        if row_exercise_type == 'EUROPEAN':
            exercise_elem = ElementTree.Element(self.EUROPEAN_TAG)
        else:
            exercise_elem = ElementTree.Element(self.AMERICAN_TAG)
        swaption_elem.append(exercise_elem)
        self.options_elem.append(swaption_elem)
    
    def _write_barrier_option_element(self, row):
        row_barrier_value = self.writer._get_raw_data(row, AptColumns.BARRIER_VALUE)
        row_barrier_direction = self.writer._get_raw_data(row, AptColumns.BARRIER_DIRECTION)
        row_barrier_type = self.writer._get_raw_data(row, AptColumns.BARRIER_TYPE)
        barrier_elem = ElementTree.Element(self.BARRIER_TAG, barrier=row_barrier_value, direction=row_barrier_direction, type=row_barrier_type)
        self.option_elem.append(barrier_elem)
        
    def _write_digital_option_element(self, row):
        row_digital_payoff = self.writer._get_raw_data(row, AptColumns.DIGITAL_PAYOFF)
        digital_elem = ElementTree.Element(self.DIGITAL_TAG, payoff=row_digital_payoff)
        if row_digital_payoff == 'CASH':
            row_digital_cash_amount = self.writer._get_raw_data(row, AptColumns.DIGITAL_CASH_AMOUNT)
            digital_elem.attrib['cash'] = row_digital_cash_amount
            self.option_elem.append(digital_elem)

    def _write_option_element(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_idType = self.writer._get_raw_data(row, AptColumns.ASSET_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_type = self.writer._get_raw_data(row, AptColumns.TYPE)
        row_expires = self.writer._get_raw_data(row, AptColumns.EXPIRES)
        self.option_elem = ElementTree.Element(self.OPTION_TAG, id=row_id, idType=row_idType, currency=row_currency, type=row_type, expires=row_expires)
        self.options_elem.append(self.option_elem)
       
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        underlying_elem = ElementTree.Element(self.UNDERLYING_TAG, id=row_und_id, idType=row_und_idType)
        self.option_elem.append(underlying_elem)
        
        row_strike = self.writer._get_raw_data(row, AptColumns.STRIKE)
        strike_elem = ElementTree.Element(self.STRIKE_TAG, value=row_strike)
        self.option_elem.append(strike_elem)
        
        row_exercise_type = self.writer._get_raw_data(row, AptColumns.EXERCISE_TYPE)
        if row_exercise_type == 'EUROPEAN':
            exercise_elem = ElementTree.Element(self.EUROPEAN_TAG)
        else:
            exercise_elem = ElementTree.Element(self.AMERICAN_TAG)
        self.option_elem.append(exercise_elem)


class AptDerivativesElementWriter(AssetClassElementWriter):
    
    DERIVATIVES_TAG     = 'derivatives'
    DERIVATIVE_TAG      = 'derivative'

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
        self.derivatives_elem = ElementTree.Element(self.DERIVATIVES_TAG)
        self.writer.assets_elem.append(self.derivatives_elem)
        self.option_elem = None
    
    def get_writer_func(self, row): 
        return self._write_derivative_element(row)
    
    def write_elem(self):
        for row in self.ins_rows:
            elem_writer_func = self.get_writer_func
            elem_writer_func(row)
            self.writer._write_marketData_element(row)
    
    def _write_derivative_element(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_und_id = self.writer._get_raw_data(row, AptColumns.UND_ID)
        row_und_idType = self.writer._get_raw_data(row, AptColumns.UND_ID_TYPE)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        self.derivative_elem = ElementTree.Element(self.DERIVATIVE_TAG, id=row_id, underlying=row_und_id, undIdType=row_und_idType, currency=row_currency)
        self.derivatives_elem.append(self.derivative_elem)
        
        
class TimeSeriesAssetsWriter(AssetClassElementWriter):
    TIME_SERIES_TAG             = 'timeSeries'
    PRICES_PARENT_TAG           = 'prices'
    PROPORTIONAL_RETURNS_TAG    = 'proportionalReturns'
    WEEKLY_DATA_TAG             = 'weeklyData'
    RETURNS_TAG                 = 'returns'
    PRICES_TAG                  = 'prices'
    DATES_TAG                   = 'dates'
    

    def __init__(self, writer, ins_rows):
        self.writer = writer
        self.ins_rows = ins_rows
       
    def _add_prices_element(self, ins_id):
        prices_parent_elem = ElementTree.Element(self.PRICES_PARENT_TAG)
        dates_elem = ElementTree.Element(self.DATES_TAG)
        prices_elem = ElementTree.Element(self.PRICES_TAG)
        time_series = FAptReportCommon.AptTimeSeries(ins_id)
        dates_elem.text = time_series.get_daily_time_series('Day')
        prices_elem.text = time_series.get_daily_time_series('Settle')
        prices_parent_elem.append(dates_elem)
        prices_parent_elem.append(prices_elem)
        self.timeSeries_elem.append(prices_parent_elem)
        
    def _add_proportionalReturns_element(self, ins_id):
        proportionlaReturns_elem = ElementTree.Element(self.PROPORTIONAL_RETURNS_TAG)
        weeklyData_elem = ElementTree.Element(self.WEEKLY_DATA_TAG)
        dates_elem = ElementTree.Element(self.DATES_TAG)
        returns_elem = ElementTree.Element(self.RETURNS_TAG)
        time_series = FAptReportCommon.AptTimeSeries(ins_id)
        dates_elem.text = time_series.get_weekly_dates()
        returns_elem.text = time_series.get_weekly_returns()
        weeklyData_elem.append(dates_elem)
        weeklyData_elem.append(returns_elem)
        proportionlaReturns_elem.append(weeklyData_elem)
        self.timeSeries_elem.append(proportionlaReturns_elem)
        
    def _write_time_series_instrument(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_class = self.writer._get_raw_data(row, AptColumns.ASSET_CLASS)
        self.timeSeries_elem = ElementTree.Element(self.TIME_SERIES_TAG, id=row_id, currency=row_currency)
        self.timeSeries_elem.attrib['class'] = row_class
        if 'SVT' not in self.writer.factor_model:
            self._add_proportionalReturns_element(row_id)
        else:
            self._add_prices_element(row_id)
        self.writer.timeSeriesAssets_elem.append(self.timeSeries_elem) #check this out on ASP
        logger.debug("Adding instrument '%s' to time series element", row_id)
        
    def _write_time_series(self, row):
        row_id = self.writer._get_raw_data(row, AptColumns.ASSET_ID)
        row_currency = self.writer._get_raw_data(row, AptColumns.CURRENCY)
        row_class = self.writer._get_raw_data(row, AptColumns.ASSET_CLASS)
        self.timeSeries_elem = ElementTree.Element(self.TIME_SERIES_TAG, id=row_id, currency=row_currency)
        self.timeSeries_elem.attrib['class'] = row_class
        if 'SVT' not in self.writer.factor_model:
            self._add_proportionalReturns_element(row_id)
        else:
            self._add_prices_element(row_id)
        self.writer.timeSeriesAssets_elem.append(self.timeSeries_elem) #check this out on ASP
        logger.debug("Adding instrument '%s' to time series element", row_id)

    def write_elem(self):
        for row in self.ins_rows:
            self._write_time_series(row)


class AptProXmlGenerator(object):

    LINE_TAG = "{http://www.apt.com/pro}line"
    
    def __init__(self, params):
        portfolios = params.portfolios
        trade_filters = params.trade_filters
        grouper = params.groupers[0]
        self.params = params
        self.instruments = self._get_instruments(portfolios, trade_filters)
        self.composition_file = params.composition_file
        self.universe_file = params.universe_file
        self.prime_report_generator = PrimeReportWriter(portfolios, trade_filters, self.instruments, grouper)
        self.report_contents = self.prime_report_generator.get_parser()
        
    def _get_underlying(ins):
        try:
            if ins.IsFutureOnNotional():
                if ins.IsAUDF(): return ins.Underlying()
                return ins.Underlying().SelectedDeliverable()
            return ins.ValuationUnderlying()
        except AttributeError:
            return ins.ValuationUnderlying()
        
    def _get_instruments_recursive(self, ins, instruments, instruments_to_report):
        und = ins.Underlying()
        if und and und not in instruments+instruments_to_report:
            instruments.append(und)
            self._get_instruments_recursive(und, instruments, instruments_to_report)
            
    def _get_open_instruments(self, port):
        piat = acm.Risk().CreatePortfolioInstrumentAndTrades(port)
        instruments = piat.Instruments()
        valuation_date = acm.Time().DateValueDay()
        date_today = acm.Time().DateToday()
        open_positions = piat.OpenPositions()
        
        def _mapped_valuation_parameters():
            mappedValuationParameters = acm.GetFunction('mappedValuationParameters', 0)
            return mappedValuationParameters()
        
        valuation_parameters = _mapped_valuation_parameters().Parameter()
        
        def _values_on_spot(ins):
            mapped_valuation_until_spot = ins.MappedValuationUntilSpotLink().Link()
            if mapped_valuation_until_spot == 'True': return 1
            report_date = valuation_parameters.ReportDate()
            if report_date == 'Instrument Spot': return 1
            return 0
        
        def _only_spot_valued_instruments(instruments):
            only_spot_valued_instruments = []
            for ins in instruments:
                only_spot_valued_instruments.append(_values_on_spot(ins) == 1)
            if 0 in only_spot_valued_instruments:
                return 0
            return 1
            
        def _include_simulated_trades():
            return valuation_parameters.IncludeSimulatedTrades()

        def _include_reserved_trades():
            return valuation_parameters.IncludeReservedTrades()

        include_simulated_trades = _include_simulated_trades()
        include_reserved_trades = _include_reserved_trades()
            
        def _tradeStatusInclusionMaskStandard(include_simulated_trades, include_reserved_trades):
            trade_status_inclusion_mask_standard = acm.GetFunction('tradeStatusInclusionMaskStandard', 2)
            return trade_status_inclusion_mask_standard(include_simulated_trades, include_reserved_trades)

        def _tradeCategoryInclusionMaskDefault():
            return acm.GetFunction('tradeCategoryInclusionMaskNotCollateral', 0)()

        def _adjustParameterDate(valuation_date, date_today):
            adjust_parameter_date = acm.GetFunction('adjustParameterDate', 2)
            return adjust_parameter_date(valuation_date, date_today)

        only_spot_valued_instruments = _only_spot_valued_instruments(instruments)
        trade_parameter_date = _adjustParameterDate(valuation_date, date_today)
        include_simulated_trades = _include_simulated_trades()
        include_reserved_trades = _include_reserved_trades()
        trade_status_inclusion_mask_default = _tradeStatusInclusionMaskStandard(include_simulated_trades, include_reserved_trades)
        trade_category_inclusion_mask_default = _tradeCategoryInclusionMaskDefault()
        open_instruments = open_positions.OpenPositionInstruments(valuation_date, only_spot_valued_instruments, trade_parameter_date, trade_status_inclusion_mask_default, trade_category_inclusion_mask_default)
        return open_instruments

    def _get_instruments(self, portfolios, trade_filters):
        instruments = []
        for item in portfolios+trade_filters:
            try:
                open_instruments = self._get_open_instruments(item)
                instruments_to_report = list(open_instruments)
            except:
                instruments_to_report = list(set([trd.Instrument() for trd in item.Query().Select()]))
            for ins in instruments_to_report:
                if not ins.IsKindOf('FInstrument'):
                    continue
                self._get_instruments_recursive(ins, instruments, instruments_to_report)
        return instruments
        
    def generate_universe(self):
        univ_writer = UniverseFileWriter(self.report_contents, self.params)
        univ_xml = univ_writer.write()

    def generate_composition(self):
        comp_writer = CompositionFileWriter(self.report_contents, self.params, self.instruments)
        comp_xml = comp_writer.write()
        return comp_xml
        
    def is_valid_composition(self, comp_xml):
        try: 
            if (ElementTree.XML(comp_xml).find(".//"+self.LINE_TAG)) != None:
                return 1
            else:
                logger.info("Cant export zero position")
                return 0
        except TypeError as err:
            logger.debug("Cant export empty position file. Reason: %s", err)
            logger.info("Cant export empty position file")
            return 0
            
    def start_apt(self):
        apt_launcher = FAptLauncher.AptLauncher(self.composition_file, self.universe_file)
        apt_launcher.create_universe_xdb_file()
        apt_launcher.run_apt_app()
        
    def _valid_comp(self, comp):
        self.is_valid_comp = self.is_valid_composition(comp)
    
    def generate(self):
        """
            1. generate apt composition xml file
            2. generate apt universe xml file
        """
        comp = self.generate_composition()
        univ = self.generate_universe()
        self._valid_comp(comp)
        
def generate(params):
    g = AptProXmlGenerator(params)
    g.generate()
    if bool(params.launch_apt) and g.is_valid_comp:
        g.start_apt()
