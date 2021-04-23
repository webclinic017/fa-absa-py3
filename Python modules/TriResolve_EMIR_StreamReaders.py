# coding=ascii
"""

Brendan Bosman      MINT-366        2015/09/15      Implement Non EU files

"""

from TriResolve_EMIR_Const import *

import json
import csv


class FileReaders:
    """ Static class

    """

    def __init__(self):
        pass

    @staticmethod
    def read_csv_file_sdsid_description(iostream):
        """


        :rtype : object
        :param iostream:
        :return:
        """
        reader = csv.reader(iostream)
        next(reader)  # Skipping header
        try:
            result = [int(row[0]) for row in reader if row[0]]
        except:
            # No recourd other than header
            result = []
        return result

    @staticmethod
    def load_all_mapping_items_from_iostream(iostream):
        """


        :rtype : object
        :param iostream:
        :return:
        """
        result = []

        reader = csv.reader(iostream, delimiter='|')
        next(reader)  # skipping header
        for row in reader:
            front_id = int(row[5]) if row[5].isdigit() else None
            le_name = row[0]
            le_sdsid = int(row[2]) if row[2].isdigit() else None
            cp_sdsid = int(row[3]) if row[3].isdigit() else None
            midas_id = int(row[6]) if row[6].isdigit() else None
            if front_id or midas_id:
                result.append(MappingItem(front_id, le_name, le_sdsid, cp_sdsid, midas_id))

        return result

    @staticmethod
    def inflate_cp_sds_ids_from_iostream(iostream):
        """

        :param iostream:
        :return:
        """

        reader = csv.reader(iostream, delimiter='|')
        next(reader)  # skipping header
        # keeping the isdigit()... csv maybe keeps the newlines? so row[3] evaluates to true
        result = [int(row[3]) for row in reader if len(row) > 3 and row[3].isdigit()]
        return result

    @staticmethod
    def read_properties_from_iostream(params, iostream):

        """

        :param params:
        :param iostream:
        """
        config = json.load(iostream)
        params.update(config)
