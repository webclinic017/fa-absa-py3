"""------------------------------------------------------------------------
MODULE
    FCustomizedFpML -
DESCRIPTION:
    This file is used to modify the FpML as per the incoming source
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
	1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
	2. This module is not customizable
	3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtU0tPGzEQ9m4CNNv0xaGnHnxBQqoIantDVVXYJFWkJKDd0AOXaGtPwLDZddeTQio40f/dzngTVahST3jlsWc8j2+8n5VYjZDm
Z5ruLQktxBnJQOhQ5IE4CwQE4jIQ92QPhW6IX7Rp8Gm62+SgNxS+90gjGh13T4e9SNLoxwuH5dz8BN23o6Hci7q9NE4GJ5PB8fjA
u0wujJMzk4OkdeFASyzlvNRmtpR4AdLHZU5aqLxuCkUJi3PpykWlIPraS1JOJneSnSjppZNkEHP2dF8OB6PB5NArB1HrXUceFss6
tVEZmrJwXIuTOlUZi25fQqGqpUVCQX6LHMikcsioNNygVKUGeW3wwhQ+TJWVh12UKN3C2rKiyI6MWu87dV91krWLWl1G9i2HqPWB
fTjH3JYFFCjn2dK7XZfVFXcMNxYUQ+GKMvsHu6awuoG/lTLkO6yoDy2jvUcb5jeNsWoQVzZo8hozbywJFEwtItt9IO4a4tbz6ioU
1YyZRlTMQ3HXFLdNcUmnQtySJ1loQ1Rses+x0BviLhTfZ964uQ7fWhkL4QNDMWPGPqGiY3xKsn8yGk7T49Mk7iFjOjr64pHic1IG
hYaboSmuQMfd1LUYczeV3ozPSEuJRTmMszmQ3cfT6t8DviKhymJmzqc2q8gDoXI+6zlgbfqR5QtAxtKnssxS5BJ05oC1Xb4o5Gwz
O8+xvdqMiUJD49DjtxX9NYWTpYW6H8v9eF4nW6TvirVw23z88DV17BIjMtePhS0v154ieBG06dum2fK7ui9OOp3qUk2n+JozclTs
Gz3hphLINFQJQ0+ePQDwXxR8Cx9rBn7iPtwmic2gHbbDPye1JMs=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
