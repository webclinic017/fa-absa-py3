
def LinkedJournalsString(journal):
    linkedJournalsString = ''
    for linkedJournal in journal.LinkedJournals():
        if linkedJournalsString != '':
            linkedJournalsString += ', '
        linkedJournalsString += str(linkedJournal.Oid())
    return linkedJournalsString
