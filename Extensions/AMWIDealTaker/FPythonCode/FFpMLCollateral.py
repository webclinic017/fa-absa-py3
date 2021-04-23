"""------------------------------------------------------------------------
MODULE
    FFpMLCollateral -
DESCRIPTION:
    This file is used to map the Collateral details if present in the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtWG1v40QQXqdp0iRt07crLXCwJwgEdM3pQPcBBKi9tCdF6hubFukqkOV6N63BsSN7c3dB9w3+FP+OmbW3cRonqaNzlck4nt15
5pln7XVtEh8L8NmHT/gYDCfkCqxBeJ7wHPmXkH8IeX0F5wukXV/EsBc5QvY+0FE+OTu8PD4qUzheveqdHDd917WkCCyX7pUPj9pN
1jq/aJ2d/qhCLm6dkHYcV1D47oeCU+nTrtWj8lbQxFAupOW4IXU6tBeIUHiSOp4Kcjzb7zreDcVk5d+OWBsnpzVWK7Oj9gVrNTFb
+xk9bp20Lg7USZT7eYMeeAPa9bnTcWxLOr4XYnqcNbQDpyfDZ1R4djDoSQAGcX1XwE+2K6yASvFOUtvngr515G0MxvYDVYnnSxr2
ez0/gJENqtJ914iqjebRUXY/lID/b+vaFSrsewzDmbo938M6u9ZARb71g7+oFVLxridsBIR5qTVWAYdhURnDZJZEcgOohtPy3gc7
ZBXkc6/LtlahAZ+XKK//wAhQoaG0mEMtggqvFmI5XuVRiugsokbRKRC+qJwi4QXlLBFeVE6J8CXllAkvKadCeFk5y4RXlLNC+LJy
VglfUU6V8FXlrBFeVc464WvK2SB8XTmbhG8oZ4vwTeU8Iqxd38ISfgej+LRdKwTreyBH4NpyXdV3LU/VkkDcWAFXUsLuOB4XPSDe
gl5aXb+PX5xHSo/GAmlGTBisRNLEjJdELdr3hJh3jqGdnHYWtJPXziK5IcopaKeoLy0h/+06pjiV2KF6CcuqgTHvNdE0e9ZABOdW
IAdMdEQAy0DIempkIGzhvBkL/nzStF0Q9YHiQT6ZFtPsBzjTQD6eFnUI5/LTaREvD5vyk6kBTfnF9OtNy8UGBvKz1Djf4Xd117GL
Mo8tFG6nrmhGE26ML5VGbyCXcEbT8Rxpmqs6jhile392LhbHnUBWwLxPCCRqrLrlh0IqZakegoW+gChjgKcKIcNgNYJVEPAmmJSW
z8a/HeU7Hx+7i1cwA8ndydvQ6ItEifNPFKShcd9Mw52AbWjYD4N3kwrvcQLeQ8mlCXK17CfwuzDKL+JIXyiza9iNsrLU4U8ysUwT
LE8qIIE/A9G70czpIGtzcL09KmRciPHtM2Y4P8rwSqTg4d1lNubVhHajMd9kYnN7VLMJiAmEGThcTYg1wrM3B3E7KcTZ8b00pm5x
lLrqkDp908228COweuzzTCTupJCo4SbQzrnmR5G9mIPOrRQ6OSSLqSyMUlkZUolPpiwa1GN+yETfVgp9CC+Bbi4FajQ/z0HZ0wmU
0et+6HgCNlAc9rSwiXoDV2DPGlNZHKWyPKQSHuGzsa+PMQnDDjKR+XQCmZOAJ3BnIHl9jGQAejQHz7WZPNvwkwjCmOCl8WWvI5tR
4Gzwa+MsN1uZSK7NJDlGnQCdgd21cXabJ3OQ23goudSOd4cxy6VxGV/begc5G/9OCsF69K+ZiG48lOi7ChIFZGB8J4VxjfhyDub3
E8yftQ6HOxP9yg9FWNdWKGjHD9QP8D7l4Hq0XF1o3IvyaC+WwYxs1mfWVo2wnCUGvc7UhP1EE+YtJlFLhrZUo8xJ6H8ModfxKRm/
fXhWV5imUqppRv8xgNOiOuW+bZoMiWP4cGA4K8M7GMO0DB8/7BGaj9CgFNjHaPCNi+Eem+E7E8ONJ8O9KsNXLfYlmq/QfD1Sy7SC
GF5DIOouVTAKRqlSys/6O43mVRr4Fg15cELFzk8RH79UNHUF438UlU/W""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
