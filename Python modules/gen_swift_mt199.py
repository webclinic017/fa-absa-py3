"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    gen_swift_mt199

DESCRIPTION
    This module contains a SWIFT MT199 message definition.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2020-05-08      FAOPS-746       Cuen Edwards            Kgomotso Gumbo          Initial implementation.
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from gen_swift_mt_messages import MtMessageBase
from gen_swift_mt_blocks import Body
from gen_swift_mt_fields import MtField20, MtField21, MtField79


class MT199(MtMessageBase):
    """
    An object used for constructing an SWIFT MT199 message.
    """
    MANDATORY = True
    OPTIONAL = False

    def __init__(self):
        """
        Constructor.
        """
        MtMessageBase.__init__(self)
        self.ApplicationHeader.MessageType = 199
        self._body = self._create_body()

    def _create_body(self):
        """
        Create the body of the MT199 message.
        """
        body = Body([
            MtField20('TransactionReference', self.MANDATORY),
            MtField21('RelatedReference', self.OPTIONAL),
            MtField79('Narrative', self.MANDATORY)
        ])
        return body