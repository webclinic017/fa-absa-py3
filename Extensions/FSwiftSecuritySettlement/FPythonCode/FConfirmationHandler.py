"""----------------------------------------------------------------------------
MODULE:
    FConfirmationHandler

DESCRIPTION:
    This module processes the confirmation updates.If the confirmation received is
    eligible as per eligibility criteria defined in the FParameter it is
    processed.

FUNCTIONS:
    process_confirmation_transfer():
        If the confirmation represents a security transfer as per the insert item
        query set in FParameter,then it finds the business process which is in
        the'TradeGenerated' state and whose subject is the same as that of the
        confirmations trade. If found,it triggers event the 'Identified'

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVltvG0UUnvUt8dZpoS0ECoUVKKorlUSl3FQBok2dYim3rh1AeVltdsf2JPbuZmbcxCjhpahShcSPKD+JF34CLzzyDN+Z3bWd
S6mQupLHszNnzpzL952zAcueIn7f4Ke6GELGtjFaLCywvsW2rXxeYNsFxgtst8DCIgtL7AlWivluiW2X8nmZbZdZWGY/Q1WFhRUz
mWHhjJnMkkyrPksX/o2rP3qFj7228WBrtXHXdvCsLMdRR8iBr0UcfetHYZ9L237QaC27zc12c2M9FWv3hHIGcTjscyeRccCV4srR
Pe4EU+edYRL6mqvFZufsnuQBF4956AhlVPK+6Iod6POVk3CZvYu+0CMnkEJzKXwn5B0R0ZnIKFzZ9KU/4NhzhM4V5faEi7a9srW+
TFa37k5vedOGeFr6kepwWb+ZCtFzvsGJ5IpHWjm+o3gwlGRafjo3m46JSHEJezQfjDXuD7kc4Zgm2yd234J8RMbDrzCN4M5QwUel
cmudg54IevAOJ8fqIHijLf2QP+QRlwhyeMNRGv8OcoYTseKOGu7s8oDiYvQq3EhW6p6vndg4OFY37agin0K+SEHoxMMovAXztBTd
LpfK4Y8RAaPvRjPEVHQE7rbt7xpui+DhLLgLtu02Wm23mYZ+abW51mzfy9JQvb3o3ItGBB4cDfIb49REJDrRSzwK5CiBTxnEloI+
9xFafqhhacidA6F7GQSCWHLyMIo1HE6SWGrKfPXjxRMgzSSCodLxQPzoA2gQukNCpGOQxBH5NfBHRu4glnsUK36YIIIwhG5EaE/b
HeJYavzkKkR3qAjAEex4lUQV/+BZ1xdQBFo8aHHdJ7LqD/C+0srwiFXd5wP40ozWY2Rn5BlGdwMLYgX8yvgtUx35CcPoE6YZO2Ls
icXkHaYtU6ksWtktsieMvYkNS5cyESti7PtomZV0me3ZTI6YdUz7OFahCqVn2JFFgukxLM9O1rICaFlWZLEfUOpa9QrZcQ3DGOtq
bH9ePGh7M90VUfckJReU+hzbDSlj6cQBQiApVz0xKUtnzqRqgVOlqZzyw8ATUScWFJ/1ehWjvoxBKC+vSF5seGTEo9ggXiIkjDXX
VzY0NYINEerr+P/P+qJJd+Mw4Akta8pDw3U3XKNBaWlWHjTubz2sU570FQwnFGVmkKG8Tj3IDGqe8n9O2V5MRvrqC4x6nw5epOOF
olWz5q3XrUsYDUhmpkHyB4HkVwIJEp3CI4XCMSaASpXtVZh8ZraKBAEsUvKPi4xQU8yzXmTHeC0Z0TKhBfO3j8vsqMzkU1KJye4M
IQ6QwUhanzKEDNfuP2X7zxigBxy1UvjZBn6/A34V4OwC261R79Rz7KgygR+WL07W0FLRTMfwmwX8bPKwbpLtpMGddKEOEHWmyJsU
rbU/vf2FqlHUF1Qzyvil30hpaQ60M/lHVPQ1y685hVNUsLMoI2C6lP8MkDS6lyjZNBgDVvw+aDJnaH8gOnptdUuLvtIfYqXLtRcP
dTcG7r2B9vQo4R588fxgkAOI3B43IKVn0mO+BgQJipDUrxnlGrU1vNd6tJr6QXens4rxtU/KiAdtOeQuscOlN5dw7tIlLpWqOul3
KVymck15bG7ObDTKEzJKE57zyI/J4+2PTTAzdy7H/0tJ4JJTN0no3QzwFYC9VrxiXS5UrDnrPbzNTuBPV1Ry+P9F8P/NlENGsAQa
AUL5S04FK6NCCv/stWhwb7G9ApPPiQa7ZcMMUyWhBLudQobRGcL7kSFVWJwSYdnECBaZtf+cRfO5rtJk32hJOVE1nPgTnCiZkr1r
G05cIKqNOVEiqozXzuEEJU+9N12ST1TPMRMumrxPf4CoJSzd33TxoQQB9HAqvdQbSQqoTnto+pGCN/NpoR5OsWbyLZVr4NnhaDjY
wTK4Ed46ac/UjqGYMSnv9oC0H/TANFhxsm+E6rOX9I3za/hpds7lnDT3ulSyTc0lGubfcV6mUV97wYZnYpJyh3S5BD9tCsxae9MX
cs3XQc/QNoy9voj2ENmUb6eoVh5TjTYQRc/Ez9B6J0k7EP6zC/8HhYipX5HQW+OeQSQCjazr1lLhHUOftHmSqOeFceB57nzeTdNC
5XIYI1dj+pJM3aWAuQs0EJ4MU81dE7Ne3uMoEF+m315fm9pBxati1Qo16zLsqxWqdvXqv7l3g5w=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

