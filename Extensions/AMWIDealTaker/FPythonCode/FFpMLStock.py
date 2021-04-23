"""------------------------------------------------------------------------
MODULE
    FFpMLStock -
DESCRIPTION:
    This file is used to map the Stock instrument attributes to/from the FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVt1vG0UQ3z1/Oymp2hKqqqBFKGBASYC+IYQIjlNZStzq7CLhF+u6tybn3ldv102MwlP6p/DAfwkzs3fnS1ICD73LbfZjdnZ+
M7+ZtWT5U4PvJ/j0DBqfsSm0nPkOCzmb8qLvsKlT9GtsWiv6dTatF/0GmzaYX2OKswVnc5iss7eMXTL267SJEuNeAw/6ymFs9z09
3ZNnhy+OB10Bz9FRenI8Nol8JXa7h4Nx3x0+nwyfjb6n1clpoMU8CJWA/0utfGESEXmpMKdK2F1BrE22jFRshGdMFrxcGqVBbH+e
JRHJ4QndXwbuGNWKHXen6w7GE3fYx3PG++J4eDKcHNDAnvrtnjiIVyJK/GAeSM8ESYwaSZmWWZAavS9ULLNVasAkkFuGCqZkqLxM
GHVuhEx8Jc4CcxrEtE0mGWGIEyP0Mk2TDHbuCTruuz2L0+oppORSmyQKfvdehorEnqAYaorSJEa4kbciybMkeyU8LdR5qiQahOcK
7wYCH7ZZGOvDPINuzQCNL7q77+0J/oZnZLrAnHWAZcFeoBL7GUn1FBrFiLEs5ypwD4naQuq95Tk5cbKZM3MKSw3qtJnfpE6HueNe
GxU+gUaGnoZwnQK0d5BGvV4GZgWsEQeHJ7iA5kkO+3huWR8VjaExjC0oEy4Ym3FmHLaAvxoOLznjvl1osLzTZKbFFq1iQ5uZDlt0
imEXxcY9PGTU20DtDwvnuApoq96ofhJFSfzCBKE2H8Bipkx1qlHIG4Q6mwVxYGYzU0eNEFly9joZSNxknq/M/WLjQf+kqhCtkJXx
vUJuGOuDMpXMHat3PUMg6FytwnkPI0qNvnMl3HvpykWhB7i0iQJ8i9/lHXi3uKzlVaz0+JeMahj6CjzGc6dfONShFlwPzuRUk3Cr
3iETDMX1Su4LmSnPqDL7TRMkBxT5UQ9tIuxpBjkgzWSVKhcF3FYRliyPiN1SQY7HuoiFvOLJaLh2eNvOTNDntznFtKzZR2kUPsZu
m3KiQ565ycSPGBEImLggpwAHiX0cvIBC+lHFYGEtrnhjZG0mxj2uSK4NX8MjL1B0CeOtkd2Cmc9wySHry3jW3m03RfLSqdqN1lTi
pG5a7pSWI7f7JDsHr1XCgBafR+FTwIFdq+RW72+Xqq5H94trcOpVOJ8zYiXAuaA6BVj+oFKQo6tZdCU3H5XHEAPFPMkIpj3U3aY6
4BRUtH7onwah76LjiKSE0P2wSDZETvtujQtm29e4VCcg97h0cjbVCyh/vTPTTFHbFvTD4NImXp1m6kzLqwK16wKZxPpsdb6WLLbB
b7BFMxdA0uZTVCP1n4VEm1R30BSo7JeW36AAqvu4R8myncMXqZfhbYXOtI6kMkfgyTU0DGIfruCNMuWHONaflvQYnKtMBlrtQRKa
UGEO9JdZBhc6VAdkmovVl/JZn0XhCK5yc7dw9HOywBZMlPhNmVmMEt1SP26wtO1AQxvQeKrpIA6ZVxxHU/rmVKF09sYLl8rmAZHh
4/8KP6L8BpcelEXlYf5t8fvwWYT5FRJ7kYIrpEsD+4sAhi0a+omczaiAu+hUF28HynoiKPGMTlub82824TTu1gityZu8095sderw
Nii8LiaeSzlNtQdtcykOn2DD/s8hBOgHC+HHjeLGafLN4nX+AdfdaoU=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
