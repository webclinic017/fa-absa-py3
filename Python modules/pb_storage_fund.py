"""
A module which contains the class and functions
for persistently storing the instances
of PrimeBrokerageFund class into Front Arena.
"""

from json import dumps, JSONDecoder, JSONEncoder

from at_logging import getLogger
from pb_fund_interface import (PrimeBrokerageFund,
                               PrimeBrokerageFundEncoder)
from pb_storage_core import (create_text_object,
                             get_text_object,
                             NoSuchTextObject,
                             TEXT_OBJECT_SUBTYPE)


LOGGER = getLogger()


def pb_fund_from_text_object(text_object):
    """
    Return an instance of the PrimeBrokerageFund class
    initialized from the provided text object.
    """
    decoder = JSONDecoder()
    json_string = text_object.Text()
    json_representation = decoder.decode(json_string)
    pb_fund = PrimeBrokerageFund.from_json(json_representation)
    LOGGER.debug("Prime brokerage fund '%s' "
                 "has been loaded from a text object "
                 "with ID == '%s'.",
                 pb_fund.fund_id,
                 text_object.Name())
    return pb_fund


def pb_fund_to_text_object(pb_fund, text_object):
    """
    Store the provided instance of the PrimeBrokerageFund class
    into the provided text object.
    """
    json_string = dumps(pb_fund, cls=PrimeBrokerageFundEncoder, indent=4)
    text_object.Text(json_string)
    text_object.Commit()
    LOGGER.debug("Prime brokerage fund '%s' "
                 "has been saved into a text object "
                 "with ID == '%s'.",
                 pb_fund.fund_id,
                 text_object.Name())


class PrimeBrokerageFundStorage(object):

    """
    A class providing access to all the instances
    of the PrimeBrokerageFund class
    which are persistently stored in Front Arena.
    """

    cls_text_object_id = "pb_funds"

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the PrimeBrokerageFundStorage class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        stored_funds = json_representation["stored_funds"]
        fund_storage = cls(stored_funds=stored_funds)
        return fund_storage


    def __init__(self, text_object_id=cls_text_object_id, stored_funds=None):
        self.text_object_id = text_object_id
        if stored_funds is None:
            self.stored_funds = {}
        else:
            assert isinstance(stored_funds, dict)
            self.stored_funds = stored_funds


    def __repr__(self):
        representation = ("{0}(text_object_id={1}, "
                          "stored_funds={2})").format(
                              type(self).__name__,
                              repr(self.text_object_id),
                              repr(self.stored_funds))
        return representation


    def __eq__(self, other):
        if isinstance(other, type(self)):
            return (self.text_object_id == other.text_object_id and
                    self.stored_funds == other.stored_funds)
        else:
            return False


    def load(self, text_object_id=None):
        """
        Load the data for the current instance
        from the underlying text object.

        If the text_object_id parameter is provided,
        it will be used to replace the stored text object ID
        before the update will take place.
        """
        if text_object_id:
            self.text_object_id = text_object_id
        text_object = get_text_object(self.text_object_id)
        json_string = text_object.Text()
        decoder = JSONDecoder()
        json_representation = decoder.decode(json_string)
        instance = self.from_json(json_representation)
        self.stored_funds = instance.stored_funds


    def save(self, text_object_id=None):
        """
        Save the data of the current instance
        to the underlying text object.

        If the text_object_id parameter is provided,
        it will be used to replace the stored text object ID
        before the save will take place.
        """
        if text_object_id:
            self.text_object_id = text_object_id
        text_object = get_text_object(self.text_object_id)
        json_string = dumps(self,
                            cls=PrimeBrokerageFundStorageEncoder,
                            indent=4)
        text_object.Text(json_string)
        text_object.Commit()
        LOGGER.debug("Prime brokerage fund storage "
                     "has been saved into a text object "
                     "with ID == '%s'.", text_object.Name())


    def load_fund(self, fund_id):
        """
        Load the PrimeBrokerageFund with the provided ID
        from the appropriate text object and return it.
        """
        if fund_id in self.stored_funds:
            text_object_id = self.stored_funds[fund_id]
            text_object = get_text_object(str(text_object_id))
            return pb_fund_from_text_object(text_object)
        else:
            exception_message = ("PrimeBrokerageFund with ID '{0}' "
                                 "does not have its persistent "
                                 "representation stored "
                                 "in Front Arena.").format(fund_id)
            raise KeyError(exception_message)


    def save_fund(self, pb_fund):
        """
        Save the provided PrimeBrokerageFund
        into the appropriate text object.

        If there is no text object currently,
        which would hold the data of the provided PrimeBrokerageFund,
        a new one will be created.
        """
        fund_id = pb_fund.fund_id
        if fund_id in self.stored_funds:
            text_object_id = self.stored_funds[fund_id]
            text_object = get_text_object(str(text_object_id))
        else:
            text_object_id = "pb_fund|{0}".format(fund_id)
            text_object = create_text_object(text_object_id,
                                             subtype=TEXT_OBJECT_SUBTYPE)
            LOGGER.info("A new text object with ID '%s' "
                        "representing a prime brokerage fund "
                        "'%s' has been created.",
                        text_object.Name(),
                        fund_id)
            self.stored_funds[fund_id] = text_object.Name()
        pb_fund_to_text_object(pb_fund, text_object)


    def delete_fund(self, fund_id):
        """
        Delete the PrimeBrokerageFund with the provided ID.
        """
        if fund_id in self.stored_funds:
            text_object_id = self.stored_funds[fund_id]
            text_object = get_text_object(str(text_object_id))
            text_object.Delete()
            LOGGER.info("Text object with ID '%s' "
                        "representing a prime brokerage fund "
                        "'%s' has been deleted.",
                        text_object.Name(),
                        fund_id)
        else:
            exception_message = ("PrimeBrokerageFund with ID '{0}' "
                                 "does not have its persistent "
                                 "representation stored "
                                 "in Front Arena.").format(fund_id)
            raise KeyError(exception_message)


    def clean_up(self):
        """
        Check each stored prime brokerage fund
        and delete it from the fund storage
        if its underlying text object does not exist.
        """
        for fund_id in list(self.stored_funds.keys()):
            text_object_id = self.stored_funds[fund_id]
            try:
                get_text_object(str(text_object_id))
            except NoSuchTextObject:
                del self.stored_funds[fund_id]
                LOGGER.info("Cleaned-up a reference "
                            "to the prime brokerage fund '%s', "
                            "because its underlying text object "
                            "'%s' does not exist.",
                            fund_id,
                            text_object_id)


def init(overwrite=False):
    """
    Initialize the presistent storage of objects
    representing the prime brokerage funds.
    """
    # Try to get an existing text object which holds
    # the prime brokerage fund storage.
    text_object_id = PrimeBrokerageFundStorage.cls_text_object_id
    try:
        get_text_object(text_object_id)
        if not overwrite:
            return
    except NoSuchTextObject:
        create_text_object(text_object_id, subtype=TEXT_OBJECT_SUBTYPE)
    # Save a valid content to this text object.
    tmp_fund_storage = PrimeBrokerageFundStorage()
    tmp_fund_storage.save()


class PrimeBrokerageFundStorageEncoder(JSONEncoder):

    """
    A class which supports encoding
    of PrimeBrokerageFundStorage objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, PrimeBrokerageFundStorage):
            pb_fund_storage_s = {"type": type(obj).__name__,
                                 "stored_funds": obj.stored_funds}
            return pb_fund_storage_s
        else:
            return super(PrimeBrokerageFundStorageEncoder, self).default(obj)
