"""----------------------------------------------------------------------------------------------------------
MODULE                  :       comment_history
PURPOSE                 :       This module stores an abstract comment_history class and a JSON-TextObject
                                implementation
DEPARTMENT AND DESK     :       Operations
REQUESTER               :       Letitia Roux
DEVELOPER               :       Jan Sinkora
CR NUMBER               :       XXXXXX
-------------------------------------------------------------------------------------------------------------

HISTORY
=============================================================================================================
Date            Change no       Developer                       Description
-------------------------------------------------------------------------------------------------------------
2012-11-14      XXXXXX          Jan Sinkora                     Initial Implementation
2014-08-22      CHNG0002230677  Andrei Conicov                  Searching is done by text_object_name. Fix of the save method
-------------------------------------------------------------------------------------------------------------

DESCRIPTION OF MODULE:

The module provides an abstract comment-holding class and contains an
implementation of the concept (the JSONTextObjectCommentHistory class).

The comments are currently only appended to trades, but this can be
extended in the future.

"""

import json
import time
import ael

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

        """
        raise NotImplementedError

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

    def __init__(self, trade, prefix=''):
        """
        The comment history initializer.

        trade -- the ACM trade object
        prefix -- used in the generating of the text_object

        """
        self.text_object = None
        self.text_object_name = prefix + str(trade.Oid())
        CommentHistory.__init__(self, trade)

    def append(self, message, datetime=None, login=None):
        """
        Create the comment and append it to the existing comments.
        """
        if not message:
            return

        if not datetime:
            datetime = time.strftime('%Y/%m/%d %H:%M:%S')

        if not login:
            login = ael.user().userid

        comment = self.Comment([('datetime', datetime),
                                ('login', login),
                                ('message', message)])
        self._comments.append(comment)

    def set(self, message, datetime=None, login=None):
        """
        Create the comment and replace the existing comments.
        """
        self._comments = []
        self.append(message, datetime=None, login=None)

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
    
    def unformatted_comments(self):
        """
        Returning unformatted comments.
        """
        return [str(c['message']) for c in self._comments]
    
    @staticmethod
    def format_comments(comments):
        """
        Format the comments to a list of strings.

        comments -- a list of Comment instances

        """
        return list(reversed([str(c) for c in comments]))

    @classmethod
    def parse_comments(cls, text_object):
        """
        Parse the given JSON data into Comment list.

        """

        saved_comments = json.loads(text_object.data)
        return [cls.Comment(c) for c in saved_comments]

    @classmethod
    def parse_and_format(cls, text_object):
        """
        Parse and format the given text object's data.
        """

        parsed = cls.parse_comments(text_object)
        return cls.format_comments(parsed)

    def _purge_empty_comments(self):
        self._comments = [c for c in self._comments if c['message']]

    def save(self):
        """
        Serializes the comments into JSON and saves them in the TextObject table.
        """
        self._purge_empty_comments()

        if self._comments:
            # there are comments to be saved
            if not self.text_object:
                # the object doesn't exist yet
                to = ael.TextObject.new()
                to.type = 'Customizable'
                to.name = self.text_object_name
                to.data = '[]'
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
