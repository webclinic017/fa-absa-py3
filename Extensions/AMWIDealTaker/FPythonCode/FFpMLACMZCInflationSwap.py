"""------------------------------------------------------------------------
MODULE
    FFpMLACMZCInflationSwap -
DESCRIPTION:
    This file is used to map all the ZCInflation Swap attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtWVtz28YVXoAXibIkS3YSx43bQS5uNG0s59ZOepm0NCVl2Eq0CtJRoklGhYClBBkEaGBpSxm57Yzbl770se1b/0Jm2l/Sh/bf
tOc7iwVAyU6VOpS5Xiz2cvbsd75zztIX+adG35/TN/uIikCIXSotEdgissSuZeq22LVNvSZ2ayKoCWmJo7oYUmNd/F6IJ0J8uttA
j/5KAxPu2ELc+oY+c1t31+5trs859NnYGG9ttjtbu51uPIw8FSZx/5E3dm7Nra33O253e9C92/sxdx0chpkzDCPp0P+TTAaOSpwR
9fWiyFGH0qnM4fAknlJpuD9RMnOoCV08f7TajTOVTkYyVs4wTUbcHsZ+MgrjAwfizH287vaxrHPTvTnnrvcHbrcDOfq3nc3uVnfQ
5gct1TurTjs+cUZJEA5DnxfPIBhmzfw0HKvstiNjPz0ZKxKZ+k0iSU1+JL3UUfJYOX4SSOdRqA5DLaSfpLzHOFFONhmPk5RGrjq8
3LurWg96HtPLn2SK5P/C248kd3sP3TDTaJzE2OnIO+Gej5L0vuNljjweSx8CYV3HO7eDgIbpbZSLeQpqT2k3gTN36xv7hP+hT09d
I5g9Aw2+wbdF3zuA41+okIIxLYBXDWhUagAtKnXAGpVGjundpggaXJkRQZMrsyKY4UpLBLNcmRNBiyuXRDDHlXkRXOLKggjmubIo
ggWuXBbBIleWRHCZK8vC7a8skXC+lYtLdiM6EPlVKpQQR/TPEqdkYpaw6L8jlhwPbGyw4OxTKioo9SMvI0wdkv4fhYT1fQnYj7UB
BFJ5YZRpKPd3tjadZOictaZxSifoK0edjKULRfZ4IXWlovNyQTVLzXt7YRyqvT3Fu0mlp+RmcnAg0543kivYmapDVhkNVzAjF9m3
nn2Iq+MTF8pYRj8MFfaS5UOMZv5lNf2DilMbanrC5HXfFumX0Be0ZkFd1I5KzVTqptJA5UldPK6J05pIP+F5mqhDvQ++BDIe18uu
jxuAyGmD1/gtUEJvY8GLzQArX7UekWVdvISJaQTBqb8yA/Fvsk5UTiqBPHZSOZQpEYDEwYSFkrN56jlIlBc5rlSTNFZzOJekGyuZ
jpNIQSObYUwswedh2rNfYgXNCs4wSc+tog06CsnIvYwoLLt1M+PCkMU4lRlgRWzTXuv3VjC7gvCb8mBAAFGXqX4g1UaUeMqlc3fl
UL1QaSOeRHMXC5vO/DCQcZJub6mr59pkGiaBesm0660wNLakOqRXeovUH4td00osEdkFPY8jqeQK1OICPgrQieSBgn8aeiQ8TxKa
SfRDrszFyoNe8cKgVS9qaarq0KrGdrIrjOQr1ttW01qym9Y8/bUsH0LhQBsG1/+GR55lzFnicRNYJAwBea8ChdRCOFIWMEugQoVh
e41Qee20Ka49nhGnM0LZAOL9pkj/Dizyyxl6Octztxi6dZH+Na8QzskANJhpsjPt1HidxuSInxVHNH4WWD5tiSc1iBo7gmB5dIk7
zIMsCxmGNqHfJgprEPRb2OEDKlKGcsbwT0lXOTpL2GsaO/R0lyF0qjuWAKau8MSacwI4Ky/OAU0WxOPL+Vwo2GVQAMIKxHSLj7vb
X2uXCGTr2k5DX8M2+8DgDYgnIznrbPum6nAvZk4SJEXf3sqCob8euUkGIsnDNmJwtCaJtVPtTNU8L5bDatM7YGGyR6No20vJofJM
h0lyn+WGi10LfXT10hM2TFLX3n15oi6BipPRKInvKeJ89bq2p8IYN8gHTG+7DbXxOBZMMzivt7N59yOWIypZfa6wLUg8rNr/1Ypp
aWvuJBNyFYvn2l2owYVZuBikWqYHc8t8pX+H4h5+zYeL1xf3JBj2uuknyO6abHffsS5bi1R/1XrJesV2tH+p5a64YzwPWWB/Bb4o
6zBmQdjEhl5KkEsLniQXG1E8tI8wKw/MvIxZXD6YhOokx3ZGEvW04DWjPxdO0102m7kQzSxrmnElM19by/I+Gm3eIm+llW+Ht/Iv
bKUBd4eyDvCTzR7/CRZ6qpnEFmuf/0Z8ZoNfiEFo48Ql2pWBelymoZncp92viewhu8Rqn9fAMtU+1EKcSysVjTQJev4ZLSTNg79x
pS4evIZ/O0QR6T/BZ8Q5cLuzXJ8B/3EQVOeHWWGcKRgFFp19l82E4hcoP0kDij2ZAaRDvE/nNCTWoKNIZcBOgBn6vF/lV+GxDDKo
eFemiUPYpbjY4VbtAN3rwCp39aJM2/QXFLzPaRPLXaM7awx/kE4kd+9EoADU2oSXE6ZCbUN17Z8y9uTsoDI2FwXhtGxwWljhC59F
wSPG72+F2chT/mGJIyYXH2sFg6nxFwfYogYY5OjGd6FNkGB2ozCgpnXDeoP+mtYVq2UvsEktlCFa3eDukIpjD8FsBWXbjLIajj1g
50XxWo6gvtBx7hHH5oQvGgD41AGf04aOzpby56BunndKIEDG5KFM0xCZ0iE5CnqoGKh7CypaYkKmNM6L+r4XSSYctpbtbqijXvYW
b6N4BwXH5Mv6iNfjyQgE2mf3w9qqTEZNZejh/gDFD6cMnQfE0wMufDQ39NFMr9eOAxMR/QLv5/igbtDhvEiRRsFsRYLxnmY2hKii
NF7EwJzqs3UtmGcdE5Oy8/z+3TxupQQZxsX+ziTN+14WZsbysImiB+v9nMU9y87sQu+zz82W83lQ1s4ts4/nZh6LkXbsXDsFWf5I
6DCHEwl9+QEY2nk4o+MijU1LZwg6Eqvo6H+hkCGw5p2wZ9RRZgbX2/bVbfrCM2c9dJFDbxIhjGaNTo9ATvdmZcSbCIACPaIaR8FD
DWkY6bVpoOx+iAJu0X0DBZIRtzOta8YqgvaAljWLfuxFF1f9y1r1+S6mpd8tj+FF62rpfgvuwDlphKJkimAfwJlWkWaZpkqyhiZi
Uh3OnhbUU6MDKrw5UqN+nnxprz7mkMTxISGFkcF084QyXOBah6EA9VSKlqdGixXHvEEOp0xwOl7k66Anb79ytqvOe649tbt+t1QZ
skbBVnZnrWMoads7gRxoplaXk+6XK/0rgVjvHu3luUzK3aTXv0Y/7Fq0rlpXn3qCPysSdFXJyJ/oO4zTijEd6QS6mSfyT+wztxzf
rqTKQzCE9urlpR3ziLveXx842+tu9+6ac6/XHfQ40Wa9nVUCkz2lee5HBuSVHlDQFOFDrZVX3efmJJMo5q68XWwkLq88rlvniXu5
0Oi5m6DVio5y54JruEx5qcYz7uKQIRUklDs6y0TxuU9pk38Lnm97L0w5qbbqQwiadXImRj1Pu8YjpSu5+9EBqm7MkVO6prM6eGXq
SiVUIelAh94PvWhiNlwzQRJfMHAv9p6bRNIRH3m19WOM1DcHsP3nU8xlc11Rzn9S8uC8dcP267kFFVb0vbNnnt9w2RyRF1YFequR
Iviq7fsVRVSSE01p5h4w99lkSqwY3iNbQa6iRfNMxH13OKSKOdgt+KRxJImmCFWUfLCNnaGhDotyRlUc6g7Ho+hr60xLokX/XWkl
FHXauYUUVvKBRlL6fg4d7TzKR9s8Cg40rSKdKIA0yPVX8aJhcbGEHI/zO58SZI8ekJ87yjvQWX/l0mzq94JAUrrw0FwmFPiEaW6w
tQbgdL6o2+3Qa/P7RH4vkmkfbk4Ns73lEGfoe/eh9CieOv9bAKTYdrtb66s9Pg4+QXms6NgoPUi9QOYqLW/nSmiqhfwqD+LpABO9
dHRWJC7Y/cVPc+XZF3YbSYpb6ZIM/1Ae8xvlMdeqUWz1mvzUKkIyfcK3z5+wyAOAXgb/dSeJg+KO7imaf16dawtggv3qfbO+in2b
KKAdBCFf7kQDmY4oFcu6wZkTcD/7Wo4bP4/8sSAcctrzpV4LwoEnOXFM7MXaPbLLQBiq3IlnhGVZsSU+KUnnJxXSKVYu1VvSDQJX
XIchLa/ExC9U777yzIZT6eslbS89pU8Z0Fb08n/54/NS/6mIcuya5Vg1awWBW/6zR+yN5N4ep+V7e/qXr709/uXCxYR88+S+hQKq
cdso7nCgggJBlPsrFIh03R0Un6PYR4GTcg+mNnGhE0YfDhQd5OJWq9FaaC236q0rrVZrptVsLVJZp28Df5wP8L3h3l6Q+CS8VaQF
rxi22Gh3vOxwI0oeleB1xdeWjHX2U62lDy8Ztepb8Hn7v2xSMuo=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
