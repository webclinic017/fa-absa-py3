"""
A module implementing the ChronicleAttribute class.
"""

from copy import deepcopy
from datetime import datetime, time

from at_chronicle import (Chronicle,
                          ChronicleEncoder,
                          TimeValue)
from pb_attr_def import AttributeDefinition
from pb_storage_attr_def import AttributeDefinitionStorage


class ChronicleAttribute(object):

    """
    A class representing a chronicle-based,
    history-tracking attribute of a Prime Brokerage fund.
    """

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the ChronicleAttribute class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        json_chronicle = json_representation["chronicle"]
        chronicle = Chronicle.from_json(json_chronicle)
        chronicle_attribute = cls(chronicle=chronicle)
        return chronicle_attribute


    def __init__(self, chronicle=None):
        if chronicle is None:
            chronicle = Chronicle()
        self.chronicle = chronicle
        super(ChronicleAttribute, self).__init__()


    def __repr__(self):
        representation = "{0}(chronicle={1})".format(type(self).__name__,
                                                     repr(self.chronicle))
        return representation


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return self.chronicle == other.chronicle
        else:
            return False


    def init(self, other):
        """
        Initialize the data of the current instance
        from the provided other instance.
        """
        self.chronicle = deepcopy(other.chronicle)


    def getvalue(self, utc_datetime=None):
        """
        Return the value of the represented attribute
        which is valid at the provided UTC date and time.
        """
        return self.chronicle.get_time_value(utc_datetime).value


    def setvalue(self, value, utc_datetime=None):
        """
        Set the value of the represented attribute
        valid at the at the provided UTC date and time
        to the provided value.
        """
        time_value = TimeValue(value, utc_datetime)
        self.chronicle.insert_time_value(time_value)


# FIXME: Is this method necessary?
# Probably not. But its tz-aware version can be useful.
    def setdatevalue(self, value, utc_date=None):
        """
        Set the value of the represented attribute
        valid at the beginning of the provided UTC date
        to the provided value.
        """
        if utc_date is None:
            utc_date = datetime.utcnow().date()
        utc_datetime = datetime.combine(utc_date, time.min)
        self.setvalue(value, utc_datetime)


def get_blank_attributes(excluded_attr_ids=None,
                         excluded_categories=None):
    """
    Return a dictionary of all the available
    chronicle attributes (as blank instances without data)
    indexed by their ID.

    Optionally, an iterable of attribute IDs or attribute categories
    which will be excluded can be provided.
    """
    if excluded_attr_ids is None:
        excluded_attr_ids = set()
    if excluded_categories is None:
        # There are no chronicle attributes
        # of category ADD_PRODUCT_TYPE_CATEGORY (yet),
        # so we will exclude it by default.
        excluded_categories = {
            AttributeDefinition.ADD_PRODUCT_TYPE_CATEGORY}
    chronicle_attributes = {}
    attr_def_storage = AttributeDefinitionStorage()
    attr_def_storage.load()
    for attr_id, attr_def in attr_def_storage.attr_defs.iteritems():
        if attr_def.category in excluded_categories:
            continue
        if attr_id in excluded_attr_ids:
            continue
        chronicle_attributes[attr_id] = ChronicleAttribute()
    return chronicle_attributes


class ChronicleAttributeEncoder(ChronicleEncoder):

    """
    A class which supports encoding of ChronicleAttribute objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, ChronicleAttribute):
            chronicle_attribute_s = {"type": type(obj).__name__,
                                     "chronicle": obj.chronicle}
            return chronicle_attribute_s
        else:
            return super(ChronicleAttributeEncoder, self).default(obj)
