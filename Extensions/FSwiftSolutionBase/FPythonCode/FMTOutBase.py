"""----------------------------------------------------------------------------
MODULE:
    FMTOutBase

DESCRIPTION:
    A module for common functions used across out base files

VERSION: 3.0.0-0.5.3344
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVN9PE0EQnrtrC21AEcVEX9yYkJwPEh8NMUaBkpBIMdeqsS+b5W5LD+9u6+1UIOFJ+Cf8a3Vmr62g4ccD29x09sfNfPN9cxvD
ZAT0vKPHviKTAPTJepD4kHmQ+9D3wUsC0AEMaLUG5wBnAF/7NUjq0A0b/GbTA3h5h6O1u7f16UN7vSVobO/29sa4oaxutbba3c1o
52NvZ69Tbb4XuUnGmRYDU4rY5LkpxGBcxJiawoqx1YlQcWmsFWaMYp+CiEGaadtqfW5HXQ4jVqPV1l2CT3/TCIkRwCdMztCMs0QS
FGlGulQOmTzOM2zR7t/i4qkePj0b/OJrMpr08JhpEubcg37A2pAETL/vHNoKnNOYqNOfg6jSJa6RqU1CbnJIRebUg1MASY7vHI9D
skPTwDkBpOCcGtvDOhw2ONuZB2UPcG6yeFa9NQ8FMAT2mwyzG3LKDnItyJl3ezhPf1umY3BXjUKum6IAqDiXZv8QmwztKB2gmy0y
8mFKnOUo8WSk8fFsP9eoEoWK+ZOJyfEec3Qc6xHTKpM0Rly+cNpadaCrIJzVoiqR9nAYOXR89AphEiMLQyEIL5eDbKzOBlGdnIjZ
jbioEKbGLl6Sc2104qqWMi1SlJKB2iU+6DVnv2VvxYu5U6aPE8nxA/DTq9jk9U7VTw/ZNbiTjzKd6wJ10i5LU7rN6N5NcLjaGSdW
fx/rItb2KR/2HbD/obBKrPZlHK78WyZ9xEkrOWg2JJFIYx3jswtp/UmLztp08WKb/kNCxJhCf5rcNdKkUa4F8sAJiPJSaz2/rniW
PJ0mt7/IiN5QC+4/EaYDoYqTF6LUOC4LumYGpcnFUJdaHKVZJva1sOoHrdOFhPRWlhbfaNY+Rl0WKttzJNCOQrq2ClQpXVd8rstU
uauNx0SttdnCepVvXXCrr8+Wq8pvpwivHBAR1Pil5GJWZyTUOyH37KRxC5VrKd3XIGV1zdLUfdym0NF9zsasRtxYEQsdrVxKfgWC
iHEuTju94S0sNOvNoBl0wvpUUEkfd0zJOPK2o+RLmRJz7eIgpdTu4+UmrHrJBbwxravqTVXH2+ZU4Ia3FPwBktZtrw==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

