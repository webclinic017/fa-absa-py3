"""
This module enables modification of Commitment Fee fields
on a trade for the Loans Portfolio business.

19/04/2016 Evgeniya Baskaeva
ABITFA-4045 - Add day count + Rolling Conv. option
"""

import acm, ael, json
from at_ael_variables import AelVariableHandler

ROLL_PERIOD_INPUT = ['Annually',
                     'At End',
                     'Daily',
                     'Monthly',
                     'Quarterly',
                     'SemiAnnually',
                     'Weekly']

ROLL_CONV_INPUT = ['Following',
                   'Preceding',
                   'Mod. Following',
                   'Mod. Preceding']

DAY_COUNT_INPUT = ['',
                   'Act/360',
                   'Act/365']

EXCEPTION_LOG = []


class CommentHistory:
    """
    A comment history abstract class.

    Defines the interface for manipulating the comment history of a trade.
    """

    def __init__(self, trade):
        """
        The initializer of the comment's history.
        """

        self.trade = trade
        self._comments = []
        self.load()

    def append(self, comment):
        if comment:
            self._comments.append(comment)

    def comments(self):
        return self._comments

    def load(self):
        """
        Load the comments.

        This must be implemented by subclasses.
        raise NotImplementedError
        """

        self.comments = []

    def save(self):
        """
        Save the comments.
        This must be implemented by subclasses.
        """

        raise NotImplementedError


class JSONTextObjectCommentHistory(CommentHistory):
    """
    An JSON-based implementation of comment history, stored
    in the TextObject table.
    """

    class Comment(dict):
        """
        An internal placeholder for a comment.
        """

        def __str__(self):
            return '[{0}] {1}: {2}'.format(self['datetime'], self['login'], self['message'])

    def __init__(self, trade, prefix='CMF'):
        """
        The comment history initializer.

        trade -- the ACM trade object
        prefix -- used in the generating of the text_object
        """

        self.text_object = None
        self.text_object_name = prefix + str(trade.Oid())
        CommentHistory.__init__(self, trade)

    def append(self, comment):
        """
        Create the comment and append it to the existing comments.
        """

        if not comment:
            return

        comment = self.Comment([(el[0], str(el[1])) for el in comment])
        self._comments.append(comment)

    def load(self):
        """
        The overriden loading method, is called automatically from
        parent initializer.
        """

        self.text_object = ael.TextObject.read(
            'type="Customizable" and name="{0}"'.format(self.text_object_name))

        if self.text_object:
            # parse the text object
            try:
                # call the static method
                self._comments = self.parse_comments(self.text_object)
            except Exception:
                # the text object doesn't contain valid XML data
                ael.log('INFO - Trade buckets: invalid comments data, the history has been deleted.')

                # delete the text object
                self.text_object.delete()
                self.text_object = None

    def formatted_comments(self):
        """
        Return self formatted comments.
        """

        self._purge_empty_comments()
        return self.format_comments(self._comments)

    @staticmethod
    def format_comments(comments):
        """
        Format the comments to a list of strings.

        comments -- a list of Comment instances
        """

        return list(reversed(map(lambda c: str(c), comments)))

    @classmethod
    def parse_comments(cls, text_object):
        """
        Parse the given JSON data into Comment list.
        """

        saved_comments = json.loads(text_object.data)
        return map(lambda c: cls.Comment(c), saved_comments)

    @classmethod
    def parse_and_format(cls, text_object):
        """
        Parse and format the given text object's data.
        """

        parsed = cls.parse_comments(text_object)
        return cls.format_comments(parsed)

    def _purge_empty_comments(self):
        self._comments = [c for c in self._comments]

    def save(self):
        """
        Serializes the comments into JSON and saves them in the TextObject table
        """

        self._purge_empty_comments()
        if self._comments:
            # there are comments to be saved
            if not self.text_object:
                # the object doesn't exist yet
                to = ael.TextObject.new()
                to.type = 'Customizable'
                to.name = self.text_object_name
                to.data = str(self._comments)

                to.commit()

                self.text_object = to

            # get the clone for updating
            self.text_object = self.text_object.clone()

            try:
                self.text_object.data = json.dumps(self._comments)
                self.text_object.commit()
            except TypeError:
                message = ('Last comment not saved, please review the content'
                           ' of the comment for any special characters')
                ael.log(message)
        else:
            # no comments, delete the object if it exists
            if self.text_object:
                self.text_object.delete()
                self.text_object = None

    def delete(self):
        ''' Deletes the text object

        (don't forget to load it)
        '''

        self.text_object.delete()
        self.text_object = None


def is_float(s):
    try:
        return float(s)
    except ValueError:
        return False


def check_float(s, title):
    if not is_float(s):
        EXCEPTION_LOG.append('%s is not a real number' % title)
    return is_float(s)


def is_date(s):
    try:
        return ael.date(s)
    except TypeError:
        return False


def check_date(s, title):
    if not is_date(s):
        EXCEPTION_LOG.append('%s is not a valid date' % title)
    return is_date(s)


def startDialog_cb(eii, *rest):
    global ael_variables
    """Starts the dialog for comment adding."""

    tr = str(eii.ExtensionObject().At(0).Oid())

    CalcCommFee = 0
    PM_FacilityMax = ''
    PM_Limit = ''
    PM_CommitFeeRate = ''
    PM_FacilityExpiry = ''
    PM_CommitFeeBase = ''
    CommitPeriod = ''
    RollingConvention = ''
    DayCount = ''
    cmf_key = acm.FPersistentText['CMF' + tr]

    if cmf_key and cmf_key.Text():

        print("\nData found for trade " + tr)
        print("Text Object: " + cmf_key.Name())

        json_string = cmf_key.Text()[1:-1]
        parsed_json = json.loads(json_string)

        CalcCommFee = str(parsed_json['CalcCommFee'])
        PM_FacilityMax = str(parsed_json['PM_FacilityMax'])
        PM_Limit = str(parsed_json['PM_Limit'])
        PM_CommitFeeRate = str(parsed_json['PM_CommitFeeRate'])
        PM_FacilityExpiry = str(parsed_json['PM_FacilityExpiry'])
        PM_CommitFeeBase = str(parsed_json['PM_CommitFeeBase'])
        CommitPeriod = str(parsed_json['CommitPeriod'])
        RollingConvention = str(parsed_json['Rolling Convention'])
        try:
            DayCount = str(parsed_json['DayCount'])
        except KeyError:
            pass

    else:
        print("\nNo data found for trade" + tr)

    ael_variables = AelVariableHandler()

    ael_variables.add_bool(
        'CalcCommFee',
        label='Calculate Comm Fee',
        default=CalcCommFee,
    )
    ael_variables.add(
        'PM_FacilityMax',
        label='Facility Limit',
        cls='string',
        default=PM_FacilityMax
    )
    ael_variables.add(
        'PM_Limit',
        label='Threshold (0<x<1)',
        cls='string',
        default=PM_Limit
    )
    ael_variables.add(
        'PM_CommitFeeRate',
        label='Comm Fee Rate (%)',
        cls='string',
        default=PM_CommitFeeRate
    )
    ael_variables.add(
        'PM_FacilityExpiry',
        label='Facility Expiry (dd/mm/yyyy)',
        cls='string',
        default=PM_FacilityExpiry
    )
    ael_variables.add(
        'PM_CommitFeeBase',
        label='Rolling Base Day (dd/mm/yyyy)',
        cls='date',
        default=PM_CommitFeeBase
    )
    ael_variables.add(
        'CommitPeriod',
        label='Rolling Period',
        cls='string',
        default=CommitPeriod,
        collection=ROLL_PERIOD_INPUT
    )
    ael_variables.add(
        'RollingConvention',
        label='Rolling Convention',
        cls='string',
        default=RollingConvention,
        collection=ROLL_CONV_INPUT
    )
    ael_variables.add(
        'DayCount',
        label='Day Count',
        cls='string',
        default=DayCount,
        collection=DAY_COUNT_INPUT,
        mandatory=False
    )

    acm.RunModuleWithParametersAndData('CommFeeUploader',
                                       'Standard',
                                       {'trdnbr': tr})


def ael_main_ex(parameter, data):
    global EXCEPTION_LOG
    EXCEPTION_LOG = []
    trdnbr = data.At('customData').At('trdnbr')
    CalcCommFee = int(parameter['CalcCommFee'])

    PM_CommitFeeRate = parameter['PM_CommitFeeRate']
    PM_CommitFeeRate = check_float(PM_CommitFeeRate, 'CommitFeeRate')

    PM_FacilityMax = parameter['PM_FacilityMax'].replace(',', '')
    PM_FacilityMax = check_float(PM_FacilityMax, 'Facility Limit')

    PM_Limit = parameter['PM_Limit']
    PM_Limit = check_float(PM_Limit, 'Threshold')
    if PM_Limit:
        PM_Limit = abs(PM_Limit)
        if PM_Limit < 0 or PM_Limit > 1:
            EXCEPTION_LOG.append('Threshold must be 0 < Threshold < 1')

    CommitPeriod = parameter['CommitPeriod']
    if not CommitPeriod or CommitPeriod not in ROLL_PERIOD_INPUT:
        EXCEPTION_LOG.append('Wrong input for RollingPeriod')

    RollingConvention = parameter['RollingConvention']
    if not RollingConvention or RollingConvention not in ROLL_CONV_INPUT:
        EXCEPTION_LOG.append('Wrong input for Rolling Conv')

    PM_FacilityExpiry = parameter['PM_FacilityExpiry']
    PM_FacilityExpiry = check_date(PM_FacilityExpiry, 'Facility Expiry')

    PM_CommitFeeBase = parameter['PM_CommitFeeBase']
    PM_CommitFeeBase = check_date(PM_CommitFeeBase, 'Rolling Base Day')

    if PM_FacilityExpiry < PM_CommitFeeBase:
        EXCEPTION_LOG.append('CommFeeBase must be smaller than FacilityExpiry')

    DayCount = parameter['DayCount']
    if DayCount not in DAY_COUNT_INPUT:
        EXCEPTION_LOG.append('Wrong input for DayCount')

    print('\nInitial Input:')
    print('CalcCommFee: ', CalcCommFee)
    print('Rolling Base Day: ', PM_CommitFeeBase)
    print('CommitPeriod: ', CommitPeriod)
    print('Rolling Convention: ', RollingConvention)
    print('PM_CommitFeeRate: ', PM_CommitFeeRate)
    print('PM_FacilityExpiry: ', PM_FacilityExpiry)
    print('PM_FacilityMax: ', str(PM_FacilityMax))
    print('Threshold: ', PM_Limit)
    print('DayCount: ', DayCount)

    if not EXCEPTION_LOG:
        print('All variables successfully input')
        trade = acm.FTrade[trdnbr]
        CMF_num = 'CMF' + str(trdnbr)
        if acm.FPersistentText[CMF_num]:
            text = acm.FPersistentText[CMF_num]
            text.Text('')
            try:
                text.Commit()
            except Exception, e:
                print("{0}: Couldn't commit to db \n{1}".format(CMF_num, e))

        comment_obj = JSONTextObjectCommentHistory(trade)
        comment = [('CalcCommFee', CalcCommFee),
                   ('PM_CommitFeeBase', PM_CommitFeeBase),
                   ('CommitPeriod', CommitPeriod),
                   ('Rolling Convention', RollingConvention),
                   ('PM_CommitFeeRate', PM_CommitFeeRate),
                   ('PM_FacilityExpiry', PM_FacilityExpiry),
                   ('PM_FacilityMax', PM_FacilityMax),
                   ('PM_Limit', PM_Limit),
                   ('DayCount', DayCount)]
        comment_obj.append(comment)
        comment_obj.load()
        comment_obj.save()
        print('\nUploaded Input:')
        print(comment_obj.comments())
    else:
        print('\nError(s):')
        print(('\n').join(EXCEPTION_LOG))


