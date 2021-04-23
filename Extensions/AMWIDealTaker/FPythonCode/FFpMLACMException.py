"""------------------------------------------------------------------------
MODULE
    FFpMLACMException -
DESCRIPTION:
    This file is used to raise the relevant exceptions for different scenarios while importing/ exporting FpML/ SWML. 
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNrtWN9v2zYQpuzEiZU2abogG4YC48M6eA9x2vVlKPbLi53NgJ1ukptu3YPAinTMRZYMklrqoW/dH7g/aXeUKXf1imZA7Yd5CkTb
x+Pdd/fdUVRiMruqcH8Dt/4TBk7IUxg9Ijwy9AivkD8IeUnIz08rhFeJqFjpRimtEr7ppLVSukH4lpNul9JNwutO6pfSGuE7Tnqj
lG4RftNJd0vpNuF7TnqrlNYJ33fS26XUJ/w9EjYOMDIAT47e0eX3H7Uf9zo+hev0dNLvtU76neexmBiZpfTIb3fCk6D7w6D76Oyh
VRqMpKZDmQgKn7kWnJqMKia1oGYkqBKJ+I2lhgpnBLQzRbkcDoUSMKFjkTIlM02vRtbMeJIpI9OLY1gz+0oRyTENn/R7Teqfd4IQ
/dO7wV0/6ISDoHuCgMJj2uv2u4OW/VHAu9+krXRKxxk4lDErAABCxKZjJSdGg580VtOJAeyglycCRHEimKJGPDc0zrigV9KMZGqX
xZmywaYZgM8nCFFwgIXuPmsWCSnsOK041yYby9/Zs0RYtQeohpYg1hSTMGZTq3mVqUvKNEYuYgSEfilbiIDDsiKMuTNmMP8KouHU
P3pnl9mHGlsohdj1lwf3t1iF2zAI6C+PBGEDZxpQlsSgOIpSNhZRZHz7o8AbRYVWOeiDf3LUnEwDnL2BGmix5pk9VGx9n2WXi3iq
Ds9xiQe7voJdD82DLW27HrpYQG/DWCUvKwQaFWDjYv01DG0xlKnQkPl54UJ9ClsBQD/Ipda5mPOTDW1xjACUbsYI1N0naPQmDC88
8gLit9tQ2MDEndnRbMEwFlqzC1EkbQOXiGQYbFwvQwazE2lhopmZfZct4sXejCXPYUF3AOTXv6MofNlvm//G68Xc68HcawOdBNZa
xYUYRTyLoyiooXTLFcdEZROhzPS1WN9SEsjUniu7mlfz6tV6dVYYuE38JwqjSEnFUXLdarAJvrOKCrAsfvRG1gMkZ053UF8M4i32
ccP4cIHmO6+oDxTjIjTM5HrtOf9kZZx/ukTOd2Di4wXOrXqrL/WYmXjUTdvMsGdMi3Xl+t7KuH6wRK7xCdJc4HrXcn2WmdAdr9aV
5YcrY/nLJbKM2fl8geX3LcvYx+cskdyebE+ZTHK1tk3dXhnd3y2R7t1XXwlKuj8oNnCmLqV5IpX4v73Bwsr4/nGJfOOpu/cmvucP
bDFkeWKg1/O17e+fVsb3L0vk+xZMnL/O91ljxxk3aLJcYd/e7fuaPc3b45197tvHgt0sbAVZs9fFYN8cvyj+kfAVWtS3LZbD6uHO
oT//+wuL7pOR""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
