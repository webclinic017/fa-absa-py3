"""
A module implementing the Chronicle class.
"""

from bisect import bisect_left
from datetime import datetime
from json import JSONEncoder


class TimeValue(object):

    """
    An object representing a value which is valid
    at a particular UTC date and time.
    """

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the TimeValue class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        value = json_representation["value"]
        utc_datetime_isoformat = json_representation["utc_datetime"]
        utc_datetime = datetime.strptime(utc_datetime_isoformat,
                                         "%Y-%m-%dT%H:%M:%S.%f")
        return cls(value=value, utc_datetime=utc_datetime)


    def __init__(self, value, utc_datetime=None):
        """
        Initialize the instance using the provided value
        valid at the provided UTC date and time.

        If no UTC date and time is provided,
        the value is supposed to be valid now.
        """
        self.value = value
        if utc_datetime is None:
            utc_datetime = datetime.utcnow()
        self.utc_datetime = utc_datetime


    def __repr__(self):
        representation = ("{0}(value={1}, "
                          "utc_datetime={2})").format(
                              type(self).__name__,
                              repr(self.value),
                              repr(self.utc_datetime))
        return representation


    def __eq__(self, other):
        return (self.utc_datetime == other.utc_datetime and
                self.value == other.value)


def get_tv_utc_datetime(time_value):
    """
    Return the UTC datetime
    at which is the provided time value valid.

    This function is suitable to be used
    as a key function for KeyedList.
    """
    return time_value.utc_datetime


class KeyedList(object):

    """
    A simple wrapper around the list
    which applies the predetermined key function to its items
    before returning them.

    Such a wrapping is necessary for bisect to use custom ordering.
    """

    def __init__(self, wrapped_list, key_function):
        self.wrapped_list = wrapped_list
        self.key_function = key_function


    def __len__(self):
        return len(self.wrapped_list)


    def __repr__(self):
        representation = ("{0}(wrapped_list={1}, "
                          "key_function={2})").format(
                              type(self).__name__,
                              repr(self.wrapped_list),
                              repr(self.key_function))
        return representation


    def __getitem__(self, index):
        return self.key_function(self.wrapped_list[index])


    def __eq__(self, other):
        return (self.wrapped_list == other.wrapped_list and
                self.key_function == other.key_function)


class Chronicle(object):

    """
    A chronicle of the wrapped value's history.

    Chronologically stores the values,
    as well as the times at which they are valid.
    Enables lookup of a value valid at the specific time.
    """

    @classmethod
    def from_json(cls, json_representation):
        """
        Return an instance of the Chronicle class
        created from the provided JSON representation.
        """
        if json_representation["type"] != cls.__name__:
            exception_message = ("JSON object '{0}' "
                                 "does not represent "
                                 "a {1} instance. ").format(
                                     json_representation,
                                     cls.__name__)
            raise TypeError(exception_message)
        initial_value = json_representation["initial_value"]
        json_sorted_tvs = json_representation["sorted_tvs"]
        sorted_tvs = [TimeValue.from_json(json_tv)
                      for json_tv in json_sorted_tvs]
        return cls(initial_value=initial_value, sorted_tvs=sorted_tvs)


    @property
    def initial_value(self):
        return self.initial_tv.value


    @initial_value.setter
    def initial_value(self, new_value):
        self.initial_tv = TimeValue(new_value, datetime.min)


    def __init__(self, initial_value=None, sorted_tvs=None):
        """
        Initialize the instance.

        Initial value is valid
        at the minimum representable date and time.
        """
        self.initial_value = initial_value
        key_function = get_tv_utc_datetime
        if not sorted_tvs:
            sorted_tvs = []
        self.sorted_tvs = KeyedList(sorted_tvs, key_function)


    def __len__(self):
        return len(self.sorted_tvs)


    def __repr__(self):
        representation = ("{0}(initial_value={1}, "
                          "sorted_tvs={2})").format(
                              type(self).__name__,
                              repr(self.initial_value),
                              repr(self.sorted_tvs.wrapped_list))
        return representation


    def __eq__(self, other):
        return (self.initial_tv == other.initial_tv and
                self.sorted_tvs == other.sorted_tvs)


    def get_time_value(self, utc_datetime=None):
        """
        Return the time value valid at the provided UTC date and time.

        If no UTC date and time is provided,
        the value which is valid now is returned.
        """
        if not self.sorted_tvs:
            return self.initial_tv
        # From now on, we can suppose that self.sorted_tvs is not empty.
        if not utc_datetime:
            utc_datetime = datetime.utcnow()
        index = bisect_left(self.sorted_tvs, utc_datetime)
        if index == len(self.sorted_tvs):
            # a value valid later than any stored one is required
            return self.sorted_tvs.wrapped_list[-1]
        if self.sorted_tvs[index] == utc_datetime:
            # a value valid *exactly* at the required
            # UTC date and time already exists
            return self.sorted_tvs.wrapped_list[index]
        if index == 0:
            # a value valid earlier than any stored one is required
            return self.initial_tv
        return self.sorted_tvs.wrapped_list[index - 1]


    def insert_time_value(self, time_value):
        """
        Insert the provided time value into the chronicle.
        """
        index = bisect_left(self.sorted_tvs, time_value.utc_datetime)
        if index == len(self.sorted_tvs):
            # the new time value is valid later
            # than any stored one
            self.sorted_tvs.wrapped_list.append(time_value)
            return
        if self.sorted_tvs[index] == time_value.utc_datetime:
            # a value valid *exactly* at the required
            # UTC date and time already exists
            self.sorted_tvs.wrapped_list[index] = time_value
            return
        self.sorted_tvs.wrapped_list.insert(index, time_value)


    def remove_time_value(self, utc_datetime):
        """
        Remove the time value valid at the provided UTC date and time
        from the chronicle.

        Do not remove anything if the initial value
        is valid at the provided UTC date and time,
        """
        if (len(self.sorted_tvs) > 0
                and self.sorted_tvs[0] <= utc_datetime):
            index = bisect_left(self.sorted_tvs, utc_datetime)
            if index == len(self.sorted_tvs):
                # the most recent time value will be removed
                del self.sorted_tvs.wrapped_list[-1]
            elif self.sorted_tvs[index] == utc_datetime:
                # a value valid *exactly* at the provided
                # UTC date and time will be removed
                del self.sorted_tvs.wrapped_list[index]
            else:
                del self.sorted_tvs.wrapped_list[index - 1]


class ChronicleEncoder(JSONEncoder):

    """
    A class which supports encoding of Chronicle objects to JSON.
    """

    def default(self, obj):
        """
        Return a serializable version of the provided object.
        """
        if isinstance(obj, datetime):
            if obj.tzinfo:
                exception_message = ("Object of type {0} with value of {1} "
                                     "is not JSON serializable").format(
                                         type(obj), repr(obj))
                raise TypeError(exception_message)
            return obj.isoformat()
        elif isinstance(obj, TimeValue):
            tv_s = {"type": type(obj).__name__,
                    "value": obj.value,
                    "utc_datetime": obj.utc_datetime}
            return tv_s
        elif isinstance(obj, Chronicle):
            chronicle_s = {"type": type(obj).__name__,
                           "initial_value": obj.initial_value,
                           "sorted_tvs": obj.sorted_tvs.wrapped_list}
            return chronicle_s
        else:
            return super(ChronicleEncoder, self).default(obj)
