"""
A module implementing the metaclass and the base class
of the PrimeBrokerageFund class.
"""

from sys import stderr

from pb_attribute import (get_blank_attributes,
                          ChronicleAttribute)
from pb_quirk import get_attribute_quirks


class BaseDescriptor(object):

    """
    A base class for descriptors used for accessing instances
    of attributes or quirks from within the PrimeBrokerageFund class.
    """

    VERBOSITY_ERROR = 1
    VERBOSITY_DEBUG = 2
    VERBOSITY_INFO = 3
    verbosity = VERBOSITY_DEBUG

    def __init__(self, name=None):
        self.name = name


    def get_accessed_object(self, instance):
        """
        Get an object used for getting and setting the values.
        """
        raise NotImplementedError


    def get_value(self, instance, accessed_object):
        """
        Get the value from the accessed object.
        """
        raise NotImplementedError


    def set_value(self, instance, accessed_object, value):
        """
        Set the provided value to the accessed object.
        """
        raise NotImplementedError


    def __get__(self, instance, owner):
        accessed_object = self.get_accessed_object(instance)
        value = self.get_value(instance, accessed_object)
        if self.verbosity >= self.VERBOSITY_INFO:
            info_message = ("PrimeBrokerageFund '{0}': "
                            "{1} '{2}' "
                            "has been read.").format(
                                instance.fund_id,
                                type(accessed_object).__name__,
                                self.name)
            print(info_message, file=stderr)
        return value


    def __set__(self, instance, value):
        accessed_object = self.get_accessed_object(instance)
        self.set_value(instance, accessed_object, value)
        if self.verbosity >= self.VERBOSITY_INFO:
            info_message = ("PrimeBrokerageFund '{0}': "
                            "{1} '{2}' has been "
                            "set to {3}").format(
                                instance.fund_id,
                                type(accessed_object).__name__,
                                self.name,
                                repr(value))
            print(info_message, file=stderr)


class AttributeDescriptor(BaseDescriptor):

    """
    A descriptor used for accessing ChronicleAttribute instances
    from within the PrimeBrokerageFund class.
    """

    def get_accessed_object(self, instance):
        return instance.attributes[self.name]


    def get_value(self, instance, accessed_object):
        utc_datetime_override = instance.utc_datetime_override
        return accessed_object.getvalue(utc_datetime=utc_datetime_override)


    def set_value(self, instance, accessed_object, value):
        utc_datetime_override = instance.utc_datetime_override
        accessed_object.setvalue(value, utc_datetime=utc_datetime_override)


class QuirkDescriptor(BaseDescriptor):

    """
    A descriptor used for accessing QuirkAttribute instances
    from within the PrimeBrokerageFund class.
    """

    def get_accessed_object(self, instance):
        return instance.quirks[self.name]


    def get_value(self, instance, accessed_object):
        return accessed_object.getvalue()


    def set_value(self, instance, accessed_object, value):
        accessed_object.setvalue(value)


class PrimeBrokerageFundMetaclass(type):

    """
    A metaclass which fills in the names of all the AttributeDescriptors
    so that they match the names of the parent class' attributes.
    """

    def __new__(mcs,
                new_class_name,
                new_class_parents,
                new_class_attrs):
        new_class_attrs_updated = {}
        for name, value in new_class_attrs.iteritems():
            if isinstance(value, BaseDescriptor):
                value.name = name
            new_class_attrs_updated[name] = value

        new_instance = super(PrimeBrokerageFundMetaclass,
                             mcs).__new__(mcs,
                                          new_class_name,
                                          new_class_parents,
                                          new_class_attrs_updated)
        return new_instance


class PrimeBrokerageFundCore(object):

    """
    A class which defines the core functionality
    used for representing a prime brokerage fund.
    """

    __metaclass__ = PrimeBrokerageFundMetaclass


    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of this class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        fund_id = json_representation["fund_id"]
        json_attributes = json_representation["attributes"]
        attributes = {}
        for (name, json_attribute) in json_attributes.iteritems():
            attributes[name] = ChronicleAttribute.from_json(json_attribute)
        fund = cls(fund_id=fund_id, attributes=attributes)
        return fund


    def __init__(self,
                 fund_id,
                 quirks=None,
                 attributes=None,
                 utc_datetime_override=None):
        self.fund_id = fund_id
        if quirks is None:
            self.quirks = get_attribute_quirks(self)
        else:
            assert isinstance(quirks, dict)
            self.quirks = quirks
        if attributes is None:
            self.attributes = get_blank_attributes(
                excluded_attr_ids=set(self.quirks))
        else:
            assert isinstance(attributes, dict)
            self.attributes = attributes
        self.utc_datetime_override = utc_datetime_override


    def __repr__(self):
        representation = ("{0}(fund_id={1}, "
                          "quirks={2}, "
                          "attributes={3}, "
                          "utc_datetime_override={4})").format(
                              type(self).__name__,
                              repr(self.fund_id),
                              repr(self.quirks),
                              repr(self.attributes),
                              repr(self.utc_datetime_override))
        return representation


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.fund_id == other.fund_id and
                    self.attributes == other.attributes)
        else:
            return False
