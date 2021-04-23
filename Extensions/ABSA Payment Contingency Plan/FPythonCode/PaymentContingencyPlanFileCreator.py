"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    PaymentContingencyPlanFileCreator

DESCRIPTION
    This module contains objects used for the creation of payment contingency plan
    files.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-03-23      FAOPS-681       Cuen Edwards            Linda Breytenbach       Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

import datetime
import os
import re

import acm
from FSettlementEnums import SettlementStatus
from FOperationsDocumentEnums import OperationsDocumentStatus

from at_logging import getLogger
import PaymentContingencyPlanGeneral


LOGGER = getLogger(__name__)


class PaymentContingencyPlanFileCreator(object):
    """
    An object responsible for the creation of payment contingency
    plan files.

    This class produces up to two files per acquirer:

    - CPS Payments File: This file contains payments that will be
      sent to CPS (Contingency Payments System) for automated
      processing.
    - Manual Payments File: This file contains payments that require
      manual processing due to likely rejection by CPS.
    """

    @classmethod
    def create_files(cls, output_directory_path):
        """
        Create any required payment contingency plan files.
        """
        message = "Creating payment contingency plan files for date "
        message += "today '{date_today}'..."
        date_today = acm.Time.DateToday()
        LOGGER.info(message.format(
            date_today=date_today
        ))
        settlements = PaymentContingencyPlanGeneral.get_settlements_to_send()
        number_of_settlements = len(settlements)
        if number_of_settlements > 0:
            LOGGER.info("Found {number_of_settlements} eligible settlements.".format(
                number_of_settlements=number_of_settlements
            ))
            cls._create_files_per_acquirer_and_processing_destination(output_directory_path, settlements)
        else:
            LOGGER.info("No eligible settlements found.".format(
                number_of_settlements=number_of_settlements
            ))
        LOGGER.info("Completed creating payment contingency plan files.")

    @classmethod
    def _create_files_per_acquirer_and_processing_destination(cls, output_directory_path, settlements):
        """
        Create payment contingency plan files per acquirer and
        processing destination for the specified settlements.
        """
        settlements_by_acquirer = cls._get_settlements_by_acquirer(settlements)
        for acquirer, acquirer_settlements in list(settlements_by_acquirer.items()):
            cls._create_acquirer_processing_destination_files(output_directory_path, acquirer, acquirer_settlements)

    @classmethod
    def _get_settlements_by_acquirer(cls, settlements):
        """
        Get settlements grouped by acquirer.
        """
        settlements_by_acquirer = dict()
        for settlement in settlements:
            acquirer = settlement.Acquirer()
            if acquirer not in list(settlements_by_acquirer.keys()):
                settlements_by_acquirer[acquirer] = list()
            settlements_by_acquirer[acquirer].append(settlement)
        return settlements_by_acquirer

    @classmethod
    def _create_acquirer_processing_destination_files(cls, output_directory_path, acquirer, acquirer_settlements):
        """
        Create payment contingency plan files per processing destination for
        the specified acquirer settlements.
        """
        manual_settlements = list()
        cps_settlements = list()
        for settlement in acquirer_settlements:
            if cls._requires_manual_processing(settlement):
                manual_settlements.append(settlement)
            else:
                cps_settlements.append(settlement)
        if len(manual_settlements) > 0:
            cls._create_acquirer_manual_payment_file(output_directory_path, acquirer, manual_settlements)
        if len(cps_settlements) > 0:
            cls._create_acquirer_cps_payment_file(output_directory_path, acquirer, cps_settlements)

    @classmethod
    def _create_acquirer_manual_payment_file(cls, output_directory_path, acquirer, manual_settlements):
        """
        Create a manual payment contingency plan file for the
        specified acquirer settlements.
        """
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        output_file_name = cls._get_output_file_name(acquirer, 'Manual', timestamp)
        message = "Creating payment contingency plan file '{output_file_name}' for acquirer '{acquirer_name}'..."
        message = message.format(
            output_file_name=output_file_name,
            acquirer_name=acquirer.Name()
        )
        LOGGER.info(message)
        output_file_path = os.path.join(output_directory_path, output_file_name)
        with open(output_file_path, 'w') as output_file:
            output_file.write(cls._create_manual_payments_file_header())
            for settlement in manual_settlements:
                try:
                    output_file_line = cls._create_manual_payments_file_settlement_line(settlement)
                    cls._update_settlement(output_file_name, settlement)
                    output_file.write(output_file_line)
                except:
                    # Prevent an exception during the processing of one settlement
                    # from preventing the processing of others.
                    message = "An exception occurred processing settlement {oid}, skipping..."
                    message = message.format(oid=settlement.Oid())
                    LOGGER.warning(message, exc_info=True)

    @classmethod
    def _create_acquirer_cps_payment_file(cls, output_directory_path, acquirer, cps_settlements):
        """
        Create a CPS payment contingency plan file for the specified
        acquirer settlements.

        Please note that following rules for files sent to CPS:

        - Required columns and order are:
            - Payee Name
            - Payee Account Number
            - Payee Branch Code
            - Payment Reference
            - Payment Amount
        - Additional columns may be appended but will be ignored
          by CPS.
        - Payment date will be the date that the file is sent.
        - Amounts must be absolute.
        - If a payment record is found to be invalid (invalid
          account number, branch code, etc.) the entire file
          will be rejected.
        """
        timestamp = datetime.datetime.today().strftime('%Y%m%d%H%M%S')
        output_file_name = cls._get_output_file_name(acquirer, 'CPS', timestamp)
        message = "Creating payment contingency plan file '{output_file_name}' for acquirer '{acquirer_name}'..."
        message = message.format(
            output_file_name=output_file_name,
            acquirer_name=acquirer.Name()
        )
        LOGGER.info(message)
        output_file_path = os.path.join(output_directory_path, output_file_name)
        with open(output_file_path, 'w') as output_file:
            # Note: CPS do not accept header lines.
            for settlement in cps_settlements:
                try:
                    output_file_line = cls._create_cps_payments_file_settlement_line(settlement)
                    cls._update_settlement(output_file_name, settlement)
                    output_file.write(output_file_line)
                except:
                    # Prevent an exception during the processing of one settlement
                    # from preventing the processing of others.
                    message = "An exception occurred processing settlement {oid}, skipping..."
                    message = message.format(oid=settlement.Oid())
                    LOGGER.warning(message, exc_info=True)

    @classmethod
    def _update_settlement(cls, output_file_name, settlement):
        """
        Update a settlement and its related operations document to
        indicate that it has been successfully sent via the payment
        contingency plan.
        """
        try:
            acm.BeginTransaction()
            if settlement.Documents().Size() != 1:
                raise RuntimeError('Expecting one operations document for settlement {oid}.'.format(
                    oid=settlement.Oid()
                ))
            operations_document = settlement.Documents()[0]
            operations_document.Status(OperationsDocumentStatus.SENT_SUCCESSFULLY)
            operations_document.Commit()
            settlement.AddDiaryNote("Exported to payment contingency file '{output_file_name}'.".format(
                output_file_name=output_file_name
            ))
            settlement.Diary().Commit()
            settlement.Status(SettlementStatus.ACKNOWLEDGED)
            settlement.Commit()
            acm.CommitTransaction()
        except:
            acm.AbortTransaction()
            raise

    @staticmethod
    def _get_output_file_name(acquirer, processing_destination, timestamp):
        """
        Get the name to be given to a payment contingency plan file
        for the specified acquirer, processing_destination and
        timestamp.
        """
        acquirer_name = acquirer.Name().strip()
        # Replace any single or multiple spaces with a single underscore.
        acquirer_name = re.sub(r' +', '_', acquirer_name)
        # Remove any characters that are not alphanumerics or underscores.
        acquirer_name = re.sub(r'(?u)[^\w]', '', acquirer_name)
        file_name = '{acquirer_name}_{processing_destination}_Payments_{timestamp}.csv'.format(
            acquirer_name=acquirer_name,
            processing_destination=processing_destination,
            timestamp=timestamp
        )
        return file_name

    @classmethod
    def _create_manual_payments_file_header(cls):
        """
        Create a header line for a manual payment contingency plan
        file.
        """
        return cls._create_manual_payments_file_line('Counterparty', 'Our Reference', 'Their Reference',
            'Our Account Number', 'Their Account Number', 'Value Day', 'Currency', 'Amount')

    @classmethod
    def _create_manual_payments_file_settlement_line(cls, settlement):
        """
        Create a file line for a manual payment contingency plan file
        for the specified settlement.
        """
        counterparty_name = settlement.Counterparty().Name()
        our_reference = 'Settlement {settlement_oid}'.format(
            settlement_oid=settlement.Oid()
        )
        their_reference = 'Absa {settlement_oid}'.format(
            settlement_oid=settlement.Oid()
        )
        our_account_number = settlement.AcquirerAccountRef().Account()
        their_account_number = settlement.CounterpartyAccountRef().Account()
        value_day = settlement.ValueDay()
        currency = settlement.Currency().Name()
        amount = '{amount:.2f}'.format(
            amount=abs(settlement.Amount())
        )
        return cls._create_manual_payments_file_line(counterparty_name, our_reference, their_reference,
            our_account_number, their_account_number, value_day, currency, amount)

    @classmethod
    def _create_manual_payments_file_line(cls, counterparty_name, our_reference, their_reference, our_account_number,
            their_account_number, value_day, currency, amount):
        """
        Create a file line for a manual payment contingency plan file
        for the specified values.
        """
        file_line = '{counterparty_name}{delimiter}{our_reference}{delimiter}{their_reference}{delimiter}'
        file_line += '{our_account_number}{delimiter}{their_account_number}{delimiter}{value_day}{delimiter}'
        file_line += '{currency}{delimiter}{amount}\n'
        file_line = file_line.format(
            delimiter=cls._get_delimiter(),
            counterparty_name=cls._to_delimited_value(counterparty_name),
            our_reference=cls._to_delimited_value(our_reference),
            their_reference=cls._to_delimited_value(their_reference),
            our_account_number=cls._to_delimited_value(our_account_number),
            their_account_number=cls._to_delimited_value(their_account_number),
            value_day=cls._to_delimited_value(value_day),
            currency=cls._to_delimited_value(currency),
            amount=cls._to_delimited_value(amount)
        )
        return file_line

    @classmethod
    def _create_cps_payments_file_settlement_line(cls, settlement):
        """
        Create a file line for a CPS payment contingency plan file
        for the specified settlement.
        """
        counterparty_name = settlement.Counterparty().Name()
        account_strings = settlement.CounterpartyAccountRef().Account().split(' ')
        their_account_branch_code = account_strings[0]
        their_account_number = account_strings[1]
        their_reference = 'Absa {settlement_oid}'.format(
            settlement_oid=settlement.Oid()
        )
        amount = '{amount:.2f}'.format(
            amount=abs(settlement.Amount())
        )
        value_day = settlement.ValueDay()
        return cls._create_cps_payments_file_line(counterparty_name, their_account_number,
            their_account_branch_code, their_reference, amount, value_day)

    @classmethod
    def _create_cps_payments_file_line(cls, counterparty_name, their_account_number, their_account_branch_code,
            their_reference, amount, value_day):
        """
        Create a file line for a CPS payment contingency plan file
        for the specified values.
        """
        file_line = '{counterparty_name}{delimiter}{their_account_number}{delimiter}{their_account_branch_code}'
        file_line += '{delimiter}{their_reference}{delimiter}{amount}{delimiter}{value_day}\n'
        file_line = file_line.format(
            delimiter=cls._get_delimiter(),
            counterparty_name=cls._to_delimited_value(counterparty_name),
            their_account_number=cls._to_delimited_value(their_account_number),
            their_account_branch_code=cls._to_delimited_value(their_account_branch_code),
            their_reference=cls._to_delimited_value(their_reference),
            amount=cls._to_delimited_value(amount),
            value_day=cls._to_delimited_value(value_day)
        )
        return file_line

    @classmethod
    def _to_delimited_value(cls, value):
        """
        Convert the specified value to a form that is safe for
        inclusion in a delimited file.
        """
        if value is None:
            return ''
        value = str(value)
        if cls._get_delimiter() in value:
            return value.replace(cls._get_delimiter(), '')
        return value
    
    @staticmethod
    def _get_delimiter():
        """
        Get the delimiter to use when creating payment contingency
        plan files.
        """
        return ','

    @classmethod
    def _requires_manual_processing(cls, settlement):
        """
        Determine whether or not a settlement requires manual
        processing.
        """
        counterparty_account = settlement.CounterpartyAccountRef()
        return not cls._are_account_details_well_formed(counterparty_account)

    @staticmethod
    def _are_account_details_well_formed(account):
        """
        Determine whether or not the details for the specified
        account appear well-formed (branch and account number
        captured in the form expected for ZAR cash accounts - with
        the account number field containing only numbers separated
        by a space in the form 'BRANCH_CODE ACCOUNT_NUMBER'.

        This check is an attempt to sanity-check the validity of
        account details as invalid account details will cause the
        entire payment contingency plan file to be rejected by the
        downstream payment processor.
        """
        # Ensure that the account is in the form 'BRANCH_CODE ACCOUNT NUMBER'
        account_strings = account.Account().split(' ')
        if len(account_strings) != 2:
            return False
        # Ensure that the branch code is numeric.
        branch_code = account_strings[0]
        if not branch_code.isdigit():
            return False
        # Ensure that the account number is numeric.
        account_number = account_strings[1]
        if not account_number.isdigit():
            return False
        return True
