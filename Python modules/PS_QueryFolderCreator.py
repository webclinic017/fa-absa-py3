"""-----------------------------------------------------------------------------
HISTORY
================================================================================
Date       Change no        Developer             Description
--------------------------------------------------------------------------------
2018-10-02                  Reiss Tibor           Use transactions
2021-02-04  FAPE-468        Frickova Katerina     Add new class PS_CallAccounts

Facilitates the creation of query folders for the PB new client setup.
"""


import re

import acm, ael

from at_logging import getLogger
from PS_Mixins import DescendantAware, AlwaysRelevant
from PS_Names import get_top_cr_portfolio_name


__all__ = ['setup_query_folders']


LOGGER = getLogger()
FOR_REGEX = re.compile('\{% +for +([^ ]+) +in +([^ ]+) +%\}(.*)\{% +endfor +%\}', re.DOTALL)


## Helper functions

def _get_textobject(qf_name):
    queryfolders = ael.TextObject.select("type='FASQL Query'")
    for qf in queryfolders:  # For some reason, selecting by name doesn't work.
        if qf.name == qf_name: return qf
    raise RuntimeError('Cannot find Query folder %s' % qf_name)


def _apply_params(template, params):
    """
    A simple templating solution that allows for simple for-loops.

    Use with caution, as this function currently doesn't deal with any edge
    cases and in general is quite error-prone.

    Templating currently supports:
         - simple replacements (via Python's %-operator)
         - Django-style for loops (only one level deep):

           {% for thing in list_of_things %}
                (stuff...)
                    {{ thing }}
                (other stuff...)
           {% endfor %}

    """
    ret = template

    # First of all, expand the for loops.
    match = FOR_REGEX.search(ret)
    while match:
        original = match.group(0)
        element_var, list_var, content = match.groups()
        new_content = []
        local_pattern = re.compile('\{\{ *%s *\}\}' % element_var)
        for replacement in params[list_var]:
            replaced = local_pattern.sub(replacement, content)
            new_content.append(replaced)
        ret = ret.replace(original, ''.join(new_content))
        match = FOR_REGEX.search(ret)

    # Now replace the remaining parameters.
    return ret % params


## Abstract classes.


class QueryFolder(DescendantAware):
    """
    An abstract descendant-aware class.

    Once a subclass is created, it will be automatically included in the
    list of QueryFolders to be created for new clients by the setup_query_folders
    function. Subclasses may/should supply the following attributes and methods:

    is_relevant - A method accepting client configuration (as specified
        in PS_MO_Onboarding), returning True or False - is the query folder
        represented by the subclass relevant to the given client?

    _get_data - Get the name of the query folder and its params.

    DO NOT SUBCLASS IN OTHER MODULES!

    """

    @staticmethod
    def _get_data(config):
        """Get the name of the query folder and its params."""
        raise NotImplementedError()

    @classmethod
    def to_acm(cls, config):
        """
        Convert to a newly created acm.FStoredASQLQuery instance.

        Unfortunately, creating the FASQLQuery programatically (using
        AddAttrNode etc.) doesn't work, which is why ael has to be used.

        """
        name, params = cls._get_data(config)
        if acm.FStoredASQLQuery.Select01('name="%s"' % name, None):
            LOGGER.warning('The QueryFolder with name %s already exists.' % name)
            return None
        text_object = _get_textobject(cls.template).new()
        text_object.name = name
        text_object.data = _apply_params(text_object.data, params)
        text_object.usrnbr = None  # By specifying None, the QF is saved as "shared".
        text_object.owner_usrnbr = None
        # Unfortunately, committing is necessary - otherwise the conversion
        # to ACM doesn't work properly.
        text_object.commit()
        acm.PollDbEvents()


## Classes representing the individual Query Folders.

class PS_General_PSwaps(QueryFolder, AlwaysRelevant):

    template = 'PS_General_PSwaps_Template'  # TODO: PS_Template should be a prefix.

    @staticmethod
    def _get_data(config):
        name = 'PS_General_PSwaps_%s' % config['shortName']
        params = {'counterparty': config['counterparty'].Name()}
        return name, params


class PS_AllTrds(QueryFolder, AlwaysRelevant):

    template = 'PS_Template_AllTrds'

    @staticmethod
    def _get_data(config):
        name = '%s~Trades' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PS_CallAccounts(QueryFolder, AlwaysRelevant):

    template = 'PS_Template_CallAccounts'

    @staticmethod
    def _get_data(config):
        name = 'PS_CallAccounts_%s' % config['shortName']
        params = {
            'portfolio': "PB_%s_FINANCING" % config['shortName'],
        }
        return name, params


class PB_Financing(QueryFolder, AlwaysRelevant):

    template = "PS_Template_Financing"

    @staticmethod
    def _get_data(config):
        name = 'PS_Financing_%s' % config['shortName']
        params = {
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
        }
        return name, params


class PB_Valuations(QueryFolder, AlwaysRelevant):

    template = "PS_Template_Valuations"

    @staticmethod
    def _get_data(config):
        name = 'PS_Valuations_%s' % config['shortName']
        params = {
            'call_accnt_prf': 'PB_CALLACCNT_%s' % config['shortName'],
            'compound_CR_prf': get_top_cr_portfolio_name(config['shortName']),
            'counterparty': config['counterparty'].Name(),
        }
        return name, params


## Main body.

def setup_query_folders(config):
    """
    Create query folders for the new PB client.

    <config> is the ael_variables instance from PS_MO_Onboarding.

    """
    ael.begin_transaction()
    try:
        for qf_cls in QueryFolder.get_descendants():
            if not qf_cls.is_relevant(config):
                continue
            LOGGER.info('Processing %s...', qf_cls.template)
            if config['dryRun']:
                LOGGER.warning('Skipping the actual creation according to the Dry Run setting.')
                continue
            qf_cls.to_acm(config)
            # Do not commit again - it was already saved to the DB in the ael context.
            LOGGER.info('Done.')
        ael.commit_transaction()
    except Exception as e:
        ael.abort_transaction()
        LOGGER.exception("Could not commit query folder")
        raise e
