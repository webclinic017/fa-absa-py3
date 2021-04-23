import acm
import traceback
import FRegulatoryLogger
import FRegulatoryUtils
import FRegulatoryLibUtils
import FRegulatoryInfoException
import FRegulatoryLib
from datetime import datetime
from datetime import timedelta
from time import mktime
import FIntegrationUtils
import FRegulatoryNotionalAmount
from contextlib import contextmanager
logger = 'FTrdRegInfoCustomMethods'
@contextmanager
def TryExcept():
    try:
        yield None
    except Exception as e:
        print((Exception, e))
        print((traceback.format_exc()))
        raise e

def Infant(regInfo):
    if regInfo.Class() == acm.FTradeRegulatoryInfo:
        if regInfo.Trade().IsInfant():
            FRegulatoryLogger.INFO(logger, "Select trade to reflect the selections")



def IsPersistent(trade_reginfo):
    persistent = False
    if not trade_reginfo.Trade().IsDeleted():
        persistent = True
    return persistent

def GetVenue(trade_reginfo):
    """The party of the venue where the trade was executed"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegVenue()

def SetVenue(trade_reginfo, venue):
    """The party of the venue where the trade was executed"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            venue_party, warn_msg, venue_name = FRegulatoryUtils.get_party(venue, 'Venue')
            if warn_msg:
                FRegulatoryLogger.WARN(logger, warn_msg)
            trade_reginfo.AdditionalInfo().RegVenue(venue_party)

def GetTransmissionOfOrdersIndicator(trade_reginfo):
    """get the Indicator of whether the conditions for order transmission are satisfied."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            transmission_of_order_indicator = trade_reginfo.AdditionalInfo().RegTransmOfOrder()
            if str(transmission_of_order_indicator) == 'None':
                transmission_of_order_indicator = False
            return transmission_of_order_indicator

def SetTransmissionOfOrdersIndicator(trade_reginfo, transm_of_order_ind):
    """set the Indicator of whether the conditions for order transmission are satisfied."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegTransmOfOrder(FRegulatoryUtils.get_bool(transm_of_order_ind, 'TransmissionOfOrdersIndicator'))

def GetRepositoryId(trade_reginfo):
    """get the RepositoryId for the trade"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegRepositoryId()

def SetRepositoryId(trade_reginfo, repository_id):
    """set the RepositoryId for the trade"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegRepositoryId(FRegulatoryUtils.get_id_val(repository_id))

def GetReportingEntity(trade_reginfo):
    """get the entity submitting the transaction report to the competent authority"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegReportingEntity()

def SetReportingEntity(trade_reginfo, reporting_entity):
    """set the entity submitting the transaction report to the competent authority"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            reporting_entity_party = FRegulatoryUtils.validate_party(reporting_entity, 'ReportingEntity')
            trade_reginfo.AdditionalInfo().RegReportingEntity(reporting_entity_party)

def GetIsSecurityFinancingTransaction(trade_reginfo):
    """Indicates whether the transaction falls within the scope of Securities Financing Activity as per Securities Financing Transactions Regulation"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            is_security_financing_trans = trade_reginfo.AdditionalInfo().RegSecFinTransInd()
            if str(is_security_financing_trans) == 'None':
                is_security_financing_trans = False
            return is_security_financing_trans

def SetIsSecurityFinancingTransaction(trade_reginfo, is_sec_fin):
    """Indicates whether the transaction falls within the scope of Securities Financing Activity as per Securities Financing Transactions Regulation"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegSecFinTransInd(FRegulatoryUtils.get_bool(is_sec_fin, 'SecurityFinanceTransactionIndicator'))

def GetCfiCode(trade_reginfo):
    """get the CfiCode of the instrument that is being traded upon. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegInsCfiCode()

def SetCfiCode(trade_reginfo, cfi_code):
    """set the CfiCode of the instrument that is being traded upon. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            if trade_reginfo.Trade().CurrencyPair():
                if cfi_code and len(cfi_code) > 6:
                    FRegulatoryLogger.WARN(logger, "The cfiCode provided <%s> is longer than the expected length of 6 characters. Truncating the CfiCode to <%s>"%(cfi_code, str(cfi_code)[:6]))
                    cfi_code = str(cfi_code)[:6]
                elif len(cfi_code) < 6:
                    FRegulatoryLogger.WARN(logger, "The cfiCode provided is <%s>. It should be of 6 characters"%(cfi_code))
            else:
                msg = "The CfiCode can be provided on FX trades only."
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            trade_reginfo.AdditionalInfo().RegInsCfiCode(cfi_code)

def GetAlgoId(trade_reginfo):
    """get the Identification No. of the Algo executing the trade"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegAlgoId()

def SetAlgoId(trade_reginfo, algo_id):
    """set the Identification No. of the Algo executing the trade"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegAlgoId(FRegulatoryUtils.get_id_val(algo_id))

def GetComplexTradeComponentId(trade_reginfo):
    """get the Internal identifier to identify the component trades of a package transaction"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegComplexTrdCmptId()

def SetComplexTradeComponentId(trade_reginfo, complex_trd_cmpt_id):
    """set the Internal identifier to identify the component trades of a package transaction"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegComplexTrdCmptId(FRegulatoryUtils.get_id_val(complex_trd_cmpt_id))

def GetExchangeId(trade_reginfo):
    """get the entity submitting the transaction report to the competent authority"""
    with TryExcept():
        return trade_reginfo.AdditionalInfo().RegExchangeId()

def SetExchangeId(trade_reginfo, exchange_id):
    """set the entity submitting the transaction report to the competent authority"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegExchangeId(FRegulatoryUtils.get_id_val(exchange_id))

def GetIsinTrade(trade_reginfo):
    """get the Isin of the instrument that is being traded upon. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegInsIsin()

def SetIsinTrade(trade_reginfo, isin):
    """set the Isin of the instrument that is being traded upon. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            if trade_reginfo.Trade().CurrencyPair():
                if not FRegulatoryLibUtils.isValidIsin(isin):
                    FRegulatoryLogger.WARN(logger, "Isin being set to <%s> is not a valid ISIN"%isin)
            else:
                msg = "The Isin can be provided on FX trades only."
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            trade_reginfo.AdditionalInfo().RegInsIsin(isin)

def GetIsCommodityDerivative(trade_reginfo):
    """Indicates whether the transaction reduces risk in an objectively measurable way in accordance with Article 57 of Directive 2014/65/EU"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            is_commodity_derivative = trade_reginfo.AdditionalInfo().RegComdtyDerivInd()
            if str(is_commodity_derivative) == 'None':
                is_commodity_derivative = False
            return is_commodity_derivative

def SetIsCommodityDerivative(trade_reginfo, is_comdty_deriv):
    """Indicates whether the transaction reduces risk in an objectively measurable way in accordance with Article 57 of Directive 2014/65/EU"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegComdtyDerivInd(FRegulatoryUtils.get_bool(is_comdty_deriv, 'CommodityDerivativeIndicator'))

def GetInvestmentDeciderCrmId(trade_reginfo):
    """get Customer Relationship Management Id of the investment decider"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegInvesDecidrCrmId()

def SetInvestmentDeciderCrmId(trade_reginfo, invest_decider_crm_id):
    """set Customer Relationship Management Id of the investment decider"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegInvesDecidrCrmId(FRegulatoryUtils.get_id_val(invest_decider_crm_id))

def GetExecutingEntity(trade_reginfo):
    """get the party executing the transaction"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegExecutingEntity()

def SetExecutingEntity(trade_reginfo, executing_entity):
    """set the party executing the transaction"""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            executing_entity_party, warn_msg, executing_entity_name = FRegulatoryUtils.get_party(executing_entity, 'ExecutingEntity', ['Market'])
            if warn_msg:
                FRegulatoryLogger.WARN(logger, warn_msg)
            trade_reginfo.AdditionalInfo().RegExecutingEntity(executing_entity_party)

def GetIsProvidingLiquidity(trade_reginfo):
    """get whether the order is Aggressive (Liquidity Taking) or Passive (Liquidity Adding)."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegProvideLiquidity()

def SetIsProvidingLiquidity(trade_reginfo, is_agg_passive):
    """set whether the order is Aggressive (Liquidity Taking) or Passive (Liquidity Adding)."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            trade_reginfo.AdditionalInfo().RegProvideLiquidity(FRegulatoryUtils.get_bool(is_agg_passive, 'IsProvidingLiquidity'))

def GetAttributes(trade_reginfo):
    return FRegulatoryUtils.log_reg_attributes(trade_reginfo)

def regExecutingEntityNames():
    """return the list of possible executing entities"""
    return FRegulatoryUtils.names_of_parties('Market')

def regVenueNames():
    """return the list of possible venues"""
    return FRegulatoryUtils.names_of_venues()

def regReportingEntityNames():
    """return the list of possible MiFID Reporters"""
    brokers = acm.FParty.Select('type="Broker"')
    counterparties = acm.FParty.Select('type="Counterparty"')
    internalDepartments = acm.FParty.Select('type="Intern Dept"')
    parties = acm.FSortedCollection()
    parties.AddAll(brokers)
    parties.AddAll(counterparties)
    parties.AddAll(internalDepartments)
    return acm.FIndexedPopulator(parties)
    #return FRegulatoryUtils.names_of_parties()

def GetTradeTimeWithPrecision(trade_reginfo):
    if IsPersistent(trade_reginfo):
        micro_seconds_val = None
        date_val, time_val, am_pm = FRegulatoryUtils.get_time_in_system_format(trade_reginfo.Trade().TradeTime())
        if FIntegrationUtils.FIntegrationUtils.get_acm_version_override() < 2016.4:
            micro_seconds_val = trade_reginfo.AdditionalInfo().RegMicroSeconds()
        else:
            micro_seconds_val = trade_reginfo.TimePrecision()
        if not micro_seconds_val:
            micro_seconds_val = '000000'
        if len(str(micro_seconds_val)) > 6:
            micro_seconds_val = str(micro_seconds_val)[0:6]
            FRegulatoryLogger.WARN(logger, 'Truncating to only the first 6 digits for microseconds')
        return date_val + ' ' + time_val + '.' + str(micro_seconds_val).zfill(6) + ' ' + am_pm

def SetTradeTimeWithPrecision(trade_reginfo, time_precision):
    if IsPersistent(trade_reginfo):
        datetime_val, micro_seconds = FRegulatoryUtils.get_datetime_microseconds(time_precision)
        try:
            datetime_val = trade_reginfo.DateTimeField(datetime_val)
            trade_time = trade_reginfo.Trade().TradeTime()
            if time_precision.find('T') != -1:
                trade_time = acm.Time().LocalToUtc(trade_reginfo.Trade().TradeTime())
            if datetime_val == trade_time:
                trade_reginfo.TimePrecision(micro_seconds)
            else:
                msg = "Only time precision can be changed here. TradeTime can be changed from the Front Office tab only"
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg) 
        except Exception as e:
            msg = 'Valid value should be provided for TradeTimeWithPrecision. Error: <%s>'%str(e)
            FRegulatoryLogger.ERROR(logger, msg)
            raise FRegulatoryInfoException.FRegInfoInvalidData(msg) 

def GetTimePrecisionInUTC(trade_reginfo):
    if IsPersistent(trade_reginfo):
        val = FRegulatoryUtils.milliseconds_to_utc_datetime(FRegulatoryUtils.locale_datetime_to_milliseconds(trade_reginfo.Trade().TradeTime()))
        date_obj = datetime.strptime(val, "%Y-%m-%d %H:%M:%S.%f")
        micro_seconds_val = None
        micro_seconds_val = trade_reginfo.TimePrecision()
        if not micro_seconds_val:
            micro_seconds_val = 0
        date_obj = date_obj + timedelta(microseconds = micro_seconds_val)
        local_val = utc_to_local(date_obj).strftime('%Y-%m-%d %H:%M:%S.%f %Z%z')
        sec_since_epoch = mktime(date_obj.timetuple()) + date_obj.microsecond/1000000.0
        millis_since_epoch = sec_since_epoch * 1000
        secs = float(millis_since_epoch) / 1000.0
        UTC_OFFSET_TIMEDELTA = datetime.utcnow() - datetime.now()
        utc_date_time = datetime.fromtimestamp(secs) + 2*UTC_OFFSET_TIMEDELTA
        return utc_date_time.strftime("%Y-%m-%dT%H:%M:%S.%fZ")

def utc_to_local(utc_dt):
    # get integer timestamp to avoid precision lost
    import calendar
    timestamp = calendar.timegm(utc_dt.timetuple())
    local_dt = datetime.fromtimestamp(timestamp)
    assert utc_dt.resolution >= timedelta(microseconds=1)
    return local_dt.replace(microsecond=utc_dt.microsecond)

def GetShortSellIndicator(trade):
    """get the ShortSellIndicator value"""
    with TryExcept():
        import string
        version = ".".join(acm.ShortVersion().strip(string.ascii_letters).split(".")[0:2])
        version = float(version.replace('Python', ''))
        if version < 2017.2:
            return trade.AdditionalInfo().RegShortSell()
        else:
            choicelist_lookup = {'Short Security' : 'Sell Short', 'Short Sell Exempt' : 'Sell Short Exempt', 'Short Sell Undi' : 'Sell Short Undi', 'Buy Cover' : 'Buy Cover'}
            cl_event = None
            choicelist_obj = None
            if trade.BusinessEventTradeLinks() and trade.BusinessEventTradeLinks()[0].BusinessEvent():
                event_type = trade.BusinessEventTradeLinks()[0].BusinessEvent().EventType()
                if event_type == 'Short Security' and trade.Nominal() > 0:
                    event_type = 'Buy Cover'
                if event_type in list(choicelist_lookup.keys()):
                    cl_event = choicelist_lookup[event_type]
                if cl_event:
                    choicelist_obj = acm.FChoiceList.Select01("list = 'ShortSellIndicator' and name = '%s'"%cl_event, None)
            return choicelist_obj

def SetShortSellIndicator(trade, short_sell_indicator):
    """set the ShortSellIndicator value"""
    with TryExcept():
        if not Infant(trade):
            import string
            version = ".".join(acm.ShortVersion().strip(string.ascii_letters).split(".")[0:2])
            version = float(version.replace('Python', ''))
            if version < 2017.2:
                trade.AdditionalInfo().RegShortSell(short_sell_indicator)
            else:
                FRegulatoryLogger.INFO(logger, "Setting of ShortSellIndicator should be done only on the Front Office tab.")
def GetTheirOrg(trade_reginfo):
    """returns TheirOrganisation on the TradeRegulatoryInfo. If not found, then returns the Counterparty of the trade"""
    their_org = None
    if IsPersistent(trade_reginfo):
        if trade_reginfo.TheirOrganisation():
            lei = FRegulatoryLib.PartyRegInfo(trade_reginfo.TheirOrganisation()).LEI()
            if lei:
                their_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
            if their_org:
                if their_org != trade_reginfo.TheirOrganisation():
                    FRegulatoryLogger.INFO(logger, "TheirOrganisation <%s> on trade <%d> does not have an LEI on it. Hence TheirOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                    trade_reginfo.TheirOrganisation().Name(), trade_reginfo.Trade().Oid(), their_org.Name(), trade_reginfo.TheirOrganisation().Name()))
            else:
                FRegulatoryLogger.INFO(logger, "No LEI found on TheirOrganisation <%s>. Hence verifying Counterparty"%trade_reginfo.TheirOrganisation().Name())
        if (not their_org) and trade_reginfo.Trade().Counterparty():
            lei = FRegulatoryLib.PartyRegInfo(trade_reginfo.Trade().Counterparty()).LEI()
            if lei:
                their_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
            if their_org:
                if their_org != trade_reginfo.Trade().Counterparty():
                    FRegulatoryLogger.INFO(logger, "Counterparty <%s> on trade <%d> does not have an LEI on it. Hence TheirOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                    trade_reginfo.Trade().Counterparty().Name(), trade_reginfo.Trade().Oid(), their_org.Name(), trade_reginfo.Trade().Counterparty().Name()))
        if not their_org:
            FRegulatoryLogger.INFO(logger, "Neither TheirOrganisation nor Counterparty are set on the trade or do not have LEI. Hence TheirOrg is None")
    return their_org

def GetOurOrg(trade_reginfo):
    """returns OurOrganisation on the TradeRegulatoryInfo. If not found, then returns the Acquirer of the trade"""
    our_org = None
    if IsPersistent(trade_reginfo):
        if trade_reginfo.OurOrganisation():
            lei = FRegulatoryLib.PartyRegInfo(trade_reginfo.OurOrganisation()).LEI()
            if lei:
                our_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
            if our_org:
                if our_org != trade_reginfo.OurOrganisation():
                    FRegulatoryLogger.INFO(logger, "OurOrganisation <%s> on trade <%d> does not have an LEI on it. Hence OurOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                    trade_reginfo.OurOrganisation().Name(), trade_reginfo.Trade().Oid(), our_org.Name(), trade_reginfo.OurOrganisation().Name()))
            else:
                FRegulatoryLogger.INFO(logger, "No LEI found on OurOrganisation <%s>. Hence verifying Acquirer"%trade_reginfo.OurOrganisation().Name())
        if (not our_org) and trade_reginfo.Trade().Acquirer():
            lei = FRegulatoryLib.PartyRegInfo(trade_reginfo.Trade().Acquirer()).LEI()
            if lei:
                our_org = FRegulatoryLib.PartyRegInfo.partyFromLEI(lei)
            if our_org:
                if our_org != trade_reginfo.Trade().Acquirer():
                    FRegulatoryLogger.INFO(logger, "Acquirer <%s> on trade <%d> does not have an LEI on it. Hence OurOrg retuned <%s> as it is a parent of <%s> with LEI on it"%(\
                    trade_reginfo.Trade().Acquirer().Name(), trade_reginfo.Trade().Oid(), our_org.Name(), trade_reginfo.Trade().Acquirer().Name()))
        if not our_org:
            FRegulatoryLogger.INFO(logger, "Neither OurOrganisation nor Acquirer are set on the trade or do not have LEI. Hence OurOrg is None")
    return our_org

def GetDateTimeField(trade_reginfo, tradeTime):
    try:
        return tradeTime
    except Exception as e:
        print(("Exception while validating the datetime format for <%s>. Error <%s>"%(tradeTime, str(e))))

def GetNearLegIsinTrade(trade_reginfo):
    """get the Near Leg Isin of the trade. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegNearLegIsin()

def SetNearLegIsinTrade(trade_reginfo, near_leg_isin):
    """set the Near Leg Isin on the trade. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            if trade_reginfo.Trade().CurrencyPair() and trade_reginfo.Trade().IsFxSwap():
                if not FRegulatoryLibUtils.isValidIsin(near_leg_isin):
                    FRegulatoryLogger.WARN(logger, "NearLegIsin being set to <%s> is not a valid ISIN"%near_leg_isin)
            else:
                msg = "The NearLegIsin can be provided on FX Swap trades only."
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            trade_reginfo.AdditionalInfo().RegNearLegIsin(near_leg_isin)

def GetFarLegIsinTrade(trade_reginfo):
    """get the Far Leg Isin of the trade. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            return trade_reginfo.AdditionalInfo().RegFarLegIsin()

def SetFarLegIsinTrade(trade_reginfo, far_leg_isin):
    """set the Far Leg Isin on the trade. Applicable only for FX trades."""
    with TryExcept():
        if IsPersistent(trade_reginfo) and not Infant(trade_reginfo):
            if trade_reginfo.Trade().CurrencyPair() and trade_reginfo.Trade().IsFxSwap():
                if not FRegulatoryLibUtils.isValidIsin(far_leg_isin):
                    FRegulatoryLogger.WARN(logger, "FarLegIsin being set to <%s> is not a valid ISIN"%far_leg_isin)
            else:
                msg = "The FarLegIsin can be provided on FX Swap trades only."
                FRegulatoryLogger.ERROR(logger, msg)
                raise FRegulatoryInfoException.FRegInfoInvalidData(msg)
            trade_reginfo.AdditionalInfo().RegFarLegIsin(far_leg_isin)

def GetNotionalAmount(trade):
    """ Returns notional amount for trade"""
    return FRegulatoryNotionalAmount.FRegulatoryNotionalAmount(trade).notional_amount()

def GetPrice(trade_reginfo):
    """Returns the calculated Trade's Regulatory Price"""
    price = FRegulatoryLib.TradeRegInfo(trade_reginfo.Trade()).price()
    return price

def GetAlternateIsin(trade_reginfo):
    """Looks through the Isin on trade, instrument and the similarIsin on the instrument to return Isin for trade"""
    with TryExcept():
        if IsPersistent(trade_reginfo):
            isin = FRegulatoryLib.TradeRegInfo(trade_reginfo.Trade()).Isin()
            return isin     

