""" Settlement:1.2.2.hotfix23 """

"""----------------------------------------------------------------------------
MODULE
    FSettlementGeneral3
    (c) Copyright 2006 by SunGard FRONT ARENA. All rights reserved.    
    
    Here we put functions that are refectored from FSettlementGeneral, 
    FSettlementGeneral2, FSettlementGeneralRT. Hence functions are still
    there but they call this module.    
    
----------------------------------------------------------------------------"""

import ael, FSettlementGeneral, FSettlementGeneral2, FSettlementGeneralRT
import FSettlementParams, FSettlementAMB, FSettlementVariables
import FUpdateFutureForward, time
param = FSettlementParams.get_default_params()
keyw = 'PAYMENT=' # SPR 269722
prefix_ok = ['ADDITIONALINFO', 'COMBINATIONLINK', 'DIVIDEND', 'INSTRUMENT', 'LEG', 'INSTRUMENTALIAS', 'TRADEACCOUNTLINK']

# _fields2 we do not want in diff_dict, adapt corresponding entity class fields as well
acc_fields = {'ACCOUNT':'account', 'NAME':'name', 'PTYNBR':'ptynbr'}
if param.network_update:
    acc_fields['NETWORK_ALIAS_TYPE'] = 'network_alias_type'
acc_fields2 = ['ACCNBR', 'CURR', 'PAYNBR']
cf_fields   = {'TYPE':'type','RATE':'rate','NOMINAL_FACTOR':'nominal_factor',\
               'START_DAY':'start_day','PAY_DAY':'pay_day','END_DAY':'end_day',\
               'FIXED_AMOUNT':'fixed_amount'}
cf_fields2  = ['CFWNBR', 'LEGNBR']

cbl_fields   = ['SEQNBR', 'OWNER_INSADDR', 'MEMBER_INSADDR', 'ARCHIVE_STATUS', 'WEIGHT', 'FIX_FX_RATE']

div_fields  = {'DIVIDEND':'dividend','PAY_DAY':'pay_day','CURR.INSID':'curr.insid',\
               'TAX_FACTOR':'tax_factor','DAY':'day'}
div_fields2 = ['SEQNBR', 'EX_DIV_DAY', 'INSADDR', 'CURR']

ins_fields = ['CONTR_SIZE', 'CURR', 'EX_COUP_PERIOD', 'EXP_DAY', 'INSADDR',\
              'INSID', 'INDEX_FACTOR', 'INSTYPE', 'ISSUER_PTYNBR',\
              'OPEN_END', 'REF_VALUE', 'UND_INSADDR', 'DIVIDEND_FACTOR']

leg_fields = ['CURR', 'END_DAY', 'FLOAT_RATE', 'FIXED_RATE', 'INSADDR',\
              'INDEX_REF', 'LEGNBR',\
              'PAY_CALNBR', 'PAY2_CALNBR', 'PAY3_CALNBR', 'PAY4_CALNBR', 'PAY5_CALNBR',\
              'REDEMPTION_CURR', 'REINVEST',\
              'RESET_CALNBR', 'RESET2_CALNBR', 'RESET3_CALNBR', 'RESET4_CALNBR', 'RESET5_CALNBR5',\
              'START_DAY', 'TYPE']

nr_fields = {'ENABLED':'enabled','INSTYPE':'instype',\
             'CURR.INSID':'curr.insid','PTYNBR.PTYID':'ptynbr.ptyid',\
             'ORDERNBR':'ordernbr','CURR_PAIR.NAME':'curr_pair.name'
            }

pay_fields  = {'PAYDAY':'payday','AMOUNT':'amount','CURR.INSID':'curr.insid',\
               'PAYNBR':'paynbr','PTYNBR.PTYID':'ptynbr.ptyid','TYPE':'type',\
               'ACCNBR':'accnbr','ACCNBR.PTYNBR':'accnbr.ptynbr',\
               'ACCNBR.PTYID':'accnbr.ptyid',\
               'OUR_ACCNBR':'our_accnbr','OUR_ACCNBR.PTYNBR':'our_accnbr.ptynbr',\
               'OUR_ACCNBR.PTYID':'our_accnbr.ptyid','VALID_FROM':'valid_from'}
pay_fields2 = ['CURR', 'PTYNBR', 'TRDNBR']

party_fields = {'PTYID':'ptyid'}
party_fields2 = ['PTYNBR']

reset_fields  = {'DAY':'day','VALUE':'value','TYPE':'type',\
                 'START_DAY':'start_day','END_DAY':'end_day',\
                 'ROLLING_BASE_DAY':'rolling_base_day','READ_TIME':'read_time'}
reset_fields2 = ['CFWNBR', 'LEGNBR', 'RESNBR', 'TYPE', 'VALUE2']

# This dictionary needs to be extended when new fields are added!!!
setl_fields = {'ACQUIRER_ACCOUNT':'acquirer_account','ACQUIRER_ACCNAME':'acquirer_accname',\
               'ACQUIRER_PTYID':'acquirer_ptyid','AMOUNT':'amount',\
               'CURR.INSID':'curr.insid',\
               'PARTY_ACCNAME':'party_accname','PARTY_ACCOUNT':'party_account',\
               'PARTY_PTYID':'party_ptyid','REF_TYPE':'ref_type',\
               'STATUS_EXPLANATION':'status_explanation', 'STATUS':'status',\
               'TRDNBR':'trdnbr','TYPE':'type','VALUE_DAY':'value_day'}

if param.network_update:
    setl_fields['ACQUIRER_ACCOUNT_NETWORK_NAME'] = 'acquirer_account_network_name'
    setl_fields['PARTY_ACCOUNT_NETWORK_NAME'] = 'party_account_network_name'
    
settl_fields2 = ['AGGREGATE', 'AGGREGATE_SEQNBR', 'CURR', 'CFWNBR', 'DELIVERY_TYPE',\
                'DIARY', 'DIVIDEND_SEQNBR', 'FROM_PRFNBR', 'NETTING_RULE_SEQNBR', \
                'MANUAL_MATCH', 'ORG_SEC_NOM', 'OWNER_USRNBR', 'PAYNBR', \
                'POST_SETTLE_ACTION', 'PRIMARY_ISSUANCE', 'PROTECTION',\
                'REF_SEQNBR', 'SEC_INSADDR', 'SEQNBR', 'SETTLE_CATEGORY', \
                'SETTLE_SEQNBR', 'SETTLEINSTRUCTION_SEQNBR', 'TEXT', 'TO_PRFNBR']

tr_fields   = ['PREMIUM', 'PRICE', 'TYPE', 'ACQUIRE_DAY', 'FEE',\
               'ACQUIRER_PTYNBR.PTYID',\
               'CURR.INSID', 'VALUE_DAY', 'QUANTITY', 'STATUS',\
               'COUNTERPARTY_PTYNBR.PTYID',\
               'PRFNBR', 'PRFNBR.PRFID', 'PROTECTION', 'OWNER_USRNBR',\
               'BROKER_PTYNBR.PTYID', 'RE_ACQUIRE_DAY']
               
tr_fields2 = ['AGGREGATE', 'ACQUIRER_PTYNBR', 'BROKER_PTYNBR',\
              'CATEGORY', 'CONTRACT_TRDNBR', 'CORRECTION_TRDNBR',\
              'COUNTERPARTY_PTYNBR', 'CURR', 'INSADDR',\
              'TRDNBR']
       
pre_settlement_status = ['New', 'Recalled', 'Updated', 'Exception', 'Manual Match', 'Hold', 
                         'Void', 'Authorised', 'Not Acknowledged']

# Entity classes in alphabetic order
class Account:

    def __init__(self,**kwrds):
        '''Fields here are reflected from cf_fields '''
        self.account = ''
        self.accnbr = 0
        self.curr = 0
        #self.network_alias_type = 0
        self.name = ''        
        self.ptynbr = 0
        self.record_type = 'Account'
        self.network_alias_type = 0
        #self.swift  = ''         
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Account class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")        
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)
    
    def get_ael_entity(self):
        ret = ael.Account[self.accnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1


class CashFlow:

    def __init__(self,**kwrds):
        '''Fields here are reflected from cf_fields '''
        self.cfwnbr = 0
        self.end_day = 0
        self.fixed_amount = 0
        self.legnbr = 0
        self.nominal_factor  = 0       
        self.pay_day  = 0
        self.rate = 0
        self.record_type = 'CashFlow'
        self.type  = ''      
        self.start_day  = 0
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to CashFlow class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")        
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)
    
    def ex_coupon_date(self):
        ael_entity = ael.CashFlow[self.cfwnbr]
        if ael_entity:
            return ael_entity.ex_coupon_date()
        else:
            raise RuntimeError, "No CashFlow ael entity found for cfwnbr %d in method ex_coupon_date" % self.cfwnbr

    def get_ael_entity(self):
        ret = ael.CashFlow[self.cfwnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1
            
    def projected_cf(self):
        ael_entity = ael.CashFlow[self.cfwnbr]
        if ael_entity:
            return ael_entity.projected_cf()
        else:
            raise RuntimeError, "No CashFlow ael entity found for cfwnbr %d in method projected_cf" % self.cfwnbr

class CombinationLink:

    def __init__(self,**kwrds):
        '''Fields here are reflected from cbl_fields (Note! no dict)'''
        self.archive_status = 0
        self.fix_fx_rate = 0
        self.member_insaddr = 0
        self.owner_insaddr = 0
        self.record_type = 'CombinationLink'
        self.seqnbr = 0
        self.weight = 0

        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to CombinationLink class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def get_ael_entity(self):
        ret = ael.CombinationLink[self.seqnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1


class Dividend:

    def __init__(self,**kwrds):
        '''Fields here are reflected from div_fields '''
        self.curr = 0
        self.day = 0        
        self.dividend = 0
        self.ex_div_day = 0
        self.insaddr = 0        
        self.pay_day = 0        
        self.record_type = 'Dividend'
        self.seqnbr = 0      
        self.tax_factor = 0

        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Dividend class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def get_ael_entity(self):
        ret = ael.Dividend[self.seqnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret
  
    def is_entity_class(self):
        return 1
  

class Instrument:

    def __init__(self,**kwrds):
        '''Fields here are reflected from ins_fields '''
        self.curr = 0
        self.dividend_factor = 0
        self.contr_size = 0
        self.ex_coup_period  = 0
        self.exp_day = 0
        self.index_factor = 0
        self.insaddr = 0
        self.insid = ''
        self.instype = ''
        self.issuer_ptynbr = 0
        self.open_end = 0
        self.ref_value = 0
        self.record_type = 'Instrument'
        self.und_insaddr = 0
                
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Instrument class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def cash_flows(self):
        ret = []
        inst = self.get_ael_entity()        
        if inst:
            if inst.instype == 'Combination':
                ret = inst.cash_flows()                
            else:
                pr = "Instrument entity class wrongly used (Error)"
                log(1, pr)
        return ret
        
    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)
        
    def get_ael_entity(self):
        ret = ael.Instrument[self.insaddr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1

    def trades(self):
        ret = []
        ael_entity = self.get_ael_entity()
        if ael_entity:
            ret = ael_entity.trades()
        return ret

class Leg:

    def __init__(self,**kwrds):
        '''Fields here are reflected from leg_fields. '''
        self.curr = 0
        self.end_day = 0
        self.float_rate = 0
        self.fixed_rate = 0
        self.insaddr = 0        
        self.index_ref = 0
        self.legnbr = 0
        self.pay_calnbr = 0
        self.pay2_calnbr = 0
        self.pay3_calnbr = 0
        self.pay4_calnbr = 0
        self.pay5_calnbr = 0
        self.redemption_curr = 0
        self.reset_calnbr = 0
        self.reset2_calnbr = 0
        self.reset3_calnbr = 0
        self.reset4_calnbr = 0
        self.reset5_calnbr5 = 0
        self.record_type = 'Leg'
        self.reinvest = 0
        self.start_day = 0
        self.type = ''        
                
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Leg class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def get_ael_entity(self):
        ret = ael.Leg[self.legnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1
            
class Payment:

    def __init__(self,**kwrds):
        '''Fields here are reflected from pay_fields
        and pay_fields2 bellow.'''
        self.accnbr = 0
        self.amount = 0.0
        self.curr = 0
        self.our_accnbr = 0
        self.payday = 0
        self.paynbr = 0        
        self.ptynbr = 0
        self.record_type = 'Payment'
        self.trdnbr = 0
        self.type = ''
        self.valid_from = 0
        
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Payment class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def get_ael_entity(self):
        ret = ael.Payment[self.paynbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1

class Reset:

    def __init__(self,**kwrds):
        '''Fields here are reflected from reset_fields '''
        
        self.cfwnbr = 0
        self.day = 0
        self.end_day = 0
        self.legnbr = 0
        self.read_time = 0        
        self.record_type = 'Reset'
        self.resnbr = 0
        self.rolling_base_day = 0
        self.start_day = 0
        self.type = ''
        self.value = 0
        self.value2 = 0
                
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Reset class ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def get_ael_entity(self):
        ret = ael.Reset[self.resnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1
            
class Settlement:

    def __init__(self,**kwrds):
        self.acquirer_accname = ''
        self.acquirer_account = ''
        self.acquirer_ptyid = ''
        self.aggregate = 0
        self.aggregate_seqnbr = 0
        self.amount = 0
        self.archive_status = 0#?
        self.cfwnbr = 0
        self.curr = 0
        self.delivery_type = 'None'
        self.diary = 0
        self.dividend_seqnbr = 0
        self.from_prfnbr = 0
        self.netting_rule_seqnbr = 0
        self.manual_match = 0
        self.org_sec_nom = 0
        self.owner_usrnbr = 0
        self.party_accname = ''
        self.party_account = ''
        self.party_ptyid = ''
        self.paynbr = 0
        self.post_settle_action = 0
        self.primary_issuance = 0
        self.protection = ''
        self.record_type = 'Settlement'
        self.ref_seqnbr = 0
        self.ref_type = 'None'
        self.sec_insaddr = 0 #combination members use this ref as well
        self.seqnbr = 0
        self.settle_category = 'None'
        self.settle_seqnbr = 0
        self.settleinstruction_seqnbr = 0 #removed in later adm versions
        self.status = 'None'
        self.status_explanation= 0
        self.text = ''        
        self.to_prfnbr = 0
        self.trdnbr = 0
        self.type = 'None'
        self.value_day = 0
        self.party_account_network_name = ''
        self.acquirer_account_network_name = ''
        
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to settlement ignored ARG = ", k
            else:
                self.__dict__[k] = v
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():
            s += ( str(k) +  " --> " + str(v)  + ' ' + str(type(v)) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]

    def add_diary_note(self, note):
        s = self.get_ael_entity()
        if s and note:
            s.add_diary_note(note)

    def check_day(self):
        ret = 0
        s = self.get_ael_entity()
        if s:
            ret = s.check_day()
        return ret
        
    def clone(self):
        c = None
        s = self.get_ael_entity()
        if s:
            c = s.clone()
            cols = s.columns()
            for k, v in self.__dict__.items():                
                if k in cols:
                    setattr(c, k, v)
            #todo, are values ok? double clone, investigate!
            try:
                c.clone_is_modified()
            except:
                c = c.clone()
                
        if not c:
            pr = "Entity class for settlement will return clone=None"
            log(2, pr)
        return c        

    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)
    
    def get_ael_entity(self):
        ret = ael.Settlement[self.seqnbr]
        if not ret:            
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret

    def is_entity_class(self):
        return 1
        
    def run_stp(self):
        ret = 0
        ael_entity = self.get_ael_entity()
        if ael_entity:
            ret = ael_entity.run_stp()
        return ret
        
        
class Trade:

    def __init__(self,**kwrds):
        '''Fields here must be reflected in tr_fields2 bellow '''
        self.aggregate = 0
        self.acquire_day = 0
        self.acquirer_ptynbr = 0
        self.broker_ptynbr = 0
        self.category = ''
        self.contract_trdnbr = 0
        self.correction_trdnbr = 0
        self.counterparty_ptynbr = 0
        self.curr = 0        
        self.fee = 0.0
        self.insaddr = 0
        self.ipa = None # special
        self.owner_usrnbr  = 0
        self.premium = 0
        self.prfnbr = 0
        self.price = 0.0  
        self.primary_issuance = None # special
        self.protection = 0
        self.re_acquire_day = 0        
        self.record_type = 'Trade'
        self.quantity = 0
        self.status = 0
        self.trdnbr = 0
        self.type = ''  
        self.value_day = 0
                
        for k, v in kwrds.items():
            if not self.__dict__.has_key(k):
                print "Bad argument to Trade class ignored ARG = ", k
            else:                
                self.__dict__[k] = v

        if self.__dict__['primary_issuance'] == None:
            for info in self.additional_infos():
                spec = info.addinf_specnbr
                name = spec.field_name
                if name == 'Primary Issuance':
                    if info.value=='Yes':                            
                        self.__dict__['primary_issuance'] = 1
                    else:
                        self.__dict__['primary_issuance'] = 0
            
        if self.__dict__['ipa'] == None:
            for info in self.additional_infos():
                spec = info.addinf_specnbr
                name = spec.field_name
                if name == 'IPA':
                    self.__dict__['ipa'] = info.value
                
    def __str__(self):
        s = "====== %s Entity Class ======\n" % self.record_type
        for k, v in self.__dict__.items():            
            s += ( str(k) +  " --> " + str(v) + "\n")
        return s

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def __getitem__(self, key):
        if self.__dict__.has_key(key):
            return self.__dict__[key]
    
    def used_accounts(self, m, d):
        ''' '''
        tr = self.get_ael_entity()
        if tr:
            if d:
                return tr.used_accounts(m, d)
            else:
                return tr.used_accounts(m)
        else:
            log(3, 'Trade entity class could not find trade, no used accounts returned (Error)')
            return []
    
    def compare(self, stt_c):
        '''Corresponds setl_diff but for entity class '''
        for k, v in self.__dict__.items():
            v1 = getattr(self, k, v)
            v2 = getattr(stt_c, k, v)
            if v1 != v2:
                pr = "%s %s != %s %s" % (k, str(v1), k, str(v2))
                log(2, pr)

    def is_entity_class(self):
        return 1

    def get_ael_entity(self):
        ret = ael.Trade[self.trdnbr]
        if not ret:
            log(2, "Could not return ael_entity from the %s class" % (self.record_type))
        return ret
        
    def nominal_amount(self, date = None):
        t = self.get_ael_entity()
        if date:
            return t.nominal_amount(date)
        else:
            return t.nominal_amount()
    
    def additional_infos(self):
        t = self.get_ael_entity()
        return t.additional_infos()

# Entity classes are introduced above

class PartyUpdate:

    def __init__(self, intermediary_update, parent_is_released_hold = False, trade_update = False):
        self.intermediary_update = intermediary_update
        self.parent_is_released_hold = parent_is_released_hold
        self.trade_update = trade_update #Also true if instrument update

def check_issuer_accounts(party):
    if not party:
        return 0
    for info in party.additional_infos():
        spec = info.addinf_specnbr
        name = spec.field_name
        if name == 'Issuer Accounts':
            if info.value=='Yes':
                return 1
            else:
                return 0
    return 0


def check_primary_issuance(trade, diff_dict = None):
    '''Function which checks if additional info field of trade states
    that this is a trade where we are issuing the bond and the
    coupon payments should go to the counterparty of the trade.'''
    if not trade:
        return 0

    if is_entity_class(trade):
        if trade.primary_issuance != None:
            return trade.primary_issuance

    if diff_dict:
        if diff_dict.has_key('primary_issuance'):
            pi = diff_dict['primary_issuance']
            if pi == 'No':
                return 0
            elif pi == 'Yes':
                return 1

    for info in trade.additional_infos():
        spec = info.addinf_specnbr
        name = spec.field_name
        if name == 'Primary Issuance':
            if info.value=='Yes':
                return 1
            else:
                return 0

    return 0


def clear_fields(settle):
    ''''''  
    log(2, 'clear_fields:')
    settle.settle_seqnbr = 0
    settle.ref_seqnbr = 0
    settle.ref_type = 'None'
    settle.status_explanation = 0
    settle.netting_rule_seqnbr = 0
    settle.manual_match = 0
    settle.post_settle_action = 0
    return


def clear_status_explanation(settle):
    '''settle can be stt_c'''  
    fcf = ael.enum_from_string('StatusExplanation', 'Undetermined Amount')
    iday = ael.enum_from_string('StatusExplanation', 'Historic Value Date')
    data = ael.enum_from_string('StatusExplanation', 'Missing Data')
    cdiff = ael.enum_from_string('StatusExplanation',\
                                 'Currency differs from account currency')
    settle.status_explanation &=~pow(2, fcf)
    settle.status_explanation &=~pow(2, iday)
    settle.status_explanation &=~pow(2, data)
    settle.status_explanation &=~pow(2, cdiff)


def create_accrued_interest(tr, tr_c=None, ins_c=None, append_trans = 1):
    ''''''  
    descr = 'Settlement for accrued interest'
    FR = 'Fixed Rate'
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    ret = None
    if FSettlementGeneral2.accrued_interest_setl_needed(tr) and FSettlementGeneralRT.is_trade(tr_c):
        if tr_c.status in FSettlementGeneralRT.tr_status:
            try:                
                sel = FSettlementGeneralRT.get_settlements(tr.trdnbr)
            except:
                sel = []

            ok = FSettlementGeneral.create_selection(tr.trdnbr, FR, tr.trdnbr, sel, append_trans)
            if ok:                
                if FSettlementGeneral.paydayOK(tr_c.value_day, tr, 1, FR):
                    amount = FSettlementGeneral2.get_interest_accrued(tr_c, ins_c)
                    # Add premium if non zero
                    if amount != 0:
                        setl = ael.Settlement.new()
                        ret = FSettlementGeneral2.interest_accrued_creation(setl, 'New', tr, amount, ins_c, tr_c, append_trans)
                    else:
                        pr = '%s not created due to zero amount (correction trade %d)!' % (descr, tr.trdnbr)
                        log(1, pr)
            else:
                pr = '%s already in Settlement table (correction trade %d)!' % (descr, tr.trdnbr)
                log(1, pr)
        else:
            pr = '%s not created due to wrong trade status(correction trade %d)!' % (descr, tr.trdnbr)
            log(1, pr)
        
    return ret


def divs_from_instrument(instr, div_dict=None, from_trade = 0):
    '''Returns dividens for current instrument. 
    When div_dict deployed all but deleted divs will be taken 
    care of (synch-safer than function instr.dividends).
    from_trade refers from where the function is called (parseInstrEntity is 0)
    instr may NOT be ins_c '''
    dividends = []
    if div_dict:
        for prfx in div_dict.keys():
            newEnt = None
            if prfx != '-':
                for mbfDiv in div_dict[prfx]:
                    seqnbr = None
                    mbfSeqnbr = mbfDiv.mbf_find_object('SEQNBR')
                    if mbfSeqnbr:
                        newEnt = ael.Dividend[int(mbfSeqnbr.mbf_get_value())]
                    div_c = get_entity_class(mbfDiv, div_fields.keys(), newEnt, 'Dividend')
                    dividends.append(div_c)                
                
    elif instr:
        if not from_trade:
            pr = 'divs_from_instrument: no div_dict for instrument %s (Error?)' % (instr.insid)
            log(1, pr)    

        if instr.instype == 'EquitySwap':
            dividends = instr.historical_dividends()
        else:
            if instr.curr:
                curr = instr.curr.insid
            else:
                curr = ael.used_acc_curr()
            days = get_bank_day_per_curr(curr)
            end_day = ael.date_today().add_banking_day(ael.Instrument[curr], days)
            divs = instr.dividends(end_day, 1) #version_ok
            dividends = divs.members()
            for d in dividends:
                if d.insaddr and d.insaddr.instype == 'EquitySwap':
                    dividends.remove(d)
    return dividends


def find_adjusted(seqnbr):
    ''''''      
    log(2, 'find_adjusted:')
    adjusted=None
    if seqnbr:
        sel = ael.Settlement.select('settle_seqnbr=%d' % seqnbr)
        for s in sel:
            if s.settle_category!='None':
                adjusted=s
    return adjusted


def get_bank_day_per_curr(inst):
    '''Returns number of days based on currency in dictionary
    FSettlementVariables.days_curr'''
    
    curr = ''
    days = 1
    acc_curr = 0
    if inst:
        if type(inst) == type(str('')):
            curr = inst
        elif inst.record_type == 'Instrument':
            curr = inst.curr.insid

    if curr == '':
        curr = ael.used_acc_curr()
        pr = "get_bank_day_per_curr: invalid input (File)"
        log(1, pr)
        acc_curr = 1 # default currency used
        
    if param.days_curr.has_key(curr):
        days = param.days_curr[curr]
        if acc_curr:
            pr = "Days based on currency %s instead (ael.used_acc_curr())" % (curr)
            log(1, pr)
    else:
        pr = "Currency %s not found in FSettlementVariables" % (curr)
        log(1, pr)
        curr = ael.used_acc_curr()
        if param.days_curr.has_key(curr):
            days = param.days_curr[curr]
            pr = "Days based on currency %s instead (ael.used_acc_curr())" % (curr)
            log(1, pr)

    return days

    
def end_security_value_day(tr, combination_member, ins_c=None):
    '''Returns value day for the end security. 
    If combination_member exp_day is returned. 
    Note todays date is returned as default.
    tr can be tr_c'''
    ret = ael.date_today()
    ins_c = FSettlementGeneralRT.set_c(ins_c, tr.insaddr, 'Instrument')
        
    if FSettlementGeneral.is_collateral_trade(tr) and tr.re_acquire_day:
        ret = tr.re_acquire_day
    elif ins_c.exp_day:
        ret = ins_c.exp_day
    
    if combination_member:
        ret = combination_member.exp_day
    return ret    


def get_cf_curr(cf, leg_c=None):
    '''cf can be cf_c '''
    curr = 0
    leg = cf.legnbr
    if leg_c:
        leg = leg_c
    if leg:        
        if leg.insaddr.instype == 'DualCurrBond' and \
            cf.type=='Fixed Amount':
            if leg.redemption_curr:
                curr = leg.redemption_curr.insaddr
        else:
            curr = leg.curr.insaddr
    return curr


def get_closed_settlement(setls, return_amount=1):
    '''From the list of settlements return the amount of the closed one. 
    Special treatment of settlements with payment reference via diary!
    If return_amount = 0 just return if closed settlement exists or not.
    See FSettlementGeneral.also check_status_closed
    '''
    amount = 0
    rs = "get_closed_settlement: amount returned = s.paynbr.amount where s.seqnbr ="
    for s in setls:
        if s.status == 'Closed':
            if has_the_keyword(s) and s.paynbr:
                pr = '%s%d' % (rs, s.seqnbr)
                log(1, pr)
                if return_amount:
                    return s.paynbr.amount
                    
            if return_amount:
                amount = amount + s.amount
            else:
                amount = 1
        elif FSettlementGeneral.check_references(s.seqnbr):
            if s.ref_type=='Net Part' and s.ref_seqnbr.status=='Closed':
                if has_the_keyword(s) and s.paynbr:
                    pr = '%s %d (net part)' % (rs, s.seqnbr)
                    log(1, pr)
                    if return_amount:
                        return s.paynbr.amount
                        
                if return_amount:
                    amount = amount + s.amount
                else:
                    amount = 1
            elif s.ref_type=='Split':
                sel = ael.Settlement.select('ref_seqnbr="%d"' % (s.seqnbr))
                for split in sel:
                    if split.status=='Closed':
                        if has_the_keyword(s) and s.paynbr:
                            pr = '%s %d (splited)' % (rs, s.seqnbr)
                            log(1, pr)
                            if return_amount:
                                return s.paynbr.amount
                        if return_amount:
                            amount = amount + split.amount
                        else:
                            amount = 1
                        break
        elif FSettlementGeneral.check_referenced_to(s.seqnbr, 1):
            # manual adjust
            sel = ael.Settlement.select('settle_seqnbr=%d' % (s.seqnbr))
            for ma in sel:
                if ma.status=='Closed':                                           
                    if has_the_keyword(s) and s.paynbr:
                        pr = '%s %d (manual adjust)' % (rs, s.seqnbr)
                        log(1, pr)
                        if return_amount:
                            return s.paynbr.amount            
            if return_amount:
                amount = amount + s.amount
            else:
                amount = 1                
                
    return amount


def get_closing_trades(tr):
    '''Returns a list of trades that have (partially) closed the trade tr.'''
    ret = []
    if not tr:        
        return ret    
    else:
        tr = get_trade_entity(tr)        
        
    selection = ael.Trade.select('contract_trdnbr="%d"' % (tr.trdnbr))
    for cl in selection:       
        if FSettlementGeneral2.is_closing(cl):
            ret.append(cl)
    return ret


def get_comblinks(combs):
    '''Returns list with combination links from the list of amb objects.'''
    ret = []
    for amb_obj in combs:
        comblink = None
        seqnbr = amb_obj.mbf_find_object('SEQNBR')
        if seqnbr:
            comblink = ael.CombinationLink[int(seqnbr.mbf_get_value())]
        cbl_c = get_entity_class(amb_obj, cbl_fields, comblink, 'CombinationLink')
        ret.append(cbl_c)
    return ret


def get_counterparty(trade, ins_c=None, cp_mode=1, ipa_mode= 0):
    '''This function should be used only when dealing with Cash flows (and dividends).'''
    ptyid = ''
    ins_c = FSettlementGeneralRT.set_c(ins_c, trade.insaddr, 'Instrument')
    instype = ins_c.instype
    #if any changes done, reflect them to FSettlmentGeneralRT.create_setlObj
    if instype in FSettlementGeneral.issuer_list:
        if ins_c.issuer_ptynbr:
            ptyid = ins_c.issuer_ptynbr.ptyid
    else:
        if trade.counterparty_ptynbr and cp_mode:
            ptyid = trade.counterparty_ptynbr.ptyid
            
    if ipa_mode:
        ipa = FSettlementGeneral.issuing_paying_agent(trade)
        if ipa:
            ptyid = ipa
            
    if instype == 'Stock' and not issuing_paying_agent(trade):
        if ins_c.issuer_ptynbr:
            ptyid = ins_c.issuer_ptynbr.ptyid
            
    return ptyid


def get_corrected_setl(entity, tr, typ=None, setl=None):
    '''Returns the amount of the closed settlement of the corrected trade.
    entity and tr can be ent_c.'''
    ret = 0
    setls = get_corresponding_setls(entity, tr, typ, setl)
    if len(setls):
        ret = get_closed_settlement(setls)
        if not ret:                
            # undeleted corresponding setlements exist
            for s in get_unclosed_settlement(setls):
                trdnbr = 0
                if s.trdnbr:
                    trdnbr = s.trdnbr.trdnbr
                pr = "Setl %d in status %s is not deleted, tr %d is corrected! (File)" % (s.seqnbr, s.status, trdnbr)
                log(1, pr)
    return ret        


def get_corresponding_setls(entity=None,tr=None,typ=None, pay_setl=None):
    '''Corresponding settlement belongs to the old trade
    that has been corrected via the Correct trade functionality.
    pay_setl has reference to closed payment in diary.
    '''
    setls = []
    if tr:
        TE = 'Termination Fee'
        if typ == TE:
            pr = 'get_corr_setl: no search on coressponding %s settlements done' % (TE)
            log(3, pr)                
            return setls
        trades = []
        last_trade = 0
        while not last_trade:
            if tr.correction_trdnbr and tr.correction_trdnbr.trdnbr != tr.trdnbr:
                trades.append(tr.correction_trdnbr)
                tr = tr.correction_trdnbr
            else:
                last_trade = 1
        for old_trade in trades:
            sel = ael.Settlement.select('trdnbr=%d' % old_trade.trdnbr)
            for s in sel:
                if entity:
                    if entity.record_type == 'CashFlow':
                        if s.cfwnbr and entity.cfwnbr and \
                           (s.cfwnbr.cfwnbr==entity.cfwnbr):
                            setls.append(s)
                    elif entity.record_type == 'Payment':
                        paynbr = 0
                        keyword_paynbr = get_keyword(pay_setl, s)
                        if keyword_paynbr != '':
                            s1=keyword_paynbr.find("=")+1
                            if len(keyword_paynbr[s1:]):
                                try:
                                    paynbr = int(keyword_paynbr[s1:])
                                except:
                                    paynbr = 0
                        if s.paynbr and (paynbr == s.paynbr.paynbr):
                            setls.append(s)
                elif typ:
                    if typ == s.type:
                        setls.append(s)
    else:
        pr = 'get_corr_setl: no search on coressponding settlements done (no trade)'
        log(3, pr)        
        
    return setls


def get_coupons(instrument):
    ''' ins_c? todo, seems NOT to be used in 3_2_fix 
    coupons = []
    sel = FSettlementGeneral.get_comb_instruments(instrument)#?
    for s in sel:
        comb_coupons = FSettlementGeneralRT.coupons_from_tr(None, s.owner_insaddr)
        for c in comb_coupons:
            coupons.append(c)
                            
    if instrument.instype in FSettlementGeneral.und_ins_security:
        und_coupons = FSettlementGeneralRT.coupons_from_tr(None, \
                                            instrument.und_insaddr)
    else:
        und_coupons = FSettlementGeneralRT.coupons_from_tr(None, instrument)
    for c in und_coupons:
        if c not in coupons:
            coupons.append(c)

    return coupons
    '''

def get_pay_type(pay):
    '''Returns a string for a Additional Payment type. 
    See also FSettlementGeneral.invalid_payment_types.'''    
    ret = ''
    if pay:
        if pay.type == 'Cash':
            ret = 'Payment Cash'
        elif pay.type == 'Premium':
            ret = 'Payment Premium'   
        else:
            ret = "%s" % (pay.type)
    else:
        log(0, 'get_pay_type: the input pay is None')

    if ret == '':
        log(0, 'get_pay_type: about to return pay.type=empty string (File)')
    return ret


def get_cf_type(cf):
    ''' Returns a string for a CashFlow type. 
    See also is_valid_cf_type.'''
    ret = 'None'
    if cf:
        # see also FSettlementGeneral2.create_coupon
        if cf.type == 'Dividend':
            ret = 'Equity Swap Dividend'
        else:
            ret = "%s" % (cf.type)        
    else:
        log(0, 'get_cf_type: the input cf is None')

    if ret == 'None':
        log(0, 'get_cf_type: about to return cf.type=None (File)')
    return ret
    
    
def get_secnom_acc_if_closed(tr):
    '''Get the account of the closed Security nominal '''
    acc = None
    setls = ael.Settlement.select('trdnbr=%d' % tr.trdnbr)
    for setl in setls:                
        if FSettlementGeneral2.check_security([setl]):
            accname = setl.acquirer_accname
            accid = setl.acquirer_ptyid
            if accid:
                party = ael.Party[accid]
                if party:
                    ptynbr = party.ptynbr
                    acc = ael.Account.read('ptynbr=%d and name="%s"' % (ptynbr, accname))
            break
    return acc


def get_tals(setl, trade=None):        
    '''no tr_c here '''
    ret = []
    if setl and not trade:
        if setl.trdnbr:
            trade = setl.trdnbr
                
    if setl.value_day and type(setl.value_day) == type(ael.date('2005-01-01')) :
        ret = trade.used_accounts(0, setl.value_day)
    elif not setl.value_day:
        pr = 'get_tals: Settlement %d has no value_day, returned TALs will not based on date.' % (setl.seqnbr)
        log(1, pr)
        ret = trade.used_accounts(0)
    if setl.type in ['Coupon', 'Redemption']:
        coupons = FSettlementGeneralRT.coupons_from_tr(trade, None)
        if len(coupons) and has_closed_security_nominal(trade):
            tal = get_coupon_redemption_TAL_for_counterparty(trade, setl.value_day, setl.type)
            tr = get_ipa_trade(trade)
            if not tal and tr:
                tal = get_coupon_redemption_TAL_for_counterparty(tr, setl.value_day, setl.type)
                if tal:
                    ret.append(tal)
    
    return ret


def get_trades(instrument):
    '''Returns trades of the instrument including combination trades where the instrument is a member.
    No reason for ins_c.'''
    trades = instrument.trades().members()    
    sel = FSettlementGeneral.get_comb_instruments(instrument)
    for comblink in sel:
        comb_trades = comblink.owner_insaddr.trades().members()
        for t in comb_trades:
            if t not in trades:
                trades.append(t)

    return trades


def get_trade_entity(tr):
    '''If the tr is int return corresponding trade. '''
    ret = tr
    if type(tr) == type(4711):
        ret = ael.Trade[tr]
    return ret        


def get_unclosed_settlement(setls):
    '''Returns the list with unlclosed settlements. Terminatin fee
    will not be included either.'''
    unclosed = []
    for s in setls:
        if s.status != 'Closed' and s.type != 'Termination Fee':
            unclosed.append(s)
    return unclosed


def has_end_security(trade=None, instr=None):
    '''instr is used only for combination_member'''
    if trade:
        instr = trade.insaddr
    if instr and instr.instype in \
       FSettlementGeneral.und_ins_security:
        return 1
    else:
        return 0


def has_security_nominal(trade):
    if trade.insaddr:
        ins = trade.insaddr
    else:
        return 0
    
    if FSettlementGeneral.ins_has_security_nominal(ins):
        return 1
    if ins.instype == 'FreeDefCF' and ins.issuer_ptynbr:
        return 1
    if ins.instype in FSettlementGeneral.ins_combination:
        for c in ins.combination_links():
            member_ins = c.member_insaddr # ent_c ok
            if member_ins and FSettlementGeneral.ins_has_security_nominal(member_ins):
                return 1
    return 0


def interest_accrued_creation(setl, status, trade, amount=None, ins_c=None, tr_c=None, append_trans = 1):
    '''Changes here need to be reflected in FSettlementGeneral.createObjTrade '''
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade')
    ins_c = FSettlementGeneralRT.set_c(ins_c, trade.insaddr, 'Instrument')
    setl.status = status
    setl.type = 'Fixed Rate' #uggly
    setl.trdnbr = trade.trdnbr
    
    FSettlementGeneral2.copy_protection_from_trade(setl, trade)
    if amount:
        setl.amount = amount
    else:
        setl.amount = FSettlementGeneral2.get_interest_accrued(tr_c, ins_c)
    setl.curr = ins_c.curr.insaddr
    setl.value_day = tr_c.value_day
        
    if tr_c.prfnbr:
        if setl.amount > 0:
            setl.to_prfnbr = tr_c.prfnbr.prfnbr
        else:
            setl.from_prfnbr = tr_c.prfnbr.prfnbr

    setl.acquirer_ptyid = FSettlementGeneral.get_acquirer(trade)
    setl.party_ptyid = get_counterparty(trade, trade.insaddr, 1, 1)

    FSettlementGeneral.account_info(trade, setl, 0)
    ret = None
    if append_trans:
        FSettlementGeneral.append_transaction(setl)
        FSettlementGeneral.print_commit(setl)
    else:
        ret = setl
    return ret

def issuing_paying_agent(trade):
    '''trade can be tr_c.'''
    if not trade:
        return None
        
    if type(trade) != ael.ael_entity:
        return trade.ipa
        
    for info in trade.additional_infos():
        spec = info.addinf_specnbr
        name = spec.field_name
        if name == 'IPA':
            return info.value
    return None

def get_coupon_redemption_TAL_for_counterparty(trade, value_day, cashflow_type):
    
    tals = []
    if value_day:
        tals = trade.used_accounts(0, value_day)
    else:
        tals = trade.used_accounts(0)
    
    for tal in tals:
        if tal.settle_cf_type == cashflow_type and \
           tal.party_type == 'Counterparty':
            return tal
    return None

def get_ipa_trade(trade):
    
    instrument = trade.insaddr
    if instrument:
        for t in instrument.trades():
            if issuing_paying_agent(t):
                return t
    return None

def issuing_paying_agent_position(trade):
    '''tr_c may be sent in here '''
    if not trade:
        return None
    ins = trade.insaddr
    if not ins:
        return None
    for t in ins.trades():
        for s in ael.Settlement.select('trdnbr=%d' % t.trdnbr):
            tr2 = s.trdnbr
            if trade.trdnbr == s.trdnbr:
                tr2 = trade.trdnbr
            ipa = issuing_paying_agent(tr2)
            if ipa:
                return ipa
    return None


def is_correction_trade(tr):
    ''' '''
    ret = 0
    if tr:
        if tr.correction_trdnbr:
            if tr.correction_trdnbr.trdnbr != tr.trdnbr:
                ret = 1
    return ret

def get_security_nominal_settlement(trade):
    
    
    returned_record = None
    settlement_list = ael.Settlement.select('trdnbr=%d' % trade.trdnbr)
    for settlement in settlement_list:
        if settlement.type == 'Security Nominal':
            returned_record = settlement
            break
    return returned_record

def has_closed_security_nominal(trade):
  
    returned_boolean = False
    sec_nom_settlement = get_security_nominal_settlement(trade)
    if sec_nom_settlement and sec_nom_settlement.status == 'Closed':
        returned_boolean = True
    return returned_boolean

def is_coupon(trade, cf, tr_c=None, cf_c=None, leg_c=None, underlying_instrument = None):
    '''cf should be cf_c where possible. '''
    coupon = 0
    instr = None
    
    if underlying_instrument:
        instr = underlying_instrument
    elif trade:
        trade = get_trade_entity(trade)
        if trade.insaddr:
            instr = trade.insaddr
    elif cf:
        instr = cf.legnbr.insaddr
        
    if instr:        
        coupon = FSettlementGeneral2.coupon_ok(instr)
            
    tr_c = FSettlementGeneralRT.set_c(tr_c, trade, 'Trade') # because of get_trade_entity
    cf_c = FSettlementGeneralRT.set_c(cf_c, cf, 'CashFlow')
    leg_c = FSettlementGeneralRT.set_c(leg_c, cf_c.legnbr, 'Leg')
    
    if coupon and cf:
        coupon = 0
        if (cf_c.type in ['Fixed Rate', 'Fixed Amount'] or  \
            FSettlementGeneral2.is_float_coupon(cf, cf_c, leg_c)) and\
            not check_primary_issuance(tr_c):
            coupon = 1

    return coupon


def is_valid_instrument(instrument):
    '''Checks if the instrument type is available in
    FSettlementVariables.valid_instrument_types'''
    ok = 0
    if instrument:
        instype = instrument.instype
        if instype in param.valid_instrument_types:
            ok = 1
    else:
        log(0, 'FSettlementGeneral.is_valid_instrument: no instrument as input')

    return ok


def is_valid_cf_type(cf):
    ''' '''
    ok = 0
    if cf.type in FSettlementGeneral.cf_types:
        ok = 1
    else:
        pr = 'CF %d, CF type=%s is not supported' % (cf.cfwnbr, cf.type)
        log(3, pr)
    return ok


def is_unqualified_trade_status(from_status):
    '''Returns true if old trade status was something like Void, 
    Confirmed Void, Terminated, Simulated. Also if old trade status
    does not qualify for settlement generation.'''
    if from_status in FSettlementGeneral.new_status_to_void:
        return 1
    elif from_status not in param.status:
        return 1
    return 0
    
def log(level, s):
    return FSettlementGeneral.log(level, s)

def port_comparison(settle, prfnbr):
    '''settle can be stt_c '''
    ok = 0    
    prfnbr2 = 0
    if not prfnbr:
        ok = 1
    elif settle.from_prfnbr:
        prfnbr2 = settle.from_prfnbr.prfnbr
    elif settle.to_prfnbr:
        prfnbr2 = settle.to_prfnbr.prfnbr
        
    if not prfnbr and not prfnbr2:
        prfnbr = 0
        prfnbr2 = 0

    if prfnbr == prfnbr2:
        ok = 1
    else:
        pr = "port_comparison: different portfolios (%s vs %s) File" % (str(prfnbr), str(prfnbr2))
        log(3, pr)

    return ok


def recall_accrued_interest(tr, original_trade_status):
    ''' '''
    closing_trades = get_closing_trades(tr)
    if len(closing_trades):
        for cl in closing_trades:           
            setls = FSettlementGeneral.get_setl_rows(cl.trdnbr, 'Fixed Rate', str(cl.value_day))
            for setl in setls:
                if FSettlementGeneral2.is_interest_accrued(setl) and FSettlementGeneral.source_data(setl):
                    pr = 'Original Trade %d is changed status from %s to %s, \
                    Recalling accrued interest Settlement %d' % (tr.trdnbr, original_trade_status, tr.status, setl.seqnbr)
                    log(1, pr) # no need for stt_c bellow
                    setlObjList = FSettlementGeneral.create_from_settle([setl])
                    if len(setlObjList):
                        setlObj = setlObjList[0]
                        setlObjNew = setlObj
                    if setlObj and setlObjNew:
                        setlObjNew['status'] = 'Recalled'
                    FSettlementGeneralRT.update_row(setlObj, setlObjNew)


def sameUser(setlObj, attrib):
    '''Checks if the user who made an ammendment is the same as the previous user.
    ATS user represents this AEL module so one should not run Prime/Settlement Manager
    with the same user.'''    
    ret = 0
    if setlObj and attrib:
        new = setlObj.mbf_find_object(attrib)
        update = "!%s" % (attrib)
        old = setlObj.mbf_find_object(update)
        if new and old:
            if new.mbf_get_value() == old.mbf_get_value():
                ret = 1
        else:
            ret = 1
    else:
        if setlObj == None:            
            log(1, 'sameUser: no Settlement object from AMB as input')
        if attrib == None:                      
            log(1, 'sameUser: no attribute as input')
        elif attrib == '':
            log(1, 'sameUser: attribute empty string, no comparation')

    return ret

def set_curr(diff_dict, curr):
    '''Currency of the deployed settlement object is returned as an Instrument
    if curr.insid is in the diff dicitonary.'''
    if diff_dict:
        if diff_dict.has_key('curr.insid'):
            insid = diff_dict['curr.insid']
            if ael.Instrument[insid]:
                curr = ael.Instrument[insid]
                # do not forget to do following
                #setlObj['curr'] = curr.insaddr
                #after using this function
    return curr
   

def setl_diff(setl1, setl2, result_dict={}, exclude_cols=[]):
    '''Function takes in two settlement entites and returns differences.
    For corresponding functionality see entity classes and their functions compare.'''
    if not setl1 or not setl2:
        log(2, "setl_diff: wrong input, 2 settlements are needed for comparation!")
        return
        
    p1 = setl1.pp().split('\n')
    p2 = setl2.pp().split('\n')
    key = "Settl %d vs %d" % (setl1.seqnbr, setl2.seqnbr)
    pr = key
    pr_shown = 0
    for i in range(0, len(p1)):
        if p1[i]!=p2[i]:
            show_col = 1
            for exclude in exclude_cols:
                if p1[i].find(exclude) > -1:
                    show_col = (show_col and 0)
                    
            if show_col:
                if not pr_shown:
                    pr_shown = 1
                pr = "%s != %s" % (p1[i].replace("  ", ""), p2[i].replace("  ", ""))
                log(4, pr)
                
                if not result_dict.has_key(key):
                    result_dict[key] = [pr]
                else:
                    result_dict[key].append(pr)
    return result_dict
    
def get_ael_cashflow(s):
    cf = None
    if type(s.cfwnbr) == int:
        cf = ael.CashFlow[s.cfwnbr]
    else:
        cf = s.cfwnbr
    return cf

def get_ael_curr(s):
    curr = None
    if type(s.curr) == int:
        curr = ael.Instrument[s.curr]
    else:
        curr = s.curr
    return curr

def get_from_portfolio(s):
    p = None
    if type(s.from_prfnbr) == int:
        p = ael.Portfolio[s.from_prfnbr]
    else:
        p = s.from_prfnbr
    return p

def get_to_portfolio(s):
    p = None
    if type(s.to_prfnbr) == int:
        p = ael.Portfolio[s.to_prfnbr]
    else:
        p = s.to_prfnbr
    return p

def get_sec_ins(s):
    i = None
    if type(s.sec_insaddr) == int:
        i = ael.Instrument[s.sec_insaddr]
    else:
        i = s.sec_insaddr
    return i

def is_equal(s1, s2):
        
    return s1.party_ptyid == s2.party_ptyid and \
           get_sec_ins(s1) == get_sec_ins(s2) and s1.party_accname == s2.party_accname and \
           s2.party_account == s2.party_account and \
           s1.type == s2.type and \
           s1.acquirer_accname == s2.acquirer_accname and \
           s1.acquirer_ptyid == s2.acquirer_ptyid and \
           s1.acquirer_account == s2.acquirer_account and \
           get_ael_cashflow(s1) ==  get_ael_cashflow(s2) and \
           get_ael_curr(s1) == get_ael_curr(s2) and \
           s1.seqnbr != s2.seqnbr and \
           get_from_portfolio(s1) == get_from_portfolio(s2) and get_to_portfolio(s1) == get_to_portfolio(s2) 

           
def get_compared_settls(cf_list=[], exclude_cols=[]):
    '''Returns dictionary with settlement comparations '''
    result_dict = {}
    compared = []
    
    for c in cf_list:
        pr = "%d CF %d %s Amount:%d" % (c.seqnbr, c.cfwnbr.cfwnbr, c.status, c.amount)
        log(4, pr)
    
        
    for c1 in cf_list:
        for c2 in cf_list:
            if c1.seqnbr != c2.seqnbr:
                if c1 not in compared:
                    result_dict = setl_diff(c1, c2, result_dict, exclude_cols)
            else:
                compared.append(c1)
    
    return result_dict 

def intact_coupon_amount(cf):

    coupon_already_exists = 0
    total_closed_amount = 0
    
    cf_list = FSettlementGeneral2.find_coupons(cf.cfwnbr, cf.type, 1)
    for s in cf_list:
        if is_equal(cf, s ) and s.status == 'Closed':
            total_closed_amount = total_closed_amount + s.amount
            
    if total_closed_amount == 0:
        new_amount = cf.amount
    else:
        new_amount = cf.amount - total_closed_amount
        coupon_already_exists = 1
           
    return coupon_already_exists, new_amount

def string_has_words(s, words):
    for w in words:
        if s.find(w) == -1:
            return 0
    return 1
    
    
def sub_combinationlink(comb_dict, comb_instr, trades, diff_dict, ins_c=None):
    '''Combination instrument update triggers this function.    
    No need for tr_c because of trades.'''
    
    diff_dict['combinationlink'] = 1
    cfs = comb_instr.cash_flows() # amb_message does not include cfs, leave it this way
    for ev in comb_dict.keys():
        if ev == '+' and len(comb_dict[ev]):
            for comblink in get_comblinks(comb_dict[ev]):
                for tr in trades:
                    FSettlementGeneral2.update_combination_cf(tr, comblink, diff_dict, tr) #no ins_c here
                    FSettlementGeneral2.update_combination_securities(tr, diff_dict, tr)
                    
        elif ev in ['!', 'empty'] and len(comb_dict[ev]):
            # COMBINATIONLINK is intact when index_factor is changed
            if ev == 'empty' and not diff_dict.has_key('index_factor'):
                continue            
            for comblink in get_comblinks(comb_dict[ev]):
                for tr in trades:                        
                    # weight of the combination member might have been updated
                    FSettlementGeneral2.update_combination_cf(tr, comblink, diff_dict, tr)
                    FSettlementGeneral2.update_combination_securities(tr, diff_dict, tr)
        elif ev == '-' and len(comb_dict[ev]):
            for comblink in get_comblinks(comb_dict[ev]):
                combination_member = FSettlementGeneral.get_combination_member(comblink)
                for tr in trades:
                    FSettlementGeneral.void_trade_recall_setls(tr, None, combination_member)### I or II
                    for leg in combination_member.legs():
                        for cf in leg.cash_flows():
                            if cf not in cfs:
                                pr = "Settlement for CF %d should be recalled, %s removed\
                                from combination %d." % (cf.cfwnbr, combination_member.insid, tr.trdnbr)
                                log(1, pr)
                                FSettlementGeneralRT.update_cf(cf, diff_dict, tr, None, tr, None, None, cf, None)
                    FSettlementGeneral2.update_combination_cf(tr, comblink, diff_dict, tr) #no ins_c here
                    FSettlementGeneral2.update_combination_securities(tr, diff_dict, tr, comblink, comb_link_removed = True)


def touch_closed_trade(closing):
    '''If it is a closing trade touch the closed trade in order to unnet it.
    See also FSettlementGeneralRT.insert_trade(tr) function for the order of functions
    as well as FSettlementAMB.parseTrEntity(trObj,ev) which does similar.'''
    tr = FSettlementGeneral2.get_closed_trade(closing)
    
    if not is_netted_trade(tr):
        return
    
    if tr:                        
        pr = "Trade %d is closing, touching settlements of the trade %d" % (closing.trdnbr, tr.trdnbr)
        log(1, pr)        
        diff_dict={'touch_closed_trade':'touch_closed_trade'}
        FSettlementGeneralRT.update_premium(tr, diff_dict, 'Premium')
        if tr.insaddr.instype in FSettlementGeneral.und_ins_security:
            FSettlementGeneralRT.update_premium(tr, diff_dict, 'End Security')
            FSettlementGeneral2.validate(tr, 'UPDATE')

        if tr.fee:
            FSettlementGeneralRT.update_premium(tr, diff_dict, 'Fee')

        cfs = FSettlementGeneralRT.cfs_from_tr(tr)
        for cf in cfs:            
            FSettlementGeneralRT.update_cf(cf, diff_dict, tr, None, tr, None, None, cf, None)

        coupons = FSettlementGeneralRT.coupons_from_tr(tr, None)
        for c in coupons:            
            FSettlementGeneralRT.update_cf(c, diff_dict, None, tr.insaddr, None, tr.insaddr, None, c, None)

        eqs_mode = is_equity_swap(tr.insaddr)
        divs = divs_from_instrument(tr.insaddr, None, 1)
        for d in divs:
            FSettlementGeneralRT.update_div(d, diff_dict, tr.insaddr, tr, eqs_mode)

        for pay in tr.payments():
            FSettlementGeneralRT.update_payment(pay, diff_dict)
        
        FSettlementGeneral2.update_combination_trade(tr, {'combination_quantity':tr.quantity}, 1, tr)


def update_accrued_interest(tr, diff_dict, ins_c=None, tr_c=None):
    ''''''
    setls = []
    descr = 'Settlement for accrued interest'
    FR ='Fixed Rate'
    tr_c = FSettlementGeneralRT.set_c(tr_c, tr, 'Trade')
    if FSettlementGeneral2.accrued_interest_setl_needed(tr_c) and FSettlementGeneralRT.is_trade(tr_c):
        if tr_c.status in FSettlementGeneralRT.tr_status:
            setls = FSettlementGeneral.get_setl_rows(tr.trdnbr, FR, str(tr_c.value_day))
    else:
        return
        
    if len(setls) == 0:            
        create_accrued_interest(tr, tr_c, ins_c)
    else:
        setl = None # no need for stt_c bellow
        if len(setls) > 1:
            pr = 'update_accrued_interest: more than one %s! (Error)' % (descr)
            log(1, pr)                
        else:
            setl = setls[0]

        if setl and not FSettlementGeneral2.is_interest_accrued(setl):
            pr = 'update_accrued_interest: wrong %s fetched! (File)' % (descr)
            log(1, pr)                
            return
            
        setlObjList = FSettlementGeneral.create_from_settle([setl])
        if len(setlObjList):
            setlObj = setlObjList[0]
                
        if setlObj:
            if setlObj.status not in FSettlementGeneralRT.noupdate_stl_status and is_updatable(setlObj):
                if diff_dict:
                    newS = FSettlementGeneralRT.create_setlObj(setlObj, diff_dict, tr, None, None, None, FR, None, None, tr_c) #, leg_c, cf_c, res_c)
                    if setl and newS != None:                
                        if newS.amount != 0:
                            FSettlementGeneralRT.update_setl_row(setl, newS, 'Updated')
                        else:
                            FSettlementGeneralRT.update_setl_row(setl, newS, 'Recalled')
                    elif not setl:
                        pr = 'update_accrued_interest: Empty settlement (File)'
                        log(1, pr)
                else:
                    pr = 'Irrelevant trade change, no settlement update. (File)'
                    log(2, pr)                        
            else:
                log(1, 'update_accrued_interest impossible, wrong setl.status')
        else:
            log(1, 'update_accrued_interest: Could not find settlement row to update')
            
    return


def update_secnom_from_instr(instr, size, currInst, ins_c=None):
    '''If an instrument is updated, the settlement 
    rows for security nominal will be updated. Input size 
    is a contract size. '''
    ins_c = FSettlementGeneralRT.set_c(ins_c, instr, 'Instrument')
    if instr:    
        trades = instr.trades().members()    
        pr = 'update_secnom_from_instrument: %s' % (instr.insid)
        log(1, pr)
    else:
        trades = []

    for t in trades:
        if t.status in FSettlementGeneralRT.tr_status:
            # get settlements that reference the sec nom
            # only SR not earlier than today
            setls = FSettlementGeneral.get_setl_rows(t.trdnbr, 'Security Nominal', '') ### IV
            for s in setls: # no need for stt_c bellow
                if s.status not in FSettlementGeneralRT.noupdate_stl_status and is_updatable(s):
                    setlObjList = FSettlementGeneral.create_from_settle([s])
                    if len(setlObjList):
                        setlObj = setlObjList[0] 
                        sn_n = setlObj

                    updateSecNom = 0
                    if size and sn_n:
                        sn_n.amount = FSettlementGeneral.calc_security_nominal(t, None, 0, 0, ins_c)
                        updateSecNom = 1
                    if currInst and sn_n:  
                        sn_n.curr = currInst
                        updateSecNom = 1
                        
                    if updateSecNom and setlObj and sn_n:
                        FSettlementGeneralRT.update_setl_row(setlObj, sn_n, 'Updated')
    return


def identical_payment_stored(p1, p2, trade):
    '''
    p1    - payment to created
    p2    - already existing payment belonging to the corrected trade
    trade - belongs to p1.
    '''
    check = False
    paynbr = -1
    if FSettlementGeneral2.is_correction_trade(trade):
        if equal_add_payments(p1, p2):
            settls = ael.Settlement.select('paynbr=%d' % p2.paynbr)
            if get_closed_settlement(settls, 0):
                check = True
                paynbr = p2.paynbr
    return (check, paynbr)

def not_in_diary(paynbr_in_diary, tr, tr_paynbr):
    ''' '''
    keyword = '%s%d' % (keyw, paynbr_in_diary)
    pr = "Checking if closed payment %d is referenced from diary" % (paynbr_in_diary)
    log(4, pr)
    for k, v in FSettlementGeneral.trans_dict.items():
        key_paynbr = get_paymentnbr_from_keyword(v)
        if has_the_keyword(v) and (key_paynbr == paynbr_in_diary):
            pr = "Trans dict includes settl that refers payment %d" % (key_paynbr)
            log(4, pr)
            return (False, '')
    
    payment_settlemnts = ael.Settlement.select("trdnbr=%d" % tr.trdnbr) #source data?    
    for new_pay in tr.payments(): #todo
        for setl in payment_settlemnts:
            if setl.paynbr:                
                if setl.paynbr.paynbr == new_pay.paynbr:
                    key_paynbr = get_paymentnbr_from_keyword(setl)
                    if has_the_keyword(setl) and (key_paynbr == paynbr_in_diary):
                        pr = "Settl %d refers payment %d from diary" % (setl.seqnbr, key_paynbr)
                        log(4, pr)
                        return (False, '')
        
    return (True, keyword) 
    
def get_keyword(setl, corr_set):
    '''This function takes settlement and corrected settlement for a payment as an input.
    If setl has reference in diary the keyword, which is reference to the payment
    of the corr_setl, is returned.'''
    ret = ''
    if not setl:
        return ret
    elif not setl.paynbr:
        return ret
    
    if not corr_set:
        return ret
    elif not corr_set.paynbr:
        return ret
    
    if setl.type != corr_set.type:
        return ret
        
    if type(setl.paynbr) == int:
        setl = ael.Settlement[setl.seqnbr]
    elif type(setl.paynbr) == str:
        setl = ael.Settlement[int(setl.seqnbr)]
    
    pay_ref = get_paymentnbr_from_keyword(setl)
    if  pay_ref != -1 and pay_ref == corr_set.paynbr.paynbr:
        ret = '%s%d' % (keyw, corr_set.paynbr.paynbr)
        pr = "Setl %d has diary reference to %s (corrected setl %d)" % (setl.seqnbr, ret, corr_set.seqnbr)
        log(5, pr)
        
    return ret

def has_the_keyword(s):
    ret = False
    if s and s.diary:
        text = s.diary.get_text()
        dateTime = text.split('<DateTime>')
        dateTime.reverse()
        for dt in dateTime:
            found = dt.find(keyw)
            if found != -1:
                ret = True
                break
    return ret

def get_input_string(pay, trade):
    '''Returns a string that includes info about which closed payment that pay should reference to.
    Pay is payment that is to be created. 
    '''
    co_tr = trade.correction_trdnbr
    co_tr_pay_list = co_tr.payments()
    for p in co_tr_pay_list:
        check, paynbr = identical_payment_stored(pay, p, trade)
        if check:
            not_in, keyw = not_in_diary(paynbr, trade, pay.paynbr)
            if not_in:
                return keyw
    return ''

def is_do_not_delete_diary_ref(settle):
    '''According to SPR 269722 and SPR 272403 settlement 
    with diary ref should not be deleted.'''
    if settle and settle.paynbr and has_the_keyword(settle) and \
    not is_in_pre_settlement_status(settle):        
        pr = "Settlement %d refers to a Payment via the diary, it can not be removed." % (settle.seqnbr)
        log(2, pr)
        return 1
    return 0   

def is_deposit_and_openEnded(trade, cf, create = 0):
    if create:
        return False
    if cf and cf.type in ['Call Float Rate', 'Call Fixed Rate', 'Call Fixed Rate Adjustable']:
        if trade and trade.insaddr.instype == 'Deposit' and \
        trade.insaddr.open_end == 'Open End':
            i = trade.insaddr
            legs = i.legs()
            for l in legs:
                if l.type in ['Call Fixed Adjustable', 'Call Fixed', 'Call Float']:
                    if l.reinvest == 0:
                        return False
                    else:
                        return True
    ret = False
    ct = ['Redemption Amount', 'Fixed Rate', 'Float Rate']
    if trade and cf:
        if trade.insaddr.instype == 'Deposit' and \
        trade.insaddr.open_end == 'Open End' and (cf.type in ct):
            ret = True
    return ret

def get_create(cashflow, instrument, leg_c=None):
    '''instrument can be ins_c, cashflow can be cf_c '''
    
    leg = cashflow.legnbr
    if leg_c:
        leg = leg_c
    
    if leg and instrument:
        if instrument.instype == 'Deposit' and \
        instrument.open_end == 'Open End' and \
        (leg.type in ['Call Fixed', 'Call Float', 'Call Fixed Adjustable']):
            return True
    return False

def get_paymentnbr_from_keyword(settlement):
    keyword = keyw
    if has_the_keyword(settlement):
        text = settlement.diary.get_text()
        dateTime = text.split('<DateTime>')
        dateTime.reverse()
        for dt in dateTime:
            found = dt.find(keyword)
            if found != -1:
                s =  dt[found:]
                s_sub1 = s.find("=")+1
                s_sub2 = s.find(" ")+1
                if s_sub2:
                    return int(s[s_sub1:s_sub2])
                else:
                    return int(s[s_sub1:])
    return -1


def get_payamount_from_keyword(settlement):
    paynbr = get_paymentnbr_from_keyword(settlement)
    if paynbr != -1:
        p = ael.Payment[paynbr]
        if p:
            return (True, p.amount)
    return (False, 0)


def equal_add_payments(p1, p2):
    ''' '''     
    return create_list_payment(p1) == create_list_payment(p2)
    
    
def create_list_payment(p): 
    ''' '''
    return [p.record_type, p.ptynbr, p.type, p.payday, p.amount, p.curr, \
    p.accnbr, p.archive_status, p.original_curr, p.fx_transaction, \
    p.our_accnbr, p.valid_from]


def has_modified_pay_when_correct_trade(tr):
    '''  
    For more information see SPR 269722 and SPR 272403.
    Before saving a new correct trade do not edit existing additional payments! 
    After saving the correct trade (Save new button) it is ok to edit payments 
    since reference in the diary than exists.
    
    This function can be used from FValidation in order to prohibit
    users from correcting the trade and at the same time modify additional payment.
    If new correcting trade has modified payment True is returned otherwise False.
    Here is the suggestion how the code in FValidation should call this function:
    
    import FSettlementGeneral3
    def validate_transaction(transaction_list):
        for (entity, operation) in transaction_list:
            if entity.record_type == "Trade" and operation == "Insert":            
                if FSettlementGeneral3.has_modified_pay_when_correct_trade(entity):
                    raise ""
    return transaction_list
    
    ''' 
    eq = []
    corrected_trade = tr.correction_trdnbr        
    ret = 0
    if not FSettlementGeneral2.is_correction_trade(tr):
        return ret
    
    if not corrected_trade:
        return ret
            
    closed_setls = get_closed_payments(corrected_trade)
    if not len(closed_setls):
        return ret
    #Payment that have closed settlement should exist in the new correction trade        
    closed_pays = []
    for settl in closed_setls:
        if settl.paynbr:
            if settl.paynbr not in closed_pays:
                closed_pays.append(settl.paynbr)
            
    for old_pay in closed_pays:
        po = create_list_payment(old_pay)    
        for pay in tr.payments():
            p = create_list_payment(pay)
            if po == p and (old_pay not in eq):
                eq.append(old_pay)
                break
    ret = not(len(eq) == len(closed_pays))
    if ret:             
        log(1, "==========================================")
        w = "Before saving a new correct trade do NOT do"
        log(1, w)
        w = "anything with additional payments, it can impact "
        log(1, w)
        w = "settlement amount! After saving the correct trade "
        log(1, w)
        w = "it is ok to edit payments since the reference in "
        log(1, w)
        w = "the Settlement diary towards the closed settlement than exists."
        log(1, w)
        log(1, "=========================================")
        
    return ret


def get_closed_payments(tr):
    '''Returns a list with closed settlements
    belonging to some additional payment.'''
    ret = []
    sel = ael.Settlement.select('trdnbr=%d' % tr.trdnbr)
    for s in sel:
        if s.paynbr and get_closed_settlement([s], 0):
            ret.append(s)
            pr = "Trade:%d has Additional Payment:%d (amount=%d) that has closed Settlement:%d (amount=%d)" % (s.paynbr.trdnbr.trdnbr, s.paynbr.paynbr, s.paynbr.amount, s.seqnbr, s.amount)
            log(1, pr)

    return ret

    
def has_closed_payments(tr):
    '''Returns True if the trade has closed settlements
    belonging to some additional payment. '''
    
    setls = get_closed_payments(tr)
    if len(setls):
        return 1
    else:
        return 0
       
def is_equity_swap(instrument):
    ret = False
    if instrument.instype == 'EquitySwap':
        ret =True
    return ret
   
def is_combination_with_dividend(instrument):
    ret = False
    if instrument.instype == 'Combination':
        links = instrument.combination_links()
        for link in links:
            ins = FSettlementGeneral.get_combination_member(link)
            if ins and ins.instype in ['EquitySwap', 'Stock']:
                ret = True
                break
    return ret

def version_not_ok(obj, ent, event= '', mode=0):
    '''Compares if amb obj version is higher then entity version.
    If returned value is not zero then version diff exists.'''
    ret = 0
              
    if obj.mbf_find_object('VERSION_ID') and event != '-':
        if not ent:
            pr = "version_not_ok: %s does not exist" % FSettlementGeneral.get_version_entity(mode)
            log(0, pr)
            return mode
        ver_amb = int(obj.mbf_find_object('VERSION_ID').mbf_get_value())
        ver_ent = int(ent.version_id)
        if ver_amb > ver_ent:
            pr = "version_not_ok: amb_msg:%s %s:%s" % (ver_amb, ent.record_type, ver_ent)
            log(0, pr)
            ret = mode
    return ret
    
def my_getattr(ent, attr = '', ent_c = None):
    '''Returns the attribute of the entity class otherwise from the real entity.
    Please note, this function is for an attribute, if you want to be sure that
    you use ent_c use function set_c instead.'''    
    
    if ent_c:
        return getattr(ent_c, attr)
    else:
        return getattr(ent, attr)
    
def convert_to(ael_value, amb_string, column_name = '', record_type= '', virt=[]):
    '''amb_string will be formatted according to the column type. 
    amb_string as unique key will result in ael_entity.'''
    ael_irregular = [0, None] # current entity may not give accurate type
    amb_irregular = ['0', 'None', '1/1/0000', '00-01-01', '000101', '01.01.00', '0000-01-01', '01/01/00', '00000101']
    ok_irreg_cols = ['read_time']
    yes_no_bool = ['manual_match', 'reinvest', 'primary_issuance', 'post_settle_action'] # represented as No in amb message when 0
    ok_str_zero = ['acquirer_accname', 'acquirer_account', 'party_accname', 'party_account']
    manual = 0
    ret = amb_string 
    typ = type(ael_value)
    rt = ''
    if typ == ael.ael_entity:
        rt = ael_value.record_type    
    virtual = 0
    if (ael_value in ael_irregular) and (amb_string not in amb_irregular):#dangerous
        if not len(virt) and column_name not in ok_irreg_cols and column_name not in yes_no_bool:
            virt = get_virtuals(record_type)
            
        for rec in virt:
            ael_value2 = getattr(rec, column_name)
            if ael_value2 not in ael_irregular:
                typ = type(ael_value2)
                if typ == ael.ael_entity:
                    rt = ael_value2.record_type
                break

    if typ == str:
        return ret # if type is str return it
    elif typ == int:
        if column_name in ok_irreg_cols and amb_string not in ['0']:
            # ugly way but how to convert read_time 1/5/2007 02:48:22 PM (getatt=1160118016)
            ret = ael.date_from_time(ael_value) 
        elif column_name in yes_no_bool:
            if amb_string == 'Yes':
                ret = 1
            else:
                ret = 0        
        else:
            ret = int(amb_string)
            
    elif typ == float:
        ret = float(amb_string)
    elif typ == long:
        ret = long(amb_string)
    elif typ == ael.ael_entity:
        ret = 0        
        key = int(amb_string)
        # represent bellow all possible entity links
        if rt == 'Settlement':
            ret = ael.Settlement[key]
        elif rt == 'Trade':
            ret = ael.Trade[key]
        elif rt == 'Instrument':
            ret = ael.Instrument[key]
        elif rt == 'CashFlow':
            ret = ael.CashFlow[key]
        elif rt == 'Party':
            ret = ael.Party[key]
        elif rt == 'Payment':
            ret = ael.Payment[key]        
        elif rt == 'Portfolio':
            ret = ael.Portfolio[key]
        elif rt == 'User':
            ret = ael.User[key]
        elif rt == 'Account':
            ret = ael.Account[key]
        elif rt == 'Dividend':
            ret = ael.Dividend[key]
        elif rt == 'Leg':
            ret = ael.Leg[key]
        elif rt == 'Reset':
            ret = ael.Reset[key]           
        elif rt == 'Calendar':
            ret = ael.Calendar[key]   
        elif rt == 'NettingRule':
            ret = ael.NettingRule[key]
        elif rt == 'TextObject':
            ret = ael.TextObject[key]
        elif rt == 'User':
            ret = ael.User[key]
        elif rt == 'InstrAliasType':
            ret = ael.InstrAliasType[key]
        else:
            pr = "Error: Unsupported record_type: %s, convert_to will return %s \
            as 0 (ael_value %s)" % (rt, column_name, amb_string)
            log(0, pr)                    
    elif typ == ael.ael_date:
        try:
            ret = ael.date(amb_string)
        except TypeError, err:
            pr = "Error: TypeError. Could not create ael.date from amb_string \'%s\'" % amb_string
            log(0, pr)
            ret = None
            
    elif typ in [type(None)]:
        if amb_string in amb_irregular:
            ret = None
        else:    
            pr = "Error: Unsupported type: %s, convert_to will return %s\
            as string" % (type, column_name)
            log(0, pr)
            ret = amb_string
    elif typ in [type]:            
        1 #it should return amb_string
    else:
        pr = "Error: ael returned type %s, convert_to will return %s\
        as ael value" % (type, column_name)
        log(0, pr)
        ret = ael_value
    
    if (typ != type(ret)) and (not virtual) and (column_name not in ok_irreg_cols):    
        pr = "convert_to: %s.%s types differ %s != %s (Error)" % (record_type,\
        column_name, str(typ), str(type(ret)))
        log(1, pr)
        if ael_value != ret:
            pr = "conver_to: Values also differ (Error)"
            log(1, pr)
    
    return ret


def set_c2(ent_c, ent, entity_type, version_not_ok):
    '''Set class.
    i.e. Trade class must be trade entity if the trade class is None. '''
    if not ent_c:
        if not ent and version_not_ok:
            gve = FSettlementGeneral.get_version_entity(version_not_ok)
            if FSettlementGeneral.print_set_c(gve, entity_type):
                pr = "set_c(%s event) about to return None no ael/class entity found (Error)" % (gve)
                log(2, pr)
        elif ent:
            gve = FSettlementGeneral.get_version_entity(version_not_ok)
            if version_not_ok and FSettlementGeneral.print_set_c(gve, ent.record_type):
                pr = "set_c(%s event) Entity class will not be used but ael %s (Error)" % (gve, ent.record_type)
                log(1, pr)
            return ent
    return ent_c
    

def log_trace():
    ''' '''
    import inspect
    s = inspect.stack()[1]
    trace_level = 4
    if trace_level == 1:
        print s[3]
    elif trace_level == 2:
        print s[3], inspect.getargvalues(s[0])[3]
    elif trace_level == 3:
        print 'File "'+s[1]+'", line '+str(s[2])+', in '+s[3]+', args:'
    elif trace_level == 4:
        print 'File "'+s[1]+'", line '+str(s[2])+', in '+s[3]+', args:',
        print inspect.getargvalues(s[0])[3]


def amb_get_cf_from_leg(leg_dict={}, tr=None, is_coupon=1):
    '''Returns cf_c from leg dictionary. CashFlows are filtered based on is_coupon. '''
    ret = []
    if not len(leg_dict.keys()):
        log(1, "amb_get_cf_from_leg: no legs deployed, no cf will be returned (File)")
    for prefix in leg_dict.keys():
        prfx_list = leg_dict[prefix]
        for legObj in prfx_list:                        
            cf_dict = FSettlementAMB.get_dict_from_MBF(legObj, 'CASHFLOW')
            legnbr = legObj.mbf_find_object('LEGNBR')
            leg_c = None
            if legnbr:
                leg_ent = ael.Leg[int(legnbr.mbf_get_value())]
                leg_c = get_entity_class(legObj, leg_fields, leg_ent, 'Leg')
                
                for prfx in cf_dict.keys():
                    event_list = cf_dict[prfx]
                    for mbfCF in event_list:
                        cfwnbr = mbfCF.mbf_find_object('CFWNBR')
                        if cfwnbr:
                            cf_ent = ael.CashFlow[int(cfwnbr.mbf_get_value())]
                            cf_c = get_entity_class(mbfCF, cf_fields.keys(), cf_ent, 'CashFlow')
                            if is_coupon and FSettlementGeneral.is_coupon(tr, cf_ent, tr, cf_c, leg_c):
                                if cf_c not in ret:
                                    ret.append(cf_c)
                            else:
                                if cf_c not in ret:
                                    ret.append(cf_c)
    return ret

def get_virtuals(record_type):
    ''' '''    
    return getattr(ael, record_type).select()

def get_entity_class(amb, fields = [], ent = None, record_type = '', version_ok = 1):
    '''Create entity class from amb_msg.
    If ent is not deployed virtual entity is used to fetch columns.
    '''
    amb_dict = {}
    virt = []
    virtual = 0
    if ent:
        record_type = ent.record_type
        
    if not ent:
        pr = "get_entity_clas: parameter ent is None, virtual %s record will be used" % (record_type)
        log(4, pr)       
        virt = get_virtuals(record_type)
        if len(virt):
            ent = virt[0]
            virtual = 1 
        else:            
            log(1, "get_entity_clas: could not found virtual %s record" % (record_type))    
        
    tmp_list = fields    
    if record_type == 'Settlement':
        for f in settl_fields2:
            if f not in tmp_list:
                tmp_list.append(f)
    elif record_type == 'Trade':
        for f in tr_fields2:
            if f not in tmp_list:
                tmp_list.append(f)
    elif record_type == 'CashFlow':
        for f in cf_fields2:
            if f not in tmp_list:
                tmp_list.append(f)
    elif record_type == 'Payment':
        for f in pay_fields2:
            if f not in tmp_list:
                tmp_list.append(f)
    elif record_type == 'Reset':
        for f in reset_fields2:
            if f not in tmp_list:
                tmp_list.append(f)
    elif record_type == 'Dividend':
        for f in div_fields2:
            if f not in tmp_list:
                tmp_list.append(f)                
    elif record_type == 'Account':
        for f in acc_fields2:
            if f not in tmp_list:
                tmp_list.append(f) 
                        
    for attr in tmp_list:
        # some fields with dots are not to be put in the class
        # threre must be other fields without dots
        if attr.find(".") == -1:
            amb_field = amb.mbf_find_object(attr)
            if amb_field:
                column_name = attr.lower()
                v = amb_field.mbf_get_value()
                amb_dict[column_name] = convert_to(getattr(ent, column_name), v, column_name, record_type, virt)

    if record_type == 'Settlement':
        ent_c = Settlement(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    if record_type == 'Trade':
        ent_c = Trade(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'Instrument':
        ent_c = Instrument(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'CashFlow':
        ent_c = CashFlow(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'Payment':
        ent_c = Payment(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'Leg':
        ent_c = Leg(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'Reset':
        ent_c = Reset(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c        
    elif ent.record_type == 'Dividend':
        ent_c = Dividend(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif record_type == 'CombinationLink':
        ent_c = CombinationLink(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif ent.record_type == 'Account':
        ent_c = Account(**amb_dict)
        log(5, ent_c.__str__())
        return ent_c
    elif virtual:
        pr = "get_entity_class: no class implemented! None will be returned, virtual=1 (Error)" % (record_type)
        log(0, pr)
        return None
    else:
        pr = "get_entity_class: no class implemented! %s-entity will be returned (Error)" % (record_type)
        log(0, pr)
        return ent


def is_entity_class(s):
    '''s can be both Settlement entity and entity class. 
    This function returns 1 if s is entity class and 
    0 if s is Settlement ael entity. '''
    try:
        return s.is_entity_class()
    except Exception, e:
        return 0

def get_settlements_from_entity(ent):
    '''Instead of reference_in '''
    setls = []
    if ent:
        if ent.record_type == 'CashFlow':
            setls = ael.Settlement.select('cfwnbr = %d' % ent.cfwnbr ) 
        elif ent.record_type == 'Dividend':
            setls = ael.Settlement.select('dividend_seqnbr = %d' % ent.seqnbr) 
        elif ent.record_type == 'Payment':
            setls = ael.Settlement.select('paynbr = %d' % ent.paynbr) 
    return setls


def create_call_fixed_float(inst, leg_c):
    ''' '''
    ret = False
    if inst and leg_c:
        if inst.instype == 'Deposit' and inst.open_end == 'Open End':
            if (leg_c.type in ['Call Fixed', 'Call Float', 'Call Fixed Adjustable']) and leg_c.reinvest == 0:
                ret = True
    return ret

def get_call_fixed_float_cf(inst, cf_c):
    pay_day = cf_c.pay_day
    if not pay_day:
        return []
    cf_list = []
    if inst:
        cfs = inst.cash_flows() #inst is ael-entity. OK?
        for cf in cfs:
            if cf.type in ['Call Float Rate', 'Call Fixed Rate', 'Call Fixed Rate Adjustable'] and \
            cf.start_day <= pay_day and cf.end_day > pay_day:
                cf_list.append(cf)
    return cf_list
def create_or_update_call_fixed(inst, cf_c, create, cfw):
    newEnt_list = get_call_fixed_float_cf(inst, cf_c)
    for cf in newEnt_list:
        try:
            cf_settle = ael.Settlement.select('cfwnbr = %d' % cf.cfwnbr)[0]
            s_clone = cf_settle.clone()
            s_clone.amount = cf.projected_cf()
            FSettlementGeneral.append_settle(s_clone)
        except Exception, e:
            FSettlementGeneralRT.create_cf(cf, None, None, create, None)
            
def set_pay_days(leg, reinv_dict, cfa_dict):
    cfs = ael.CashFlow.select('legnbr = %d' % leg.legnbr)
    for cf in cfs:
        if cf.type in ['Call Fixed Rate Adjustable', 'Call Fixed Rate', 'Call Float Rate']:
            cfa_dict[cf.pay_day.to_string()] = cf
        elif cf.type == 'Interest Reinvestment':
            if reinv_dict.has_key(cf.pay_day.to_string()):
                reinv_dict[cf.pay_day.to_string()].append(cf)
            else:
                reinv_dict[cf.pay_day.to_string()] = [cf]

def get_cfs_to_create(reinv_dict, cfa_dict):
    cfs_to_be_created = []
    checked_dates = []
    for k, v in reinv_dict.items():
        checked_dates.append(k)
        reinv_sum = 0.0
        cfa_sum = 0.0
        for cf in v:
            reinv_sum = reinv_sum + cf.projected_cf()
        try:
            cfa_cf = cfa_dict[k]
            cfa_sum = cfa_cf.projected_cf()
            if (round(cfa_sum, 3) + round(reinv_sum, 3)) != 0.000:
                cfs_to_be_created.append(cfa_cf)
                for cf in v:
                    cfs_to_be_created.append(cf)
        except KeyError, e:
            pr = 'No Call Fixed Adjustable cashflow exist for date %s' % k
            log(1, pr)
            for cf in v:
                cfs_to_be_created.append(cf)
    for k, v in cfa_dict.items():
        if k not in checked_dates:
            cfs_to_be_created.append(v)
    return cfs_to_be_created

def create_cf_for_call_dep(cf_c, tr):
    if tr:
        i = tr.insaddr
        if i.instype != 'Deposit':
            return True
        legs = i.legs()
        has_cfa_leg = False #check if instrument has Call Fixed Adjustable, Call Fixed, Call Float leg
        input_leg = None
        for l in legs:
            input_leg = l
            if l.type in ['Call Fixed Adjustable', 'Call Fixed', 'Call Float'] and l.reinvest == 1:
                has_cfa_leg = True
                break
        if not has_cfa_leg:
            return True
        
        pay_days_intr_reinv = {}
        pay_days_cfa = {}
        set_pay_days(input_leg, pay_days_intr_reinv, pay_days_cfa)
        cfs_to_be_created = get_cfs_to_create(pay_days_intr_reinv, pay_days_cfa)
        for csh in FSettlementGeneralRT.cfs_from_tr(tr):
            if csh.type not in ['Call Fixed Rate Adjustable', 'Interest Reinvestment', 'Call Fixed Rate', 'Call Float Rate']:
                cfs_to_be_created.append(csh)
        cf = ael.CashFlow[cf_c.cfwnbr] #ok?
        if cf in cfs_to_be_created:
            return True
        else:
            return False
            
def is_in_pre_settlement_status(settle):
    ret = False
    if settle.status in pre_settlement_status:
        ret = True
    return ret

def is_updatable(s): #s is a settlement record
    if s.status not in ['Void', 'Updated']:
        return True
    
    message = None
    closed = False
    
    adjusted = FSettlementGeneral2.find_adjusted(s.seqnbr)
    if adjusted:
        if adjusted.status not in ['Void', 'Closed']:
            return True
        if adjusted.status == 'Closed':
            closed = True
        message = 'Adjusted hierarchy: Settlement %d is not updatable due to settlement %d in status %s' % (s.seqnbr, adjusted.seqnbr, adjusted.status)
    
    if s.ref_type and s.ref_type == 'Split':
        do_return = True
        ss = ael.Settlement.select('ref_seqnbr = %d' % s.seqnbr)
        for settle in ss:
            if settle.ref_type == 'Split Part' and settle.status in ['Void', 'Closed']:
                do_return = False
                message = 'Split hierarchy: Settlement %d is not updatable due to settlement %d in status %s' % (s.seqnbr, settle.seqnbr, settle.status)
                if settle.status == 'Closed':
                    closed = True
                    break
        if do_return:
            return True
    
    if s.ref_type and s.ref_seqnbr and s.ref_type == 'Net Part':
        parent = ael.Settlement[s.ref_seqnbr.seqnbr]
        if parent:
            if parent.status not in ['Void', 'Closed']:
                return True
            if parent.status == 'Closed':
                closed = True
            message = 'Netted hierarchy: Settlement %d is not updatable due to settlement %d in status %s' % (s.seqnbr, parent.seqnbr, parent.status)
    
    ret = True
    if closed:
        ret = False
        log(2, message)
    elif s.status == 'Updated':
        ret = True
    elif s.status == 'Void' and not param.update_void:
        if not message:
            message = 'Settlement %d is not updatable due to status %s' % (s.seqnbr, s.status)
        log(2, message)
        ret = False
    return ret
    
def is_in_update_status(s): #s is a settlement record
    l = ['Hold', 'Void']
    return s.status in l or s.status in FSettlementGeneral2.D_status

def check_otc_handling(t):
    """Input t is a trade. This function checks if settlement records 
    shall be created according to variable special_otc_instrument_handling in
    FSettlementvariables. Returns True if settlement records shall be created.
    Returns False otherwise."""
    
    otc = t.insaddr.otc
    ret = False
    soih = param.special_otc_instrument_handling
    
    if not soih or soih not in [1, 2]: 
        ret = True
    
    if (otc and soih == 1) or (not otc and soih == 2):
        ret = True
        
    if not ret:
        log(3, 'Settlement records will not be created for trade %d.' % t.trdnbr)
        log(3, 'Check setting of variable special_otc_instrument_handling in FSettlementVariables.')
    
    return ret
    
def div_dict_has_values(div_dict):
    """div_dict is a dictionary with keys represented by the strings '!', '+', '-'.
    Each key points to a list. This function returns False if all lists are empty."""
    
    ret = False
    for key in div_dict.keys():
        if len(div_dict[key]) > 0:
            ret = True
            break
    return ret

def is_netted_trade(trade):
    """
    Returns true if trade has netted settlement records.
    """
    ret = False
    if FSettlementGeneralRT.is_trade(trade):
        settlements = ael.Settlement.select('trdnbr = %d' % trade.trdnbr)
        for s in settlements:
            if s.ref_type == 'Net Part' or \
            s.ref_type == 'Net' or \
            s.ref_type == 'Ad_hoc Net':
                ret = True
    return ret


#-----Functions for cash-settled Future/Forwards in EOD-script begin!------------

def is_future_forward_and_otc(trade):
    i = trade.insaddr
    ret = False
    if i.instype in ['Future/Forward', 'VarianceSwap'] and i.otc:
        ret = True
    return ret
    
def get_value_day(trade, case):

    if case == 2 and not param.forward_early_termination: #closing trade
        return trade.value_day
        
    i = trade.insaddr
    spot_days = i.spot_banking_days_offset
    curr = i.curr
    date = i.exp_day.add_banking_day(curr, spot_days)
    date_curr_cal = date.adjust_to_banking_day(curr, 'Mod. Following') 
    settle_calnbr = i.settle_calnbr
    if settle_calnbr:
        date_settle_cal = date.adjust_to_banking_day(settle_calnbr, 'Mod. Following')
        if date_curr_cal.to_time() >= date_settle_cal.to_time():
            return date_curr_cal
        else:
            return date_settle_cal
    else:
        return date_curr_cal
        
def settle_exists(trade):
    return FSettlementGeneral.settle_exists(trade)

def exp_day_today(trade):
    i = trade.insaddr
    today = ael.date_today()
    if i.exp_day == today:
        if i.exp_time > time.time():
            return False
        else:
            if not settle_exists(trade): 
                return True
            return False
    if i.exp_day == today.add_banking_day(i, -1) and not \
    settle_exists(trade):
        return True
    else:
        return False

def set_amount(t, settle, case = 1, ref_tr = None, closing_trs = None):
    i = t.insaddr
    if case == 1:
        nominal = t.nominal_amount()
        settle.amount = nominal * (i.mtm_price(i.exp_day) - t.price )
    elif case == 2:
        t_nominal = t.nominal_amount()
        if param.forward_early_termination and \
           t.insaddr.settlement != 'Physical Delivery':
            settle.amount = t_nominal * (i.mtm_price(i.exp_day) - t.price)
        else:
            settle.amount = t_nominal * (ref_tr.price - t.price)
    elif case == 3:
        close_nom = 0.0
        if not param.forward_early_termination:
            for c_t in closing_trs:
                if c_t.status in FSettlementVariables.status:
                    close_nom = close_nom + c_t.nominal_amount()
        t_nominal = t.nominal_amount()
        nominal = t_nominal + close_nom
        settle.amount = nominal * (i.mtm_price(i.exp_day) - t.price)
        
def create_payout_settlement(t, case = 1, ref_tr = None, tr_l = None):
    i = t.insaddr
    s = ael.Settlement.new()
    s.trdnbr = t.trdnbr
    set_amount(t, s, case, ref_tr, tr_l)
    s.curr = i.curr
    s.value_day = get_value_day(t, case)
    s.status = 'New'
    s.type = 'Payout'
    s.party_ptyid = t.counterparty_ptynbr.ptyid
    s.acquirer_ptyid = t.acquirer_ptynbr.ptyid
    if t.prfnbr:
        if s.amount > 0:
            s.to_prfnbr = t.prfnbr.prfnbr
        else:
            s.from_prfnbr = t.prfnbr.prfnbr
    FSettlementGeneral.account_info(t, s, 0)
    return s
    
def create_new(trade, update = 0):
    s = None
    if trade.status in FSettlementVariables.status:
        if FSettlementGeneral2.is_closing(trade):
            closed_tr = ael.Trade[trade.contract_trdnbr]
            s = create_payout_settlement(trade, 2, closed_tr)
        elif FSettlementGeneral2.is_closed(trade):
            if trade.insaddr.settlement != 'Physical Delivery':
                closing_trs = FSettlementGeneral2.get_closing_trades(trade.trdnbr)
                s = create_payout_settlement(trade, 3, None, closing_trs)
        else:
            if trade.insaddr.settlement != 'Physical Delivery':
                s = create_payout_settlement(trade)
    if s and s.amount != 0.0 and not update and FSettlementGeneral.paydayOK(s.value_day, trade, 1, 'Payout'):
        FSettlementGeneral.append_transaction(s)
        return (None, 1)   
    else:
        return (s, 1)

def create_settle_future_forward(trade):
    new_s = None
    old_s = None
    if is_future_forward_and_otc(trade) and trade.status in \
    FSettlementVariables.status:
        if FSettlementGeneral2.is_closing(trade):
            old_s = settle_exists(trade)
            if old_s:
                closed_tr = ael.Trade[trade.contract_trdnbr]
                new_s = create_payout_settlement(trade, 2, closed_tr)
            elif (not param.forward_early_termination) or \
               (param.forward_early_termination and exp_day_today(trade)):
                closed_tr = ael.Trade[trade.contract_trdnbr]
                new_s = create_payout_settlement(trade, 2, closed_tr)
        elif FSettlementGeneral2.is_closed(trade):
            old_s = settle_exists(trade)
            if old_s:
                closing_trs = FSettlementGeneral2.get_closing_trades(trade.trdnbr)
                new_s = create_payout_settlement(trade, 3, None, closing_trs)
            else:
                if exp_day_today(trade) and trade.insaddr.settlement != 'Physical Delivery':
                    closing_trs = FSettlementGeneral2.get_closing_trades(trade.trdnbr)
                    new_s = create_payout_settlement(trade, 3, None, closing_trs)
        else:
            old_s = settle_exists(trade)
            if old_s:
                new_s = create_payout_settlement(trade)
            else:
                if exp_day_today(trade) and trade.insaddr.settlement != 'Physical Delivery':
                    new_s = create_payout_settlement(trade)
    if new_s and FSettlementGeneral.paydayOK(new_s.value_day, trade, 1, 'Payout'):
        if old_s:
            if old_s.status not in FSettlementGeneralRT.noupdate_stl_status and is_updatable(old_s):
                if (not old_s.ref_seqnbr or (old_s.ref_seqnbr and old_s.ref_type in ['Net Part', 'None'])) \
                and FUpdateFutureForward.is_updated(old_s, new_s):
                    if new_s.amount != 0.0:
                        FSettlementGeneralRT.update_setl_row(old_s, new_s, 'Updated')
                    else:
                        FSettlementGeneralRT.update_setl_row(old_s, new_s, 'Recalled')
        else:
            if new_s.amount != 0.0:
                FSettlementGeneral.append_transaction(new_s)
                
#-----Functions for cash-settled Future/Forwards in EOD-script end!------------


