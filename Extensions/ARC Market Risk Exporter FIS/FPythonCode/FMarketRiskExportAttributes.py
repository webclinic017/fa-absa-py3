""" Compiled: 2020-08-14 16:40:05 """

#__src_file__ = "extensions/arc_writers/./etc/FMarketRiskExportAttributes.py"

"""-------------------------------------------------------------------------------------------------------
MODULE
    FMarketRiskExportAttributes - Position attributes in the reports

    (c) Copyright 2019 by FIS FRONT ARENA. All rights reserved.

DESCRIPTION

-------------------------------------------------------------------------------------------------------"""
import acm
from collections import namedtuple
import json


AttributeSpec = namedtuple('AttributeSpec', ['label', 'method', 'required'])

BOOK_STRUCTURE_LEVELS = 5
BOOK_STRUCTURE_STRING = 'Level'
# The list of attributes which defines a position group. To change the list of
# trade/position attributes to be exported, add or delete this default list.
# "method" is chained grouper method, "label" is the column name in the output
# file.
ATTRIBUTES_STRING = """
[
    {
        "method": "Status",
        "label": "Status"
    },
    {
        "method": "Trader.Name",
        "label": "Trader"
    },
    {
        "method": "Acquirer.Name",
        "label": "Acquirer"
    },
    {
        "method": "Counterparty.Name",
        "label": "Counterparty"
    },
    {
        "method": "Currency.Name",
        "label": "Trade Currency"
    },
    {
        "method": "Instrument.CreditReferenceOrSelf.Issuer.Name",
        "label": "Issuer"
    },
    {
        "method": "Instrument.CategoryChlItem.Name",
        "label": "Class"
    },
    {
        "method": "Instrument.Category",
        "label": "Instrument Type"
    },
    {
        "method": "Portfolio",
        "label": "Portfolio"
    },
    {
        "method": "Instrument.Name",
        "label": "Instrument"
    }
]
"""

ArtiQ_ATTRIBUTES_STRING = """
[
    {
        "method": "Status",
        "label": "Status"
    },
    {
        "method": "Trader.Name",
        "label": "Trader"
    },
    {
        "method": "Acquirer.Name",
        "label": "Acquirer"
    },
    {
        "method": "Counterparty.Name",
        "label": "Counterparty"
    },
    {
        "method": "Currency.Name",
        "label": "Currency"
    },
    {
        "method": "Instrument.CreditReferenceOrSelf.Issuer.Name",
        "label": "Issuer"
    },
    {
        "method": "Instrument.CategoryChlItem.Name",
        "label": "Class"
    },
    {
        "method": "Instrument.Category",
        "label": "Instrument Type"
    },
    {
        "method": "Portfolio",
        "label": "Portfolio"
    },
    {
        "method": "Instrument.Name",
        "label": "Instrument Name"
    },
    {
        "method": "Oid",
        "label": "Reference"
    }
]
"""

_attributeSpecs = []
_artiQ_attributeSpecs = []

def getAttributeSpecs():
    global _attributeSpecs

    if _attributeSpecs:
        return _attributeSpecs

    try:
        chain = json.loads(ATTRIBUTES_STRING, encoding='ascii')
        for attr in chain[:-1]:
            args = [attr[k].encode('ascii', 'ignore')
                    for k in ('label', 'method',)]
            _attributeSpecs.append(AttributeSpec(*args, required=False))

        last = [chain[-1][k].encode('ascii', 'ignore')
                for k in ('label', 'method')]
        _attributeSpecs.append(AttributeSpec(*last, required=True))

        return _attributeSpecs
    except Exception as e:
        print(("Invalid attribute list: {0}".format(e)))
        return None


def getArtiQAttributeSpecs():
    global _artiQ_attributeSpecs

    if _artiQ_attributeSpecs:
        return _artiQ_attributeSpecs

    try:
        chain = json.loads(ArtiQ_ATTRIBUTES_STRING, encoding='ascii')
        for attr in chain[:-1]:
            args = [attr[k].encode('ascii', 'ignore')
                    for k in ('label', 'method',)]
            _artiQ_attributeSpecs.append(AttributeSpec(*args, required=False))

        last = [chain[-1][k].encode('ascii', 'ignore')
                for k in ('label', 'method')]
        _artiQ_attributeSpecs.append(AttributeSpec(*last, required=True))

        return _artiQ_attributeSpecs
    except Exception as e:
        print(("Invalid attribute list: {0}".format(e)))
        return None
