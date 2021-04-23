"""------------------------------------------------------------------------
MODULE
    FFpMLSingleNameCDS -
DESCRIPTION:
    This file is used to map the CDS instrument attributes to/from the FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVUtvGzcQJiX5tX4mji/1IWyBBLpYTlMgAYKgqGIphQBbNlZy0OiyWO9SNpVdrkBSsVWkJ/e39Af01EN/W9sZ7tKSYheQ21BY
ipzHNzOcGTIixSjD9wN8ugNTTEgPZkriEkko6VG3LpFeya3LpFd26wrpVUhcJpySASV9IFbIr4RcE/K+t4ASneoCgj8rEbL3hYZ3
dNw4PWx6DMbbt8Ojw46Q5wlvhyk/aHTYntdodg781km3ddx+ZaW6F0Kzvkg4g/+R5jEzGUvDITMXnKGOkNqoUcqlYaExSpyNDNcg
tN9XWWql0I73rul3EJQ98Z94frPT9VsHaKWzzw5bR61u3W5ym9/WWF2OWZrFoi+i0IhMIqIF05ESQ6P3GZeRGg8NOARyo4QDKUp4
qJjhV4ZFWczZpTAXQlq1KFM2ApkZpkfDYaZAs8asuee1PMocx0lFI22yVPwcniXcin2HYoiUDjOJ4abh2EpeZuoDCzXjV0MeoUNo
l4W3IohBLQ9jYiw0eKgKoomZt/fFhvgbRts8hPq5nebI1S+F7w2W2FcwcWJrlmAN5gWLizLxO1UoQBLRQgE3B6j0CCZDyIBg+X6C
wqWEgnqnilJtq2SWnQNg1m6CQEhhgsAKmQri8KRfRW/spHfudLk2HPsI+ABFStb3yDmz4Bz6k+YO2c4DhwYlcl0i6g+K6zIZVCzX
tlbONYvkumz9LiSWnER5oo/sArUyhfq7FV2eIf5CiVkhgxXsYSAGnmV5ZLBKPtFpO2skXrB7+ZvzeHEK+y+HvTiLvU4G6/+OLXsO
a2kK6yd6h0vTLhQwG2SwSQR17C1UiJfJC4tMHPmBO6CV2QMq2A8d27uTve3Yq7NswI/XoHDWMYvPsRavjAojwxTvcwWNDk0p+5lK
bSOxoqWFhFaEImExDxP9Naidc8lVmHS5SnXtRrc1UdWv55GaEJvSCDOucfuHpahf/Q+AVnxf9eOzRJzntLNMxrZfcKGb/xknyuRH
royAW+0NIr2cC0lm/m0sg++f32zo/bkwwiT5cRSqUBrOtX52vwhOlIi43v1cKYxjgYL5vl21d9KWu0JOQgV366kRiTYbeIdd8OhD
G16G5pXQxqxhuV2mCVIOHWEa3iJpbiD25k0JGLyDFIeXjn/kqPouTEbcpqarYLHxmU6rYXGnNaAjCw8xBWYTXVMcIjmVMVfJGPKz
M+kClKnfvKzGy/FbUnfHQz4J9mCSWIONBO/ylNajG63isa4nItQ8P5fzWXeLqOvT+bJR52FNJcRR6zNpsFe/X3b3PxYsRj3PJW92
J3H7dxSEDeMpYpR26Df0Md2B3ybdotvFarvYPwXeY1qtOCeCQIKRILDHFwT56xsE9lHxd51jc71DyLZHhOCLdKVcXUQrSxY4ziJA
xafJR6qPufW3cSL3MWJ9fp17+f0qinrW2Frx+wfJRq6T""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
