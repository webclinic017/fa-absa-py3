"""------------------------------------------------------------------------
MODULE
    FFpMLDocumentation -
DESCRIPTION:
    This file is used to parse and map the documentation details from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVttu00AQXefapCAQpaitSrUPVIqApFzeUIUoSSpFalpkByTyYpn1JjX4Ju9GbVDf4MOZWduJ0yaQlNryZGzPzpw5e3YdRpIj
D9cHuMRTMDYhfbAasQvEzpHfhPwi5Gsf7vPEqBUx7DBHSP2Ojmr3rPX5pF2lcBwfh92TVsBGHvelJZ3Ap/Vqq2009c6nXufs9J2K
6p07gg4cl1P4HQluUxnQ0IoEp5ZvU88KqTzn1J7JY3NpOS6MiwJPvXZ8FniOP6RYs/qlrRtYgO7r+1W9bfT0ThMrGgf0pNPt9I7U
TVz/dYMe+WPqBbYzcJhKLxACZhUsckIpDij3WTQOJYCDuJHL4RFzuRVRyS8lZYHN6YUjzx1fDWNBpLrxA0nFKAyDCEY2qCr3phF3
HOdJo9hISMD/0/rmchX2FsMwkxcGPrQNPIxV5EUQ/aCWoPwy5AwBYV1g6noHNgyL25gWsyQSHEE3Nq3W7+yQj0BFNyebpXrU4PqI
QvsKhoMeNVQlKLGfQ2Gik0+02S+gLtEpomDRKRG7qJwysUvKWSN2WTkVYq8pp0p0o1aB7ExL6oGkSRNr1ohS/xUh5sTRUieXOqq+
UcOVI+o41LWEUgELoBuYVst1J6ILBrNqlNjkaa0AVmI58yYXpulZQvLoaBhxjk9745DLF4uCsWpkMTmy3BYfOL6j5lQ+XyLeAL25
qsTi9DGWZuAPnMhTzxBODXmT2IXg7gAbIcqIzbnT2wjHcg0rmIjPNO9jKD4guYqGJ8sl8zCZCwy5ysyFUcul25TgUi2dGBq1Up6o
BGSnCpqOwWqEXkKkG2DmsLoU8EpcsquGP8abnEI+0Y+WYi4jZkK+E0CrpWiHf0ObAaulYJcGNUxBbWVALUvkXobIjCRAuKmGEibz
s0w+wZUzV3JL4d6KyzbnZdhdidu9DLfzG8jgX43crTj1XJD0FlzvJFxnYYrJ2kt4LszyvDnL83Sp3pLmaYJnK9G8k9A8H3sG+v9S
PNvhqhTvJhQnq4xl9qvstlC8KeYFG9wyTWxnd4brGV6uRPNuQvMi/Bn4qxG9nd0ormN8NcVYW0dC4k3atzxumrKqbuL/A6apI2Yd
9x0dX+j30OBs6A/QPESDH3d9YwbaP/Dp+BpTCRxb0irlSiF7nsZJEKMsKzzwOQUwZJUiqq3DuJH362nPJe0P60qQUw==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
