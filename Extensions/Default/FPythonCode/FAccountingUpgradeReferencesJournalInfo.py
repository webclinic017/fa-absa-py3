""" Compiled: 2020-09-18 10:38:46 """

#__src_file__ = "extensions/accounting/etc/upgrade/FAccountingUpgradeReferencesJournalInfo.py"
import acm
import acm, time

from FAccountingUpdateAggregatedJournalInfo import UpdateJournalInformation

KEY_REFERENCES = ['AccountingInstruction', 'Treatment', 'Book', 'ContractTrade',
                 'Trade', 'Portfolio', 'Instrument', 'CashFlow', 'Dividend',
                 'Payment', 'CombinationLink', 'Leg', 'Settlement']

#-------------------------------------------------------------------------
def GetEndOfDayGeneratedTradeJournals():
    query = acm.CreateFASQLQuery(acm.FJournalInformation, 'AND')

    # Only EOD journals are selected.
    query.AddAttrNode('AccountingInstruction.Oid', 'NOT_EQUAL', 0)
    query.AddAttrNode('Treatment.Oid', 'NOT_EQUAL', 0)
    query.AddAttrNode('Book.Oid', 'NOT_EQUAL', 0)

    # Aggregation Levels applicable for update.
    orNode = query.AddOpNode('OR')
    orNode.AddAttrNode('AccountingInstruction.AggregationLevel', 'EQUAL', 'Contract Trade Number')
    orNode.AddAttrNode('AccountingInstruction.AggregationLevel', 'EQUAL', 'Contract Trdnbr and Moneyflow')
    orNode.AddAttrNode('AccountingInstruction.AggregationLevel', 'EQUAL', 'Moneyflow')

    return query.Select()

#-------------------------------------------------------------------------
def GetJournalInformationKey(journalInformation):
    keyValues = []

    for method in KEY_REFERENCES:
        obj = getattr(journalInformation, method)()
        keyValues.append(str(obj.Oid()) if obj else "")

    keyValues.append(str(journalInformation.AggregationDate()))

    return '-'.join(keyValues)

#-------------------------------------------------------------------------
def AddForUpdate(ji, journalInformations, moveJournals, journalsToMove):
    key = GetJournalInformationKey(ji)

    dup = journalInformations.get(key, None)

    if not dup:
        journalInformations[key] = ji

    elif not moveJournals:
        acm.Log('INFO: Journal information {} will not be updated since the set of references will not be unique'.format(ji.Original().Oid()))

    else:
        acm.Log('INFO: Journals for journal information {} will be moved to journal information {} as an update would create duplicate journal informations'\
                .format(ji.Original().Oid(), dup.Original().Oid()))

        for journal in ji.Original().Journals():

            journalClone = journal.Clone()
            journalClone.JournalInformation(dup.Original())

            journalsToMove.append(journalClone)



#-------------------------------------------------------------------------
def CommitUpdate(object):
    org = object.Original()
    org.Apply(object)
    org.Commit()

#-------------------------------------------------------------------------
def CommitJournalInformations(journalInformations):
    updatedJournalInfos = 0
    for key, journalInformation in journalInformations.items():
        try:
            CommitUpdate(journalInformation)
            updatedJournalInfos += 1

        except Exception as e:
            acm.Log('ERROR: Journal information {} could not be updated: {}'.format(ji.Original().Oid(), str(e)))

    acm.Log('\nINFO: Updated {} journal informations\n'.format(updatedJournalInfos))

#-------------------------------------------------------------------------
def GetAggregationDate(ji):
    aggDate = None

    if ji.AccountingInstruction().IsNonPeriodic():
        journals = ji.Journals()
        liveJournals = [journal for journal in journals]

        if len(liveJournals) > 0:
            aggDate = liveJournals[0].EventDate()
        elif len(journals) > 0:
            journals.SortByProperty('CreateTime')
            aggDate = journals[0].Eventdate()

    return aggDate

#-------------------------------------------------------------------------
def CommitJournalsToMove(journalsToMove):
    movedJournals = 0

    for journal in journalsToMove:
        try:
            CommitUpdate(journal)
            movedJournals += 1

        except Exception as e:
            acm.Log('ERROR: Journal {} could not be moved to upgraded journal information {}: {}'.format(journal.Oid(), journal.JournalInformation().Oid(), str(e)))

    acm.Log('\nINFO: Moved {} journals\n'.format(movedJournals))

#-------------------------------------------------------------------------
ael_variables = [['moveJournals', 'Read Tooltip - Journals will be updated as part of the script', 'int', [1, 0], 0, 0, 0, 'If set, the upgrade script will cater for updating the Journals '\
                                                                                                                           'with the upgraded Journal Information. If not set Accounting EOD '\
                                                                                                                           'will instead create Reversal Journals to update the Journals with '\
                                                                                                                           'the upgraded Journal Information. ']]

#-------------------------------------------------------------------------
def ael_main(params):
    acm.Log('INFO: FAccountingUpgradeReferencesJournalInfo started at {} \n'.format(time.ctime()))

    journalInformations = GetEndOfDayGeneratedTradeJournals().SortByProperty('CreateTime')
    acm.Log('INFO: Found {} journal informations to update \n'.format(len(journalInformations)))

    moveJournals = params['moveJournals']

    journalInformationsToCommit = dict()
    journalsToMove = list()

    for ji in journalInformations:
        try:
            if not ji.Journals():
                acm.Log('INFO: Journal information {} will not be updated as it has no journals'.format(ji.Oid()))
            else:
                aggregationDate = GetAggregationDate(ji)

                jiClone = ji.Clone()
                UpdateJournalInformation(jiClone, aggregationDate)
                AddForUpdate(jiClone, journalInformationsToCommit, moveJournals, journalsToMove)

        except Exception as e:
            acm.Log('ERROR: Exception occurred while processing journal information {}: {}'.format(ji.Oid(), str(e)))

    CommitJournalInformations(journalInformationsToCommit)

    if moveJournals:
        CommitJournalsToMove(journalsToMove)

    acm.Log('INFO: FAccountingUpgradeReferencesJournalInfo ended at {}'.format(time.ctime()))

