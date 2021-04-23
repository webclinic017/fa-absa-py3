# coding=ascii
"""
Brendan Bosman      MINT-164.3      2015/09/03    1. Created as part of a refactoring process of
                                                    Triresolve_EMIRReportGenerator
Brendan Bosman      MINT-366        2015/09/15    Implement Non EU files
Main Purpose:
1. Class declarations of Emir Context

"""

import os

import re
from TriResolve_EMIR_MidasTradeColl import *

from TriResolve_EMIR_Const import *

import TriResolve_EMIR_StreamReaders


class BaseEMIRContext(object):
    """

    :param params:
    """

    def __init__(self, params, from_fa):
        """ Init BaseEMIRContext.

         This Init object is used to keep all input parameters for the processing

        :type params: dict
        :type self: BaseEMIRContext
        :rtype : BaseEMIRContext
        :param from_fa: it this is called from FA. This will assist is the macros
        :param params: dictionary of params
        """
        self._params = params
        self._from_fa = from_fa

        params[const_output_path] = self.demacroize(self.get_property(const_output_path, None), from_fa)
        params[const_issue_output_path] = self.demacroize(self.get_property(const_issue_output_path, None), from_fa)
        params[const_fxf_filtered_clients_path] = self.demacroize(self.get_property(const_fxf_filtered_clients_path, None), from_fa)

        # Read write_to_log_test from params. must be a boolean
        self.write_to_log_test = False
        if CONST_WRITE_TO_LOG_FILE in params.keys():
            b = params[CONST_WRITE_TO_LOG_FILE]
            if isinstance(b, type(True)):
                self.write_to_log_test = b

        self._output_path = self.get_property(const_output_path, None)
        self.issue_output_path = self.get_property(const_issue_output_path, None)
        self._is_front_arena_data_run = self.get_property(const_is_front_arena_data_run, None)
        self._use_trade_filter = self.get_property(const_use_trade_filter, None)
        self._error_output = None
        self._today = acm.Time.DateToday()
        self._tomorrow = acm.Time.DateAddDelta(self._today, 0, 0, 1)

        # Data checks
        if self._use_trade_filter:
            if not isinstance(self._use_trade_filter, type(True)):
                raise ValueError('_use_trade_filter is not a boolean')
        else:
            self._use_trade_filter = True

        self.load_properties()

        self._mappings = self.load_mappings()
        self._le_sds_ids = self.load_legal_entities()
        self._eu_cp_sds_ids = self.load_eu_counter_parties()
        self._non_eu_cp_ids = self.load_non_eu_counter_parties()
        self._le_names_by_front_id = dict((m.front_id, m.le_name) for m in self.get_mappings() if m.front_id)
        self._le_names_by_midas_id = dict((m.midas_id, m.le_name) for m in self.get_mappings() if m.midas_id)

        self._exc_fa_trades = self.get_property(const_exc_fa_trades, [])
        self._inc_fa_trades = self.get_property(const_inc_fa_trades, [])
        self._exc_midas_trades = self.get_property(const_exc_midas_trades, [])
        self._inc_midas_trades = self.get_property(const_inc_midas_trades, [])
        self._exc_fa_acquirers = [acm.FParty[acq.encode()] for acq in self.get_property(const_exc_fa_acquirers, [])]
        self._exclude_instypes = self.get_property(const_exclude_instypes, [])
        self._coll_fa_trades = self.get_property(const_coll_fa_trades, [])
        self._noncoll_fa_trades = self.get_property(const_noncoll_fa_trades, [])
        self._coll_midas_trades = self.get_property(const_coll_midas_trades, [])
        self._noncoll_midas_trades = self.get_property(const_noncoll_midas_trades, [])
        self._non_coll_instypes = self.get_property(const_non_coll_instypes, [])

        # Trades booked in these portfolios where OTS is False
        # will be marked as NON_COLLATERALIZED
        self._noncoll_nonotc_pf = self.get_property('noncoll_nonotc_pf', [])

        # Midas move portfolios - these will be looked up in FA
        self._midas_moved_pf = self.get_property('midas_moved_pf', [])

        # Midas Settlement portfolios - these will be excluded from selection.
        self._midas_stl_pf = self.get_property('midas_stl_pf', [])

    @staticmethod
    def demacroize(s, from_fa):
        """Returns the input string with macros replaced.
        :param from_fa:
        :param s:
        """

        def todayrepl_format(matchobj):
            """Today.
            :param matchobj:
            """
            today = at.date_to_datetime(acm.Time.DateToday())
            ##
            return today.strftime(matchobj.group(1))

        def nextbdrepl_format(matchobj):
            """Next business day.
            :param matchobj:
            """
            cal = acm.FInstrument['ZAR'].Calendar()
            today = acm.Time.DateToday()
            nextbd = at.date_to_datetime(cal.AdjustBankingDays(today, 1))
            ##
            return nextbd.strftime(matchobj.group(1))

        if from_fa:
            s = re.sub('{TODAY:([^}]+)}', todayrepl_format, s)
            s = re.sub('{NEXTBD:([^}]+)}', nextbdrepl_format, s)
            # add more macros here if necessary...
        ##
        return s

    def load_mappings(self):
        """
        This function can be seen as a virtual abstract method that has to create mappings
        """
        return []

    def load_legal_entities(self):
        """This file upload the legal entities

        This is a tuple of legal entities which is a tuple of int



        :rtype : tuple
        :return:
        """
        return []

    def load_eu_counter_parties(self):
        """This file upload the eu collatoral counter entities

        This is a tuple of legal entities which is a tuple of int



        :rtype : tuple
        :return:
        """
        return []

    def load_non_eu_counter_parties(self):
        """This file upload the non eu collatoral counter entities

        This is a tuple of legal entities which is a tuple of int


        :rtype : tuple
        :return:
        """
        return []

    def load_properties(self):
        """ Load properties from file

        This methos acts as a virtual abstract. All descendents must override this method
        """
        pass

    def get_property(self, property_name, default_value):
        """

        :param property_name:
        :param default_value:
        :return:
        """
        result = default_value
        if property_name in self._params.keys():
            result = self._params[property_name]
        return result

    def get_exc_fa_trades(self):
        """


        :return:
        """
        return self._exc_fa_trades

    def get_inc_fa_trades(self):
        """


        :return:
        """
        return self._inc_fa_trades

    def get_exc_midas_trades(self):
        """


        :return:
        """
        return self._exc_midas_trades

    def get_inc_midas_trades(self):
        """


        :return:
        """
        return self._inc_midas_trades

    def get_exc_fa_acquirers(self):
        """


        :return:
        """
        return self._exc_fa_acquirers

    def get_exclude_instypes(self):
        """


        :return:
        """
        return self._exclude_instypes

    def get_coll_fa_trades(self):
        """


        :return:
        """
        return self._coll_fa_trades

    def get_noncoll_fa_trades(self):
        """


        :return:
        """
        return self._noncoll_fa_trades

    def get_coll_midas_trades(self):
        """


        :return:
        """
        return self._coll_midas_trades

    def get_noncoll_midas_trades(self):
        """


        :return:
        """
        return self._noncoll_midas_trades

    def get_noncoll_nonotc_pf(self):
        """


        :return:
        """
        return self._noncoll_nonotc_pf

    def get_midas_moved_pf(self):
        """


        :return:
        """
        return self._midas_moved_pf

    def get_midas_stl_pf(self):
        """


        :return:
        """
        return self._midas_stl_pf

    def get_output_path(self):
        """

        :param self:
        :return:
        """
        return self._output_path

    def get_non_coll_instypes(self):
        """

        :param self:
        :return:
        """
        return self._non_coll_instypes

    def print_params(self):
        """
        Printing the params
        """
        print("Print params begin")
        i = 0
        for s in self._params.keys():
            print(str(i) + ": " + s + ": " + str(self._params[s]))
            i += 1
        print("Print params end")

    def get_params(self):
        """

        :rtype : object
        """
        return self._params

    def get_issue_output_path(self):
        """

        :param self:
        :return:
        """
        return self.issue_output_path

    def get_error_output(self):
        """

        :param self:
        :return:
        """
        return self._error_output

    def get_today(self):
        """


        :return:
        """
        return self._today

    def get_tomorrow(self):
        """


        :return:
        """
        return self._tomorrow

    def get_is_front_arena_data_run(self):
        """


        :return:
        """
        return self._is_front_arena_data_run

    def get_use_trade_filter(self):
        """



        :rtype : bool
        :return:
        """
        return self._use_trade_filter

    def get_mappings(self):
        """

        :param self:
        :return:
        """
        return self._mappings

    def get_le_names_by_front_id(self):
        """

        :param self:
        :return:
        """
        return self._le_names_by_front_id

    def get_le_names_by_midas_id(self):
        """

        :param self:
        :return:
        """
        return self._le_names_by_midas_id

    def get_le_sds_ids(self):
        """

        :param self:
        :return:
        """
        return self._le_sds_ids

    def get_eu_cp_sds_ids(self):
        """

        :param self:
        :return:
        """
        return self._eu_cp_sds_ids

    def get_non_eu_cp_ids(self):
        """

        :param self:
        :return:
        """
        return self._non_eu_cp_ids

    def get_write_to_log_test(self):
        """


        :return:
        """
        return self.write_to_log_test


class EMIRContext(BaseEMIRContext):
    """

    :param params:
    :param from_fa:
    """

    def __init__(self, params, from_fa):
        """

        :type params: TriResolve_EMIR_Context.EMIRContext
        """
        super(EMIRContext, self).__init__(params, from_fa)

    def load_mappings(self):
        """


        :return: :raise ValueError:
        """

        # File 1: midas_map file
        # Counterparty mappings among different systems

        self._params[const_midas_map_path] = self.demacroize(self._params[const_midas_map_path], self._from_fa)
        filename = self._params[const_midas_map_path]
        file_exist = True
        file_exist &= os.path.exists(filename)
        file_exist &= os.path.isfile(filename)
        if not file_exist:
            raise ValueError('midas_map file does not exist. Filename: ' + self._params[const_midas_map_path])

        print("Mapping file: " + filename + " found.")
        with open(filename, 'rb') as f:
            result = TriResolve_EMIR_StreamReaders.FileReaders.load_all_mapping_items_from_iostream(f)
        print("Mapping file: " + filename + " read.")
        return result

    def load_legal_entities(self):
        """


        :return: :raise ValueError:
        """
        # File 2: Legal entities file

        self._params[const_le_sds_ids_path] = self.demacroize(self._params[const_le_sds_ids_path], self._from_fa)
        filename = self._params[const_le_sds_ids_path]
        file_exist = True
        file_exist &= os.path.exists(filename)
        file_exist &= os.path.isfile(filename)
        if not file_exist:
            raise ValueError('Legal entities file does not exist. Filename: ' + self._params[const_le_sds_ids_path])

        print("Legal entities file: " + filename + " found.")
        with open(filename, 'rb') as f:
            result = TriResolve_EMIR_StreamReaders.FileReaders.read_csv_file_sdsid_description(f)
        print("Legal entities file: " + filename + " read.")

        return result

    def load_eu_counter_parties(self):
        """


        :return: :raise ValueError:
        """
        # File 3: CP file
        self._params[const_cp_sds_ids_path] = self.demacroize(self._params[const_cp_sds_ids_path], self._from_fa)
        filename = self._params[const_cp_sds_ids_path]
        file_exist = True
        file_exist &= os.path.exists(filename)
        file_exist &= os.path.isfile(filename)
        if not file_exist:
            raise ValueError('Counter parties file does not exist. Filename: ' + self._params[const_cp_sds_ids_path])

        print("EU Counter parties entities file: " + filename + " found.")
        with open(filename, 'rb') as f_cp_sds:
            result = TriResolve_EMIR_StreamReaders.FileReaders.inflate_cp_sds_ids_from_iostream(f_cp_sds)
        print("EU Counter parties entities file: " + filename + " read.")

        return result

    def load_non_eu_counter_parties(self):
        """


        :return: :raise ValueError:
        """
        # File : NON  EU CP file
        self._params[const_le_sds_non_coll_ids_path] = self.demacroize(self._params[const_le_sds_non_coll_ids_path], self._from_fa)
        filename = self._params[const_le_sds_non_coll_ids_path]
        file_exist = True
        file_exist &= os.path.exists(filename)
        file_exist &= os.path.isfile(filename)

        if file_exist:
            print("NON EU Counter parties entities file: " + filename + " found.")
            with open(filename, 'rb') as f_cp_sds:
                result = TriResolve_EMIR_StreamReaders.FileReaders.read_csv_file_sdsid_description(f_cp_sds)
            print("NON EU Counter parties entities file: " + filename + " read.")

            return result
        else:
            print("NON EU Counter parties entities file: " + filename + " does not exist.")
            return []

    def load_properties(self):
        """


        :raise ValueError:
        """
        # File 4: config file
        self._params['config_path'] = self.demacroize(self._params['config_path'], self._from_fa)
        config_path = self._params['config_path']
        file_exist = True
        file_exist &= os.path.exists(config_path)
        file_exist &= os.path.isfile(config_path)
        if not file_exist:
            raise ValueError('Config file does not exist. Filename: ' + config_path)

        # Load the configuration data to the params
        with open(config_path, 'r') as config_file:
            TriResolve_EMIR_StreamReaders.FileReaders.read_properties_from_iostream(self._params, config_file)


class EMIRContextForTesting(BaseEMIRContext):
    """

    :param params:
    :param from_fa:
    """

    def __init__(self, params, from_fa):
        """

        :type params: TriResolve_EMIR_Context.EMIRContextForTesting
        """
        super(EMIRContextForTesting, self).__init__(params, from_fa)
