import acm
import traceback
import FRegulatoryLogger
import FRegulatoryUtils
import FRegulatoryLibUtils
import FRegulatoryInfoException
import FRegulatoryLookup
import FInstrumentClassification
import FRegulatoryLib
from contextlib import contextmanager
logger = 'FInsRegInfoCustomMethods'
@contextmanager
def TryExcept():
    try:
        yield None
    except Exception as e:
        print((Exception, e))
        print((traceback.format_exc()))
        raise e

def Infant(reginfo):
    if reginfo.Class() == acm.FInstrumentRegulatoryInfo:
        if reginfo.Instrument().IsInfant():
            FRegulatoryLogger.INFO(logger, "Select instrument to reflect the selections")

def IsPersistent(ins_reginfo):
    persistent = False
    if not ins_reginfo.Instrument().IsDeleted():
        persistent = True
    return persistent

def GetAdmissionApprovalTime(ins_reginfo):
    """get Date and time the issuer has approved admission to trading on a Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            approval_time = ins_reginfo.AdditionalInfo().RegTrdAdmisAppTime()
            if not approval_time:
                return ""
            else:
                return acm.Time().DateTimeFromTime(approval_time)

def SetAdmissionApprovalTime(ins_reginfo, approval_time):
    """set Date and time the issuer has approved admission to trading on a Trading Venue"""
    with TryExcept():
        if (not Infant(ins_reginfo)) and IsPersistent(ins_reginfo):
            approval_date_time, is_valid = FRegulatoryUtils.get_date_time(approval_time)
            if not is_valid:
                msg = "The TradingAdmissionApprovalTime provided <%s> is either not a valid entry or is in format not supported"%approval_time
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            ins_reginfo.AdditionalInfo().RegTrdAdmisAppTime(approval_date_time)

def GetAdmissionRequestTime(ins_reginfo):
    """get Date and time of the request for admission to trading on a Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            request_time = ins_reginfo.AdditionalInfo().RegTrdAdmisReqTime()
            if not request_time:
                return ""
            else:
                return acm.Time().DateTimeFromTime(request_time)

def SetAdmissionRequestTime(ins_reginfo, request_time):
    """set Date and time of the request for admission to trading on a Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            request_date_time, is_valid = FRegulatoryUtils.get_date_time(request_time)
            if not is_valid:
                msg = "The TradingAdmissionRequestTime provided <%s> is either not a valid entry or is in format not supported"%request_time
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            ins_reginfo.AdditionalInfo().RegTrdAdmisReqTime(request_date_time)

def GetTradingTerminationDate(ins_reginfo):
    """get Date when Instrument ceases to be traded on Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegTrdTerminateDate()

def SetTradingTerminationDate(ins_reginfo, termination_date):
    """set Date when Instrument ceases to be traded on Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            trading_term_date, err_msg = FRegulatoryUtils.validate_date(termination_date)
            if err_msg:
                msg = "The TradingTerminationDate provided <%s> is either not a valid entry or is in format not supported"%termination_date
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            ins_reginfo.AdditionalInfo().RegTrdTerminateDate(trading_term_date)

def GetFirstTradingTime(ins_reginfo):
    """get Date and time of the admission to, or the first quote, order or trade on a Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            trading_time = ins_reginfo.AdditionalInfo().RegFirstTradeTime()
            if trading_time:
                trading_time = acm.Time().DateTimeFromTime(trading_time)
            return trading_time

def SetFirstTradingTime(ins_reginfo, first_trading_time):
    """set Date and time of the admission to, or the first quote, order or trade on a Trading Venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            first_trading_datetime, is_valid = FRegulatoryUtils.get_date_time(first_trading_time)
            if not is_valid:
                msg = "The FirstTradingTime provided <%s> is either not a valid entry or is in format not supported"%first_trading_time
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            ins_reginfo.AdditionalInfo().RegFirstTradeTime(first_trading_datetime)

def GetTransactionType(ins_reginfo):
    """get Transaction type as specified by the trading venue for commodity derivatives"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegTransactionType()

def SetTransactionType(ins_reginfo, transaction_type):
    """set Transaction type as specified by the trading venue for commodity derivatives"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            transaction_type_val = None
            if str(transaction_type) not in ['', 'None']:
                transaction_type_val, err_msg = FRegulatoryUtils.get_choice_list_val(transaction_type, 'TransactionType')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegTransactionType(transaction_type_val)

def GetStandardMarketSize(ins_reginfo):
    """get Average values of orders executed on a Trading Venue, per instrument class, during previous year"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            standardMarketSize = ins_reginfo.AdditionalInfo().RegSMS()
            if standardMarketSize:
                return standardMarketSize
            else:
                return 0.0

def SetStandardMarketSize(ins_reginfo, std_market_size):
    """set Average values of orders executed on a Trading Venue, per instrument class, during previous year"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            sms, err_msg = FRegulatoryUtils.get_float(std_market_size, 'StandardMarketSize')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            if str(sms) == '0.0':#it means the value is being removed
                sms = None
            ins_reginfo.AdditionalInfo().RegSMS(sms)

def GetIsTradedOnTradingVenue(ins_reginfo):
    """Is this instrument being traded on the trading venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegToTV()

def SetIsTradedOnTradingVenue(ins_reginfo, is_traded_on_tv):
    """set True if this instrument is being traded on the trading venue"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            is_to_tv = FRegulatoryUtils.get_bool(is_traded_on_tv, 'TradedOnTradingVenue')
            ins_reginfo.AdditionalInfo().RegToTV(is_to_tv)

def GetHasTradingObligation(ins_reginfo):
    """Must this instrument be traded on a regulated exchange, or can it be traded OTC as well [tri-state]"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegHasTrdObligation()

def SetHasTradingObligation(ins_reginfo, has_trading_obligation):
    """set True if this instrument must be traded on a regulated exchange, or can it be traded OTC as well [tri-state]"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            trading_obligation = FRegulatoryUtils.get_bool(has_trading_obligation, 'TradingObligation')
            ins_reginfo.AdditionalInfo().RegHasTrdObligation(trading_obligation)

def GetFinalPriceType(ins_reginfo):
    """get Final price type as specified by the trading venue for commodity derivatives"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegFinalPriceType()

def SetFinalPriceType(ins_reginfo, final_price_type):
    """set Final price type as specified by the trading venue for commodity derivatives"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            final_prc_type, err_msg = FRegulatoryUtils.get_choice_list_val(final_price_type, 'FinalPriceType')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegFinalPriceType(final_prc_type)

def GetFinancialInstrumentShortName(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegFISN()

def SetFinancialInstrumentShortName(ins_reginfo, fisn):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            ins_reginfo.AdditionalInfo().RegFISN(fisn)

def transactionTypes():
    with TryExcept():
        return acm.FChoiceList.Select("list = 'TransactionType'")

def finalPriceTypes():
    with TryExcept():
        return acm.FChoiceList.Select("list = 'FinalPriceType'")

def GetLiquidityBand(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegLiquidityBand()

def GetInstypeRTS2(ins_reginfo):
    """returns the RTS2 instrument type classification"""
    if IsPersistent(ins_reginfo):
        rts2_classify = FInstrumentClassification.FInstrumentClassification(ins_reginfo.Instrument())
        return rts2_classify.mifid2_rts2_instype()

def GetInstypeRTS28(ins_reginfo):
    """get the instype for rts28 as per mifid classification"""
    ins_type = None
    if IsPersistent(ins_reginfo):
        if ins_reginfo.Instrument().InsType() in FRegulatoryLookup.rts_28_ins_type:
            ins_type = FRegulatoryLookup.rts_28_ins_type[ins_reginfo.Instrument().InsType()]
    return ins_type

def GetInsSubtypeRTS2(ins_reginfo):
    """returns the RTS2 instrument sub type classification"""
    sub_type_rts2 = None
    if IsPersistent(ins_reginfo):
        rts2_classify = FInstrumentClassification.FInstrumentClassification(ins_reginfo.Instrument())
        sub_type_rts2 = rts2_classify.mifid2_rts2_inssubtype()
    return sub_type_rts2 

def GetAttributes(ins_reginfo):
    return FRegulatoryUtils.log_reg_attributes(ins_reginfo)

def GetLiquidityBand(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegLiquidityBand()

def SetLiquidityBand(ins_reginfo, liquidity_band):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            liquidity_band_val, err_msg = FRegulatoryUtils.get_integer(liquidity_band, 'LiquidityBand')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegLiquidityBand(liquidity_band_val)

def SetPrimaryMarketMic(ins_reginfo, primary_market_mic):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            primary_market_mic_val, err_msg = FRegulatoryUtils.is_mic(primary_market_mic, 'PrimaryMarketMic')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegPrimaryMktMic(primary_market_mic_val)

def SetMaterialMarketMic(ins_reginfo, material_market_mic):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            material_market_mic_val, err_msg = FRegulatoryUtils.is_mic(material_market_mic, 'MaterialMarketMic')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegMaterialMktMic(material_market_mic_val)

def SetDarkCapStatus(ins_reginfo, dark_cap_status):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            dark_cap_status_val = None
            if str(dark_cap_status) not in ['', 'None']:
                dark_cap_status_val, err_msg = FRegulatoryUtils.get_choice_list_val(dark_cap_status, 'DarkCapStatus')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegDarkCapStatus(dark_cap_status_val)

def SetDoubleVolumeCapStatus(ins_reginfo, double_volume_cap_status):
    with TryExcept():
        if IsPersistent(ins_reginfo)and not Infant(ins_reginfo):
            double_volume_cap_status_val = None
            if str(double_volume_cap_status) not in ['', 'None']:
                double_volume_cap_status_val, err_msg = FRegulatoryUtils.get_choice_list_val(double_volume_cap_status, 'DoubleVolumeCapStatus')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegDblVolCapStatus(double_volume_cap_status_val)

def SetDarkCapMic(ins_reginfo, dark_cap_mic):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            dark_cap_mic_val, err_msg = FRegulatoryUtils.is_mic(dark_cap_mic, 'DarkCapMic')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegDarkCapMic(dark_cap_mic_val)

def SetIsMiFIDTransparent(ins_reginfo, is_mifid_transparent):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            is_mifid_tran = FRegulatoryUtils.get_bool(is_mifid_transparent, 'IsMiFIDTransparent')
            ins_reginfo.AdditionalInfo().RegMiFIDTransparent(is_mifid_tran)

def GetPrimaryMarketMic(ins_reginfo):
    with TryExcept():
        return ins_reginfo.AdditionalInfo().RegPrimaryMktMic()

def GetMaterialMarketMic(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegMaterialMktMic()

def GetDarkCapStatus(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            dark_cap_status = ins_reginfo.AdditionalInfo().RegDarkCapStatus()
            if dark_cap_status:
                dark_cap_status = acm.FChoiceList.Select01("name = '%s' and list = 'DarkCapStatus'"%dark_cap_status, None)
            return dark_cap_status

def GetDoubleVolumeCapStatus(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            double_volume_cap_status = ins_reginfo.AdditionalInfo().RegDblVolCapStatus()
            if double_volume_cap_status:
                double_volume_cap_status = acm.FChoiceList.Select01("name = '%s' and list = 'DoubleVolumeCapStatus'"%double_volume_cap_status, None)
            return double_volume_cap_status

def GetDarkCapMic(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegDarkCapMic()

def GetIsMiFIDTransparent(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            is_mifid_transparent = ins_reginfo.AdditionalInfo().RegMiFIDTransparent()
            if not is_mifid_transparent:
                is_mifid_transparent = False
            return is_mifid_transparent

def darkCapStatuses():
    with TryExcept():
        return acm.FChoiceList.Select("list = 'DarkCapStatus'")

def doubleVolumeCapStatus():
    with TryExcept():
        return acm.FChoiceList.Select("list = 'DoubleVolumeCapStatus'")

def GetTickSize(ins_reginfo):
    """minimum price movement of a trading instrument"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            tickSize = ins_reginfo.AdditionalInfo().RegTickSize()
            if tickSize:
                return tickSize
            else:
                return 0.0

def SetTickSize(ins_reginfo, tick_size):
    """minimum price movement of a trading instrument"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            tickSize, err_msg = FRegulatoryUtils.get_float(tick_size, 'TickSize')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            if str(tickSize) == '0.0':#it means the value is being removed
                tickSize = None
            ins_reginfo.AdditionalInfo().RegTickSize(tickSize)

def GetSimilarIsin(ins_reginfo):
    """get the linked isin that is similar to this one"""
    with TryExcept():
        if IsPersistent(ins_reginfo):
            return ins_reginfo.AdditionalInfo().RegSimilarIsin()

def SetSimilarIsin(ins_reginfo, similar_isin):
    """set link to the isin that is similar to this one"""
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            if not FRegulatoryLibUtils.isValidIsin(similar_isin):
                FRegulatoryLogger.WARN(logger, "Similar Isin being set to <%s> is not a valid ISIN"%similar_isin)
            ins_reginfo.AdditionalInfo().RegSimilarIsin(similar_isin)

def GetRegPostLargeInScale(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            post_large_in_scale = ins_reginfo.AdditionalInfo().RegPostLargeInScale()
            if post_large_in_scale:
                return post_large_in_scale
            else:
                return 0.0

def SetRegPostLargeInScale(ins_reginfo, post_large_in_scale):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            post_large_in_scale, err_msg = FRegulatoryUtils.get_float(post_large_in_scale, 'PostLargeInScale')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegPostLargeInScale(post_large_in_scale)

def GetRegPostSSTI(ins_reginfo):
    with TryExcept():
        if IsPersistent(ins_reginfo):
            post_ssti = ins_reginfo.AdditionalInfo().RegPostSSTI()
            if post_ssti:
                return post_ssti
            else:
                return 0.0

def SetRegPostSSTI(ins_reginfo, post_ssti):
    with TryExcept():
        if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
            post_ssti, err_msg = FRegulatoryUtils.get_float(post_ssti, 'PostSizeSpecificToInstrument')
            if err_msg:
                raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
            ins_reginfo.AdditionalInfo().RegPostSSTI(post_ssti)

def GetPostLargeInScaleInCurrency(ins_reginfo, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(currency)
        SetPostLargeInScaleInCurrency(ins_reginfo, currency, market, latest_fx_rate)
    except:
        with TryExcept():
            if IsPersistent(ins_reginfo):
                post_large_in_scale = ins_reginfo.AdditionalInfo().RegPostLargeInScale()
                if post_large_in_scale:
                    return FRegulatoryUtils.get_fx_value(post_large_in_scale, 'Destination Currency', \
                                        ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                else:
                    return 0.0

def SetPostLargeInScaleInCurrency(ins_reginfo, post_large_in_scale, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(post_large_in_scale)
        with TryExcept():
            if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
                if not latest_fx_rate:
                    FRegulatoryLogger.ERROR(logger, \
                    "The latest FxRates are to be considered while setting the LargeInScale. Argument latest_fx_rate = False is not supported.")
                post_large_in_scale, err_msg = FRegulatoryUtils.get_float(post_large_in_scale, 'PostLargeInScale')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
                post_large_in_scale = FRegulatoryUtils.get_fx_value(post_large_in_scale, 'Source Currency', \
                                    ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                ins_reginfo.AdditionalInfo().RegPostLargeInScale(post_large_in_scale)
    except Exception:
        if str(latest_fx_rate).upper() == str(market).upper():
            market = currency
        return GetPostLargeInScaleInCurrency(ins_reginfo, post_large_in_scale, market, latest_fx_rate)

def GetPostSSTIInCurrency(ins_reginfo, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(currency)
        SetPostSSTIInCurrency(ins_reginfo, currency, market, latest_fx_rate)
    except:
        with TryExcept():
            if IsPersistent(ins_reginfo):
                post_ssti = ins_reginfo.AdditionalInfo().RegPostSSTI()
                if post_ssti:
                    return FRegulatoryUtils.get_fx_value(post_ssti, 'Destination Currency', \
                                        ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                else:
                    return 0.0

def SetPostSSTIInCurrency(ins_reginfo, post_ssti, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(post_ssti)
        with TryExcept():
            if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
                if not latest_fx_rate:
                    FRegulatoryLogger.ERROR(logger, \
                    "The latest FxRates are to be considered while setting the LargeInScale. Argument latest_fx_rate = False is not supported.")
                post_ssti, err_msg = FRegulatoryUtils.get_float(post_ssti, 'PostSizeSpecificToInstrument')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
                post_ssti = FRegulatoryUtils.get_fx_value(post_ssti, 'Source Currency', \
                                    ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                ins_reginfo.AdditionalInfo().RegPostSSTI(post_ssti)
    except Exception:
        if str(latest_fx_rate).upper() == str(market).upper():
            market = currency
        return GetPostSSTIInCurrency(ins_reginfo, post_ssti, market, latest_fx_rate)

def GetLargeInScaleInCurrency(ins_reginfo, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(currency)
        SetLargeInScaleInCurrency(ins_reginfo, currency, market, latest_fx_rate)
    except:
        with TryExcept():
            if IsPersistent(ins_reginfo):
                large_in_scale = ins_reginfo.LargeInScale()
                if large_in_scale:
                    return FRegulatoryUtils.get_fx_value(large_in_scale, 'Destination Currency', \
                                        ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                else:
                    return 0.0

def SetLargeInScaleInCurrency(ins_reginfo, large_in_scale, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(large_in_scale)
        with TryExcept():
            if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
                if not latest_fx_rate:
                    FRegulatoryLogger.ERROR(logger, \
                    "The latest FxRates are to be considered while setting the LargeInScale. Argument latest_fx_rate = False is not supported.")
                large_in_scale, err_msg = FRegulatoryUtils.get_float(large_in_scale, 'LargeInScale')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
                large_in_scale = FRegulatoryUtils.get_fx_value(large_in_scale, 'Source Currency', \
                                    ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                ins_reginfo.LargeInScale(large_in_scale)
    except Exception:
        if str(latest_fx_rate).upper() == str(market).upper():
            market = currency
        return GetLargeInScaleInCurrency(ins_reginfo, large_in_scale, market, latest_fx_rate)

def GetSSTIInCurrency(ins_reginfo, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(currency)
        SetSSTIInCurrency(ins_reginfo, currency, market, latest_fx_rate)
    except:
        with TryExcept():
            if IsPersistent(ins_reginfo):
                ssti = ins_reginfo.SizeSpecificToInstrument()
                if ssti:
                    return FRegulatoryUtils.get_fx_value(ssti, 'Destination Currency', \
                                        ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                else:
                    return 0.0

def SetSSTIInCurrency(ins_reginfo, ssti, currency = None, market = 'ECBFIX', latest_fx_rate = True):
    try:
        float(ssti)
        with TryExcept():
            if IsPersistent(ins_reginfo) and not Infant(ins_reginfo):
                if not latest_fx_rate:
                    FRegulatoryLogger.ERROR(logger, \
                    "The latest FxRates are to be considered while setting the LargeInScale. Argument latest_fx_rate = False is not supported.")
                ssti, err_msg = FRegulatoryUtils.get_float(ssti, 'SizeSpecificToInstrument')
                if err_msg:
                    raise FRegulatoryInfoException.FRegInfoInvalidData(err_msg)
                ssti = FRegulatoryUtils.get_fx_value(ssti, 'Source Currency', \
                        ins_reginfo.Instrument().Currency(), market, currency, latest_fx_rate)
                ins_reginfo.SizeSpecificToInstrument(ssti)
    except Exception:
        if str(latest_fx_rate).upper() == str(market).upper():
            market = currency
        return GetSSTIInCurrency(ins_reginfo, ssti, market, latest_fx_rate)
def GetIsEquityLike(ins_reginfo):
    """returns True if the instrument is an equity/equity like instrument"""
    return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_equity_like()

def GetIsBondLike(ins_reginfo):
    """returns True if the instrument is an bond/bond like instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_bond_like()

def GetIsInterestRateDerivative(ins_reginfo):
    """returns True if the instrument is an interest rate derivative instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_interest_rate_derivative()

def GetIsEquityDerivative(ins_reginfo):
    """returns True if the instrument is an equity derivative instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_equity_derivative()

def GetIsC10Derivative(ins_reginfo):
    """returns True if the instrument is a C10 derivative instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_c10_derivative()

def GetIsFxDerivative(ins_reginfo):
    """returns True if the instrument is a FX derivative instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_fx_derivative()

def GetIsCFD(ins_reginfo):
    """returns True if the instrument is a cfd instrument"""
    if IsPersistent(ins_reginfo):
        return FRegulatoryLib.InstrumentRegInfo(ins_reginfo.Instrument()).is_cfd()


