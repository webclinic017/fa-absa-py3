"""
Purpose                : Only users in FO PSSecLend Trader group can deleted SecLoan cashflows. None other person with FO Call Trades in their profile
                         can deleted cashflows.
                         Added Create Bill and FRN helper functions
Department and Desk    : Money Market Desk
Requester              : Venessa Kennel, Jansen Van Vuuren, Correy, Jan Sinkora
Developer              : Heinrich Cronje, Rohan vd Walt, Jan Sinkora, Jan Sinkora
CR Number              : 616426, 651043, 586166, 1024176
"""

import ael, uuid, acm

from FBDPCommon import is_acm_object

class ObjectHelper:
    """ Parent class to create different AEL Objects"""
    ZAR         = ael.Instrument['ZAR']
    TODAY       = ael.date_today().add_banking_day(ZAR, 0)
    TOMORROW    = TODAY.add_banking_day(ZAR, 1)
    ONEMONTH    = TODAY.add_banking_day(ZAR, 30)
    ZAR_CAL     = ael.Calendar['ZAR Johannesburg']

    @classmethod
    def SetProp(cls, obj, PropertyDict):
        """ This method sets the attributes of an object
            Arguments:
            the object to set attributes on
            A dictionary with the key as the attribute name and the value as the attribute value
        """
        for property, value in PropertyDict.items():
            setattr(obj, property, value)
        return

    @classmethod
    def Commit(cls, obj, isPersistant=1):
        """ This method Commits an object based on whether the object is required to be persistant
            Arguments:
            the object to commit
            Key woord argument IsPersistant to indicate if the object should be persitant
        """
        if isPersistant:
            if is_acm_object(obj):
                try:
                    obj.Commit()

                    return
                except Exception, ex:
                    print cls.commit_error_message(obj, ex)
            else:
                try:
                    obj.commit()

                    return
                except Exception, ex:
                    print cls.commit_error_message(obj, ex)
        return

    @classmethod
    def commit_error_message(cls, obj, ex):
        return 'Error Commiting object {0} ({1})'.format(obj, ex.message)

    @classmethod
    def Delete(cls, obj, isPersistant=1):
        """ This method Deletes an object based on whether the object is required to be persistant
            Arguments:
            the object to commit
            Key word argument IsPersistant to indicate if the object should be persitant
        """
        if isPersistant:
            if is_acm_object(obj):
                try:
                    obj.Delete()

                    return
                except Exception, ex:
                    print 'Error Deleting object: ', ex
            else:
                try:
                    obj.delete()

                    return
                except Exception, ex:
                    print 'Error Deleting object: ', ex
        return

    @classmethod
    def SetAddInfo(cls, obj, PropertyDict):
        """ This method sets the additional Infos on an object
            This works for creating new as well as updating add infos
            Arguments:
            the object to set additional infos on
            A dictionary with the key as the add info name and the value as the add info value
        """
        if PropertyDict:
            done = []
            for ai in obj.additional_infos():
                if ai.addinf_specnbr.field_name in PropertyDict.keys():
                    ai.value = str(PropertyDict[ai.addinf_specnbr.field_name])
                    done.append(ai.addinf_specnbr.field_name)
            for property, value in PropertyDict.items():
                if property not in done:
                    ai_new = ael.AdditionalInfo.new(obj)
                    ai_new.addinf_specnbr = ael.AdditionalInfoSpec[property]
                    ai_new.value = str(value)


        return


class PartyHelper(ObjectHelper):
    """
        This class inherits from Object Helper class. It is useful for creating Parties of different types
        By default the Party created will be BESA and FICA Compliant
    """

    PAddInfo_DICT =  {'FICA_Compliant': 'Yes', 'BESA_Member_Agree': 'Yes'}
    @classmethod
    def _DefaultPartyDict(cls):
        return {'ptyid': str(uuid.uuid4())}

    @classmethod
    def _GenericParty(cls, PartyDataDict = {'type' :'Counterparty'}, AddInfoDict=PAddInfo_DICT, isPersistant=True):
        party = ael.Party.new()
        partydict = cls._DefaultPartyDict()
        partydict.update(PartyDataDict)
        cls.SetProp(party, partydict)
        if AddInfoDict:
            cls.SetAddInfo(party, AddInfoDict)
        cls.Commit(party, isPersistant)
        return party

    @classmethod
    def CreateCounterparty(cls, PartyDataDict = {}, AddInfoDict=PAddInfo_DICT, isPersistant=True):
        """
            Method to create a Counterparty
            Keyword Arguments:
                PartyDataDict   -       Dictionary containing attributes that need to be specified on a counterparty. By default there are none
                AddInfoDict     -       Dictionary containing additional infos that need to be stored. By default Besa and Fica set to yes
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """
        return cls._GenericParty(AddInfoDict = AddInfoDict, isPersistant = isPersistant )

    @classmethod
    def CreateAcquirer(cls, PartyDataDict = {'type' :'Intern Dept'},AddInfoDict=PAddInfo_DICT, isPersistant=True):
        """
            Method to create an Acquirer (Intern Dept)
            Keyword Arguments:
                PartyDataDict   -       Dictionary containing attributes that need to be specified on a counterparty. By default there are none
                AddInfoDict     -       Dictionary containing additional infos that need to be stored. By default Besa and Fica set to yes
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """
        return cls._GenericParty(PartyDataDict, AddInfoDict, isPersistant )

class PortfolioHelper(ObjectHelper):
    @classmethod
    def _DefaultPortDict(cls):
        name  = str(uuid.uuid4())
        return {'prfid': name, 'assinf':name[0:35], 'curr': cls.ZAR}

    @classmethod
    def CreateAndLinkTo(cls, Name, ParentName, Compound, PortDataDict={}, AddInfoDict={}, isPersistant=True):
        portfolio = ael.Portfolio.new()
        portdict = cls._DefaultPortDict()
        portdict.update(PortDataDict)
        if Name:
            portdict['prfid'] = Name
        cls.SetProp(portfolio, portdict)
        if AddInfoDict:
            cls.SetAddInfo(portfolio.clone(), AddInfoDict)

        portfolio.compound = Compound

        cls.Commit(portfolio, isPersistant)

        parent_prf = ael.Portfolio[ParentName].clone()
        plink = ael.PortfolioLink.new(parent_prf)
        plink.member_prfnbr = portfolio
        cls.Commit(plink, isPersistant)

        return portfolio

    @classmethod
    def SetUpCreateTestingPortfolio(cls):
        p = ael.Portfolio['UNITTEST']

        if not p:
            cls.CreateAndLinkTo('UNITTEST', 'ABSA CAPITAL', 1)

    @classmethod
    def CreatePhysicalPortfolio(cls, PortDataDict = {}, AddInfoDict = None, isPersistant =True):
        """
            Method to create a Physical Portfolio
            Keyword Arguments:
                PartyDataDict   -       Dictionary containing attributes that need to be set for the portfolio. By default there are none
                AddInfoDict     -       Dictionary containing additional infos that need to be stored.No defaults
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """

        cls.SetUpCreateTestingPortfolio()

        return cls.CreateAndLinkTo(None, 'UNITTEST', 0)


class InstrumentHelper(ObjectHelper):

    FI_UNDERLYING =    ael.Instrument['ZAR/R204']
    @classmethod
    def CreateCloneFromInstrument(cls, original, isPersistant =1):
        """
            Method to create a cloned instrument from an object
            Argumments:
                The original instrument which should be cloned. The instrument ID will be set to a uuid
            Keyword Arguments:
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """
        clone = ael.Instrument.new(original)
        cls.SetProp(clone, {'insid': str(uuid.uuid4())})
        cls.Commit(clone, isPersistant)
        return clone

    #=====FIXED DEPOSIT=====
    @classmethod
    def _FixedDepoDefaultDict(cls):
        return {'quote_type':'Yield' , 'open_end': 'None', 'contr_size': 1000000}

    @classmethod
    def _FixedDepoLegDefaultDict(cls):
        return {'type': 'Fixed', 'start_day': cls.TODAY, 'end_day': cls.ONEMONTH, 'daycount_method': 'Act/365', 'fixed_rate':10, \
        'rolling_base_day':cls.ONEMONTH}

    @classmethod
    def CreateFixedDepositInstrument(cls, InsDataDict = {},LegDataDict={},AddInfoDict = {}, isPersistant = True):
        """
            Method to create a Fixed Deposit Instrument
            Keyword Arguments:
                InsDataDict     -       Dictionary containing attributes that need to be set for the instrument.
                                        Default values {'quote_type':'Yield' , 'open_end': 'None', 'contr_size': 1000000}
                LegDataDict     -       Dictionary containing attributes that need to be set for the instrument.
                                        Default value create a fixed leg starting today expiring in one month with a fixed rate of 10
                                        and a day count of 365
                AddInfoDict     -       Dictionary containing additional infos that need to be stored. No defaults
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """
        depo = ael.Instrument.new('Deposit')
        insdict = cls._FixedDepoDefaultDict()
        insdict.update(InsDataDict)
        leg = depo.legs()[0]
        legdict =  cls._FixedDepoLegDefaultDict()
        legdict.update(LegDataDict)
        cls.SetProp(depo, insdict)
        cls.SetProp(leg, legdict)
        if AddInfoDict:
            cls.SetAddInfo(depo, AddInfoDict)
        cls.Commit(depo, isPersistant)
        return depo

    @classmethod
    def _BSBDefaultDict(cls):
        return {'start_day': cls.TODAY, 'exp_day': cls.ONEMONTH, 'daycount_method': 'Act/365', 'rate':10,'contr_size': 1000000,\
                'und_insaddr': cls.FI_UNDERLYING}
    @classmethod
    def CreateBSBInstrument(cls, InsDataDict = {},AddInfoDict={} , isPersistant = True):
        """
            Method to create a Fixed Deposit Instrument
            Keyword Arguments:
                InsDataDict     -       Dictionary containing attributes that need to be set for the instrument.
                                        Default instrument starts today with expiry in one month at a rate of 10 on the R204
                AddInfoDict     -       Dictionary containing additional infos that need to be stored. No defaults
                isPersistant    -       Bool to indicate whether or not the object should be persistant. The default is TRUE
        """
        bsb = ael.Instrument.new('BuySellback')
        insdict = cls._BSBDefaultDict()
        insdict.update(InsDataDict)
        cls.SetProp(bsb, insdict)
        if AddInfoDict:
            cls.SetAddInfo(bsb, AddInfoDict)
        cls.Commit(bsb, isPersistant)
        return bsb

    @classmethod
    def _RepoDefaultDict(cls):
        return {'quote_type':'Pct of Nominal' , 'open_end': 'None', 'contr_size': 1000000, 'und_insaddr':cls.FI_UNDERLYING,'spot_banking_days_offset':0}

    @classmethod
    def _RepoLegDefaultDict(cls):
        return {'type': 'Fixed', 'start_day': cls.TODAY, 'end_day': cls.ONEMONTH, 'daycount_method': 'Act/365', 'fixed_rate':10, \
        'rolling_base_day':cls.ONEMONTH}

    @classmethod
    def CreateRepoInstrument(cls, InsDataDict = {},AddInfoDict={} , isPersistant = True):
        repo = ael.Instrument.new('Repo/Reverse')
        insdict = cls._RepoDefaultDict()
        insdict.update(InsDataDict)
        leg = repo.legs()[0]
        legdict = cls._RepoLegDefaultDict()
        cls.SetProp(repo, insdict)
        cls.SetProp(leg, legdict)
        if AddInfoDict:
            cls.SetAddInfo(repo, AddInfoDict)
        cls.Commit(repo, isPersistant)
        return repo

    @classmethod
    def _CallAccDefaultDict(cls):
        return { 'quote_type':'Yield' , 'open_end': 'Open End', 'contr_size': 1,'daycount_method': 'Act/365'}

    @classmethod
    def _CallAccLegDefaultDict(cls):
        return {'type': 'Call Fixed Adjustable', 'start_day': cls.TODAY, 'end_day': cls.TOMORROW, 'daycount_method': 'Act/365', 'fixed_rate':10, \
        'rolling_base_day':cls.TODAY.add_months(1).first_day_of_month(), 'rolling_period' : '1m','pay_day_method' : 'Following', \
        'pay_calnbr':cls.ZAR_CAL, 'reset_type' :'Weighted', 'float_rate_factor' : 1, 'fixed_coupon': 1}

    @classmethod
    def CreateCallAccountInstrument(cls, InsDataDict = {},LegDataDict={}, AddInfoDict = {},isPersistant = True):
        depo = ael.Instrument.new('Deposit')
        insdict = cls._CallAccDefaultDict()
        insdict.update(InsDataDict)
        leg = depo.legs()[0]
        legdict =  cls._CallAccLegDefaultDict()
        legdict.update(LegDataDict)
        cls.SetProp(depo, insdict)
        cls.SetProp(leg, legdict)
        if AddInfoDict:
            cls.SetAddInfo(cls, AddInfoDict)
        cls.Commit(depo, isPersistant)
        return depo

    @classmethod
    def _SecLoanDefaultDict(cls):
        return {}

    @classmethod
    def _SecLoanLegDefaultDict(cls):
        return {}

    @classmethod
    def CreateSecLoanInstrument(cls, InsDataDict = {},LegDataDict={}, AddInfoDict = {},isPersistant = True):
        secLoan = ael.Instrument.new('SecurityLoan')
        insdict = cls._SecLoanDefaultDict()
        insdict.update(InsDataDict)
        leg = secLoan.legs()[0]
        legdict = cls._SecLoanLegDefaultDict()
        legdict.update(LegDataDict)
        cls.SetProp(secLoan, insdict)
        cls.SetProp(leg, legdict)
        if AddInfoDict:
            cls.SetAddInfo(secLoan, AddInfoDict)
        cls.Commit(secLoan, isPersistant)
        return secLoan

    @classmethod
    def _BillDefaultDict(cls):
        return {'daycount_method': 'Act/365', 'issuer' : 'ABSA BANK LTD'}

    @classmethod
    def _BillLegDefaultDict(cls):
        return {'start_day': cls.TODAY, 'end_day': cls.TODAY.add_years(1), 'type' : 'Fixed' }

    @classmethod
    def CreateBillInstrument(cls, InsDataDict = {}, LegDataDict = {}, isPersistant = True):
        bill = ael.Instrument.new('Bill')
        insdict = cls._BillDefaultDict()
        insdict.update(InsDataDict)
        leg = bill.legs()[0]
        legdict =  cls._BillLegDefaultDict()
        legdict.update(LegDataDict)
        cls.SetProp(bill, insdict)
        cls.SetProp(leg, legdict)
        cls.Commit(bill, isPersistant)
        return bill

    @classmethod
    def _FRNDefaultDict(cls):
        return {'daycount_method': 'Act/365', 'issuer' : 'ABSA BANK LTD'}

    @classmethod
    def _FRNLegDefaultDict(cls):
        return {'start_day': cls.TODAY, 'end_day': cls.TODAY.add_years(1) }

    @classmethod
    def CreateFRNInstrument(cls, InsDataDict = {}, LegDataDict = {}, isPersistant = True):
        frn = ael.Instrument.new('FRN')
        insdict = cls._FRNDefaultDict()
        insdict.update(InsDataDict)
        leg = frn.legs()[0]
        legdict =  cls._FRNLegDefaultDict()
        legdict.update(LegDataDict)
        cls.SetProp(frn, insdict)
        cls.SetProp(leg, legdict)
        cls.Commit(frn, isPersistant)
        return frn

    @classmethod
    def _swap_default_dict(cls):
        """The minimal required fields for a correct swap instrument."""
        return {'start_day': ael.date_today(),
                'exp_day': ael.date_today().add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'])}

    @classmethod
    def create_swap_instrument(cls, ins_data_dict={}, is_persistent=True):
        """
        Create a swap instrument.
        """
        swp = ael.Instrument.new('Swap')
        insdict = cls._swap_default_dict()
        insdict.update(ins_data_dict)
        cls.SetProp(swp, insdict)
        cls.Commit(swp, is_persistent)
        return swp

    @classmethod
    def _option_default_dict(cls):
        """The minimal required fields for a correct swap instrument."""
        return {'exp_day': ael.date_today().add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'])}

    @classmethod
    def create_option_instrument(cls, ins_data_dict={}, is_persistent=True):
        """
        Create an option instrument.
        """
        opt = ael.Instrument.new('Option')
        insdict = cls._option_default_dict()
        insdict.update(ins_data_dict)
        cls.SetProp(opt, insdict)
        cls.Commit(opt, is_persistent)
        return opt

    @classmethod
    def create_swaption_instrument(cls, ins_data_dict={}, und_data_dict={}, is_persistent=True):
        """
        Create a swap and an option and connect them.
        """
        swp = cls.create_swap_instrument(und_data_dict, is_persistent)
        opt = cls.create_option_instrument(ins_data_dict, is_persistent).clone()

        opt.und_insaddr = swp
        opt.commit()
        opt = opt.clone()
        opt.quotation_seqnbr = ael.Quotation['Pct of Nominal']
        opt.call_option = 1
        opt.commit()

        return opt

    @classmethod
    def _fra_default_dict(cls):
        """The minimal required fields for a correct fra instrument."""
        return {'start_day': ael.date_today(),
                'exp_day': ael.date_today().add_years(1).adjust_to_banking_day(ael.Instrument['ZAR'])}

    @classmethod
    def create_fra_instrument(cls, ins_data_dict = {}, is_persistent = True):
        """
        Create a FRA instrument.
        """
        fra = ael.Instrument.new('FRA')
        insdict = cls._fra_default_dict()
        insdict.update(ins_data_dict)
        cls.SetProp(fra, insdict)
        cls.Commit(fra, is_persistent)
        return fra

    @classmethod
    def create_fra_option_instrument(cls, ins_data_dict={}, und_data_dict={}, is_persistent=True):
        """
        Create a FRA and an option and connect them.
        """
        fra = cls.create_fra_instrument(und_data_dict, is_persistent)
        opt = cls.create_option_instrument(ins_data_dict, is_persistent).clone()

        opt.und_insaddr = fra
        opt.commit()
        opt = opt.clone()
        opt.quotation_seqnbr = ael.Quotation['Pct of Nominal']
        opt.commit()

        return opt


    @classmethod
    def get_or_create_instrument(cls, name, creation_method, *args):
        """
        Gets or creates an instrument with the given name.

        creation_method -- a method reference, i.e. InstrumentHelper.create_fra_instrument

        """
        ins = ael.Instrument[name]
        if not ins:
            ins = creation_method(*args).clone()
            ins.insid = name
            ins.commit()

        return ins


    @classmethod
    def get_or_create_stock_instrument(cls, name):
        stock = ael.Instrument[name]
        if not stock:
            stock = ael.Instrument.new('Stock')
            stock.insid = name

            stock.commit()

        return stock


    @classmethod
    def get_or_create_trs_eqi_instrument(cls, name, und_name):
        """
        Convenience method for getting a TRS with index-referenced eqindex.
        """
        eqi = ael.Instrument[und_name]
        if eqi:
            eqi = eqi.clone()
        else:
            eqi = ael.Instrument.new('EquityIndex')
            eqi.insid = und_name

        ins = ael.Instrument[name]
        if ins:
            ins = ins.clone()
        else:
            ins = ael.Instrument.new('TotalReturnSwap')
            ins.insid = name

        leg = ins.legs()[1]
        if leg.index_ref.insaddr != eqi.insaddr:
            # link the instruments
            leg.index_ref = eqi

        eqi.commit()
        ins.commit()

        return ael.Instrument[name]


    @classmethod
    def get_or_create_swaption_instrument(cls, name):
        """
        Convenience method for getting a swaption with the given name.
        """
        return cls.get_or_create_instrument(name, cls.create_swaption_instrument)

    @classmethod
    def get_or_create_fra_option_instrument(cls, name):
        """
        Convenience method for getting a fra-based option with the given name.
        """
        return cls.get_or_create_instrument(name, cls.create_fra_option_instrument)

class TradeHelper(ObjectHelper):

    DEFAULTINS  = ael.Instrument['ZAR/AGL']
    CD = ael.ChoiceList[1227].entry
    CALLDEPO = ael.ChoiceList[1622].entry
    FUNDING_DESK = ael.Party['Funding Desk']
    CALL_2474   = ael.Portfolio['Call_2474']
    CALL_REGION = "INST GAUTENG"
    NON_ZAR_CFC  =   ael.Party['ABCAP NON ZAR CFCI DIV']

    @classmethod
    def _TradeDefaultDict(cls):
        return {'insaddr' : cls.DEFAULTINS, 'quantity': 1, 'price': 100, 'status': 'FO Confirmed', 'counterparty_ptynbr' : PartyHelper.CreateCounterparty(), \
            'acquirer_ptynbr': PartyHelper.CreateAcquirer(), 'prfnbr': PortfolioHelper.CreatePhysicalPortfolio(), 'curr': cls.ZAR,\
            'time': ael.date_today().to_time(), 'value_day' : cls.TODAY, 'acquire_day':cls.TODAY}


    @classmethod
    def CreateMMTrade(cls,TradeDataDict={}, AddInfoDict={"Funding Instype": CD},isPersistant = True):
        trade =cls.CreateTrade(TradeDataDict, AddInfoDict, isPersistant)
        return trade

    @classmethod
    def _CallTradeDefaultDict(cls):
        return {'insaddr' : InstrumentHelper.CreateCallAccountInstrument(), 'quantity': 1, 'price': 0, 'status': 'FO Confirmed',\
            'counterparty_ptynbr' : PartyHelper.CreateCounterparty(), 'acquirer_ptynbr': cls.FUNDING_DESK, 'prfnbr': cls.CALL_2474, 'curr': cls.ZAR,\
            'time': ael.date_today().to_time(), 'value_day' : cls.TODAY, 'acquire_day':cls.TODAY}

    @classmethod
    def _CallTradeAddInfoDefault(cls):
        return {"Funding Instype":cls.CALLDEPO, "Call_Region":cls.CALL_REGION, 'Account_Name': str(uuid.uuid4())}

    @classmethod
    def CreateCallTrade(cls,TradeDataDict={},AddInfoDict={"Funding Instype":"Call Deposit DTI", "Call_Region":"INST GAUTENG", 'Account_Name': str(uuid.uuid4())},isPersistant = True):
        tradedict = cls._CallTradeDefaultDict()
        ael.poll()
        tradedict.update(TradeDataDict)
        trade =cls.CreateTrade(TradeDataDict=tradedict, AddInfoDict = AddInfoDict, isPersistant= isPersistant)
        return trade

    @classmethod
    def CreateNonZARCallTrade(cls, TradeDataDict={},AddInfoDict={"Funding Instype":"Non Zar CFC I/Div"},isPersistant = True):
        USD = ael.Instrument['USD']
        leg = {'curr': USD, 'daycount_method': 'Act/360' , 'reinvest':1}
        ins = InstrumentHelper.CreateCallAccountInstrument(InsDataDict = {'curr': USD}, LegDataDict = leg)
        tradedict = cls._CallTradeDefaultDict()
        tradedict['insaddr'] = ins
        tradedict['acquirer_ptynbr'] = cls.NON_ZAR_CFC
        ael.poll()
        tradedict.update(TradeDataDict)
        trade =cls.CreateTrade(TradeDataDict=tradedict, AddInfoDict = AddInfoDict, isPersistant= isPersistant)
        return trade

    @classmethod
    def CreateTrade(cls, TradeDataDict={}, AddInfoDict={}, isPersistant = True):

        tradedict = cls._TradeDefaultDict()
        ael.poll()
        tradedict.update(TradeDataDict)
        trade = ael.Trade.new(tradedict['insaddr'])
        cls.SetProp(trade, tradedict)
        if AddInfoDict:
            cls.SetAddInfo(trade, AddInfoDict)
        cls.Commit(trade, isPersistant)
        return trade

    @classmethod
    def _BSBTradeDefaultDict(cls):
        return {'insaddr' : InstrumentHelper.CreateBSBInstrument(isPersistant = False), 'quantity': 1, 'price': 100, 'status': 'FO Confirmed', 'counterparty_ptynbr' : PartyHelper.CreateCounterparty(), \
            'acquirer_ptynbr': PartyHelper.CreateAcquirer(), 'prfnbr': PortfolioHelper.CreatePhysicalPortfolio(), 'curr': cls.ZAR,\
            'time': ael.date_today().to_time(), 'value_day' : cls.TODAY, 'acquire_day':cls.TODAY, 'premium_calculation_method': 'Consideration'}

    @classmethod
    def CreateBSBTrade(cls, TradeDataDict={}, AddInfoDict={},isPersistant = True):

        d = cls._BSBTradeDefaultDict()
        d.update(TradeDataDict)
        trade =cls.CreateTrade(TradeDataDict=d, AddInfoDict = AddInfoDict, isPersistant= False)
        ins = trade.insaddr
        trade.price = (float)(ins.und_insaddr.mtm_price_suggest(cls.TODAY, 'ZAR'))
        trade.premium=trade.premium_from_quote(ins.start_day, trade.price)
        ins.ref_price=trade.buy_sellback_ref_price()
        ins.ref_value=trade.buy_sellback_ref_value(1)
        cls.Commit(ins, isPersistant)
        cls.Commit(trade, isPersistant)
        return trade

    @classmethod
    def _BillTradeDefaultDict(cls):
        return {'insaddr' : InstrumentHelper.CreateBillInstrument(isPersistant = False), \
                'quantity': 1, 'price': 100, 'status': 'FO Confirmed', 'counterparty_ptynbr' : PartyHelper.CreateCounterparty(), \
                'acquirer_ptynbr': PartyHelper.CreateAcquirer(), 'prfnbr': PortfolioHelper.CreatePhysicalPortfolio(), \
                'curr': cls.ZAR, 'time': ael.date_today().to_time(), 'value_day' : cls.TODAY.add_banking_day(cls.ZAR, 3), \
                'acquire_day':cls.TODAY.add_banking_day(cls.ZAR, 3)}

    @classmethod
    def CreateBillTrade(cls, TradeDataDict={}, AddInfoDict={'MM_Original_Nominal' : 1000000 },isPersistant = True):
        d = cls._BillTradeDefaultDict()
        d.update(TradeDataDict)
        trade = cls.CreateTrade(TradeDataDict=d, isPersistant= False)
        ins = trade.insaddr
        if AddInfoDict:
            cls.SetAddInfo(trade, AddInfoDict)
        cls.Commit(ins, isPersistant)
        cls.Commit(trade, isPersistant)
        return trade

    @classmethod
    def _FRNTradeDefaultDict(cls):
        return {'insaddr' : InstrumentHelper.CreateFRNInstrument(isPersistant = False), \
                'quantity': 1, 'price': 100, 'status': 'FO Confirmed', 'counterparty_ptynbr' : PartyHelper.CreateCounterparty(), \
                'acquirer_ptynbr': PartyHelper.CreateAcquirer(), 'prfnbr': PortfolioHelper.CreatePhysicalPortfolio(), \
                'curr': cls.ZAR, 'time': ael.date_today().to_time(), 'value_day' : cls.TODAY.add_banking_day(cls.ZAR, 3), \
                'acquire_day':cls.TODAY.add_banking_day(cls.ZAR, 3)}

    @classmethod
    def CreateFRNTrade(cls, TradeDataDict={}, AddInfoDict={},isPersistant = True):
        d = cls._FRNTradeDefaultDict()
        d.update(TradeDataDict)
        trade = cls.CreateTrade(TradeDataDict=d, isPersistant= False)
        ins = trade.insaddr
        if AddInfoDict:
            cls.SetAddInfo(trade, AddInfoDict)
        cls.Commit(ins, isPersistant)
        cls.Commit(trade, isPersistant)
        return trade

    @classmethod
    def _swaption_trade_default_dict(cls):
        return {'quantity': 1,
                'price': 100,
                'status': 'FO Confirmed',
                'counterparty_ptynbr' : PartyHelper.CreateCounterparty(),
                'acquirer_ptynbr': PartyHelper.CreateAcquirer(),
                'prfnbr': PortfolioHelper.CreatePhysicalPortfolio(),
                'curr': cls.ZAR,
                'time': ael.date_today().to_time(),
                'value_day' : cls.TODAY.add_banking_day(cls.ZAR, 3),
                'acquire_day':cls.TODAY.add_banking_day(cls.ZAR, 3)}

    @classmethod
    def _fra_option_trade_default_dict(cls):
        """
        This is the same as swaption, but can be changed if needed.
        """
        return cls._swaption_trade_default_dict()

    @classmethod
    def _create_trade_on_opt_fixed_rate_und(cls, trade_data_dict={}, add_info_dict={},
                                            is_persistent=True, und_type='swap'):
        """
        Create a trade on an option instrument which has an underlying
        fixed-rate instrument.
        This includes swaptions and fra-based options.
        Factory class method, builds according to the und_type param.

        If the 'insaddr' key is not present in the trade_data_dict, a default
        instrument is created.

        """

        # factory selection
        if und_type == 'swap':
            d = cls._swaption_trade_default_dict()
            insid = 'UNITTEST/OPTION/SWAP'
            creator = InstrumentHelper.create_swaption_instrument
        elif und_type == 'fra':
            d = cls._fra_option_trade_default_dict()
            insid = 'UNITTEST/OPTION/FRA'
            creator = InstrumentHelper.create_fra_option_instrument
        else:
            raise ValueError('unsupported underlying instrument ({0})'.format(und_type))

        # update the dict with the provided values
        d.update(trade_data_dict)

        # create the default instrument if not present
        if 'insaddr' not in d.keys():
            d['insaddr'] = InstrumentHelper.get_or_create_instrument(insid, creator)

        # create the trade with the required persistency
        trade = cls.CreateTrade(TradeDataDict=d, isPersistant=False)
        if add_info_dict:
            cls.SetAddInfo(trade, add_info_dict)
        cls.Commit(trade, is_persistent)
        return trade

    @classmethod
    def create_swaption_trade(cls, trade_data_dict={}, add_info_dict={}, is_persistent=True):
        """
        Convenience method for creating a swaption trade.

        See TradeHelper._create_trade_on_opt_fixed_rate_und.

        """
        return cls._create_trade_on_opt_fixed_rate_und(trade_data_dict, add_info_dict, is_persistent, 'swap')

    @classmethod
    def create_fra_option_trade(cls, trade_data_dict={}, add_info_dict={}, is_persistent=True):
        """
        Convenience method for creating a fra-based option trade.

        See TradeHelper._create_trade_on_opt_fixed_rate_und.

        """
        return cls._create_trade_on_opt_fixed_rate_und(trade_data_dict, add_info_dict, is_persistent, 'fra')

    @classmethod
    def _default_trs_trade_data(cls):
        return cls._swaption_trade_default_dict()

    @classmethod
    def create_trs_trade(cls, trs, trade_data_dict={}):
        data = cls._default_trs_trade_data()
        data.update(trade_data_dict)
        data['insaddr'] = trs
        trade = cls.CreateTrade(TradeDataDict=data, isPersistant=True)
        return trade

class ProfileHelper(ObjectHelper):

    @classmethod
    def RemoveAccessProfileFromGroup(cls, AccessProfileList=[], isPersistant=True):
        user = ael.user()
        user = acm.FUser[user.userid]
        group = user.UserGroup()
        groupProfileLink = acm.FGroupProfileLink.Select('userGroup=%i' %group.Oid())

        for profile in groupProfileLink:
            if profile.UserProfile().Name() in AccessProfileList:
                cls.Delete(profile, isPersistant)

    @classmethod
    def AddAccessProfileToGroup(cls, AccessProfileList = [], isPersistant = True):
        for i in AccessProfileList:
            new_GroupProfileLink = acm.FGroupProfileLink()
            new_GroupProfileLink.UserGroup(acm.FUser[ael.user().userid].UserGroup())
            new_GroupProfileLink.UserProfile(acm.FUserProfile[i])
            cls.Commit(new_GroupProfileLink, isPersistant)

    @classmethod
    def MoveUserToDifferentUserGroup(cls, newUserGroup, isPersistant = True):
        newUserGroup = acm.FUserGroup[newUserGroup]
        user = ael.user()
        user = acm.FUser[user.userid]
        user.UserGroup(newUserGroup)
        cls.Commit(user, isPersistant = True)


