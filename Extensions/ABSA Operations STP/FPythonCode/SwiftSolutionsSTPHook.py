"""---------------------------------------------------------------------------------------------------------------------
MODULE
    SwiftSolutionsSTPHook

DESCRIPTION
    Module to handle all Swift Solutions STP.

------------------------------------------------------------------------------------------------------------------------
HISTORY
========================================================================================================================
Date            Change no       Developer           Requester           Description
------------------------------------------------------------------------------------------------------------------------
2020-10-26      FAOPS-821       Tawanda Mukhalela   Martin Wortmann     Initial implementation
------------------------------------------------------------------------------------------------------------------------
"""

import urllib3
import json

import acm
from at_logging import getLogger

from EnvironmentFunctions import is_production_environment

HTTP = urllib3.PoolManager()
BASE_URL = 'https://bic-rma-file-service.pagamentos-prod.cto-payments.prod.caas.absa.co.za/swift/api/rmas/'
LOGGER = getLogger(__name__)


class MT202COVMethodSTPHook(object):
    """
    Definition of a hook used to perform Operations STP.
    """

    def Name(self):
        """
        Get the name of the Operations STP Hook.
        """
        return 'MT202COV STP Hook'

    def IsTriggeredBy(self, eventObject):
        """
        Checks is settlement is eligible for the Cov Method
        """
        if not eventObject.IsKindOf(acm.FSettlement):
            return False
        settlement = eventObject
        if settlement.Currency().Name() == 'ZAR':
            return False
        if settlement.MTMessages() != '103':
            return False
        if settlement.CounterpartyAccountRef() is None:
            return False
        if settlement.CounterpartyAccountRef().CorrespondentBank2() is None:
            return False
        if not self._perform_rma_checks(settlement):
            return False

        return True

    def PerformSTP(self, settlement):
        """
        Flag Settlement as COV
        """
        settlement.IsCov(True)
        settlement.Commit()

    def _perform_rma_checks(self, settlement):
        """
        Checks if payment is eligible for a Cov Method via the Swagger API
        """
        acquirer_alias = settlement.Acquirer().Swift()
        acquirer_correspondent = settlement.AcquirerAccountRef().Bic().Name()
        counterparty_correspondent = settlement.CounterpartyAccountRef().Bic().Name()
        if not is_production_environment():
            acquirer_alias = self._apply_non_production_bic_address(acquirer_alias)
            acquirer_correspondent = self._apply_non_production_bic_address(acquirer_correspondent)
            counterparty_correspondent = self._apply_non_production_bic_address(counterparty_correspondent)

        rma_url_for_mt103 = '{host}{receiver}/{sender}/103'.format(
            host=BASE_URL, receiver=counterparty_correspondent, sender=acquirer_alias
        )
        rma_url_for_mt202 = '{host}{receiver}/{sender}/202'.format(
            host=BASE_URL, receiver=acquirer_correspondent, sender=acquirer_alias
        )
        urllib3.disable_warnings()
        response_for_103 = HTTP.request('GET', rma_url_for_mt103)
        response_for_202 = HTTP.request('GET', rma_url_for_mt202)
        if json.loads(response_for_103.data)['status'] and json.loads(response_for_202.data)['status']:
            LOGGER.info(
                'Settlement {} qualifies for COV Method.. Setting COV Flag'.format(settlement.Oid())
            )
            return True

        return False

    @staticmethod
    def _apply_non_production_bic_address(bic_address):
        """
        Change Production Bic to Dev for Non-Prod environments
        """
        index = 8
        if len(bic_address) == index:
            bic_address = bic_address[:index - 1] + '0' + bic_address[index:]

        return bic_address
