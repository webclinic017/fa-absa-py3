"""------------------------------------------------------------------------
MODULE
    FFpMLACMFX -
DESCRIPTION:
    This file is used to map all the FX attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVd1vIzUQ9yZpeklb6BVUQLwYRFGE1FR39wYnRGgTKVKTnjbtAXmJnF2n3bBfsmeVBsoLvf8bZsbZJIBU8XBO1lmPx/Pxm984
gViNKj4/4GNHOIVCjHH2RFgRsSfGXvleEeNK+V4V42r5XhPjmgirQlfFfEfMUFgT74R4FOKXcZ00Rq0dMv66IsTpexrNwdXFzWW3
KXH0evngsnM+6P0sT5sX3dG5339z3b8afsu713eRlbMo1hJ/C6tDCZlMVC5VHEu40xKPKQATTQvQVmYpC1WQtPupBVMkOgU5M1nC
8igNsiRKbyX5bL7t+iNyJE/8k6bfHV37/XPyPDqTl/1B/7rDCxfHi7bspEuZZGE0iwIFUZZaCoWs2sBEOdgzqdPALHPAIFGviDWK
glgrI0HfgwyyUMtFBHeRCzLIDGeVZiBtkeeZwZNtye5etl3mzk6pFRQWMP7f1DTWrPaK1MhSkmcpZZqoJWsuMvOrVFbq+1wHFBD5
leo/GYR4zKWxcaaAgDaYTSibp+9tRH/hGEITubQpeVByGMklfiSafY2TFsxbQTxE0mrm6juPiVph4Y7wRy3ifeDh5K0MnJOBb3AC
Ieb49cQDEtkTHv7Mmfy0gCqJJzXHbTJiBzht8SWIlcXq3iESiwh5NtVEudyRL9Sgotg6Uo1+GlzKbCb7/kjmBvELQMIy1z7lNOTG
gaOtjDdO4BmKJ5MojWAygUNKxWgF+jK7vdVmqBINdLqnYqthH9+mHXuThtrES21alDHUKHQdz1rkjCd78A902/nSJ1woAltnmA+9
Ay+ori6NaokZ3hjiwSPMzOcCPAIL+59Qqor0O5bUWGGH5J+5DQK1KuxbAXUxrxO6a41jxPlPT6RiC+Mv1ykihDNVxHDWTXJYUgdv
YLFfUUyFMdhLS3nieJ8bbaku2DihAjVVVreHrV3CgDCK7PCiB+QE+x52GYICCqN9hqlBgtIkQ3mroVy/gOdbkHXvA51TZ3DIPkHG
hJ3lSfxGGewK+IAcpna7GE/Av1XYTY6fkmqTy9HwjirHXsMLKqty1MqS/L4pyYILwFV5YOFjxVHaowI8cHEeHdERDywFiXa5Un/w
EVJ8Jh4q617AdYM3mmK+t/ojeHTbKf+FuJoNGUwM/BopzXQj2FoEoU87Dt9PmIawya+zvo8ZvO59HpnlBUIABw78XnSPlzBJfOoC
n7T8vRLsFbCowWBvlhwFqeF9l2TpDWAbcvnQZDctkh525Ahdp7f/Kp9drMtHYQeYxNV0/mTbUMt8QVuUrMAKfeQd43Potdiqa94U
uxSbt8kLd3tOJtxxPoHlf0jTUenlSX8kfl62ad1r1PcbjuC7bDzMArTMYO2vgT8srbjcHB4fk7BzruxdL84Wm6L44v/EwYm9dql8
v1fytO7tu0/lb5WZ6Ns=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
