# core libs
import re
import copy
from time import mktime
from datetime import datetime, timedelta
from functools import partial

# front libs
import at


class StateProperty(type):
    """Enforce 'state' property for all derived sub-classes"""

    def __new__(cls, classname, bases, _dict):

        if bases != (object,):
            assert _dict.has_key("state"), \
                "Class {0} must have attribute 'state'".format(classname)

            assert _dict["state"] in (at.TS_BO_CONFIRMED, at.TS_BOBO_CONFIRMED), \
                "'state' attribute has to be in BO or BO-BO Confirmed status"

        return super(StateProperty, cls).__new__(cls, classname, bases, _dict)


class AutoConfirmation(object):
    """Abstract class the provide auto confirmation agains user define rules
    before moving trade into desired confirmed state.
    """

    __metaclass__ = StateProperty

    __strict_rules_cache = []
    __soft_rules_cache = []

    def __init__(self, candidates, exec_delay=None):
        """Initializer of auto confirmation

        Arguments:
        candidates -- list of candidate trades
        exec_delay -- execution delay string eg. -5m, -1h
        """
        self.candidates = candidates
        self.exec_delay = exec_delay

        # list of passed trades to be confirmed
        self.__passed = []

        # list of mirror trades excluded from passed trades
        self.__mirrors = []

        # dict with verification errors
        self.__errors = {}

    @property
    def errors(self):
        """Error dictionary
        Keys are FTrade objects, values are string error explanation"""
        return self.__errors

    @property
    def passed(self):
        """List of passed trade to final confirmation"""
        return self.__passed

    @property
    def mirrors(self):
        """List of mirror trades excluded from passed trades"""
        return self.__mirrors

    @property
    def candidates(self):
        """List of candidate trades to perform validation upon"""
        return self.__candidates

    @candidates.setter
    def candidates(self, lst):
        self.__candidates = copy.copy(lst)

    @property
    def exec_delay(self):
        return self.__exec_delay

    @exec_delay.setter
    def exec_delay(self, delay):
        """
        Converts exec delay string literal to unix timestamp.

        Execution timestamp appears once a trade is move to FO Confirmed state.
        As a safery precautions it's highly recommended to BO / BO-BO Confirm only mature trades
        that that are older than exec delay as script could be running very frequently.
        """
        if delay is None:
            self.__exec_delay = None
            return

        valid_delay_re = re.compile(r'(?P<num>-\d+)(?P<period>[smhdw])')
        match = valid_delay_re.match(delay)

        if match:
            td = dict(list(zip(
                ('s', 'm', 'h', 'd', 'w'),
                ('seconds', 'minutes', 'hours', 'days', 'weeks')
            )))
            params = {td[match.group('period')] : int(match.group('num'))}
            delta = timedelta(**params)

            self.__exec_delay = mktime((datetime.now() + delta).timetuple())
        else:
            raise ValueError('Execution delay has incorrect format')

    @property
    def strict_rules(self):
        if len(self.__strict_rules_cache) == 0:
            name = "_{0}{1}".format(self.__class__.__name__, '__strict_rule')
            self.__strict_rules_cache = map(partial(getattr, self), [rule for rule in dir(self)
                if rule.startswith(name)])
        return self.__strict_rules_cache

    @property
    def soft_rules(self):
        if len(self.__soft_rules_cache) == 0:
            name = "_{0}{1}".format(self.__class__.__name__, '__soft_rule')
            self.__soft_rules_cache = map(partial(getattr, self), [rule for rule in dir(self)
                if rule.startswith(name)])
        return self.__soft_rules_cache

    def print_errors(self):
        """Print errors"""
        for trade, msg in self.__errors.iteritems():
            print "Trade {0} not confirmed, reason: {1}".format(trade.Oid(), msg)

    @staticmethod
    def check(bool_expr, warning_message):
        """
        Assert-like function which raises UserWarning if 'bool_expr' is False.
        """
        if not bool_expr:
            raise UserWarning(warning_message)

    def verify(self, trade):
        """Method verifies if a Trade is suitable to be automatically confirmed
        depending on defined internal rules.

        Arguments:
        trade -- a FTrade instance
        """

        # The flag indicates if a trade has passed all strict rules
        # and should be validated against all soft rules
        passed_on_strict_rule = True

        # Validate against all strict rules, in case of error halt
        # execution and don't continue validate soft rules
        for rule in self.strict_rules:
            try:
                rule(trade)
            except (AssertionError, UserWarning) as warning:
                passed_on_strict_rule = False
                self.__errors[trade] = warning
                break

        # Validate against soft rules, in case of a exception continue
        # with next rule, if a rule is valid - stop the verification
        if passed_on_strict_rule:
            # trade is valid since it passed on all strict rules,
            # but no soft rules are available
            if not self.soft_rules:
                self.__passed.append(trade)
            else:
                for rule in self.soft_rules:
                    try:
                        if rule(trade) is True:
                            self.__passed.append(trade)
                            self.__errors.pop(trade, None)
                            break # no need to re-approve trade multiple times
                    except (AssertionError, UserWarning) as warning:
                        self.__errors[trade] = warning


    def confirm(self, dry_run=False):
        """Actual trade confirmation method

        Arguments:
        dry_run -- Flag to only perform checking against defined rules (default: False)
        """

        if len(self.__candidates) == 0:
            print "No trades to automatically {0}".format(self.state)
            return

        # validate each trade from candidate list
        for trade in self.__candidates:
            self.verify(trade)

        # iterate through a trade list copy and remove mirror
        # trades from the original list
        for trade in self.__passed[:]:
            mirror = trade.GetMirrorTrade()
            if (mirror and mirror in self.__passed and trade not in self.__mirrors):
                self.__mirrors.append(mirror)
                self.__passed.remove(mirror)

        # remove error messages if trade and its mirror were
        # didn't pass simulatiniously
        for trade in self.__passed:
            mirror = trade.GetMirrorTrade()
            if mirror not in self.__mirrors:
                self.__errors.pop(mirror, None)

        # confirm passed trades
        if not dry_run:
            for trade in self.__passed:
                try:
                    trade.Status(self.state)
                    trade.Commit()
                    print "Trade {0} was automatically {1}".format(trade.Oid(), self.state)
                except Exception as e:
                    trade.Undo()
                    bo_error = "Unable to {1} trade {1}\n".format(trade.Oid(), self.state)
                    bo_error += " Reason: {0}".format(e)
                    self.__errors[trade] = bo_error
                    print bo_error


    @staticmethod
    def hotfix_confirm_trade(trade, status):
        """In version 2014.4.8 there is a problem with BO Confirmation of mirror trades
        (the one with lower trade number), doing so it produces a Runtime exception.
        This function is automatically changing status of a trade with higher trade number.

        Arguments:
        trade -- FTrade object
        status -- Valid trade status supported by Front Arena
        """

        mirror_trade = trade.MirrorTrade()
        if trade.GetMirrorTrade() and mirror_trade is not None and mirror_trade.Oid() == trade.Oid():
            m = mirror_trade.GetMirrorTrade()
            m.Status(status)
            m.Commit()
        else:
            trade.Status(status)
            trade.Commit()
