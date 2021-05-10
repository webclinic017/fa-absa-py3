""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/FAccountingLedgerKeyParser.py"

# operations
from FOperationsExceptions import IncorrectMethodException
from FOperationsMethodChainParser import ParseAttributeMethodChain, SetAttributeFromObj, CallMethodChain

# accounting
from FAccountingExceptions import IncorrectLedgerKeyException

#-------------------------------------------------------------------------
def ParseLedgerKey(domains, methodChains, domain):
    chains = list()
    attributes = list()

    for chain in methodChains:
        try:
            methodChain, domainName, attribute = ParseAttributeMethodChain(domains, domain, chain.split('.'), 0)

            if attribute.Domain().IsClass():
                idAttribute = attribute.Domain().IdentityAttribute()
                method = idAttribute.GetMethod()
                methodChain.append(str(method.Name()))

            chains.append('.'.join(methodChain))
            attributes.append((domainName, attribute))

        except (IncorrectMethodException, AssertionError) as e:
            raise IncorrectLedgerKeyException('Error detected when processing methodchain %s: %s' % (chain, str(e)))

    return chains, attributes

#-------------------------------------------------------------------------
def SetValuesFromLedgerKey(attributes, j1, j2):

    for (domain, attribute) in attributes:

        if domain == 'FJournal':
            SetAttributeFromObj(j1, j2, attribute)
        elif domain == 'FJournalInformation':
            SetAttributeFromObj(j1.JournalInformation(), j2.JournalInformation(), attribute)
        elif domain == 'FJournalAdditionalInfo':
            SetAttributeFromObj(j1.AdditionalInfo(), j2.AdditionalInfo(), attribute)
        elif domain == 'FJournalInformationAdditionalInfo':
            SetAttributeFromObj(j1.JournalInformation().AdditionalInfo(), j2.JournalInformation().AdditionalInfo(), attribute)

#-------------------------------------------------------------------------
def ComputeKeyForJournal(journal, tAccountLedgerKeyMapper):
    ledgerKeyMethodChains = tAccountLedgerKeyMapper.GetLedgerKeyMethodChains(journal.Account())

    if ledgerKeyMethodChains:

        # Customer defined values from ledger key in taccount setup
        keyValues = [ ''.join([attribute, '=', str(CallMethodChain(attribute, journal))]) for attribute in ledgerKeyMethodChains]

        # Hardcoded values, always part of the ledger key
        keyValues.append(journal.Currency().Name())
        keyValues.append(journal.Book().Name())
        keyValues.append(journal.ChartOfAccount().Account().Number())

        return '-'.join(keyValues)

    return None
