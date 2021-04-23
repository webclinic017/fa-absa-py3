import os
import xlrd
from datetime import datetime

ABAM = "ABAM"                # ABSA ASSET MANAGEMENT PTY LTD
OMIG = "OMIG"                # Old Mutual Investment Group
CORONATION = "Coronation"
TAQUANTA = "Taquanta"

# Header start in the file (row number).
ABAM_FILE_OFFSET = 7


CLIENTS = [ABAM, OMIG, CORONATION, TAQUANTA]

def get_client_name(filename):
    """Return client name based on heuristics from filename.
    
    ABAM (ABSA ASSET MANAGEMENT PTY LTD):
        - filename: Cash DDMMYYYY.xls
    OMIG (Old Mutual Investment Group):
        -filename: ABMN_DDMMYYY_HHMMSS.xlsx
    Taquanta:
        - they send and e-mail (will be copied to Excel file
        -filename: TAQUANTA.xlsx
    Coronation:
        - filename: e.g. Book5.xlsx (no naming convention)
    
    """
    name = os.path.basename(filename).strip().upper()
    if name.startswith("CASH"):
        return ABAM
    elif name.startswith("ABMN"):
        return OMIG
    elif name.startswith("TAQUANTA"):
        return TAQUANTA
    else:
        return CORONATION


def get_data(client, row):
    """Convert data from client's file into generic format."""
    if client == ABAM:
        return get_abam_data(row)
    elif client == OMIG:
        return get_omig_data(row)
    elif client == CORONATION:
        return get_coronation_data(row)
    elif client == TAQUANTA:
        return get_taquanta_data(row)
    else:
        return None


def get_abam_data(row):
    """Return client data for ABSA ASSET MANAGEMENT PTY LTD."""
    data = {
        'code': row['Account'],
        'name': row['Account Name'],
        'amount': get_abam_amount(row)
    }
    return data


def get_abam_amount(row):
    """Return fixed amount for ABSA ASSET MANAGEMENT PTY LTD's cash flow.

    Return positive amount from the 'DEPOSIT' column or negative amount from
    the 'WITHDRAWAL' column (to prevent issues with incorrect signs - column
    description dictates direction). If both columns have values, 'DEPOSIT'
    has precedence.

    """
    if row['DEPOSIT']:
        return abs(float(row['DEPOSIT']))
    elif row['WITHDRAWAL']:
        return -1 * abs(float(row['WITHDRAWAL']))
    else:
        return 0.0


def get_omig_data(row):
    """Return client data for Old Mutual Investment Group."""
    data = {
        'code': row['Client Code'],
        'name': row['Portfolio Name'],
        'amount': get_omig_amount(row)
    }
    return data


def get_omig_amount(row):
    """Return fixed amount for Old Mutual Investment Group's cash flow.

    Return positive amount from the column 'Settle Gross Amt.' if 'Type' is
    Place or negative amount if the 'Type' is Call.

    """
    amount = float(row['Settle Gross Amt.'])
    if row['Type'] == 'Place':
        return abs(amount)
    elif row['Type'] == 'Call':
        return -1 * abs(amount)
    else:
        return amount

def get_coronation_data(row):
    """Return client data for Coronation."""
    data = {
        'code': row['Portfolio Code'],
        'name': row['Portfolio Name'],
        'amount': get_coronation_amount(row)
    }
    return data


def get_coronation_amount(row):
    """Return fixed amount for Coronation's cash flow.
    
    Return positive amount from the 'Deposit' column or negative amount from
    the 'Withdrawal' column (to prevent issues with incorrect signs - column
    description dictates direction). If both columns have values, 'Deposit'
    has precedence.

    """
    if row['Deposit']:
        return abs(float(row['Deposit']))
    elif row['Withdrawal']:
        return -1 * abs(float(row['Withdrawal']))
    else:
        return 0.0


def get_taquanta_data(row):
    """Return client data for Taquanta."""
    data = {
        'code': row['Fund'],
        'name': row['Full name'],
        'amount': get_taquanta_amount(row)
    }
    return data


def get_taquanta_amount(row):
    """Return fixed amount for Taquanta's cash flow.

    Return positive amount from the 'Sum of ABSA(Mil)' multiplied by 1 mil
    if 'Transaction Type' is Deposit or negative amount if 'Transaction Type'
    is Withdrawal

    """
    amount = float(row['Sum of ABSA(Mil)']) * 1000000
    if row['Transaction Type'] == 'Deposit':
        return abs(amount)
    elif row['Transaction Type'] == 'Withdrawal':
        return -1 * abs(amount)
    else:
        return amount


def decode(cell_type, cell_value, datemode):
    """Decode xlrd value based on type."""
    if cell_type == xlrd.XL_CELL_DATE:
        try:
            value = datetime(*xlrd.xldate_as_tuple(cell_value, datemode))
        except xlrd.XLDateError:
            e1, e2 = sys.exc_info()[:2]
            value = '%s:%s' % (e1.__name__, e2)
    elif cell_type == xlrd.XL_CELL_ERROR:
        value = xlrd.error_text_from_code.get(
            cell_value, '<Unkown error code 0x%02x>' % cell_value)
    elif isinstance(cell_value, unicode):
        value = cell_value.replace(u'\xa0', u'').encode('utf8').strip()
    elif cell_type == xlrd.XL_CELL_TEXT:
        value = cell_value.strip()
    else:
        value = cell_value
    return value
            

def load_file_content(filename, start=0):
    """Load content of the file.

    filename = Filename of the input file
    start = Row at which to start parsing

    """
    book = xlrd.open_workbook(filename)
    sheet = book.sheet_by_index(0)

    # Read header values into the list
    keys = []
    for col_index in range(sheet.ncols):
        key = sheet.cell(start, col_index).value
        if isinstance(key, unicode):
            key = key.encode('utf8')
        keys.append(key.strip())

    # Read the file content
    data = []
    for row_index in range(start + 1, sheet.nrows):
        # Skip processing row if the first cell is empty (heuristics)
        if sheet.cell(row_index, 0).ctype == xlrd.XL_CELL_EMPTY:
            continue
        d = {}
        for col_index in range(sheet.ncols):
            item = sheet.cell(row_index, col_index)
            value = decode(item.ctype, item.value, book.datemode)
            d[keys[col_index]] = value
        data.append(d)
    
    return data


FILENAMES = [
    r"C:\Front Arena\ABITFA-4464\TAQUANTA (Potential format).xlsx",
    r"C:\Front Arena\ABITFA-4464\ABMN_18082016_112618.xlsx",
    r"C:\Front Arena\ABITFA-4464\Book5.xlsx",
    r"C:\Front Arena\ABITFA-4464\CASH 06122016.xls"
]


for filename in FILENAMES:
    client = get_client_name(filename)
    offset = ABAM_FILE_OFFSET if client == ABAM else 0
    data = load_file_content(filename, offset)
    for row in data:
        print get_data(client, row)
