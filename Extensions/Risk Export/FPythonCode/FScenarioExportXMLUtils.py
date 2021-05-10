""" Compiled: 2020-09-18 10:38:54 """

#__src_file__ = "extensions/risk_export/./etc/FScenarioExportXMLUtils.py"
PRIME_REPORT = "PRIMEReport"
MULTI_REPORT = "MultiReport"
REPORT_CONTENTS = "ReportContents"

TABLE = "Table"

NAME = "Name"
TYPE = "Type"
LABEL = "Label"

NUMBER_OF_COLUMNS = "NumberOfColumns"
COLUMNS = "Columns"
COLUMN = "Column"
COLUMN_ID = "ColumnId"
COLUMN_UNIQUE_ID = "ColumnUniqueId"
CONTEXT = "Context"
GROUP_LABEL = "GroupLabel"

SETTINGS = "Settings"
GROUPS = "Groups"
GROUP = "Group"

ROWS = "Rows"
ROW = "Row"
ROW_ID = "RowId"
INSTRUMENT = "Instrument"

CELLS = "Cells"
CELL = "Cell"

DEFAULT_DATA = "DefaultData"
RAW_DATA = "RawData"
FORMATTED_DATA = "FormattedData"


def mkpath(*path_items):
    return "/".join(path_items)
