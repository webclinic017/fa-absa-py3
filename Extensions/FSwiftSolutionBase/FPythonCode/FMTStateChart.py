"""----------------------------------------------------------------------------
MODULE:
    FMTStatechart

DESCRIPTION:
    This module creates a state chart

FUNCTIONS:
    create_state_chart(state_chart_name, definition):
        Returns created state chart of name state_chart_name.
        definition is a transition dictionary
        e.g.
        {'state a': {'event to go to b':'state b',
                     'event to go to c':'state c'
                    }
        }

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

