"""
Script automatically pick up file Y:\Jhb\FALanding\Prod\ExposureManager\ABSA_Trades_yyyy-mm-dd.csv
and updated `CSA_Trade` additional info.

Date            JIRA          Developer               Reporter
==========      ====          ======================  ======================
2012-09-10      ABITFA-1534   Pavel Saparov           Rishaan Ramnarain
2014-08-06      ABITFA-2871   Pavel Saparov           Sean Laing
"""
# import core libs
import os
import csv

# import arena libs
import acm
import at_portfolio
import FRunScriptGUI


def filter_trades_by_addinfo(addinfo, value):
    """Function returns set of FTrade objects
    having ``addinfo`` set to ``value``.
    """
    trades = set()
    addInfoSpec = acm.FAdditionalInfoSpec[addinfo]
    if addInfoSpec:
        for record in addInfoSpec.AddInf():
            if record.FieldValue() == value:
                trade = acm.FTrade[record.Recaddr()]
                trades.add(trade)
    return trades


def set_additional_info(entity, addinfo, value=None, delete=False):
    """Function sets AdditionalInfo for and entity to a ``value``.
    If delete is True than AdditionalInfo is removed from an entity.
    """
    # Skip Archived, Aggregated, Voided and Simulated entities
    if (entity.ArchiveStatus() != 1 and entity.Aggregate() == 0
        and entity.Status() not in ('Void', 'Simulated')):
        # GetProperty doesn't support spaces, replace them with underscores
        try:
            if entity.AdditionalInfo().GetProperty(addinfo.replace(' ', '_')) is None:
                addInfo = acm.FAdditionalInfo()
                addInfo.Recaddr(entity.Oid())
                addInfo.AddInf(acm.FAdditionalInfoSpec[addinfo])
                addInfo.FieldValue(value)
                addInfo.Commit()
            else:
                addInfo = filter(lambda i: i.AddInf().Name() == addinfo,
                                 acm.FAdditionalInfo.Select('recaddr = %i' % entity.Oid()))[0]
                if not delete:
                    addInfo.FieldValue(value)
                    addInfo.Commit()
                else:
                    addInfo.Delete()
        except AttributeError, err:
            acm.LogAll('ERROR: Undefined AdditionalInfo %s for Trade ID: %d, %s.' % \
                (addinfo, entity.Oid(), err))
        except RuntimeError, err:
            acm.LogAll('ERROR: Failed to update AdditionalInfo for Trade ID: %d, %s.' % \
                (entity.Oid(), err))


# Define variables for `ael_variables` used in GUI
input_dir = FRunScriptGUI.DirectorySelection()

today = acm.Time().DateToday()
start_dates = {
   'Today': today,
   'Yesterday': acm.Time.DateAddDelta(today, 0, 0, -1),
   'Custom Date': today
}

def custom_start_date(index, fieldValues):
    """ Input hook """
    ael_variables[1][9] = (fieldValues[0] == 'Custom Date')
    return fieldValues

ael_variables = [
    ['date', 'Date', 'string', start_dates.keys(), 'Today', 1, 0, 'Date for witch the file should be selected.', custom_start_date, 1],
    ['dateCustom', 'Date Custom', 'string', None, today, 0, 0, 'Custom date', None, 0],
    ['directory', 'Directory', input_dir, None, input_dir, 1, 1, 'Directory where a file will be uploaded from.', None, 1],
    ['fileName', 'File name', 'string', None, 'ABSA_Trades_', 1, 0, 'File name prefix. Will be followed by the date specified', None, 1],
]

def ael_main(argc):
    """ Main function """
    # Get Start date
    date = start_dates[argc['date']]
    if argc['date'] == 'Custom Date':
        date = argc['dateCustom']

    acm.LogAll('Starting %s' % __name__)

    # Check if file ABSA_Trades_yyyy-mm-dd.csv exists in directory
    directory = argc['directory'].SelectedDirectory().Text()
    filename = os.path.join(directory, "%s%s.csv" % (argc['fileName'], date))

    if os.path.isfile(filename):
        # Obtain Front Arena Trade IDs from a file
        reader = csv.reader(open(filename, 'rb'))
        tradeIDs = [row[3].replace('F_', '') for row in reader
                     if len(row) > 1 and row[3].startswith('F_')]

        # Create FTrade set from file trade IDs
        file_trades = set(map(lambda t: acm.FTrade[t], tradeIDs))

        # Obtain Trades from Database having additional info 'CSA Trade'
        csa_trades = filter_trades_by_addinfo('CSA Trade', 'Yes')

        # Delete `CSA_Trade` AdditionalInfo from diff but exclude 3306 CC
        excluded_portfolio = acm.FCompoundPortfolio['3306']
        tree = at_portfolio.create_tree(excluded_portfolio)

        diff = csa_trades - file_trades
        acm.LogAll('Removing AdditionalInfo for %d Trades' % len(diff))

        for t in diff:
            if t.Portfolio() and not tree.has(t.Portfolio().Name()):
                set_additional_info(t, 'CSA Trade', delete=True)

        # Set `CSA_Trade` AdditionalInfo to diff
        diff = file_trades - csa_trades
        acm.LogAll('Setting AdditionalInfo for %d Trades' % len(diff))

        for t in diff:
            set_additional_info(t, 'CSA Trade', 'Yes')

        acm.LogAll('%s completed successfully' % __name__)
    else:
        acm.LogAll('ERROR: File: %s does not exist.' % filename)
        acm.LogAll('%s failed' % __name__)

