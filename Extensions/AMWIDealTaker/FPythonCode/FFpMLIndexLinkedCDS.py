"""------------------------------------------------------------------------
MODULE
    FFpMLIndexLinkedCDS -
DESCRIPTION:
    This file is used to map the Index Linked CDS details to the FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVt1vG0UQ3zs7buKmJP2CAC+LUKtINCm0lAdUIRLbqSw5dnR2qBqBjsvd2lnnvrq7bmKUPpW/uRJPMDPrtRtSiSL1HF92Zmfn
8zezjtnsqcD3Z/jqZ/BKGDuCt8cSn6UeO/Lc2mdHvltX2FGFJRUmPDb22BCYVfYnY28Ye3FURYn+5hIq/MZnbOsjPfX9XvOw06pz
ePb2yv1OO0/EeUfmpyJpNPt8q95s9RtB+2DQ7nV/JLHBidR8KFPB4f9Ei4SbgmdRyc2J4HSc2/McFSTCRDLVKIP7aKL+Syvoozp+
L7hXD1r9QdBuoP7+Q95p77cHO0RYa99t8518yrMikUMZR0YW+VyZjpUsjX7IRR6raWnAJMhNUgGsOBWR4kacGx4XieBn0pzInI7F
hSLf88JwPSnLQsHJbU7mHm3b+KweJxVPtCky+Ud0nAoSe4xiqCkri1zkBuKfkuRZoU55pLk4L0WMDqFdHl2JIIFjNoyFschgOhVE
k/D61kd75N/wdM1tgM57Khw7vHrw3UV4PYCXYIRRhvizAMVFBUGIiyrCFBdLLOhvVuFA7M1UADZZA9XcgZdhbMwQzBcAY495oLC/
iVLdTZQzy84ncISIMJS5NGFIQgYVa5EON9E/eulP3x/FdjkNUOM6yvgUTuy8qTiPfp95RM0HHo199sZn6ldiVi4xX3tofVzF5gNm
uERbS2xcYxcehYL0NTZexpQgnTPMiU2GfoQpPDcqig1XYigUABTAlA8LlREA+AyKMgcIyXwEbRKl+j4cG4lcqCgdCJXpbYlBBk5B
e3HefAKil3e7mysY37pL0EGkAEyHBpqPpOMTEZ92oRVa51Ibs4p+nmUpcjqOoYRRUrwSyDT1S6k2a6hDiUSaQ6BVOhXKfLGIc87c
MaDjeGKEJpXvxkMqtTDtXA+mpSAMBFgec+tqOODCB9XdfLlw4n2pQtxrNMz8u95db81b966C9XtGdR47dLgK+wQMf04zxATUmcBc
dQN5YMOaDzjoZJcD7PHilVBKJkDIITfRiAZFqYSGwfHADohXUTqB/aEqMl6AGoVyNoEwoPd6nU7vebv7TF8Dxk5j8PDxD98aDGC/
Sx4EKGhuWjcOomkGmpuREbvNhqkBdyhER4xoBIBAM5o2iklu9jBlCKaNKwf3lHh5IJQsEupEKtKHVWOma19qDbhGmQUgsFK6RqVY
d2VA96uuDOvelTJA8k+hSf9i83JcUBGwAueTGdH8bYwtC60JPQot+9qndY3WcKLyjlYq3mmFqSfswmfzNraNjusVXI/AbI1kgFlH
DWjw5RMGf8+Rdx2l9KpDySqZqjovb8wcu6jSiHnr1Fj8VNnn1jfS+Za9XPUAptCl0GQ4KUHBOm57yRJArOYmCkLs7ERYeADUUjHC
CyriJVw+SBQKCCViIQFxyDE3LIDghg/7vcOg0TKIoN3dZ1gYGgvADQ92gsGLsNFrtiSj4XzTwSku8qEchWWkokwYoewoGQljWQRb
c50Es6zI7bRBdADccyOH095EwSAy03behAlHgC6RbtqfBU7dXpmlVq5JQ2KEaCQyQNCazyyvDZeDjEAS5gztQ8Obu5f2AhHPd9Zs
0gjsswPEG/2Ld8vyZr5KoRswfDQpPoZunDHbuQvGUNdPSqECzBclAMeaBsegz2xL0lxbcvHS7VY6x1YcgYaoSFGaLsx/2H2HAl+h
zAZ11IZ3G3pqFT5PvTvwXvM2vK99Qs/sas2hhmFI+Q1D+5sjDOnaDDArAdoirQv7/+kE7lOa0UTNW6msLK/UKAGEtDBMihiM0BCh
tGDoAftfRsj9p9bhn64vjK3S5x9Nmrzr""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
