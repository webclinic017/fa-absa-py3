"""------------------------------------------------------------------------
MODULE
    FFpMLACMIRS -
DESCRIPTION:
    This file is used to map all the IRS attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVN9rG0cQnjtJdq24iQlpKH1aKClqwTZJ6UsIoaosg0BSzEmpG0MR69OefPb9yu4IScV+csAP/aPbmTmf5bZg+pBFt5qdnZ2Z
b+bbDeF21Oj7mT63T9MU4IRmD6Y+JB6ckFAD48G5DxHJdfgEcA3w4aTGFqNWgw++9QF2P9NoDt4dvO93m4rG4WEx6Lc7g14wUrvN
g+6oE/SOxr13w9eyPT6LnYrixCj6nzszVZirVBdKJ4nCM6P4nEa08ekcjVN5Jlodpnu9zKGdpyZDFdk8FX2chXkaZzPFUZu/doMR
R1IvghfNoDsaB70Ohx7tq35v0Bu3ZVEm8nJPtbOVSvNpHMWhxjjPHOfCXl1o4wLdvjJZaFcFUpZkN08MqcLEaKvQLFGF+dSoRYxn
cZlkmFuBleWo3Lwocksn95SEe7VXQi/9VFbh3CHl/4c+TYyY/chm7Ckt8oyRpnollovcXijtlFkWJuSEOK7S/0EwpWMljHUwjVxp
S2imqrn72Ub8F40hPiI23Wt6WFGU+AW/MNO+o8mA0BKYiic+mBrT9RNxtc6UZGUDglGLaR16NHm3Djrs4AeaEOCcfh5cEpc98OiP
6E1OeIE1Vk/qJb3ZiRvQdI8wYaIdtfeMSrGIiWmnhklXlPSbGtRx4kpWjY4HfZVHwsPCUgFDVLgqTMCYhnJ38Ol9yHdB8AtSTyZx
FuNkgjsMxRqNpp/PZsYOdWqQTx/qxBncJum07d5nU2OTlbEtRox1Tt0kUYuDyeQe/7O8e8Uq4MI84b0NqfOO96UX1m4fhXpVtG//
VbRLmn24rlHpfKmWVG/U8ivjMlkqRqTnCe530wJXUoU1wqHUNpBU1/jW+wHjK204NWzSFBVpcqQt8Q8ZSpy5+6gfxLlJqq94ry44
n3shJ9u4/QTlnzRdCkp7AyvDKM/l4aP3zqayVWP5yodlRwoAcPD7T3BFjKnBeZ3XVIYLH+wH0TQAN4RTH19W681qfZwBHH+8gTp1
+qIJ9hq8qzrt3MBvtLPm3vfSRXql4iURLDEzvrgFXWQW42j9vCmyKjnBlsPWFleuURGBK4fc55nBI70aLXQhdrhZ6vpm5kQmYUwM
Ra45GdJSzo/t3AQsIPvtLkNT8BshFF73xy3u+sO6SIvbRiUiN9s82Cd8VuItQ/eiu+5+w/pn0rstr+Y98ba9He+pt+N/TXJLMiiv
TEZ3g65MUxblozWZCM0lfyFC8LxK4WHSsP5xdTk2vK2N7UZLirAp3qd5SK6FwZzZYbuj3dlhki/usRj+VyTJ/U2Z7dtHFU03vG3/
b+67u2Q=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
