"""------------------------------------------------------------------------
MODULE
    FFpMLEquityOption -
DESCRIPTION:
    This file is used to parse and map the equity option details from/to the incoming/outgoing FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNq1OstyJEt1Wf1Ut54jjTTSPIsbDLe5MDNc3gYC0LQkkGPUEtW6l0Bg2jVd2VJJ3VV9q7JnJMfMgrgQrCCI8GvhwI7wyt7YC3th
b2HjhRcEG3+ANywIfgHOOZlZlVXdmmmNsSo6lZWZlXnyvM/J7DL1V4Tf1+EXn0HhMXYEpcW8Autb7MjS9QI7Kuh6kR0Vdb3Ejkq6
XmZHZV2vsKMK84qMW+zUYj1oLLEfMvYhY985quKIdqOMi36jwNiDP9JffW9/670n23Ub/nZ2hntPtj8Y+eJifyj8MLAf1Le2201n
9+Bwd7/1JRp0eOLHds/vcxv+j2Lu2SK0h24Uc9sNPHvgDm1xwm1O09ihnMfjwvX78F0UDh7BeBzhB91w4AfHj8KROA6hYuPy9fe3
nTYuZt937ted7fahs9vE1duP7Ce7e7uHm/QiYXn3ob0ZXNiD0PN7ftfFpWJbTR93I38o4kc2D7rRxVAAoDBu1OfQ1O1zN7IFPxd2
N/S4/dwXJ35An3XDiHYWhMKOR8NhGMGXD21a7tMP5e7lPHpUdxQL2MhfuE/7nIZ9BofhTINhGPBAAE4uaOTzMDqz3djm50PeRYBw
XcBafgcefCa3kS7mCkR2BLvx7PqDP9qf/3v4a4lrwFZj1O9qbrfg9xgZ7zbUOCMOZ4q3gT+RsQtUKSH3YqWsWBf5uUwV4N8KVWaY
V6VKjXkzVKkzr0aVWebVqTLHvFmqzDNvjioLzJunyiLzFqiyxLxFqlxj3hJVlpl3jSorzFumynXmrVBllXnXqbLGvFWq3GDeGlXW
mXeDKhvMW6fKTeZtUOUW825S5TbzblHlDvNuU+Uu8+5Q5R7z7lLFZk67cQ+x9DYUzb4bA+24C+RP5CMrE73hoN+1FHoL+A1+/AEU
grFThirgBQi/xSxRYKcFVAPw3iEtgpWSrpR1paIrVV2Z0ZWartSZmGWnc3q2ealWUJ/FX74MbpTrbsRdwUlEJI/YSkXswDbsMOhf
CGSVVmMBNzCr+UkOEjPw3un4gS86HVHXnW0Rds8EqTSqfQRHjbFhpzMKPB71L3h0eDHk4t1LRknsvu/2RyRG7wWudwqiyb0tAFx8
bLqvHm81xf0phzbFJ6cb2XT7ILaAykuhGHBxEnr7vU0CeQBKQ3z0kqE9UKSjiB+GW7zvP+ORWNfodLiIfP6MN8PBAPYvQOGSYG/x
njvqiwM3cmEdHslWL9/aQD4UJaQG7/caSE0q4uuTlMPD4YWDXLOqR7DCkrVo1TLPOHuvMeI7yd6KB0mPtBsF3R9zYatdIg96cp8t
YlJnEYFEMTvmwoRnJ4cWZw7hx7WdJb2TV29HrMi18zO9hc0F2mGyH0vvp5rsp02L0QaOJ25AAvNmYB2Pg/WxCWAlaG7k0Bzd0vJf
YEENZV4hvghwE8kfKMSjgEtutMOe7Sb8aPfCSCkwJdMIP3B2d9QnJt88Rq5F8sj+ePu8e+IGx1wSTsxD4XYHu0EsohFxODbvi64z
e2WUrEpg98ak5h3sqBBSFq25aej1QNFr6n1LSN8M5uNJML/7KkJ+3iQkVsAUFJGiaBdUR0l3lHVHKk9fgSIEbol8cHP4OY+6Pip0
IaKn/kjwGN2RCLcXaXdE6QX7GWgvHrcaiE2BXIv2alvNIK5LCmyfD/2IyI9KFpSnlE97XD7HRgol6qitwEXjiArd9db49xOGXQ3/
Nw1M6G1sJnj4HH5bIiJsWN2icvFLmgw3c1b5BZRgkYsmqu8bEoQI9p8SgkEBGLYTIOu3aLyDhagqnQO4lfoNt+MgashmgsAcRq7H
p9HGiPQvXUlXNQzeV77JM22z7FFiP20PoJfIrl6Z7TOscIlx/qoBdUFxfyIBqDdeSN3FDEPRMLD9OthbBvAFDby4A8UrfYZptxe/
ZnuPr0SUT72KKE9HsR9w8NA8CCm6YfAMpCHRSTNvqpO2x3ygnTegyKdeRZFLAG8ZkKeUWR6nDIr79IZhfEN/eiUafHwqGnRhD9pv
cmpXRv71ychvtt4A9x+fCvcK4JYBcYr0axOQ3px2HxNw3nSuhPK3XoXyrnagJeT1K+P61kRcJ375+2+A8rdehfIE4JYBcYrr9XFc
J7BMu5348u0cvcqj+F6C+RdkzWRkqd2Jom4tma1l3VoxW6u6dWbc7/jIOHYS7yNBU6uBPOhgpOPc1D7isfIqLlB1OhhLJ5Iy5myg
u6f941xv00HPjqz+WGczy05X8SASrGsXIsH+97F3hpC+ZuHzOk7SrK9YpJJlERybiXungXBJQvie+R1PmMF6vRiasFwJN0sSz5mV
T4yV0bdBYpf1ys2CgQvJR8qpKrCXRawDY76gZAe2SB+3SM4uDCtho2JNYEqjySK+LKkQR7FmUXYUqKNIE5aZqNEImRCZxcb4n4zG
OcqSFFj0Kw0MJbXw24oaczpPK1do5WAl21pOQFxQ8HnlHCT04UspRos0qGpuooqZMuxbYqfXkn3A+7I5Ft5X1Ls3g5m0D0uy9fpE
tNRpxtVxtBAGXs4wNXQGM284dM1c+UYO++u5943c+82UqPR+i96Lyfvt3Psd413cpfXvoWbx5tlZiUVfK3gLxDI2Cxjm/9oNYnnM
BzSlk+32+6R0hHsc67wuetcUwmTiV9TJMhVHaaWaKXAUx4LVPO7zhKXJIQ9C/MDti4VkuiQmQgvqjkQ4AH3QTVoXpEyKfhK60Mpp
E7k7ExJAqNf4uYjcMPL8wI0uttFpiknU8kkgn2woev8onLYX8kwGG+JZz5eAH7gXOHtsA15MdMQPWw1U2gJl/3zQ/wYMwg3J2IWC
kG9yKCLK7cnW5onf95LY8NA9D4NwcEE7Vp/pJtQbT0eAxDbv93nk8B6PMJozlnicdhNGjCW+DWQEPavNw35KNMSkD3SKhQuzOV9E
lVXKJCB3RgIQRQMlhyCoBogtk6CySZNO2iRlfDbHCLuafpC1w0Qh2dNOqTyfNO5AATA5Gwjtig6v1QcQN55xchBkg9zsFg/wrERO
n850EPGBPxoY+DpwI3GxJU9bzFlAJCLq0/Q3gGyG/T78iwAJ6Z62wi5lafRcqMDBatJS49xEdAS77nsE4h54m+4xl+adItrHOrdI
6EfqCGIpN/D6nPYvRVE2SEL+CRaYlHa+Pp0Vcvag40ynPVihZi3DswLPBvx/B35rBXxbtpas2/Bbgx/2bBSWoLZUpBKe1QkZgM9L
241uU0Hl0mRqTWtR2VFQuRjVkebXPpFgltRTci6W0tWOOJLBI9VFCigYDZ7yaL+nJJSQLD/chuhJMZbKi+7qkBa9HaM3N8XC2Agj
7YBEcv58Sly/Bx0/G8ualEwbf5bDmUcJR7BPL4up85k1ABa5oPmm0nhTWTWhSUZElwHRqLriR1lEuwPQjl03SN1PzAjE0j6Qbdh7
QqkoqQw31fBEytF/8aWS0zOQDr9u6H/tWx76A64SZivjGgyTTVKlrBmil81q0bRaC5kuqyHLTxB+oQHENSd+hR3EeoYA4i6GLmhe
oeSMT+nepRDnEfTX+F2dWGCdRG1FMkLFZIT/+v9gBDEWlQAvoJfwL9qHKZLLRd7j+YPM4K0/20AX8AUFL9IVeyG9sw9+yr4dJLFR
TXNZVXLZDHBZbQKXgYwNRt5ruGw1YZnHcnhiaHpIoWPkNKZNztPskC0iOpITJ3ZOyFdHtDu+jp6cUyxQ5pw+Ft/FqZZ0/GNM42xp
heEMkPSVrAIIsBhi8YHOUOKaYN6uxilqkwmn/By/W85wyi1UydbNCapj+//EMa9TCnwUhUM+tVLYVsPH6aUIUcoS4ixBbWkCap9d
Weby6/9zesqxruUtY6weZE4NLIVD7cQzjTvpl6cHwPeyWOpJPyWLFWQH1aEOdmaVVVduDVmppunokMlfSVvPjfa89QmmtD5t6PjX
1PqsSSRU1U9GmJZGQvQ1stAJHnIRJrGWQow8WyklgRHxUtpdMrutjIZ5IY2S1CVydMX0D2RfVfdVzT4504wKTNXoMgZzavRMbnQZ
A7k0FK2pOFSNrquTVazPGnU69cdAr5KAVMQwDzxKNWJBaVJcCiOseWCNhQmsMZSOZ9ZlmU8ERvulK2RvLpTrmXr9SLQTYADi8Yh3
OcYwuTHz8lu0jJuDcAQeNMZf3VGE3RcUpriyfTYdSaZygSK5zOn/olJiaXgVxxt5cB+YkyDnDUHc4B082f2ejhNajUWtFRUSpDpF
6df5dDUfOMd6T7keh3d1j3TcljPdTb3JpUyzQoNy4Q4MYO+mSnerCZb9scr4Ninhe6iJk06Fh2xz2ZamjnSSBp0mI98/FpG4oQZM
QEujOu5FOj/WiayhuQHnQ+z70ZSCjqnZf8cR64lLfw+eZXDgb1O5bH1hgvD/Zc5+pDLPlMynUssyaaFUwkpZX14NLWuRr6iUVCp6
JS1rZV0hDYDLg8SBXmgTmuiC0Nh9miR8HI8DcqliQmmSRE1YXjI83kKjzOkPNZZbkjap0cfMtfMTLPDI0kECOBie5GlI1uqvsEAn
z/mbq5DtW9DxSxwxR2RbpkgMY63E1CfG6puvJdWkWKuotXIaa5X0/ci7WfzGFFNn0VqRLI2x9mxSPQDPljs/IJwVNc60vLXTIWTi
kiYtrXljTyLwt1Pi6xA6/js164ir8dT9ZybcDUvuBEgGlKyX5unTjPwtIyOvDHhsnFMrLilo/xMPpeWozWSMc6FDG+zVZhyUGKIg
PbRO1BcipAUB2JVSyc7fQcevU9O+JBFRVj4OIeK3lyIi+g0Dv+ylZaSLdZL4Q211k/OKlwVkueh7xGw18ocssnsKqTJXqq/LGdim
DK/xvnDpKseWcYhyuohNyNxF/cEStqy+TK5wXENbgAlUS8OSUvCGQUFtgNXF2lZjJU89bTRS6v1Yc3Mkb13oO2LKymh1v9n33djB
XKDz84Skqs/5e50idIdDaCFVFJtmRV4AWTHP23I2J87bnHiSzUE4d8LouRt52ptABm1RuqQvFC4mmSIyV+7TmHSBPEyppTYI1lyg
ZKRpISVqqpTfpfmn4dN/gI7/SS3TklWzKtbb8MOk0pLVqC2ib17I8+7/modAQscxQOUNZZQK1FpU7Ci5BXTdGXDqjjJKnRIL1pX3
ie3fV04ntsOkZX0sQiuRj1/XRygzyOkYzlos+kdaqZ6sP6OMYrCW66ipDnlSomZOs/xz6gwGx5LSqQPLklq9o2IDeZE0ostUmeuj
FPCSK5bk3h/m8+6VxATGyFfq+/aJC7GJyuUjhn344NwcsYsNegRy3m6rs3Ow96Szt7+17WBCj26cmlnww8gNYreL1fZoONQZtnmd
PImfD/qt0ONP/FiQ3BBnHNDmpDAtSs7v9PwoFp0uZciV39QJ4MtOAAqxg/fg6VU6r1HojbqCMtplPSkxLc1M8RPp0jBQGfMw6PnH
nWF6o1MZKdlEV7dIbvWqpBkcnDuVCuffxs4ZcWsOWZn0cATbphGH/4SO39ElcemoQUy2aM3Jp7ACYoF51jVrpSCPGeSNYEKGvBHc
6cib7vBapVcv7HY6dMfUWdaZcgdlTSbOMSKhO0/Sn/lo4s+8nTg172jPhs6CnU9j8Vks8LYXJYspi+mEWIyweI4Fxpbkd5IXQ6aZ
jBJJPO0zxcdrkIK9ZC/xilMFkFCbr5XgqcKvTLXsU60V4bkPfTO1uVoF/i/WavT/RgMx5vxCq3k65nCeYIHusfMfWCAxHXYFAIkM
X5GI/ypJ7AIBOpc+hT8ARyi4pQ==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
