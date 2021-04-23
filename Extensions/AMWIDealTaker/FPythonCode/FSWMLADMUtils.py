"""------------------------------------------------------------------------
MODULE
    FSWMLADMUtils -
DESCRIPTION:
    To validate that the user has the rights to do a given operation. This is currently not being used. 
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVF9vE0cQnzvbCTlMhRoKVOrDViqqEYr515ei0hLFSbGUEHR2iIRUWZe7tb3O+fbYXSc2cp7ge/RT5HP1I7Qzc2eHFAQvrLzr
3bmZ+f1mZ3ZiKIeP8xlO+wsuCcBrXD1IfEg9eI2bCiRVeI97H5IavEcFlKzwpkpqncYqWT9HPxtfaQR7+62D3e1A4NjpHO7tbrb2
DpxKrdgIWtudrbD9stvef/GEFbpanESpSiInhRtGDhcpJlYaMYwsH4waDB1utUi0iMRAnchM6FyayCmdNUV3qKzAXzwxRmYunYlM
O3EkVTYgR0lTBK+2ww4hijvhnSDc7nTD9hZR6NwXu+29dneTDwWhh02xmc3EWCeqr2LGYHCiYmOjcmfvC5nFZpY7mZDeJJUoilMZ
GeHk1IlYJ1KcKjdUGZvF2khiSLzsJM+1cUyL4B6VARR+FlrxxDo9Vm+jo1Sy2mNSI0/jXGcYpRhHRZyn2hwLvCk5zWVMhAhXRB9F
kKBZEcYFGN4237TMEhFsfLWh/sXxwq1hXe0v0hRTna7grOLcoor7B5c5F+uxD+Y616IDGHlAqw/vAL4/82H6CuY+jCp0bv31HM4q
MP0D5hUYVWFUK6RNOKvCHM8rMFolp+RxZyG5AnOvlBDGmx04fPMADqcpA63BKKBX4q4yTp1+7zy4hZPhagxX+yLc+Udw5wXcOcL9
DYf4CjuNGgX+Ky4tLW2RirLUT2RxvEgw1g6lTPcFyXOj+wrrzNEdbqan0cwqj7zR6x2YPDsyTxX1g8Y1XFwFl0imjm77ABHYjKBU
4kihdNdLVXZs3WopQSfu2w++LskUKnQklSuLfTSWjOBmuXTXcfOn0ZP8ZWG9i64Z1soUK5MpWVcwKQg3aBtSmTi6mJjdVJiocVQv
eVr8xSwd5GmDI6TFEtyl5tLMZ+4HFCp7wbunsh5F3Ssj+oYsb5N9pe5V/XVv3bvp/eTVK3eLfy+mO/XKtsplGhA9rlSsiE6D7/we
fRzK+NiKvjYXvUhQBJQ4wvx5mTQ2Cm8QddpxApYPo4smXwqLcoLdcGkTckf8kfSJJ1T5dfmfou19QPsxZUhiZfUvN9lLDdZqTOqQ
eqfFhqKi9ElB/yZRJPcuKGtq/2iEeQ2/W3D/TAD1/wXQWFL3+U1wefV6iY57vdBf3BZjhrcv+f8MCJXlb0Vn+/0qaZFgxav79fW1
1f8AHV23jQ==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
