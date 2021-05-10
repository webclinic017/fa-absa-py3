"""
Module for handling password reset policy

History:
Date        Who                   What
2010-07-14  Rohan van der Walt    CHNG0000371408
2010-11-16  Jaysen Naicker        CHNG0000495337
2014-07-18  Frantisek Jahoda      CHNG0002141151
2016-03-01  Frantisek Jahoda      ABITFA-2818 complete rewrite
"""

import acm


def _has_kerberos_principal(user):
    principals = acm.FPrincipalUser.Select('user=%d' % user.Oid())
    return any(p.Type() == 'Kerberos' for p in principals)


def _outside_of_organization(user, organization_oid):
    """
    Check if user does not belong to organization
    """
    return user.UserGroup().Organisation().Oid() != organization_oid


class PasswordPolicy(object):
    """
    Class which represents password expiration policy for a given user

    Attributes:
        user (FUser)
    """
    EXPIRATION_IN_DAYS = 30

    def __init__(self, user):
        self.user = user

    def does_apply(self):
        """Is user a subject of the password expiration policy?"""
        if self.user.UserGroup() is None:
            # do not apply policy to broken user records
            return False
        # Check if user does not belong to 'ABSA CAPITAL'
        outside_of_capital = _outside_of_organization(self.user, 162)
        # Check if user does not belong to 'ABSA AAM'
        outside_of_aam = _outside_of_organization(self.user, 165)
        return (outside_of_capital and outside_of_aam
                and not _has_kerberos_principal(self.user))

    def days_to_expiration(self):
        """Return after how many days the password will expire"""
        if not self.does_apply():
            return self.EXPIRATION_IN_DAYS

        last_reset_date = self.user.AdditionalInfo().PasswordResetDate()
        next_reset_date = acm.Time.DateAddDelta(last_reset_date, 0, 0,
                self.EXPIRATION_IN_DAYS)
        today = acm.Time.DateToday()
        return acm.Time.DateDifference(next_reset_date, today)

    def is_password_expired(self):
        return self.does_apply() and self.days_to_expiration() < 0

