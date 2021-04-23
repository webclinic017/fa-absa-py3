"""-------------------------------------------------------------------------------------------------------
MODULE
    FReportSettings - Settings for reporting system

-------------------------------------------------------------------------------------------------------"""

# Command to FO renderer, typically FOP.
FOP_BAT = r'call "C:\program files\fop\fop.bat" "${filename}.fo" -${extension} "${filename}.${extension}"'

# Standard file extensions for secondary output
FILE_EXTENSIONS = ['.pdf', '.xls', '.csv', '.txt']
