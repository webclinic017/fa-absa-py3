"""-----------------------------------------------------------------------------
Script used to on board a broker used for offshore CFDs within the Prime services
space.

CSV file headers: 'Short Name': Clients FA alias
                  'Alias': Clients broker account name

HISTORY
================================================================================
Date           Developer          Description
--------------------------------------------------------------------------------
2020-11-20     Marcus Ambrose     Implemented
-----------------------------------------------------------------------------"""
import csv

import acm

from at_logging import getLogger
from at_ael_variables import AelVariableHandler
from FRunScriptGUI import DirectorySelection
from PS_Functions import get_pb_fund_counterparty
from pb_offshore_cfd_config import get_broker_onboarding_config

LOGGER = getLogger(__name__)


class OffshoreBrokerOnboarder:
    def __init__(self, file_path, broker_name):
        self.broker_name = broker_name
        self.file_path = file_path
        self.broker_alias_type = acm.FPartyAliasType[
            "PB_{}_Account".format(self.broker_name)
        ]

    def on_board_broker(self):
        self._create_broker_alias()

        with open(self.file_path) as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                self.map_broker_clients(row)
                self.create_sweeper_task(row["Short Name"])
                self.create_reset_task(row["Short Name"])

    def _create_broker_alias(self):
        try:
            broker_alias_type = acm.FPartyAliasType()
            broker_alias_type.Name("PB_{}_Account".format(self.broker_name))
            broker_alias_type.AliasTypeDescription(
                "Offshore broker {} external client account mapping.".format(
                    self.broker_name
                )
            )
            broker_alias_type.Commit()
            LOGGER.info("Party alias {} created".format(broker_alias_type.Name()))
        except Exception as e:
            LOGGER.error(
                "Party alias {} was not created: {}".format(broker_alias_type.Name(), e)
            )

    def map_broker_clients(self, row):
        try:
            party = get_pb_fund_counterparty(row["Short Name"])
            new_alias = acm.FPartyAlias()
            new_alias.Type = self.broker_alias_type
            new_alias.Party(party)
            new_alias.Name(row["Alias"])
            new_alias.Commit()
        except Exception as e:
            LOGGER.error("Unable to map party {}: {}".format(row["Short Name"], e))

    def create_sweeper_task(self, short_name):
        template_name = "PS_Template_OffshoreCFDSweeper"
        name = "PS_{}_OffshoreCFDSweeper_{}_SERVER".format(self.broker_name, short_name)

        on_boarding_config = get_broker_onboarding_config(self.broker_name)

        params = {
            "start_date": "Previous Business day",
            "end_date": "Previous Business day",
            "cp_alias": short_name,
            "broker": self.broker_name,
            "file_dir": on_boarding_config["file_dir"],
            "funding_file": on_boarding_config["funding_file"],
            "synthetic_file": on_boarding_config["synthetic_file"],
            "funding_sweeping_report": on_boarding_config["funding_sweeping_report"],
            "pnl_sweeping_report": on_boarding_config["pnl_sweeping_report"],
        }

        self.create_new_task(template_name, name, params)

    def create_reset_task(self, short_name):
        template_name = "PS_Template_OffshoreCFDReset"
        name = "PS_{}_OffshoreCFDReset_{}_SERVER".format(self.broker_name, short_name)

        params = {
            "date": "Previous Business day",
            "client_short_name": short_name,
            "broker": self.broker_name,
        }

        self.create_new_task(template_name, name, params)

    @staticmethod
    def create_new_task(template_name, name, params):
        template_task = acm.FAelTask[template_name]
        if template_task:
            new_task = template_task.Clone()
            new_task.Name(name)
            new_task.Parameters(params)
            try:
                new_task.Commit()
            except Exception as e:
                LOGGER.error("Could not create task {}: {}".format(name, e))
        else:
            raise Exception("No template task found with name {}".format(template_name))


directory_selection = DirectorySelection()
ael_variables = AelVariableHandler()

ael_variables.add("broker", label="Broker Name", cls="string", mandatory=True)
ael_variables.add(
    "file_path", label="Client Mappings File", mandatory=True, cls="string"
)


def ael_main(ael_dict):
    broker = ael_dict["broker"]
    file_path = ael_dict["file_path"]

    LOGGER.info("Started to on board {}".format(broker))

    broker_onboarder = OffshoreBrokerOnboarder(file_path, broker)
    broker_onboarder.on_board_broker()

    LOGGER.info("Completed")
