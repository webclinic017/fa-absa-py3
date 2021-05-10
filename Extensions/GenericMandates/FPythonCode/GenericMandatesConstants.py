"""
This file contains constants that specify string types associated with them.
"""

# Limit specification names for each mandate type
M_TYPE_TRADER = "Mandate - Trader Group"
M_TYPE_PORTFOLIO = "Mandate - Portfolio"
M_TYPE_COUNTERPARTY = "Mandate - Counterparty"

# Limit specification descriptions for each mandate type
M_DESCR_TRADER = "Limit specification for the Trader Group mandates."
M_DESCR_PORTFOLIO = "Limit specification for the Portfolio mandates."
M_DESCR_COUNTERPARTY = "Limit specification for the Counterparty mandates."

# Limit method names
M_METHOD_TRADER = "FUserGroup"
M_METHOD_PORTFOLIO = "FPhysicalPortfolio"
M_METHOD_COUNTERPARTY = "FCounterparty"

# Additional info names
MANDATE_TYPE = "Mandate_Type"
MANDATE_TARGET = "Mandate_Target"

# SQL TextObject names
MANDATE_TEXT_OBJECT_TYPE = "Customizable"
MANDATE_TEXT_OBJECT_SUBTYPE = "Mandates"

# ADFL Column string values
MANDATE_ALLOWED_TEXT = "Allowed"
MANDATE_NOT_ALLOWED_TEXT = "Not Allowed"
MANDATE_NOT_FOUND_TEXT = "No Mandate Found"

# Limit blocking types
MANDATE_LIMIT_BLOCKING = "Blocking"
MANDATE_LIMIT_NON_BLOCKING = "Allow comment"
MANDATE_LIMIT_UNKNOWN = "Unknown"

# Limit specification names
MANDATE_SPEC_TRADER = "Mandate - Trader Group"
MANDATE_SPEC_PORTFOLIO = "Mandate - Portfolio"
MANDATE_SPEC_COUNTERPARTY = "Mandate - Counterparty"

# Query folder name to set limit on
MANDATE_QUERY_FOLDER_NAME = "TradesForToday"
# Query folder name for "special" query filters
MANDATE_QUERY_FOLDER_SPECIAL_NAME = "Mandate - Trade Filter Template"
# Query folder to select "rules" for mandate
MANDATE_QUERY_FOLDER_SELECT_FOLDERS_NAME = "Mandate - Applicable Query Filters"

# Create Mandate GUI display constants
MANDATE_GUI_BLOCKING = "Blocking"
MANDATE_GUI_NON_BLOCKING = "Non-Blocking"

# FParameter constants used as keys
FPARAM_VIOLATION_EMAIL_SENDER = "Violation Email Sender"
FPARAM_VIOLATION_EMAIL_RECIPIENT = "Violation Email Recipient"
FPARAM_VIOLATION_EMAIL_SERVER = "Violation Email Server"
FPARAM_VIOLATION_EMAIL_ENABLED = "Violation Email Enabled"
FPARAM_PRODUCT_SUPERVISOR_PROFILES = "Product Supervisor Checking Enabled"
FPARAM_LIMIT_PROTECTION = "LimitProtectionLevel"
FPARAM_LIMIT_OWNER = "LimitOwnerName"

# Operations used in User Profiles
OPERATION_CREATE = 'Mandate Creation'
OPERATION_MODIFY = 'Mandate Modification'
OPERATION_DEACTIVATE = 'Mandate Deactivation'
OPERATION_AUTHORIZE = 'Mandate Authorization'
OPERATION_SAVE = 'Mandate Save to DB'

# Africa Supervisor User Group
SUPERVISOR_GROUP_NAME = 'Africa Supervisors'
