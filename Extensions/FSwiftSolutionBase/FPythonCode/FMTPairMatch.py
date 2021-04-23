"""----------------------------------------------------------------------------
MODULE:
    FMTPairMatch

DESCRIPTION:
    Performs the pairing and the matching.
    For pairing and matching 2 instances of FMTnnn class are created.
    1. their_mt_object is instance populated with the incoming swift data
    2. our_mt_object is instance populated with underlying acm object (e.g. 545)
       or outgoing swift message (e.g. 300)
       (The security settlement comparison is ACM object vs Swift message.
        The FX Trade comparison is Swift message against Swift message).
    Based on the pairing and matching criteria defined in the FParameter
    FMTnnn_Config i.e. FMTnnn_Pair and FMTnnn_Match the above 2 objects are
    compared.

FUNCTIONS:
    get_pairing_object(their_mt_object):
        Returns the paired object for the given incoming message.
        their_mt_object is an instance of the FMTnnn class populated with the
        incoming swift message.
        It searches in the following order and breaks if searched for object is
        found
        1. FMTHooks.pre_pair
        2. FMTnnn.UniquePair
        3. attribute pair as per FMTnnn_Pair
        Finally FMTHooks.post_pair is called.

        Note that a wide pairing hook might find more than one object, and that
        in such a case, the post_pair hook can be used to choose the best of the
        set. If the whole pairing returns more than one object, the pairing is
        deemed to have failed.

    attribute_pair(their_mt_object):
        an our_mt_object is created for each acm object returned by the
        eligibility query set in the FParameter FMTnnn_EligibilityQuery. This
        our_mt_object is compared with the their_mt_object based on the
        configuration in FMTnnn_Pair.
        All the paired "our" objects are returned as a list of paired_objects

    do_matching(their_mt_object, our_mt_object):
        The their_mt_object is compared with the our_mt_object based on the
        configuration in FMTnnn_Match.
        Returns a tuple (cmp _success, cmp_result) where cmp_success is a
        Boolean and cmp_result is a dictionary of tuples (their_value, our_value)
        E.g. the cmp_result could be { "amount":("3000","4000") }

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNrtW91zHNlVvz1fmhmNvi3Lsr3rXrOK5Y099nrXSdbsLrH1sRFIstKS4+DEmWpN90gtjbrH3T22tZEgxKlAQQEFZKF4XF54gqrs
A0/khaJ4zQtv/AE8wCNFwQMF53fuvd09I8lWUktVqsBb09t9P8+955zf+bhXTaH+5en3VfpFbxhCOEI8oqchnJxoG+KRod9z4lFO
uDmxkxNOXjgF8YJK8rq2IB4V9HtRPCrq95J4VNLvA+LRgH4vi0dl4VaEUxQ/oFmq/F7i90HhDIgfEBk14ZT5ZUg4FX4ZFk6VX0aE
M8gvo8Kp8cuYcIb4ZVw4w/wyIZwRfjkjnFF+mRTuWeGM8SxTwhnnwnPCmeCXaeFQy0muPc/vZ/n9gnCmuMFFUL4+ew5b9VZViOuf
47/qyv35B8sLd6om/Vtc2VizvXDFjpvb1er8wvqctbS2sXR/VVavuWErCPciM952zQ419Pwt0/Yd/t5DJyqoy5GCsKeFrjVvmZ4f
xbbfdCMzaGFG3/fNZtuOItMOXbMZunbsOnKUt+sY2gsbe3Ej2Nxxm7HpRckAZifodNtobT7z4m2mwvObwR7miZ55rdh07NjmkW7V
zaB7ynG6vuOG7X0mvblnqg6zbn2rbt5+9/ZVHpD+0RKDbrwVpNPtuVFkb7mq7Ts3byZtZzeIuMhtdkMv3qeXOG67e64fm0Ruxw69
KPBB0t25FT3f08hczw5a10OZGGrxm+ZGaDtuX/+eHqa9ZWONvaVX5UD37IjWS736eZlwqkmkuqFnm47b8nxq7MnGi2t2aO+5VKdl
hjjYmAv8lrdlenW3rosgSjyk+max4iHszeCpS6Igl8qM57HkYsD96uKD1TlI3roUvS03bigqFQdn+yTj6p1kgyw37oZ+KqZYqNxU
El8u3fKeun4qLEe2+Bips/1UYEhweSeywntUGJPR+oTyyGxLMUmEHTa33Uhvcitot4Nn6BOEJI28jZukGrvUoqVbO7yehMRkvFZA
Ipx8vc0M+VoQ7Eb1TujyNiaVtzS36g9870nXXctWvlM37TgOvc1uLDfStGmdRE2GwUnjRc+32+39zFxBJHmG3WtSHfNVN18NaMx4
245NmzbMSWVwmzqbe97WNnHLgzwGITf0SVhdtdhrCnXsOLPHZtQl8bJpqsi9JnmfUMCDNmmMTdfsQvDjwGxSYeRyw02XtEQyNRmQ
dLRuLklGP9sO2imFoRKv4ynL6lOGJ45L+s7zbtsk+y3bS/cj2WQm9iWCjan6UUwBJouCa2MHUsySlFLl5n7P2ty2t+Vtem1gETE9
ZEQ6qt+azwtp86+jdZ0gKLO0oyQpNU5huV+fNjPok4zTZAjphnbsAc38rJilynK33c4q9mWa/XIWSNJFk7DaZtuTrJXN1fyR3Hcn
aGi069/0a72ryvBg45jlHLvm3m35mVbMSFk/gme2GXc7JIizzb2O2SBxJyMaXTPpqxG6UbcdXyVJdWFEqURVM3QlI90LSJBJiqA+
aTduYzpeE2TYJA1QBcwUmWpfntrtriv3hF8Tu2YuwNJhuZnhmkG37UDVvmtetvcIjOLLd2Yvkzm8efna5Xfxv6vmYbX6jQVrHb6F
OWPNVKvWwvqGtSQx/8by0srSxl2F/xVCsLv+Pumb47W8Jm9WBE3CtBGZqU58w/Wb4X4HekCtum33RpPWSVjvPgc5BC9gixLwJvSW
luwHhLvdTicI2eGo3JJyrUbQLZrdKCb0/tjebBNkV96pswSA3aT1ZMD37H1u9ywIdyFy7vMO8VsLgn2EbgdgwcSnUxEKEiqR/vpE
x+fp3Xn/Tf9W40HyHNkJsFzyGcIYnuRipoDA2GvtSxPezFFliX5F+s3B5fxXesRC7LBH/sIQBvnLhzmx/4diS4jDvIjzYqcgDgTq
qPwgJ6JPRVxECfmt1PhFXhxSg4IIH+D5QqCZL9Ay/J44METUEXFJ7AyghAZBIY1ZVp+GXxNxRU8g56vikxpRLCDHeujPiQItdLcq
wn8WxmFRGKC5hpghHhIHRXQ+i9HkUpIyCigcvBiGb4hvHsDRHsCq6/QwPyJY1GCecSGON+jRh9RlI2THkRgsTV+fi6GlIrHaUiTh
pwIhYvLuRWqJo+v0ufC86XYYIIIm+Y+h9MSOOkQmKVIUl6mH+7zZ8PxW4FFYJVZnh8E/lPtgs0f8B2vnF+49+CguoAVJJNdr080f
2lWIsRs0G4wUbZoWnJXlB7HXjuJxKvGihrQobVfREkOA7E6HBDrG9L0WjphJ42vjzF/JIpm2Bcu6b8UID6M4nMVY3ChB0/gsZt3y
SZEztmlu223usqxjWN10WH2n4B+PUlGXN5kJaLS6fjPGXrmzCEv5EY3IDUnioXpnnxd7dOPvoflldMoNGSUjT78R+o3Tr2ZcMEZz
NWOaSqaM14z/Vy6pXF89jXKFbieQJjLckxby81Y3C+yI3v8ZlKxBFDZAWAOERaxzFgQ1o2sWlMoChy2w2sKKLaiUBSG2oOIWpNSq
gfcXj6hH7xwWDwlptCC31hgklMeFNFoTeJzBYxIPKIY1pYX4ZEl+41hJ7lvdw0Sw86cS7Lz6sWBfTQQ7K7xxDiJJn7sknjOQtnXC
oPVZuXtFvT/xLyn6dIANTyre77hMIXm4imDeDQaxjbDrMnYs2u3InQUZjFyqLSMXi48eiYECter7FRs2TWXk+niOnp0pUdu3h16g
QtB2NLEW/ZvTNaTd67Msbh9B9i13DyEwRUXkPPjXQ1eGjlpsQVBktsJgj+VVo2s2cQDHdpX3jaVMvo2/mvPYiL1oS+4m6H+CljmG
LyZ9MAtPD6hkv2gQC3cEYwspt4FUHHEOhZx7e5FTDCYG7JSAS8RphgOJYc83UDD/eBlIRVwB+BTENMEIoUT0Xe5WYSypMoQpLHny
NUaqQbQirKHZd4bwVHUPCdoBUhK2RsTOKD4hbDmUbDGEzT8eF4clcUAAOIa+38mJJz8RhwOaVELOAYVc41pQyyKeUAh4UGZ8rRAC
LhECnmEEXDOMwyp1oBEmAW+gupoiIBWfTcsIoZ0BRkD6/r4hGAcrJAsAhOgmZGHrKA5mowWVrEgwgs1Xf0gWfQGs9trI2NAw3QjP
o2Ee4CqyqCl3og92XTlfALzTuFg318h9jljetMtMvj15vA7GzUSIXNGM2/v16M2ErLabBGStbB4wdHn+qyfibS8O9oHr7FSi6yS6
EiaGpYsAgLCjBlSCMTYGssrgikYiWhmSue/S6uJ99ixIjXknF9djciOcu+tfX+ZN4VYP71qrEltK7E/FcGSKet+4cN1tw70AUS3e
934fKGLgjwHLGUY0eLAIng6ouO85TEUWixGIsSNI8akqy+A/qJgd1MrOGKcRbbxvKua5dHf6aePxkS6QjRgMI94IuULQBtg8c0zf
RkBE15RbpQmW5ufVlscC/nQ5k82Qk2dTMkYmZciAkTmfe41Kxo1LVFYzzrJ5mTaqxlFoWgI0/af4RYWmnZGXw9GohqMfHw9HYxk4
Gj8ejiYYjuZTODpzPBxN/q/CEbsc5DPMZTy16P8MKPHq30z8upnEzftC4glewQMKYWES6y3txVlfxOMaHtcTP/EGHuBD/PoxsNDn
Gt7qdQ17ocF6B4938biNx5fw+DIeX8HjPTzuJI7jKTQXLtAfoHL2RM1Vepvr09tCVm+f0yOrtB5HLPsXob1wD6kq36O6MvoosLBH
FH3kpVSzNpPKSh8gEfZyWqaOC7PRB6hYZYjn+HoeFsFnvy6RiEweDKdddnzNbCKyzErYFfS+Yi6EYRD2CURFCwTP4tLYGXkYSYQi
8eUl1wo9XJMBMkIBhtZT8OZtKvtLVI6yF1pjd/2ids5/EXlQy8AG82L55+VFdpRX8MT6sFc/T8kP61dOqSIIJX98IhtA0KhKADAb
/pHcbmmH9n8jl/KD430KnPBeBD8kM7Tlev43BsVQ84//2lCmpKDMB6L7WUNZMf78dg7GRVqz8Le4cYWtVZUHLwt/hK3eIOyONDZk
5cjM7OZF+BfiyXucSaC+P4VPRZaOzBy1dET/UNIs+eO62YgekFMLcM0r6EXyZNAb+eJk01haJmC1qEi2JW/pgHsgOZFn8qvicFD4
PwRdJGsIGz8wHM55KNK+YySkSbpgp6lBTfgXMuQIuOUvuAEsck0c1JgukdAlsnRNMhW1fkLIaoZ/b8D2T6ktNmiTFIsKvCvnMAvF
iweDqG4pplGrh/F5rRRFXsjbOdWxhHKyy9M7F3hLLzKhqojH08P4lkhHGeBR1vUoZZnPuZn1NYhdQ4ok+BqPcofDmlra52E5qPQm
XmPl/mnOOByh9VOb13HpIb4kDkZS5aZiMy1zBnV6h761N0Eh/SyUezWaUTDLdlZb0Uj5Acnx8p2ZiMFgZeO92zfnqeipK31tLogu
SS8Zdte5Zs6lx93ysOFOdSZiJWdTv8hOQ++ZL/kTnAVSg0Qeay/M3zyVsKuBc0Zk6ns6RulRjoYjTXO0msx13CFg2lFGBkm/unnE
F8GJFTsgMyc6IGkYkDofs28kZgZothSpjUs9Dk7iLkW/Rmu732L3Q4Y797D9bhSthQHOh2QcdUn5GluuT+M0GzJTAs+rgSREY7MT
cqx113E8BuT2kt8KeECZDZZ5CwRm7A9irCRjgwF4QA46CDIX7SaFGvscGs3x8aWifmXjvkzrlHRwJ6t1Ofe46+x0o3jRc9tOtBFI
gXDjCSbF7vSVWxe1Z8X7EfgN149p6mEZXunbEwjHKnox87Rszs1JPwxN08OtBoWbHB21XZmrnsPpv8yjk0HqS9RJYzKaGJPbiTGZ
7LH1XsI/+Ga8TykLOGWTHDlypFfSJRFHbpnzPu6bksujQ5QaQTeMOFHIIaMOUU9h0+Bk/i0qN9imwaLVyMUbyw2RuzdJ35O5EVi6
XMm4khvPjZIzOGJcyNWMCtVdyF1ASe4cvY/mrlCPd+k3mrtEPU92Ef8L3CnDMdn/K+Bw+JmyiDJHDjtA9qnBhTldmKewLddbhEhO
cDzIFY4Mnwy2HIaIPkZVXDiu6hOuKh5X9ZlKpztcK8H9szRLXmYY/Q/lI7GVJHxHAJbxkUowuUkZAXnWR0KmEGyLzuksuRRTm5TG
5LMKiCs2rc7newxoEgNN7ODRxj0xVXTrpfnudK5G0j2BnVVGdqmeBc58qLxI1KGATuZeJqQMzfG5aUoM6y6Vr8e279ihk9ZIzHrr
aJo7dcXkZCCnrMSbP0CHPEI9Tc57SgHTMSv8t/QIh/PcuUljgv6bzJfkj0ovZJ3pXFZa/5we+/fZQxNid0CEfF/vgHO+75NcOHld
cVtX5GVFQVesKmmikvcTSRIsST8iSYLIcGoDkpRXGXQpSQa7f7oMklROJUloSUJ4gDt55EGb5DXbHFSzd81XAWyHDJkXsV3uaMda
HgPOraw1cBcrxuYw8N21PmKWLy98Y2GZxXAlunGiSEm3vQGWYWIOaPpj6OJLXXHsNUNgzxinYTjQ7rj5h2nW6GwSxA6p35jmMKio
ZDn8d/Isg3zO/ecIkdK0c47dNENM47uoUk/wGXPsYGt2pSUD7LPu4nnAeIL+OTGNFgX2asch7TtF9mQH2FctkEB8QAJRYoH4CQlE
WSg3H5mpCueFtEAMwCOX5244HdSiUOg511a3VTLXu/RZA5kUFgmYC+WkWFvgBVAmer2Hz8ReNVADA0m2bqNxyltOR7yGBw5JrFbP
MZg0XmoIRMonCgF3+XWNBCAuQQI+mB7PfChGw3KW5ek03/KxHD1j5k4L28fkWstphKqWIRmzXYQwnU+go2aMkoHDEdlFlQWZkgIF
N2JAC9Qn1MmTkR558OMQLj8PycrGe+TcH3KATUKzP2Y8rxoxtyfZkKnG+cf/zpFJmUOnkhaoMsdTBUQsCMMFi4eUvkEuMTIlNYQ0
0aeIVijaoTBDxn9AIaqI5UHdJQRtMLAkV/j+B0WqPyN0hYxo/gXj4FnDUzXiaARjFEUN/yvxxwCHPWU1Mc3VKoizX6alrj25ZKDP
iQ2ezImHUiGkrT00DIpzODapqLCTP6qAQ2I4RUBaO+hVhSk9raGMBSxe5UFvZHWEpENfcvbCIxlRCB3jEWf5WPh38NiFnEED7keo
oSjFvH79Q9wdIg2Dopj3u+rFi1i46D18SRqy11tlXZPG+GKiYQV99LEcbG0Rli+7T902KwxORhi0KQ7Zi6xuooUjyVF1erg8rHXN
CrTfrFfJN4cCIo6shetkCWoEvvUt9HmEPlDHtiSi0QYVfB+FPU8qhg9tddAYZ49WiEeER3zKNMsalV2H3r2r9G6cD6bzBtxKqX0T
rIkV46JRyU0Y542B3GVqM0TaWCXHNXE5E41ck2e0ZGqfz0EdkwwM69kN1jNO5B8Y6hQBwE2Sf8CB/3QrL85OkRZM0QhPpsVD9uLg
n3AS3FyFGWp7H/dc2GZb6PlxYMozLBafCEffJBUrXsSwRZyWQgNRgRxCbnQYK70+PKpsJy0k9qz9JIP1Le3vg4G087zrSQEu17x8
o5GVX8FGl9VGXzKuyLP+Hvu4iaOYL2ZOifmUX73n+eRCuuzr7CXxJzIaOHNhv0YerRgwlvz2ffa2kY8sKC9cphpVPrJIBvEm6X+e
9f9TgUQYu0IDbBB19kuqfClR+Yq+2sKJTXBUnhoNauQsQn0IOVXarAzbioyXrB1g2MzUUklY4XmHpQMvDH9KrQgHMSNZwyy7A2Oy
tD82Etqld3cC7YRkCpt+GeKUXqU//iqahin9FwDpnWBOfCSyhfswFE/WIVTmygZ/mB9oSWO56ymWeRl0jRYz6drkbwaO5GtluvZa
T76W+2cStdGEHpTXIePYVrcdTWfLu35aUyc4Zb06ESoTijDBqozA30ycizTW6MsHp17HQJKGJzsv/Yc1DbQcY/P9NVnB0G/1uCkM
nTK+H2QPI713wtE8EiN7igs8HL+lni3DKKvvK9yRQZnI0OvdgLJeS1zbGqMgAnKdhq4a5yiUeT2HcHzKGOYyxh3OToO9Za3V/4Sh
iwrzwjl2fOVfZRXTW2cw/BXUelLVCzp1mRPvk6EmLZb+jLzEJjVPHx3Ic9oB7iHgzb7IfmayyxQsv7qwpnRQlreKacZySIVWErRJ
gw2iWqEzTt7MZc/fzd6bZ3MfeltbuJP7FLdtPIeeuDzpyMN/8i0pvoXpvdvck8kpWXbPJcF3VdYz+jY1uLdmmTOOufCchN+320la
EtnIDTkJn4vyPEvJPHAuMKRLAlw32X2YTWuvwpmYkdmetFTdPyv1OtlnkkubmgaVTRthz8DfzV6oSk8sb2pTsd6VzSFqc1Ayn9ZK
aldUG+FaD7Scb9ghRdhcKOVcrq/Bi+M4j0NIpBOr6eUsDF6U91PdKB7rqSAjxVstLyjglYP2V2iFuj2BxdHeBlCKM9KCsbOAc5mJ
/ITxJeO2kch9Qcs9VA8nDEflPp+R+/zPIfcOcuMFfT7UL3bWb2Pbfye9CdfLR+t38fi9JGD+Izz+GI8/weNHeHzyasCY6Nkacttw
Qybe/03s0fCRPWJHKZ/dnadCnlmRo+RhafOPbXW3b0co24dzKJtL8tgVGcpE81zC+1Sj6uyFDKn0MpU2pPJs6Q1VKpLuVD5Jiqm8
utuXTWfndw5/otVuy3sIDegHLgpz+j57l3Sm5x5A3VzwyJyGpsd/DYE/gIDNa2bGwt/7IYnmu8/w50IIfrfJupoS9Of1Ib+8I529
DCHT9Bc4Hb/KnZf8bP0chulTPM4/84I5Z8yZdrno9B4z54pf4cAh2v/9DGvJFrxNiF8yxozZ17SCNxpO0Gw0JPnjfX8bgFjCVTm6
anJNwcZjE49fTcIPcMZCJGzx4QTSaXzbhy8O8Ak1n4/KWwutJCXQTYKYNW1HrR/i8ad4/Bke9Z6FnizbMF3vy4Tgh7juwPFByajl
ayzQ6r9cbbJ2tlKg/6bpv2plsPKVyvnKcGWsZlYGKhdqo7Xh/wFJKQWt""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

