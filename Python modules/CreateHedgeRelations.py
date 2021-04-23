# HedgeDataTakeOn

import re

import acm
import FLogger

import HedgeRelation
import HedgeDealPackage
import HedgeConstants
import HedgeUtils

FLOG = FLogger.FLogger(__name__)

# default column structure
EXPECTED_COLUMNS = 'RelationshipId,'\
                   'Type,'\
                   'SubType,'\
                   'RiskType,'\
                   'Objective,'\
                   'HedgeStatus,'\
                   'ProTest,'\
                   'RetTest,'\
                   'External,'\
                   'ExternalPercentage,'\
                   'Internal,'\
                   'InternalPercentage,'\
                   'Hypo,'\
                   'HypoPercentage,'\
                   'Original,'\
                   'OriginalPercentage,'\
                   'ZeroBond,'\
                   'DesignationDate'

EXPECTED_COLUMN_LENGTH = 18

RELATIONSHIP_INDEX = 0
TYPE_INDEX = 1
SUBTYPE_INDEX = 2
RISKTYPE_INDEX = 3
OBJECTIVE_INDEX = 4
HEDGE_STATUS_INDEX = 5
PROTYPE_INDEX = 6
RETTYPE_INDEX = 7
EXTERNAL_INDEX = 8
EXTERNAL_PERCENTAGE_INDEX = 9
INTERNAL_INDEX = 10
INTERNAL_PERCENTAGE_INDEX = 11
HYPO_INDEX = 12
HYPO_PERCENTAGE_INDEX = 13
ORIGINAL_INDEX = 14
ORIGINAL_PERCENTAGE_INDEX = 15
ZERO_BOND_INDEX = 16
DESIGNATION_DATE_INDEX = 17

ALLOWED_HEDGE_TYPES = [m_type.Name() for m_type in HedgeUtils.get_hedge_types()]
ALLOWED_HEDGE_SUB_TYPES = [m_type.Name() for m_type in HedgeUtils.get_hedge_sub_types()]
ALLOWED_HEDGE_RISK_TYPES = [m_type.Name() for m_type in HedgeUtils.get_risk_types()]
ALLOWED_HEDGE_STATUS_TYPES = HedgeConstants.Hedge_Relation_Status().get_all_as_list()

ALLOWED_PRO_TESTS = ['ProDollarOffset', 'Regression', 'CriticalTerms', 'ProVRM']
ALLOWED_RET_TESTS = ['RetroDollarOffset', 'RetroVRM']


path_selection = acm.FFileSelection()
path_selection.PickDirectory(False)
path_selection.SelectedFile(r"C:\temp\HE\Hedge RelationshipsFull.csv")
tooltip = 'The path where the Hedge Relationship csv is located.'

ael_variables = [
    ['InputPath', 'Input Path', path_selection, None, path_selection, 0, 1, tooltip, None, 1]
]


def ParseDate(input_date):
    # 2017-12-07
    if re.match('^[0-9]{4}-[0-1][0-9]-[0-3][0-9]$', input_date):
        year, month, day = input_date.split('-')
        try:
            return acm.Time.DateFromYMD(year, month, day)
        except:
            pass

    # 2017/12/07
    if re.match('^[0-9]{4}/[0-1][0-9]/[0-3][0-9]$', input_date):
        year, month, day = input_date.split('/')
        try:
            return acm.Time.DateFromYMD(year, month, day)
        except:
            pass

    # 07/12/2017
    if re.match('^[0-3][0-9]/[0-1][0-9]/[0-9]{4}$', input_date):
        day, month, year = input_date.split('/')
        try:
            return acm.Time.DateFromYMD(year, month, day)
        except:
            pass
    return None


def GetSoonestEndDate(trade_list):
    '''This function will loop through all the trades in the current hedge
        relationship and find the soonest end date on the relevant instruments.
    '''

    champion = '9999/12/31'
    for tradeId in trade_list:
        trd = acm.FTrade[tradeId]
        ins = trd.Instrument()
        if ins.EndDate() < champion:
            champion = ins.EndDate()
    return champion


def TestRowValidity(row):
    '''Function will return a list of errors to assist the users in correcting source data
    '''

    errors = []

    if len(row) != EXPECTED_COLUMN_LENGTH:
        errors.append('Expect each row to have %i columns' % EXPECTED_COLUMN_LENGTH)
        return errors

    # Static Data
    if not row[RELATIONSHIP_INDEX]:
        errors.append('UniqueId must be populated')
    if row[TYPE_INDEX]:
        if row[TYPE_INDEX] not in ALLOWED_HEDGE_TYPES:
            errors.append('Hedge Type must be valid, "%s" does not exist as Hedge Type'
                          % row[TYPE_INDEX])
    else:
        errors.append('Hedge Type must be populated')
    if row[SUBTYPE_INDEX]:
        if row[SUBTYPE_INDEX] not in ALLOWED_HEDGE_SUB_TYPES:
            errors.append('Hedge Sub Type must be valid, "%s" does not exist as Hedge Sub Type'
                          % row[SUBTYPE_INDEX])
    else:
        errors.append('Hedge Sub Type must be populated')
    if row[RISKTYPE_INDEX]:
        if row[RISKTYPE_INDEX] not in ALLOWED_HEDGE_RISK_TYPES:
            errors.append('Hedge Risk Type must be valid, "%s" does not exist as Hedge Risk Type'
                          % row[RISKTYPE_INDEX])
    else:
        errors.append('Hedge Risk Type must be populated')
    if row[HEDGE_STATUS_INDEX]:
        if row[HEDGE_STATUS_INDEX] not in ALLOWED_HEDGE_STATUS_TYPES:
            errors.append('Hedge Status must be valid, "%s" does not exist as a Hedge Status'
                          % row[HEDGE_STATUS_INDEX])

    # Test Types
    if row[PROTYPE_INDEX]:
        if row[PROTYPE_INDEX] not in ALLOWED_PRO_TESTS:
            errors.append('Prospective Test must be valid, "%s" does not exist as Prospective Test '
                          'Type' % row[PROTYPE_INDEX])
    if row[RETTYPE_INDEX]:
        if row[RETTYPE_INDEX] not in ALLOWED_RET_TESTS:
            errors.append('Retrospective Test must be valid, "%s" does not exist as Retrospective '
                          'Test Type' % row[RETTYPE_INDEX])

    date = ParseDate(row[DESIGNATION_DATE_INDEX])
    if date is None:
        errors.append("Can't convert '%s' to datetime" % row[DESIGNATION_DATE_INDEX])
    elif date != row[DESIGNATION_DATE_INDEX]:
        row[DESIGNATION_DATE_INDEX] = date

    try:
        external_percentage = row[EXTERNAL_PERCENTAGE_INDEX]
        if external_percentage:
            external_percentage = float(external_percentage)
            if 0.0 > external_percentage or external_percentage > 100.0:
                errors.append("External percentage '%s' must be between 0 and 100"
                              % row[EXTERNAL_PERCENTAGE_INDEX])
    except:
        errors.append("Can't convert external percentage '%s' to float"
                      % row[EXTERNAL_PERCENTAGE_INDEX])

    try:
        internal_percentage = row[INTERNAL_PERCENTAGE_INDEX]
        if internal_percentage:
            internal_percentage = float(internal_percentage)
            if 0.0 > internal_percentage or internal_percentage > 100.0:
                errors.append("Internal percentage '%s' must be between 0 and 100"
                              % row[INTERNAL_PERCENTAGE_INDEX])
    except:
        errors.append("Can't convert internal percentage '%s' to float"
                      % row[INTERNAL_PERCENTAGE_INDEX])

    try:
        hypo_percentage = row[HYPO_PERCENTAGE_INDEX]
        if hypo_percentage:
            hypo_percentage = float(hypo_percentage)
            if 0.0 > hypo_percentage or hypo_percentage > 100.0:
                errors.append("Hypo percentage '%s' must be between 0 and 100"
                              % row[HYPO_PERCENTAGE_INDEX])
    except:
        errors.append("Can't convert hypo percentage '%s' to float" % row[HYPO_PERCENTAGE_INDEX])

    try:
        original_percentage = row[ORIGINAL_PERCENTAGE_INDEX]
        if original_percentage:
            original_percentage = float(original_percentage)
            if 0.0 > original_percentage or original_percentage > 100.0:
                errors.append("Original percentage '%s' must be between 0 and 100"
                              % row[ORIGINAL_PERCENTAGE_INDEX])
    except:
        errors.append("Can't convert original percentage '%s' to float"
                      % row[ORIGINAL_PERCENTAGE_INDEX])

    if row[EXTERNAL_INDEX]:
        if not acm.FTrade[row[EXTERNAL_INDEX]]:
            errors.append("External trade '%s' must exist in Front Arena" % row[EXTERNAL_INDEX])
    if row[INTERNAL_INDEX]:
        if not acm.FTrade[row[INTERNAL_INDEX]]:
            errors.append("Internal trade '%s' must exist in Front Arena" % row[INTERNAL_INDEX])
    if row[HYPO_INDEX]:
        if not acm.FTrade[row[HYPO_INDEX]]:
            errors.append("Hypo trade '%s' must exist in Front Arena" % row[HYPO_INDEX])
    if row[ORIGINAL_INDEX]:
        if not acm.FTrade[row[ORIGINAL_INDEX]]:
            errors.append("Original trade '%s' must exist in Front Arena" % row[ORIGINAL_INDEX])
    if row[ZERO_BOND_INDEX]:
        if not acm.FTrade[row[ZERO_BOND_INDEX]]:
            errors.append("ZeroBond trade '%s' must exist in Front Arena" % row[ZERO_BOND_INDEX])

    return errors


def GetTestSettings(config_row):
    '''Returns the default Hedge Effectiveness Test settings.
    '''
    hedge_type = config_row[TYPE_INDEX]
    sub_type = config_row[SUBTYPE_INDEX]
    risk_type = config_row[RISKTYPE_INDEX]
    objective = config_row[OBJECTIVE_INDEX]
    pro_type = config_row[PROTYPE_INDEX]
    ret_type = config_row[RETTYPE_INDEX]

    testsettings = {}
    testsettings['Properties'] = {
        'HedgeType': hedge_type,
        'HedgeSubType': sub_type,
        'HedgeRiskType': risk_type,
        'HedgeObjective': objective,
    }
    testsettings['ProDollarOffset'] = {
        'Enabled': False,
        'LoLimit': HedgeConstants.DBL_PRO_DO_LO_LIMIT,
        'HiLimit': HedgeConstants.DBL_PRO_DO_HI_LIMIT,
        'LoWarning': HedgeConstants.DBL_PRO_DO_LO_WARNING,
        'HiWarning': HedgeConstants.DBL_PRO_DO_HI_WARNING,
    }
    testsettings['Regression'] = {
        'Enabled': False,
        'HiBetaLimit': HedgeConstants.DBL_PRO_REG_HI_B_LIMIT,
        'LoBetaLimit': HedgeConstants.DBL_PRO_REG_LO_B_LIMIT,
        'R2Limit': HedgeConstants.DBL_PRO_REG_R2_LIMIT,
        'PValueLimit': HedgeConstants.DBL_PRO_REG_P_LIMIT,
        'HiBetaWarning': HedgeConstants.DBL_PRO_REG_HI_B_WARNING,
        'LoBetaWarning': HedgeConstants.DBL_PRO_REG_LO_B_WARNING,
        'R2Warning': HedgeConstants.DBL_PRO_REG_R2_WARNING,
        'PValueWarning': HedgeConstants.DBL_PRO_REG_P_WARNING,
    }
    testsettings['CriticalTerms'] = {
        'Enabled': False,
    }
    testsettings['ProVRM'] = {
        'Enabled': False,
        'Limit': HedgeConstants.DBL_PRO_VRM_LIMIT,
        'Warning': HedgeConstants.DBL_PRO_VRM_WARNING,
    }
    testsettings['RetroDollarOffset'] = {
        'Enabled': False,
        'LoLimit': HedgeConstants.DBL_RETRO_DO_LO_LIMIT,
        'HiLimit': HedgeConstants.DBL_RETRO_DO_HI_LIMIT,
        'LoWarning': HedgeConstants.DBL_RETRO_DO_LO_WARNING,
        'HiWarning': HedgeConstants.DBL_RETRO_DO_HI_WARNING,
    }
    testsettings['RetroVRM'] = {
        'Enabled': False,
        'Limit': HedgeConstants.DBL_RETRO_VRM_LIMIT,
        'Warning': HedgeConstants.DBL_RETRO_VRM_WARNING,
    }
    testsettings['TimeBuckets'] = {
        'TimeBuckets': HedgeConstants.STR_DEFAULT_TIME_BUCKETS,
    }
    if pro_type in testsettings.keys():
        testsettings[pro_type]['Enabled'] = True
    else:
        testsettings['ProDollarOffset']['Enabled'] = True
    if ret_type in testsettings.keys():
        testsettings[ret_type]['Enabled'] = True
    else:
        testsettings['RetroDollarOffset']['Enabled'] = True
    return testsettings


def DoDataTakeOn(input_path):
    '''This function will loop through the rows in the given csv and create a
        dictionary which contains the legacy hedge id and the new front arena id.
    '''

    hedge_old_to_new_id_mapping = {}
    failed_ids = set()
    file_rows_grouped = {}

    try:
        with open(str(input_path.SelectedFile()), 'rb') as f:
            all_rows = f.read()
    except Exception, e:
        FLOG.ELOG('Critical Error opening csv: %s' % str(e))
        raise
    all_rows = all_rows.split('\r\n')
    print(len(all_rows))
    all_rows = all_rows[1:]  # Skip header row
    print(len(all_rows))
    FLOG.LOG("Column order expected: %s" % EXPECTED_COLUMNS)

    for row in all_rows:

        if len(row) <= 1:
            continue
        row = row.split('|')

        # check row validity
        errors = TestRowValidity(row)
        if errors:
            for msg in errors:
                FLOG.ELOG(msg)
            if row[RELATIONSHIP_INDEX]:
                failed_ids.add(row[RELATIONSHIP_INDEX])
            continue

        # Don't process errored relationships
        if row[RELATIONSHIP_INDEX] in failed_ids:
            continue

        if row[RELATIONSHIP_INDEX] in file_rows_grouped.keys():
            file_rows_grouped[row[RELATIONSHIP_INDEX]].append(row)
        else:
            new_config_list = []
            new_config_list.append(row)
            file_rows_grouped[row[RELATIONSHIP_INDEX]] = new_config_list

    for old_id_key in file_rows_grouped:
        # Don't process errored relationships
        if old_id_key in failed_ids:
            continue
        try:
            # 1. build the trade list
            trade_list = {}

            for config_row in file_rows_grouped[old_id_key]:
                externalId = config_row[EXTERNAL_INDEX]
                extPercent = config_row[EXTERNAL_PERCENTAGE_INDEX]
                externalPercentage = extPercent if extPercent else 100
                internalId = config_row[INTERNAL_INDEX]
                intPercent = config_row[INTERNAL_PERCENTAGE_INDEX]
                internalPercentage = intPercent if intPercent else 100
                hypoId = config_row[HYPO_INDEX]
                hypPercent = config_row[HYPO_PERCENTAGE_INDEX]
                hypoPercentage = hypPercent if hypPercent else 100
                originalId = config_row[ORIGINAL_INDEX]
                oriPercent = config_row[ORIGINAL_PERCENTAGE_INDEX]
                originalPercentage = oriPercent if oriPercent else 100
                zero_bondId = config_row[ZERO_BOND_INDEX]

                if externalId:
                    trade_list[externalId] = [HedgeConstants.Hedge_Trade_Types.External,
                                              externalPercentage,
                                              '']

                if internalId:
                    trade_list[internalId] = [HedgeConstants.Hedge_Trade_Types.Internal,
                                              internalPercentage,
                                              '']

                if hypoId:
                    trade_list[hypoId] = [HedgeConstants.Hedge_Trade_Types.Hypo,
                                          hypoPercentage,
                                          '']

                if originalId:
                    trade_list[originalId] = [HedgeConstants.Hedge_Trade_Types.Original,
                                              originalPercentage,
                                              '']

                if zero_bondId:
                    trade_list[zero_bondId] = [HedgeConstants.Hedge_Trade_Types.ZeroBond,
                                               100,
                                               '']

            designation_date = config_row[DESIGNATION_DATE_INDEX]
            end_date = GetSoonestEndDate(trade_list)
            hedge_status = config_row[HEDGE_STATUS_INDEX]

            # 2. create the HedgeRelation
            hedge_relationship = HedgeRelation.HedgeRelation(None)
            hedge_relationship.new()

            hedge_relationship.set_trades(trade_list)
            hedge_relationship.set_status(HedgeConstants.Hedge_Relation_Status.Simulated)
            hedge_relationship.set_inception_date(designation_date)
            hedge_relationship.set_start_date(designation_date)
            hedge_relationship.set_end_date(end_date)

            testsettings = GetTestSettings(config_row)
            hedge_relationship.set_test_settings(testsettings)

            # initialise return variables
            names = [None, None]
            updatedTradeList = None

            try:

                # first save to build the HR name to be used when creating the Deal Package as well.
                hedge_relationship.save()

                # re-retrieve Id after it was set on TextObject creation
                hedgeRelationshipName = hedge_relationship.get_id()
                status = hedge_relationship.get_status()

                # Create DealPackage
                names, updatedTradeList = HedgeDealPackage.set_dealpackage(
                    None,
                    hedgeRelationshipName,
                    trade_list,
                    designation_date,
                    status,
                    None
                )

            except Exception, ex:
                print(ex)
                message = 'Error creating new Deal Package for Hedge Relationship %s. Message: %s'\
                          % (ex, hedgeRelationshipName)
                FLOG.ELOG(message)
                raise

            if updatedTradeList:
                hedge_relationship.set_trades(updatedTradeList)

            if names and len(names) > 1 and names[0] and names[1]:
                hedge_relationship.set_dealpackage(names[0], names[1])

            if hedge_status:
                hedge_relationship.set_status(hedge_status)

            # save completed HedgeRelation
            hedge_relationship.save()
            hedge_old_to_new_id_mapping[old_id_key] = hedgeRelationshipName

        except Exception, ex:
            message = 'Exception creating Hedge Relationship for config item:\n%s\n\n\t%s'\
                      % (file_rows_grouped[old_id_key], ex)
            failed_ids.add(old_id_key)
            FLOG.ELOG(message)

    return hedge_old_to_new_id_mapping, failed_ids


def ael_main(params):
    '''Main entry point
    '''

    file_name = 'DataTakeOn '
    for t in str(acm.Time.TimeNow()).replace(':', ''):
        if ord(t) in range(48, 57 + 1) or ord(t) == 32:  # Read only numbers and spaces
            file_name += t

    input_path = params['InputPath']

    # Create log file in the same location as source file
    folders = str(input_path).split('\\')
    m_file = len(folders) - 1
    folders[m_file] = '%s.log' % file_name
    path = '\\'.join(folders)
    FLOG.Reinitialize(logToFileAtSpecifiedPath=path)

    m_map, failed = DoDataTakeOn(input_path)

    # Log results
    if failed:
        message = 'The following old hedge relation IDs failed: \n'
        id_string = ''
        for m_id in failed:
            id_string += '\t\t%s\n' % m_id
        FLOG.LOG(message + '%s' % id_string)
    if m_map:
        message = 'The following relations were successfully loaded : \n'
        map_string = ''
        for key in m_map:
            map_string += '\t\t%s\t->\t%s\n' % (key, m_map[key])
        FLOG.LOG(message + '%s' % map_string)

    # Close logger files
    log = FLOG.logger.logger
    FLOG.logger.closeFileHandlers(log)
