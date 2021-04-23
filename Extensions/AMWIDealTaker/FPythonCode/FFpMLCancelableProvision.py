"""------------------------------------------------------------------------
MODULE
    FFpMLCancelableProvision -
DESCRIPTION:
    This file is used to map the cancelable provision if applicable
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNq1WG1T20YQPhtiY2MwbwUSQnJ0Suu+YJp08qGdtlNjnBnPBELP0Jkw0/EI3RlEZUmjOze4k2/tP+oPbG9PEpxsAZaSyONjJe/u
Pfvc7t0KE4XXlPz+Ir/8hRwoQqdyzCGaR3YOneYiOY9O84hOIfoA0Wn0D0J/I/TmdAp+69QKYF7PI7Tzga7ywev9k1etMpbXy5fe
waum4ZjMNs5sduS7f1rcch28U95vdZqkfXTcfn34g9I9vrA47lk2w/LvgDOKhYv7hofFBcPmtQ/sXTuxetjwPNsy4Xn5txbpgDO8
TbbLpNU5Ju0meO/s4lftg/ZxQ90Ecz2r44YzxH2XWj1pLqQ3DtPBVNz0LU/wXcwc0x96QgKRegObyUemzQwfC3YlsOlSht9a4sJy
AoSur5A7rsB84HmuLy3rWE33vB5EF/iJtMwBF27f+kuhB7XvQA089T3XYY6Q0Q+V5lvX/wMbHLMrj5kACObFxlgEVJoFYdxMZggg
05fRUFze+WCX9Z+8DsW6zJ7bFtmMsjQnv3uQZv/KgSGVmQjyENIypwSVjCBMQ6KCEOXqaQHyFoQiogUlzCBaVEIJ0RkllBEtKWEW
0bISKojOKmEO0YoS5hGdU0IV0XklLCBaVcIiogtKWEJ0UQnLiC4pYQWRTm1Z4jZzYSSyVFATouFyEAhdqnp6h1A3h0QeXeaj2ykI
DoTpSHgQCYVIKEbCTCSUIqEcCbPoPHBYCSoWip6vACSfGUIuuG/IVHTPLmVuYAGEH9bmANvq9eK4Ts86PzJ8o0+YVPbFIpirp10P
HjPBfC6WI4NG86Dp9vuucyIsm4tZpX1z/4W879627N0uu2K+aXF2PPSYqN+tezYYMl8iE0PCesyXNcfE7t0mnNn2mM03d9vICH1Z
Jk5HSLN9yZr4ajKDlkOV+s49IQ9812NS/cqz/KGyeD6Zxd6AWw7jvCkLHtagPqFZs2nYsqYNafLtPRQzvz+ggC1YFkDHa5DKYhpS
idm9GmSNGvjGHRVd94ZiBibrWo4lut0qGECWoXw1V82VRj5mPiyX65KBtHwXZLU6qTo1+Il/omAItY9GyYMhew4VTAJnlNIkMKOo
wDai5VgK9NVgppZmvQmP8iqI6xrPRYCLSJWerPGOgqKgnidB1ZDmIqQpgZ3HgW1pwCZlclNjUpUW9qBOsB8VSshoMc4oFH5CJabA
vxpMvDfuZDsVv5sav4kBaPiz8Lwa+E/A+WUGup9odAfb0i18z8T5Xgnqzn4PwteCqTsJXnZSMf5EYzw5Bi2ELJSvBRMkIX2WgfMN
jfNGuEtjDvs6pnJnCwkvxQmH827sDEgRQ7BgojHq4kUqqjc0qhOga8iz8LwSeB/D+H0Gkh8mkQwtpEZxOU5xVaM4PDVTgF+KExw6
+CkVvQ+T6I1Aa5izkLsUJzfE18hA7WON2lZ4mkNnL/sGnd3ZOLsw/3iTkSKA8IxtjflopeL4scZxEnoNfBaaw+N1HGU7A9NYY3oP
miDZLjk3pzbA5SHb83G2AUZy2zR5KOvhiZjk5iAV51jj/LY4tDCy8L4eHotJYH/NQP1WUpJHrS4Oe92Q+0qc+zUt00ea4xQBPYqn
+4ijk1T8byXl/GgwWixZFuBRPPFH8L75yEswN94OJrxopG8HW+NOfv9Y1M+9Z0uYgNW4wVqDLSF8+XHkMdftirK6Cf7N0u2SBZga
tmkC9BHQJ+CaQG0ROJsIICGwgxJoushTGCBC8ikMn8EA3TKB92sC4Am8pZKvY/FMFBQBJdgN+OdyKORK86Xp+z6Bd3glFEUVGnVN
GZdKC3hKUHocirEfA45+hlOBFxSeivz8D3UXz8Y=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
