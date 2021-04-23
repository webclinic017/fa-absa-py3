"""------------------------------------------------------------------------
MODULE
    FFpMLACMFXOption -
DESCRIPTION:
    This file is used to map all the FX Option attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVd1v4kYQXxsCCZfk8nGX9ENqtw8noapJ1PatqqpyBCSkQKhN7q68IMdegom/5F2aUJGnuz+q/107M2tjNz317uEMLN7Z3Znf
zPxm1mXZU4Hfr/CTNgweY2MYDeaZLDDY2MjfTTY28/cKG1fy9yobV5lXYaLC5htsCsIqe8fYW8Z+H9dwh93cQOU9k7GTT/Q0+pfn
VxedBoen2036F612v/vmMlF+HPGTxnnHblu94ah3OfiJ9oxmvuRTPxAc/hdSeFzFPHQS7gQBVzPBu294dtpRKvWvF0pIDjNcc9zw
tBdJlS5CESk+TeOQ5H7kxqEf3XAE0HjVsWy0x19YLxpWxx5ZvTYCsM/4Ra/fG7VoouF8f8pb0ZKHsedPfddBuxIRoVbppn6i5BkX
kZsuEwVYYd8iECByA+GkXIl7xd3YE/zOVzNfg3TjlJyLYsXlIkniFE6ecjL3w6kOgNaT73IXUgH+P53rQNC2H3EbagqTOEJPQ2dJ
O+/i9JY7kov7RLgICO1y5z8eeHBMu1EYcxTGOwVvPN44+WSP/zc8A7UHxHqcfzenNfCNvUTmncEgGFGZITWBx4Lo+84g7pok3EAS
40uNWXazCmdcAwYj09RGTd/CoBibw9dgKyC5wQz4m1Nh4ERVUDypat5jYck+DCX6uIEjIdkzCMydD+y7FkjERFPSE8rxA6k5Zr/u
X/B4ynuWzZMUwukqrpaJsNC5ARWVOigFoDCiNkE8mfiRryYTCpKbCkeJi/jmRqQDJxQKT3edQAq1DW/XLXkVeSINliJtoscK/Zci
mDbRGA3y8D3BPk2WFkYHccgaRX3P2DHcStZWKnnkjh9FbgXxMpkBCbHJ4KCJaiyyXQAuXKJYWmhBNWCYJmEwdFJgltqFqR/Jsgcf
xlwH+We4Aa0ywzUzrOtMc0YY59TIHkyEDMAh0SuTEg35tgmyfEaRUjzW/cNdpCmU7pIPCDLBuxFquFDtbEU7iSnKJSXnqplzqq7d
wi0f9kc91yCKeOWqv8SFKiVmW7uJma/mbn5nvDctKy0yKQQVDAGRu4odHkU1FH2ehQW+9Tws2XyTFrbYvJHdEm//tfyElGznejPp
Dkl3cylU40OFRE9RBLfKrcnSv5i3gfKI5bb32KpSVrPPvNoa7gGbH5KOZ6ij8MZkD9VcwXO2qpYVHJXA15m3mYMnrm4hVyk5EOsR
VCNlDKMtkbZDaHVXUHa8F/0hgJ7qCxQWuYf1Ntw5+VRuls74a/KfA/VB6sdeX6hZ7JGNAXTX5vG6SI4fZ7y1vrioQjr3iZ8uUZPa
0RQsSZBvcK0p9Kabg1FP9b4yQFKVFRZcdcTmYkr+P8FqjcMwjq4U9C61n1mLFmEX2pgNqOAg7sLXWzFMfXeNSYssxLS73rEuFDSu
Dss7f1vESrx0pC8JbSGkK4h6WU+iA7o0KHAjP9Ta0fVzfzoVqF03PlD8ygkWgqKCgqEDEVpeTqcQWzIxzGc6FdR2iz4k79Z9CDmB
xX95PSdvZQGYNCclzR/RobCtYBOSX1GHOjSO4LdnfG0ewVvNODC2YLZnfgNjs543lMkkguYOPb9BE30HTybUoi2MBTU+C4NBBgoc
/w8GFzGvxNeasVXbrmxtaLN1suTFLpihJr9f0tG5dwUpKRo7LemQab4gjm6r7chZN4jvCj5b7OMBkvM/a3d/oeA3COi2/pj/AGAt
hkA=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
