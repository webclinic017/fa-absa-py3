'''
As per ABITFA-4841 - Client Service to FA Integration
Business requires the ability to obtain Party and Counterparty data from Client 
static, via the Client Static Service, and integrate it into Front Arena.

Operations requires the ability to check if a Party is an "Internal" type or not
as this affect the process used to settle trades/money_flows

The script below, requests the Client Service via a system user that was created, 
named: sysFAINTERNAL

The service uses NTLM Authentication, as such to run this code, a NTLM package is
required for the python environment this is executed in.

Information returned as "JSON" type (Which can be configured via the headers)

Initial Deployment - 2017-09-06

Date            Change            Developer                     Requester
==========      ===========       ==================            ======================
2017-09-06	ABITFA-4841       Kunal Maharaj/ Bhavik Mistry  Linda Breytenbach
								 
'''

import json
import urllib.request, urllib.error, urllib.parse
from ntlm import HTTPNtlmAuthHandler

import acm
from at_logging import getLogger


LOGGER = getLogger("ClientStaticUpload")

class ClientServicesRequest(object):

    def __init__(self, user, password, base_url):
        self.user = user
        self.password = password
        self.base_url = base_url
        self.headers = {'Format': 'Json', 'Compressed': 'False', 'Encoding': 'Unicode'}

    def authenticate_service(self):
        LOGGER.info("Authenticating...")
        passman = urllib.request.HTTPPasswordMgrWithDefaultRealm()
        passman.add_password(None, self.base_url, self.user, self.password)
        auth_NTLM = HTTPNtlmAuthHandler.HTTPNtlmAuthHandler(passman)
        opener = urllib.request.build_opener(auth_NTLM)
        urllib.request.install_opener(opener)
        LOGGER.info('Authentication completed')

    def client_request(self, client_service_url):
        request_sent = urllib.request.Request(client_service_url, headers = self.headers)
        response_received = urllib.request.urlopen(request_sent)

        return response_received

    def call_api(self, method_url):
        client_service_url = self.base_url + "/" + method_url
        response = self.client_request(client_service_url).read()
        json_response_body = json.loads(response)

        return json_response_body


class ClientServiceMessageProcessor(object):

    def process(self, json_message):
        data = json_message['Pegasus']['Data']

        for legal_entity in data:
            legal_name = legal_entity['Item']['client']['legalName']

            try:
                source_sytem_list = legal_entity['Item']['client']['counterpartyId']['aliases']['enterpriseId']
                intra_group_type = legal_entity['Item']['client']['intragroupType']['Value']

                for source in source_sytem_list:
                    if source['sourceSystem']['Value'] == 'Frontarena':
                        source_front_id = source['id']
                        self.commit_to_FA(intra_group_type, source_front_id)

            except Exception:
                LOGGER.exception("Unable to commit party '%s'", legal_name)

    def commit_to_FA(self, free_value, source_front_id):
        source_front_id = source_front_id.encode('utf-8')
        source_front_id = int(source_front_id)
        free_value = free_value.encode('utf-8')
        party = acm.FParty[source_front_id]
        
        if not party:
            LOGGER.warning("Nonexisting FA party ID: %s", source_front_id)
            return
        
        if not (party.Free3ChoiceList() and party.Free3ChoiceList().Name() == free_value):
            party.Free3ChoiceList = free_value
            party.Commit()
            LOGGER.info("Party '%s' updated with '%s'", party.Name(), party.Free3ChoiceList().Name())

        return party.Name()
