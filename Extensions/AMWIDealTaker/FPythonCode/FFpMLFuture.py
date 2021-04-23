"""------------------------------------------------------------------------
MODULE
    FFpMLFuture -
DESCRIPTION:
    This file is used to map the Future details to the FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVm1T20YQPkl+wYYChU6Gpu3kmpSO+wEyTT61k2nrGuh4BpuORNKpv3iEdA5y9TbSOcEZ+on873Z3TyfLSaAwjYTF6l72nn3u
uV15rLgs+P0Cv9yBh8/YCJ4G800WGmxkaNtkI1PbFhtZ2q6xUY35FhMGmxpsAo019paxK8b+HNVxhNOpo/PPTcb2PtLVHpwcPD8+
bHO4jo7SwfHRTM4ywffaB4dOz+7/fto/Gf5I3afnQc4nQSg4/J/lwucy4ZGbcnkueDHNF9INwhx7qBUctl8c2g464bv2bts+dE7t
fg+9Oo/5cX/QP+3Si1rj+33ejec8SvxgEniuDJK4dJZ7WZDK/DEXsZfNUwkAYNwsFNDkhcLNuBQXknuJL/jrQJ4HMU3zkowQx4nk
+SxNkwxm7nNa7sm+ikr50aO8WS6TKHjjnoWChj3FYegpSpNYxBKintPI10n2F3dzLi5S4SEgXJe770XgwzQVxmIxVyKJGUTj8/be
R7uCf+AaylUQSmU/Pa1QkA77FUV0Bg/BSJWs0CNoDcVokkFKRKNeyHDUYH6djCbzG2SsML/N/CZ7C+oGY4UaV5nfImON2U4HceRd
eHihm8NWnkPY18onB1JkFpzNJJiTLIl492CAwzAQzwAvRhFCD90CfCYZm9IRuWRsbDBpsqmpXy0ma2wKf3V8vTKYIRts2tDdTYwc
jZY22sgCGqvaWMMup4NLDiXy1/kEF93R7NoC8IpXopdEURI/l6B9uQ6dmZDVpm09vtsbVNuRHa/yXtfj5ApY43EQB3I8llu6uR/n
3ZIhiVCCpZYa4gStybbqktksAr2SX5m5cDrvod+KMMbjyIX/gZzL++91eUkMszzpBG9EB6mnBXIRTjrEBT7y9WWl7adzuwlNGHK+
iSOMDbg34deiu9xHQ+8jDr+kfXRolXwPHi+FJGVoeNx3peDJZEkuGiBNs5EPZW1odNdBJOZhiUHh/SscZtIBuSM+DYHnQJLGN/kg
vvU74NtQS/QqO/B1BaNZnIPyLGDsl0qzVHOUZglpfhcmhxUqTQ2V9PPKDWfiv0nNF6Tu/k/At6J2WOG2BGxv3YrgfJng7z4gAkvj
fVaKAJ8Gphk0LEwwV5RdMMFgU113NIoOYxHefZUbKGcUoVRy3rCDUrPx6Nh0ZLeUCg5gw/px3zk5SjLYRRt5piN+eJEG2Ry77c+w
bQ3Rvntob6G2nQos1bpIKrQjNWLloeFZBSclL0+r+3hpFnkYGTCRBOyChGwqaoiqCh0Pit1GNEu5P8m0Mof0zUMh2xie3cJAv6wA
7pd5bgHaxog6VilgVJvrRYuhlGCh5RSz4s3kNBXIozQKn6C5QlxgKtte8FHXfJyUOgGRVKJXiqE6Ky1WkoG6sardSlZ16oMOKMJO
h7LuF1grMoFnt/jYku7LgiqsGKiHaBbKIA0DkVF8+sQPO42SORzWIzcTCIgUprz2zoPQ/wO+X164obSofkj7U5y3ucwl+rqIwt+A
RTSVim+m8F656Lvq+gFnNIjRbeOB4rNW1de3Sl9TVpAHZP5tFWcQ6bWIXvo4xjn5TrmUUlVFStx+hPWRpKdK7yJw+xvEXysTyENd
7ZAlmndzyUMl/7w4KVvGUH0pqDoeuxGUU+IeCi59/8Frk179xBuPqWQS0YpySgF4pEnINk60UfMEkxZbwLkWE7ajtxwdNYyG0Wq3
asVdX2u2GkoWmPZssih/EgcI22a3WoZCfKaC+okqQJuWW1O3+S/IQ8xH""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
