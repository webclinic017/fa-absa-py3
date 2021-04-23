"""----------------------------------------------------------------------------
MODULE:
    FSwiftWriterEngine

DESCRIPTION:
    Engine to generate the swift message. All the fields of the swift message is mapped in SwiftWriterEngine class.

FUNCTIONS:

    _get_overridable_mappingsSwiftWriterEngine
        This function will return list of all getter functions i.e. mappings which are allowed to be overridden by end user

    _map_attributes
        This function will call all setters defined in FMTXXXOutBase i.e. functions starting with '_set_' and populate the swift
        python object.

    _swift_python_object
        This function will return the populated swift python object.

    _attribute_exception_dict
        This functions returns attribute _exception_dict which contains a key-value pairs of setter
        functions and exceptions caught while calling the setter function.

    attributes_to_compare_for_amendment_generation
        This function by default returns all getter methods as returned by function '_get_overridable_functions'.
        User can override this function to specify which getter methods should be used for checksum generation.

    is_mandatory_tag
        check if tag is mandatory from the XSD isMandatory attribute.

    validate_with
        This is decorator. This decorator is applied to each valiadator function in FMTXXXBase class.
        This is used to generate swift message with errors.

    should_use_operations_xml
        Check if should_use_operations_xml parameter is set to True for the FMTXXXBase message

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtWs1vHEd2r+r5IGdEaihSlCzbWnU2UUhjZcqWkGAta+XIIuVwI1JSk5IYeZVOa7pn2NRM97C7xxIXJBBAxlrOIggC7CWnLLAb
IEACLIIAi9xzzL+w5xyNnJLDHjbv96qqu4cUJSowyWlWV7169erV+65pC/1Toc+f0Cf9V3r4QjykpxS+JXpSPJSmbYmHlggssWUJ
vyL8qnhOPRUzWhUPq6ZdEw9r3K6JXl30x8TDMSH12Lh4OC78uviSlmmIoIk/f0x8SbiOCX+c+yeE3+DGpPCb3Dgu/GMiaIkOIZlA
z3Mh/vzhFDCuzU+C9K/HhHj/W/xprtxevHdr6UrTpp+ba0/DTvYgCbMgWYq6YRQ0m4tLazec5Tvry7dXFZAasLPY7gZRkHgZtTcD
O8VUux+kqdcNFuzrvR53d8Kg56d23DkIZIep3fcGg8C3w8g+sLTd7nlputBs3ry3egPLr11pMgFuN8jc+IsgSULfe9wLXCAJo256
kHpb/6xv0lqdYdTOwjiyn4ZEXBJkwySye2GagTqPuggvTc3hUjtcoJ0Y7PbTzbC9aXtJAOD4KZFNPHgc2JoUP4jsxzt2EPn2MA0S
TSvNdr0sS8LHwyxIX0VQGyTgkzIZqe0HHdoDM+fmyvrGxsbtYfaplwaKrILKNPOSjCgkNNmmPefSfHfO9oiOQTwY9kYOKCdgsJNt
0srx462gnS1oYhnEVUOuGjoCC4HcrOTrI34p+pwPbvCsHQyAyPXDw9ZINf7UzufZ+ybqI2nHUeaFALSfBDvvf+H1hkSRFyYsd4qd
+RoFenAox5cS/4fdTUbZC/gwwFJm3KhY6N0Uh+pmsduO+wOSDLcTJ67XJxmgT+ZqBaFJh7CR5IVO2Rv2smKzhSD2A2IiKY9nWEHs
pRn57LkDmpBvbm4hX/EeCSPtJzJyCmko00BCnA6CdtjZ0ezct3q6GQ97PgSdxNq3aYd2ezNoP0mHfbvYoOZKmJLER76XxcmOm3nd
nAqeYodkBryuUnwNZXeSuM983lhbpJGVfCDnsMZN50rbJOmBnI8yNIS2tOMEExdUV/6OQVLhXqgUNvBoi0Dl8TIFH3I1Yx3Txmf/
KsyCsukbtWisgcTlOEk10Yp7Ls1z44HmVeo+6/dy1DcMZw4FJVlOSKhwKEQCiSMoWE9IyHEYYF2JcE1Ks3l/yVmD0bbPO+ebTWdp
bd1ZVnb04q3lleX169qmNj4kax3t2P3YDzthWy2LFVj220k4yC4GUTvZGUC9CWrYCy62e4FHSwfPMtI+X208VKaA2M6mPYozOx0O
BnFC8xaajUv6YBQGA9EeplncD38M8SWgywACjv4gjkiFSE52GO5pnDyBIgTPSFZBCLPaO0C3HyvflJWW8jK2yDDNC81v03mGv6Of
1ewYOeaS78neoveyK12NM9KuG3HUCbvzkgazGj2eJt4gbeO1Sh/03ICD/0d67HwudoVIHopnq2hs0Z9EKLD46Ir4kSX2pNizxC5H
LE8skZwRGb1SxFIRz6XYqgKUIgYMrWGtte0zgv4eRII+N0Q1q4snTZH8XMi9ipDZmNgaR6gDJIzhFH24u1H0URxEYc5zKWUkxUbW
pHikTpSqzZe0NsNm1p17S+l3qbFkzCu0a79tsEk002ycwMgKu2HUiUNwYx4YMwQ77nVjAVa8AfOMuNlPM8RxaZZkZ0dgyM657jAK
IY+LyqjyHBJBOhMmi1Qma5TJ4tUjHE9IMIBecpzbDrcWlz699xm3bnq9NJgHhmwKS7OXpA1oF5lJpgzPLX4G84g2+ZHO7pMFFZgs
kH+cYsaNsuSPMOUkJsqKrMt35YT1jpyWLXlanpXtipaVqo5lUyyh400hvhbiK/qT4itLfFURnSrO9CdC0BnTEa4x/ekmzTO2zCvZ
SGX59XugvBCUWdtcsmdsa4ydU1Hdgr1Mnj5IaKSPcURFcJq5Fyrs5wcL9iL5GJ9QhyoUPOAHCH3Mh+IVtpFMkwJXJoWcWO6wld/Q
vgp2nIjwRjw9z/+QB3gmzLLZwXzfJU8dX7DnclmYu4Ddvjc6/ZIyt0TvyHRYIg4zcuhLhlLVD2qZd/qVBqIcleoiT26iDK+dDb1e
weyFMhH2cokDigq2tGF6YQTs0uv3uhzdxxL3sT5tl6Dcftp9bx+aI+/5Mu8Z1rm81XKooo7nYn42oxTr9e0fjCQet+JuN0gWVBeF
vLlpWfe6RPlKmKbEs3no38DLNvnUaG+5IM2N7Ofy67miMSquXJxbjMlek8EpGLTAG9uH9nVcIt6wd2ALb9EH5nIGOvg9GBIhXgjY
Va2vAir7VVV0OKH8CQ+RmScbvzaPyattPI9pR8FofidZ+ckT+KzkaFdhC/Zq4gW169wzxs9x8aIi0g7W3GKsu3WktbQCDHwdq6Xr
4kVVJI9gNQh+uwOTTw1yGpj7dwAjB7Ol/QBy23NbNeS0lM0C1xhACXXyG0EOhhrwRWNIcZ9zJ6W4RB9Z3F36qxYwzyvYA9llWoCc
mCIrOieB6mcSFDc1JL2Su9magHeAi9o5J15YcJAY5mm7Bim1H0TnyNUdZ1d3Tcq9Bvk0GmZyaEG4MVou+a2klBuMmxBbLabKYsqn
0IN9TopzmNEsSN9tvpzo7d/KqCv840AH79xiF/wrSQ3qAXfYz6Lzf2V2QmxNi90xhpwyCPMlyJvPHMKaKg58jUXjBLtgdjSQCfKn
9ufswR7Bt35MnxSO4vOVR+r/7Ufs0Nz1nUEQQiDZX7kphOv9a+kEHODGjSXO9sk9O+jI8ChbDp5jh5YZK+sPO1SjQexrc72ch19j
P7xKMVo2R40k6FNS4kaUzimn2t6kSLeN7NeFeYdLJGVy4EQZs+tGFAi7Lu+CQgCKTccYz6DntQMHIBSaYIhS4hQhYvYOvSJNMjbI
d1lfXa2vma3HR3pdL9UUfZHvinw1mznewmDn2ePsNDWcYHsYJgFz5wEZ+TteAmY4UFXFPoBvxWGkaKY8JMum9wUFyuRl5/LuQ80e
I2GaVJjEhEW03agdcFxEY8wSbbo4jioCloyC+Kli1KWoOegiajte6tScao3M5HyIlzOGN4P8KCPq8NFieZo/DxKzE/u2eC8Leypy
85Iu84SjhJpi7MoGS1I5HHpd+DSmQ2iKPxxArgLeqsvSb70up61p2bAaY3V5Xr5Do29Rz6w1SdFVS07hUwHkdynGmqXRCdmgiGtW
zsrpSlVyqO5AzNkEO1fw+AFeQb7zfTw+wuNjPK5iQBq4VxAOpcgDr7uArXLAN/eJmv79fIWPDF61wjUTVB66/itWnVSyUSTQnwIe
RyiOT8i3rnNwWdPBJSciZ1VwqcJHZWTJBnUq4hTMW9U4psMMj6IUGJ0/NpKai1tFiZtzGcMf5Pt69ZE7f0AjP8vJpnObkewWK/rD
ZH+gvOsWuzZ4iV0WTe1r2PTr4aoaRmkVjF9VxMIuOaDEgaKwSWFlnscKrCcj6hQw+c7Fo+7hPI38PUDGeQ+TJHmTMo8RcuZfzndB
R0A7OKV8WqbSPnb55By0M7mIvawh0WPJWE1x2DfPp2RFXJV1stJTgnQ7rytsrNxS26qbbEvRu3JLaSqs6B1TdkhZ28hKoiTjfMew
hDnEUsAWTfHFWFDwhpW6zRS4XMM4UmJ0hhOVQ2oh/1AozIxkK3MAR9vU+0EZi/kaxE1wjX8crPtS6oo+au4cM6FRAz/RqCP0QWMM
sQ4apVI+ivjUaApnbR6qnEsg/n9msrJQ4NRcdrBoWKaHJREN5cVLkqds8Eh9kxnMvD3ICN67iq+Vk+IZ3Dt6EJSkKtnlBDDodZxV
80amOD3SkSjfG0Zh5rq/LKS3wb8svfWy9P4TSBMQ2C6L8a4qYEix+OgdLl2o2xUV1J3C619YYvsUbA1NIHPDcGxlAMd6nF7DK+Cu
Ae7ZpwruCsLd3Zq+rQG+vwWHKVKlTjpGxG6Sgtmir5b3PeAYCpSnMOv2ZxQNmMQ36HQotQ+/CA7eCpiimyr96RI38xOld5Z5rsHf
5jBKxSrcEbK3qxoLzlbQDxM+D+f30QNa4NIin8lybqPzmI5QdEGWDwPomCJ4aaKZ8RsAIEecxDNVJ8dNRzrqt0EtlgPWnAuu4kL6
z5g8pV3th+QiJ8mJniSXyUJQKQvB34jS2ftcQUI8yzKhylfJVfBgq2rC+6vc4FEEy5ZI7/L0WtHps/A8qYukz1JU19IhMVYxY1+b
sYoZYyvPAdgTItT+U6TTTwO+zEkCz0cSPvdmFf05dXWUV69HpAE5O/LiQRKkqGJy+q/Wy7PIzHvCub8WuANipq/MVtZVLZrFLiek
XHm3r/foiIfdzTfeQk6Lqq2UbhJyOi7YYWZqtZ65CyuK5rhDob21wUaK5TEWaqaAPQt2Bs/ovhldGcf75D/cuFNYPffSpevZSZb9
yEeGkAQdOkZa2730weo8PJRzEw9WJzgp9loUHaNirEN4pQ3Oj4yyqQyE7WOhbKCW6ewPeMGX3TUeSZcWNLKjb/3fgfAU0NZmZZ30
aoLCnBY9p/CxWMuw3pjRss9qpRLgntTqRtaQVEZ2VejzEutbNdbyPWN932Or+j9VtqrfVPfY7uYFBTzrYBml+cRWhVKnpOMI7rYa
yFyB8a7Y+auqXoNDrERKMrrUc5pycAos9OQGJifflNBxj0q0ga7Jk7/hhsDC29+wXRgTSauGxWiH261adLx6OPoV+Rr0K7JAvyIL
9BYXOPaOwd+TUOh3mnF6bwJRxL6+ScNVVe1oWYq+veNi97hIfiPpqXBRQ2PgFt/8c6tVYkRL83W7ZZE72ZrEtwL0wR7nZSc4Dodt
oyZGWui++vQuGFTgOcZ4qqWeCe6plXomuacO50r71rxR59aq4dj52wd7J8TODPcLtHdPoP9BNBRVCi1RYflvS+5NC/kSco8xr6aB
0RANqBNFtz+JognuFvxW0XuaVshfij3y9QN1T5nuaSxxFf59BnSB8F9XyNHTU++mpjt3ptBWMCB/+98qhvxfVQ4jf+LbJZ/W3Nj+
dUW5sr0ZlH72TqK+k/yXIZfLcfSKog/vksAiLmzsEvwJluuo6k/jdeskTgQ+L6q+hPhJJsGAvXQLpcFiI/sGStwXYuc+xpJfVlGp
mhEFNn+mtDJtZVZ0LLUa1OqkSP6jilM6VaCjTgoJMPxge6JmzmK8xmexH3aaYQ/lPSHYgDUArk9yXB+/ChfBbWzfFfT3gL9gw87l
p/Q45Lbea2d8Ge/xNw6SuNcjh33BfAmBHHmqvfiF4jbiQvkKBd5Sf7sjX4LcPF9J85XKgq6eXyk8MxeRnXX4ppYJJJ2lO0vry+vL
95c4sXP5cp18S+SHIJTjTBWzKzpcTufcPP93kBA5XDZBDYuS95GLOnpHFp++y7W64hJX38/kFX6H41m4pIOVQ/gw530MwVXp2kB6
Rq22pmMdimjOq8v7mBzm/Om8rLFq8p48i0mD7SF8fercM9FyKRFlv/+XeHjG7296KWernMAjv3WQXznI0Jw/M8U5Byx1VvD4Q0Ow
g4pgdopRRD65fNT6ii+epPOzJlhQtG4AvFGKyVMTsSM1Y+HBuz4Jfh8pxuQ9+KpQXltQhTuFQwUtHIrsO2kO6186wFinRulQ0FOj
xKjO6f0UqW5T78uxpfuxTebYUFpFsRYBnyoIlrepxo5a6uFcePSrU/+JCf/CkdGEnLQ+pMzDFPpwQYqCXpNaaLeob9LK36w6tU9S
ltKqNhi+yb+zVZug6pVpC7+zGLEqlM42aU5DnpVnKOY6bc1UWnKWsE+Ves9WgWWWMP8erfC2PGe9W6kw3ga91QmqJU/JOZqZV9Xy
eA2JJlKfj3R5Z1flwRaiL/RwYkQxmEp0zBcQLXV/wBWDGtf8gfj2UIW1KNpyuQVa3qZ8JuMAk8cIphvjvoxD3EUci6l4pxkAUXLP
VFkdQWk/U6i+o4GoS2N8PEzpcNLUHSQx6WGqymW3jb557T5KDdzWBLHcl1Zhoh8PkiNJAApl7nDgv2xpLmCalHRJliqC0yoRNR9m
ObiSf4vCVFys3Mw08ooJKiXSbOpIRJ5ki3zwW3M/BE0W03SQnrGcHkOMNEbpDZc/M5Jb7fty3Mr/g4aVN6dhVgvKgVLUnWL9Vb6s
UIaVPZGrvpnjusqGowrOOZkT4LGLx1d4fI3HX+Px0xF6Xldl/SGN/MKUKupyYqwx2Zhp/LhRa1QaFb41Yzl1XT9uExHsOb6XO4pF
Uwdm2WDbF8e9lK8C1JdPdlK+k1Il4k/wQG2ai7vOssktlSgwLUemnHX2quLOtQsAfVvtgH6n+UmJoNWYbDm0l3qj+n/gO9dU""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

