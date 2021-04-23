"""------------------------------------------------------------------------
MODULE
    FFpMLACMCrossCurrencyIRS -
DESCRIPTION:
    This file is used to map all the Cross Currency Interest Rate Swap attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtWF9vG8cR3z3+kyjKliXLkWPFOCNWTQSwHPdPgCZGW4WSUqISrR4VUxZiCKe7pXTU8Y68W1akSwVoXaDwU1+KFHnsB+hDgb70
vUDRl36CfocC/QLtzOwt72TJrY2GIvd252ZnZ2dnfjMrhyWfHPx+BL/4ABqXsX1oOXMN5nO2z3XfYPuG7ufYfk7382w/r/sFtl9g
bo6JHOsUWRuIefYrxl4w9nS/hBzNagEX8gzG7n9Dn/L24/XPtzbKJnw2N3vbW2u17VoUxnFtEEUicEZ1q2neL69vNGtWfWe3/rjx
MfHuHnux2fZ8YcJzEAvXlKHZtXum7fumPBYmCTG1FLMeSBGJWJqWLYXZPEVOKSPvcCBFbIYBzbGd7mo9iGU06IpAmu0o7BLdC5yw
6wVHJipYfrJhNVEPc8VaKVsbzV2rXkPFmg/Mrfp2fXeNBkrNh6vmWjAyu6HrtT3Hll4YxKgpSo2dyOvJ+IEJCkajnoQ9AN/AF0By
fGFHphRDaTqhK8xTTx57SkknjGjTQSjNeNDrhRHMXDVpuW+vKsMoOZrLGcQS9H9uH/qC2L6DbCip2wsD3GnXHhHnaRidmHZsimFP
OKgQrmvaF3bgwjS1jXQxW+I5RLAb1yzf/8Y+3r/h05BL4Hiv8w9HhwKH36fooZ9BIxi5P0MXVr6PnRz6MXby6OnYKSRuvl9kboE6
4OtF6kwxq1ktgSyHJ9LB81kNV7gDjWSsA1/OxhAknHF4dGghHFC4YGzGX0CT8SrHt8Ex5THY69QDZz0U6Lc95cGukLbnx8r1mq3t
LTNsX3BliIheBEZ3pClHPWHh1hu0lpzPmCldU04B+eDACzx5cCDncEORgDjYCo+ORNSwu6KKm5N5VFf47SpKpCa+9V/svtobWWiQ
BWTEucyY4w7qMQu/ojbVrkGIdJZDg53l2fAuGxts/dkyOyuwcQENCBATLTBp4Oud/gKDb2v4riFzbMyR+QXyTxtfAEMRZ4GmnQKe
5DiH784Inc6m2DjPot/zcRHxC2X+jckSmwzhWM6mSWKJ3exMEcefiCNLQq4y63/IX51aZsERG/1Ui5y6KFItWuIZkdnZ8xemllkr
WGCco7eAHGyBj7O9MQgts0XcEhhomuS+5KmxXvLhQ2XFb7GzGTaeQb6THIuecuh3ymSbKbaInth/it9W/yUPWMbeVUPZrF81gl+n
y8RVY/TRJXu83Eypni2Qk5cz7KTMorsGP6swLiusM4vB0bmCwSavsnEF592AI+Pghp1rGHpA+CVHLfZQPYrPd8BXUKEy7oEiCwbz
etCvsRZEarOKHhZ/SD4rCRobiNK2b7ZtR4YRho6wnWPTF0fY9ybx4KGveujy8XVoNqIIuR0HXdv92Ly3Et+Lf4KOD7GYZhZcAUAS
ABCXwADFuFg1dwCrY0DTY+GcEMlsgzjXljZidTTo4ZRGFaNEFkiqDwpjSNbjrdA5ES4F3m40EBKD5zlkBXwb9kRkwz6IOIQnSjgS
sj3c8gKY1Uh0IaFtP4R8NqM4Jm/QQjv2aEscSQzJxD6bZB45jVsfOoL0o6kU6AoUSKX1rcefyTJ0/AlQkDJgR3ktAwyplKtIXUPg
SmnXCP886dl+PXDF8IntD0QV9bHyGnXgiGLStm1vYZdANxxg0qb+YWKogmYhPWAW7QKejUH3EHivwChQuzxQXkBTAjh21XMFvE7E
4HR0AvHmeEfgGaOFM5ZcIpQj/CsaRT7LK7zIp/gyn4dnEUbzfI7fNBaNXNK7wXNALxtlowJvkf82/CowQo4b/Aq/yt/jN4wyvHOM
pMbLaTzFZvgIo3H92XfZmYE40GEKeqjPM30jpVDslBh8WwDHzSoKjlcy4ROJtsC9CnJgR+cbKI7QwCrBLCkPo3KqK1xPQhqBoz62
A6C+e95Bn9jRCKombUFyMVhLj0kguYCFUq339CG82UncUtLAF/SLFhQrlt7DNr4u0qHM8iVlxlI2Lf2Rq7RksOFvORgTTLj+7CVH
6MlpG84RJOfZqMWRaBDR56N/IXCdUfrp5IloY2xPhi9IbvBXNvwL06L/fC7dxSfErTLGH4iuBM1xWUiHSlB/jgcOERX/31nCU8ws
9mlGm39eps2d/7EKwi9gdQlhH3MuuMtO/4TBt9Xqf8nzEGoI7secQxLmgAudGZpQIXCfxYShwV1h/jivfO5Lvoe574JGrf7XkPpe
Yf6a7/XnYMes9aoyYPLkAmJmnNbLVFYANhFEpBl7zwVhfHx4KYq3hz456CtwruqtiCrhNoCPC8KR6K+aP6awcEXbHvgSbwI1vVYT
1nptFmlUr2r3JqCC4FBwbK1o5GtAKW0RGFawwRixqBjDoV4FF7EQeiwEUwurPAuzgYULy3eUOdJ6r473lZ4vpKDqNYXZdq/rk2An
KxgDjzKOwC1sx0cEuciLmr7/dmE5P1Emq3wTqY8URAIEIkDmeIVgsMIXDaTg3xKOJj+kIhBeJ8BcUqVlLluFfwCNQj+MsgnKJcAH
pJwmpYj3MHGeBMLXZFPakYRLjpuSNmAA1yAoy32488C1qVElG15Jk2gyj/ZLgEgJbgKFlSwniKPEAfRNpGiuDALiGVjLb2fq6+dy
UaIQrPWztB5fuMRoP5wYTaqrChpKQdsnqdHAYFhPfqJZVXgCRqQXmzuJJX3IzfoKjbWW185YTqrbCcathdhrUY/cf/l8tdKECgpv
kmv6Xm6hG/6fNiolWQJU/Hk2I9xWhsHXeW2Yf6g7HWQARHe4qDxQJfY9jdyGvqjkWFKhEpoBq76z/E7N+A3NyLFK7OIj+ioz/SsC
TQJv9X+XF3SrQYZSgqFU704lxTHvb6Sz443zs3Ovnz2ezIZvKwVP7f9JmdR0bB8BzSa4g/IsUwakZ0ru20hniF28eGL4SfSrzb1G
dXpyuB9MzrqkkeVcDQDg1A2DzyVcdKk4BB/YgAptEzC4CUcfHGXjLNFP1cuoH2T4FNVU5XATm1t6LS/hIlfJVoSJqLfwnuVzEZbM
Xwtcrcgv8P3tBNZ05bcAz5sAX7N8zqjQk2yTXMIDKKLhEl6mgfrXycEBXaOtu9igYhaekfURNt/HpnbO59/sYo5MhMVogCKfLkx/
b7o4/T48i1XUhCLj4MANHViezm5xknowMmynS8mGUGZzrWbHx5t+eJomGYu9vVZkg0dq1z+gcrBC2lX0n/EflCyjCA==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
