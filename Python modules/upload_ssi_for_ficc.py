"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    upload_ssi_for_ficc.

DESCRIPTION
    This module contains a temporary AEL main script used for the setup
    of FICC party data.

    PLEASE NOTE: This script is intended to be manually deleted after
    execution.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2018-10-11      FAOPS-42       Sadanand Upase           Rayan Govender         Initial Implementation
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import acm
import os
import datetime
import re
from at_ael_variables import AelVariableHandler
from at_logging import getLogger
from SAGEN_Add_SSI_ASQLQuery import main
import traceback
import sys

LOGGER = getLogger(__name__)

ssi_types_vs_payment = {'Delivery versus Payment':['<NOT>Free of payment'], 'Security':[]}


def _create_ael_variable_handler():
    """
    Create an AelVariableHandler for this script.
    """
    ael_variable_handler = AelVariableHandler()
    # Input File Path.
    ael_variable_handler.add_input_file(
        name='input_file_path',
        label='Input File Path',
        file_filter='*.xlsx',
        mandatory=True,
        multiple=False,
        alt='The file path of the input party data excel file.'
    )
    ael_variable_handler.add_bool('deploy_or_rollback',
                       label='Rollback',
                       default=False,
                       alt='Rollback: Disable SSIs created as part of the upload')
    return ael_variable_handler


ael_variables = _create_ael_variable_handler()

def ael_main(ael_parameters):
    """
    AEL Main Function.
    """
    try:
        start_date_time = datetime.datetime.today()
        LOGGER.info('Starting at {start_date_time}'.format(start_date_time=start_date_time))
        input_file_path = ael_parameters['input_file_path'].AsString()
        _validate_input_file_path(input_file_path)
        perform_rollback = ael_parameters['deploy_or_rollback']

	newline = '\n'
	seperator = ','
	path = ael_parameters['input_file_path']
        accounts_created_on_parties = {}
        ssis_created_on_parties = {}
        
	data = []
	with open(str(path), "r") as file:
            for line in file:
                print line.strip(newline)
                line = line.strip(newline)
                data.append(line.split(seperator))
	for line in data[1:]:
            update_main(line, accounts_created_on_parties, ssis_created_on_parties, perform_rollback)

        '''if accounts_created_on_parties:
            LOGGER.info("Created following accounts:")
            LOGGER.info(str(accounts_created_on_parties))
            #for each_party, accounts in accounts_created_on_parties.iteritems():
            #    LOGGER.info("%s : %s" % (str(each_party), str(accounts)))
        if ssis_created_on_parties:
            LOGGER.info("Created following SSIs:")
            LOGGER.info(str(ssis_created_on_parties))
            #for each_party, ssis in ssis_created_on_parties.iteritems():
            #    LOGGER.info("%s : %s" % (str(each_party), str(ssis)))'''
        end_date_time = datetime.datetime.today()
        LOGGER.info('Completed successfully at {end_date_time}'.format(end_date_time=end_date_time))
        duration = end_date_time - start_date_time
        LOGGER.info('Duration: {duration}'.format(duration=duration))
    except Exception as exception:
        exc_type, exc_value, exc_traceback = sys.exc_info()
        traceback.print_tb(exc_traceback, limit=1, file=sys.stdout)
        LOGGER.error('Exception: %s' % str(exception))

def _validate_input_file_path(input_file_path):
    """
    Validate the input file path.
    """
    if not os.path.exists(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not exist."
        raise ValueError(exception_message.format(
            input_file_path=input_file_path
        ))
    if not os.path.isfile(input_file_path):
        exception_message = "The specified input file path '{input_file_path}' "
        exception_message += "does not point to a file."
        raise ValueError(exception_message.format(
            input_file_path=input_file_path
        ))


def _create_ssi_name(party_name, intermediary2_name, correspondent_bank_acc_number, intermediary2_acc_number, ssi_type):
    acc_number = intermediary2_acc_number if intermediary2_acc_number else correspondent_bank_acc_number
    if ssi_type == 'Security':
        ssi_code = 'SEC'
    elif ssi_type == 'Delivery versus Payment':
        ssi_code = 'DVP'
    return '/'.join([party_name[:4], intermediary2_name[:4], acc_number, ssi_code])

def _check_account(party_oid, account_number, acc_corr_bank, account_number_corr_bank3=None, acc_corr_bank3=None):
    #print party_oid, account_number, acc_corr_bank
    acc = acm.FAccount.Select("party = %i and account = '%s' and correspondentBank = '%s' and account3= '%s' and correspondentBank3 = '%s'" % (party_oid, account_number, acc_corr_bank, account_number_corr_bank3, acc_corr_bank3))
    return acc

def _create_account(party, curr, account_number, acc_corr_bank, corr_cp_code, corr_bank_dss, account_number_corr_bank2, acc_corr_bank2, corr_cp_code2, corr_bank2_dss, account_number_corr_bank3, acc_corr_bank3, corr_cp_code3, corr_bank3_dss):
    party_swift_alias_map = {'BARCLAYS BANK PLC' : 'BARCGB22',
                                'BARCLAYS BANK PLC LONDON' :'BARCGB5G',
                                'MERRILL LYNCH INT' : 'MLMBIE2D',
                                'SOCIETE GENERALE PARIS' :  'SOGEFRPP',
                                'UBS AG' : 'UBSBCHZZ'}
    acmParty = acm.FParty[party]
    if not acmParty:
        LOGGER.error("Party %s not found. Aborting upload" % str(party))
        return
    corrbank = acm.FParty[acc_corr_bank]
    if not acmParty:
        LOGGER.error("Party %s not found. Aborting upload" % str(acc_corr_bank))
        return

    if party in party_swift_alias_map:
        try:
            corr_alias = acm.FPartyAlias.Select01("party =  %i and type = 'SWIFT' and alias = '%s'" % (corrbank.Oid(), corr_cp_code), "")
            party_alias = acm.FPartyAlias.Select01("party =  %i and type = 'SWIFT' and alias = '%s'" % (acmParty.Oid(), party_swift_alias_map[party]), "")
        except Exception, e:
            LOGGER.error(str(e))
            return
    else:
        try:
            corr_alias = acm.FPartyAlias.Select01("party =  %i and type = 'SWIFT' and alias = '%s'" % (corrbank.Oid(), corr_cp_code), "")
            party_alias = acm.FPartyAlias.Select01("party =  %i and type = 'SWIFT' and alias <> 'ZAGTZAJ0'" % (acmParty.Oid()), "")
        except Exception, e:
            LOGGER.error(str(e))
            return
        
    if corr_alias is None or party_alias is None:
        if corr_alias is None:
            LOGGER.error('Missing Correspondent Alias!!!') 
            LOGGER.error(str(party)) 
            LOGGER.error(str(corrbank.Name()) + ' ' + str(corr_cp_code))
            return
        else:
            LOGGER.error('Counterparty  %s has no Swift Alias...' % str(party))


    acc = _check_account(acmParty.Oid(), account_number, acc_corr_bank, account_number_corr_bank3, acc_corr_bank3)
    #print "party = %i and account = '%s' and correspondentBank = '%s'  " % ( pty.Oid(), acc_number, acc_corr_bank )
    if not acc:
        LOGGER.info('Creating account on %s...' % party)
        acc = acm.FAccount()
        acc.Name('SecAccount')
        acc.AccountType('Cash and Security')
        acc.NetworkAliasType('SWIFT')
        acc.NetworkAlias(party_alias)
        acc.CorrespondentBank(acc_corr_bank)
        acc.Bic(corr_alias)
        if corr_bank_dss:
            corr_bank_dss_alias = acm.FPartyAlias.Select01("party =  %i and type= 'DataSourceScheme' and alias = '%s'" % (corrbank.Oid(), corr_bank_dss), "")
            if  corr_bank_dss_alias:
                acc.DataSourceScheme(corr_bank_dss_alias)
        
        if acc_corr_bank2 and acc_corr_bank3:
            acc.CorrespondentBank2(acc_corr_bank2)
            acc.Account2(account_number_corr_bank2)
            corrbank = acm.FParty[acc_corr_bank2]
            corr_alias = acm.FPartyAlias.Select01("party =  %i and type= 'SWIFT' and alias = '%s'" % (corrbank.Oid(), corr_cp_code2), "")
            acc.Bic2(corr_alias)
            if corr_bank2_dss:
                corr_bank2_dss_alias = acm.FPartyAlias.Select01("party =  %i and type= 'DataSourceScheme' and alias = '%s'" % (corrbank.Oid(), corr_bank2_dss), "")
                if corr_bank2_dss_alias:
                    acc.DataSourceScheme2(corr_bank2_dss_alias)
            
            acc.CorrespondentBank3(acc_corr_bank3)
            acc.Account3(account_number_corr_bank3)
            corrbank = acm.FParty[acc_corr_bank3]
            corr_alias = acm.FPartyAlias.Select01("party =  %i and type= 'SWIFT' and alias = '%s'" % (corrbank.Oid(), corr_cp_code3), "")
            acc.Bic3(corr_alias)
            if corr_bank3_dss:
                corr_bank3_dss_alias = acm.FPartyAlias.Select01("party =  %i and type= 'DataSourceScheme' and alias = '%s'" % (corrbank.Oid(), corr_bank3_dss), "")
                if corr_bank3_dss_alias:
                    acc.DataSourceScheme3(corr_bank3_dss_alias)

            if corr_cp_code == 'DTCYUS33' and corr_cp_code3 == 'FRNYUS33':
                acc.DetailsOfCharges('Our')
        acc.Account(account_number)
        #checking if multiple currencies have been specified, if yes then create account with currency as blank i.e. ALL will be considered
        if ';' not in str(curr) :
            acc.Currency(curr)
        acc.Party(party)
        try:
            acc.Commit()
            LOGGER.info('Account %s created for party %s.' % (str(acc.Name()), str(party)))
            return acc.Name()
        except Exception, e:
            LOGGER.error('Cannot create account %s for party %s  : %s' % (str(account_number), str(party), str(e)))
    else:
        if type(list(acc)) == type([]):
            acc =acc[0]
        LOGGER.warn('Account already exists for party [%s] with account number [%s], Corr Bank [%s] and Bic [%s] ' % (party, acc.Account(), acc.CorrespondentBank().Name(), acc.Bic().Name() ))
        return acc.Name()

def _get_ssi_from(ssi_name, party):
    for party_ssi in party.SettleInstructions():
        if party_ssi.Name() == ssi_name:
            return party_ssi

def disable_ssi(party_name, ssi_name):
    party = acm.FParty[party_name]
    if party:
        for each_ssi in party.SettleInstructions():
            if each_ssi.Name() == ssi_name:
                try:
                    each_ssi.DefaultInstruction(False)
                    each_ssi.Commit()
                    LOGGER.info('Disabled SSI %s on party %s' % (each_ssi.Name(), party_name))
                    return
                except Exception, e:
                    LOGGER.error('Could not disable ssi %s on party %s' % (each_ssi.Name(), party_name))
                    LOGGER.error(str(e))
                    return

def update_main(data, accounts_created_on_parties, ssis_created_on_parties, perform_rollback):
    global account_created
    party = data[0]
    curr = data[1]
    account_number = data[2]
    acc_corr_bank = data[3]
    corr_cp_code = data[4]

    #Below fields are optional
    try:
        corr_bank_dss = data[5]
        account_number_corr_bank2 = data[6]
        acc_corr_bank2 = data[7]
        corr_cp_code2 = data[8]
        corr_bank2_dss = data[9]
        account_number_corr_bank3 = data[10]
        acc_corr_bank3 = data[11]
        corr_cp_code3 = data[12]
        corr_bank3_dss = data[13]
        is_default_ssi = data[14]
    except IndexError, e:
	LOGGER.error('Please provide all required data. %s' % str(e))
	return
        corr_bank_dss = ''
        account_number_corr_bank2 = ''
        acc_corr_bank2 = ''
        corr_cp_code2 = ''
        corr_bank2_dss = ''
        account_number_corr_bank3 = ''
        acc_corr_bank3 = ''
        corr_cp_code3 = ''
        corr_bank3_dss = ''
        is_default_ssi = ''

    if not perform_rollback:
        account_name = _create_account(party, curr, account_number, acc_corr_bank, corr_cp_code, corr_bank_dss, account_number_corr_bank2, acc_corr_bank2, corr_cp_code2, corr_bank2_dss, account_number_corr_bank3, acc_corr_bank3, corr_cp_code3, corr_bank3_dss)
        if account_name:
            print account_name
            accounts_created_on_parties.setdefault(party, []).append(account_name)
            #ptyid, ssiName, accType, overrideSSI, acquirer, instype, currency, tradesettlecat, inssettlecat, optkey1, cftype, account_name
            
            for ssi_type in ssi_types_vs_payment:
                ssi_name = _create_ssi_name(party, acc_corr_bank3, account_number, account_number_corr_bank3, ssi_type)
                try:
                    main(party,
                        ssi_name,
                        ssi_type,
                        False,
                        [],
                        ['Bill', 'Bond', 'FRN', 'Repo/Reverse'],
                        str(curr).split(';'),
                        ['Euroclear'],
                        [],
                        ssi_types_vs_payment[ssi_type],
                        ['Security Nominal', 'End Security'],
                        account_name)
                except Exception, e:
                    print e
                ssis_created_on_parties.setdefault(party, []).append(ssi_name)
                ssi = _get_ssi_from(ssi_name, acm.FParty[party])
                if is_default_ssi in ('True', 'TRUE', 'Yes', 'YES'):
                    ssi.DefaultInstruction(True)
                    ssi.Commit()
                else:
                    ssi.DefaultInstruction(False)
                    ssi.Commit()
        else:
            return
    else:
        for ssi_type in ssi_types_vs_payment:
            ssi_name = _create_ssi_name(party, acc_corr_bank3, account_number, account_number_corr_bank3, ssi_type)
            disable_ssi(party, ssi_name)
        

#********************************************************
