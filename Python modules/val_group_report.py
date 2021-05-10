"""--------------------------------------------------------------------------------------
MODULE
    val_group_report

DESCRIPTION
    Date                : 2020-10-20
    Purpose             : This preprocesses the transaction history XML to generate a
                          val group amendments only report
    Department and Desk : PCG
    Requester           : James Stevens
    Developer           : Sihle Gaxa
    JIRA Number         : PCGDEV-546

HISTORY
=========================================================================================
Date            JIRA no       Developer               Description
-----------------------------------------------------------------------------------------
2020-10-20      PCGDEV-546    Sihle Gaxa              Initial implementation.

ENDDESCRIPTION
--------------------------------------------------------------------------------------"""

import xml.etree.ElementTree as ET

def preprocess(report, params, xml_string):
    root = ET.fromstring(xml_string)
    contents = root.find("./ReportContents")
    table = contents.find("./Table")
    contents.remove(table)
    child_reports = contents.find('./ChildReports')
    val_group_amends = child_reports.findall(".//Cell[RawData='Val Group']/../../../../../../../../../../..")
    all_children = child_reports.findall("./ChildReport")
    for child in all_children:
        child_reports.remove(child)

    for child in val_group_amends:
        child_reports.append(child)

    output = ET.tostring(root, "UTF-8")
    return output

