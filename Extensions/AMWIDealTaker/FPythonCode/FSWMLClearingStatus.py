"""------------------------------------------------------------------------
MODULE
    FSWMLClearingStatus -
DESCRIPTION:
    This file is used to provide the current business process state for trade update during SWMLImport
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVF9P2zAQt9NRoMD+gJimPUx+GBLS1KJtb9M0UUorVWpL1xSQkFCVJi51aZPMvgw6gXhg34MvxKR9o+3OadcxXvaAlZzt8+98
v7vcxWeT4eC7ja95gyJg7AglZ4HDhpwd8enaYUcOCzLsOwIypHE3H5FRDc3zDzRy9b3d/Vo5J3BU3MN6rTSUnlbhiQseJEbkc7tl
t9SqNtvVvcYHC2v3lRE9NZQC58TIQEAkYh19VYEU0JfCT7SWIYhuYlQojaFDn2aDd0rRi7QA7SE4iQNSBAk5FOS9OoojDbmDcssl
f2KjtZFrld12q1oiAu6WqFXr1XbRblI6bwuiGI7FKApUT/keqCg0xIiYGF+rGMyWkKGvxzEgV8QlQ4kqnwIVIM9B+BGSOVPQV2Ea
QKRtcGEEwiQxUZJBQVh37wppAtJ7pig/MRCN1DevO5QW9p5gdBMGFFIyRt7YIs8ifSo8I+R5LH0iRH6Fdy+CAM3SMGbOPKB8a4wm
ELn8gw31C0fD51hbVF8ZfEtUZz+ZLctLzoCxAWfXjIrwlDOdZxeocUgzyJBETHhDlXzp2KM5UupjBlk2mGeDhZkSMdcOwcL1O6d/
9BcO07fs/DMtdo8r7DLDLjJssGid5UjOfC+RPEWDK4tZtsqVGRJpNb9cMXwOQ7Tj2EEUXQOoCU9+3OIY3mxvPsYdPEVRqcT1WtPT
mOR9UEMDK4STUCzVD6Q2+GGAsMUgUPSVvGE17EWwSgkrNf1J53SMbR2gXDbwK8ICLva0OlFoAOTf80fwBOedSYM00/6Al0RBhcHO
2E26AyyPYhhQH8pS39MAOTz+a2vv90YS1v7xP2k3WCJ92osuyBjmpvb2N2K3tg9hEVfUtPbQMuzGBhw7b1KqrDDPid79f0QhHsOz
NE93DyhVhmJiPMtX+bqT5cv8lbOOuxX+mr/gSzxlMo+i0wkiv9Np0bpFpdhamzr+PwqU5Y9po3yiyE0WBXlc5r8BoOpfAg==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
