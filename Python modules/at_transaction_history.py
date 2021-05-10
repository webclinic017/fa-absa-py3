"""
Module
    at_transaction_history.py

Description
    Helper module to provide abstraction when working with transaction history

History
Date          Developer          Description
--------------------------------------------------------------------------------
2020-10-02    Marcus Ambrose     Implement
"""
from datetime import datetime

import acm


class TransactionHistoryHelper:
    # Each table in report is separated by 47 hyphens
    REPORT_SEPARATOR = "-" * 47
    IGNORE_UPDATES = ["Update Time", "Update User", "Version"]

    def __init__(self, record_type, record):
        self.record_type = record_type
        self.record_id = self._get_record_id(record)

        self.transactions = self._get_record_transaction_history()

    def get_all_transactions(self):
        return self.transactions

    def get_latest_transaction(self):
        return self._get_record_transaction_history()[-1]

    def get_latest_transaction_details(self):
        return self.get_transaction_details(self.get_latest_transaction())

    def get_transaction_details(self, transaction):
        comparison_report = transaction.Compare(
            transaction.GetPreviousTransaction(), False, False
        )

        comparison_dict = self._transform_to_dict(comparison_report)

        return self._add_transaction_details_to_dict(comparison_dict, transaction)

    @staticmethod
    def _get_record_id(record):
        try:
            return int(record)
        except ValueError:
            raise ValueError("Record ID should be an integer.")

    def _get_record_transaction_history(self):
        all_transactions = acm.FTransactionHistory.Select(
            "transRecordType = '%s' and recordId = %d"
            % (self.record_type, self.record_id)
        ).SortByProperty("Oid", True)

        return all_transactions

    @staticmethod
    def _add_transaction_details_to_dict(comparison_dict, transaction):
        comparison_dict["Update User"] = transaction.UpdateUser().Name()
        comparison_dict["Version"] = transaction.Version()
        comparison_dict["Update Time"] = datetime.fromtimestamp(
            transaction.UpdateTime()
        ).strftime("%d/%m/%Y %H:%M:%S")

        return comparison_dict

    def _clean_report_list(self, report_list):
        report_list = report_list.split("\n")

        for index in range(len(report_list)):
            report_list[index] = report_list[index].strip()

        start_point = report_list.index(self.REPORT_SEPARATOR) + 1

        return report_list[start_point:]

    def _valid_record(self, record):
        return record and not any(
            [True for field in self.IGNORE_UPDATES if record.startswith(field)]
        )

    def _transform_to_dict(self, transaction_compare_report):
        transformed_report = {}
        cleaned_report_list = self._clean_report_list(transaction_compare_report)

        for index in range(len(cleaned_report_list)):
            if self._valid_record(cleaned_report_list[index]):

                record = cleaned_report_list[index].split(":", 1)

                updated_field = record[0].strip()
                values = record[-1].split("->")
                new_value = ""

                if len(values) > 1:
                    new_value = values[1].strip()
                old_value = values[0].strip()

                transformed_report[updated_field] = {"Old": old_value, "New": new_value}

        return transformed_report
