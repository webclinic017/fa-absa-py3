"""FMXOutBase"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqNks1O6zAQhcdp+Ql/C0AseACUFU+Arq64gMSCILkb6MYKjgtBddxbTwVIrIAHx2eaIlUIiUg+Gjv2N2fGttR9vTT+phEPk9RE
jmikqFb0QfROdDtMk4wGBfbxRpKLq5vrGZ9W0dkFI0vjFIwjEgDO9AD7UDTsdbBhHyAEK6QHRT9ttZB+B/gHQJHkVdErkUlBJoGi
hiTIQEIg7EGBUyWvJz0LZeCraiJUXktSWW/C3SPnoD41I5bZDvw9WzfhJrSmbixLSXUwbWDjFwBIdOORRgYtlR98cbzjqq64Ms9+
bOrgYZlE4vZSe44nL2LOmKZt2BhwIhZI5SrP8p5ViLsh5cMME72peYFYL0V5D2HgSz8ZO+9advX5dBqm8lOvLhz8ZGMXNryLsbp3
Jrr/M9daF9GNmImh71bQxNTrx2Uf0oxfJt1H0nnP0uwhNTxdgbNSSpe2LEDputRW3hkjF2KMD/VsjGlfCm+dxiaNn3pzKfMP6fXi
YUakWFVbm/lKKU+GsTC3ouk3KPF3Mnf0R5DY9wnmMZF+""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

