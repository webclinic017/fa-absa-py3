"""MODULE FReportSettings - Settings for reporting system"""

import platform

if platform.system() == 'Windows':
    # Command to FO renderer, typically FOP.
    FOP_BAT = r'""Y:\Jhb\Arena\Prime\FOP\fop.bat" "${filename}.fo" -${extension} "${filename}.${extension}" -c "Y:\Jhb\Arena\Prime\FOP\conf\config.xml""'
    
    # Default path to logos
    LOGOS_PATH = r'Y:\Jhb\Arena\Data\Confirmations\Logos'
    
    # Path to logos used by STATIC_TEMPLATE_IS
    LOGOS_PMO_PATH = r'/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/InterestStatements/Logos' 
    
    # Path to XSLT templates
    XSLT_PATH = r'Y:\Jhb\Arena\Data\Confirmations\Templates'
else: # Linux backend
    # Command to FO renderer, typically FOP.
    # FOP_BAT = r'""/apps/services/front/FOP/fop-1.0/fop" "${filename}.fo" -${extension} "${filename}.${extension}" -c "/apps/services/front/FOP/fop-1.0/conf/config.xml""'
    
    #2016-12-02 CHNG0004158449
    #FOP_BAT ='"/apps/services/front/FOP/fop-1.0/fop" ${filename}.fo ${filename}.${extension}'
    FOP_BAT ='"/apps/services/front/FOP/fop-1.0/fop" "${filename}.fo" "${filename}.${extension}"'
    
    # Default path to logos
    LOGOS_PATH = r'/apps/services/front/FOP/fop-1.0/Images'
    
    # Path to logos used by STATIC_TEMPLATE_IS
    LOGOS_PMO_PATH = r'/nfs/fa/reports/EMEA/prod/FAReports/AtlasEndOfDay/InterestStatements/Logos' 
    
    # Path to XSLT templates
    XSLT_PATH = r'/apps/services/front/FOP/fop-1.0/Templates'

# Standard file extensions for secondary output
FILE_EXTENSIONS = ['.pdf', '.xls', '.csv', '.txt']

# --- Debugging --- 
# Keep XML:FO files
KEEP_FO = 0

# Keep XML files
KEEP_XML = 0

# Keep partial pdf files
KEEP_PARTIAL_PDF = 0

# Validate XML file before transformation
VALIDATE_XML = 1
