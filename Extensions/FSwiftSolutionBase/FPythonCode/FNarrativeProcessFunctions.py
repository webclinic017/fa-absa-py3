"""----------------------------------------------------------------------------
MODULE:
    FNarrativeProcessFunctions

DESCRIPTION:
    Processing functions for the MTx99 messages. This module is used by
    FNarrativeInProcessingBase

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtll9PG0cQwHdtY+BwCoSqSau0XaRYch8wavtQBUWowZjIFTbobJqWl9P5bm2vsXetvTHgCB4q+oH6DduZPR/gpA95yCne7M3O
zr/9zR4Rmz95/P2Kv8THIWbsHEfO4hwbcXbOmeRsiK95FhfYXY6d57LVPDvPZ/MCOy+weIn9jduXWFx0kyIttSvLZLuZY2znMz5e
8+Tw7Li+5wl8jlqhtSGoS3lqTSST5GiqI1BGJ553WG/X/MZpp3HSSpXnKkr3RS9TEz1jBQykaHauX70SY1wP+zKpis5AJWJs4ulI
CpxNExmL7uwDpw39YPMgTKTn/V732+RQlP2y5/n1dsdv1CiE9u5xo9novHHzPW/1x6p4o2fkQfVUFKbBgHGxJJFVE9iVOrKzCaDj
NI7daCRDjFZeg4hMLMWVgoHSbktkrItTGxDJdDIxFvdVvdWfPsqENKJpAmas3ofdkUSln0mJbIwnRksNYhzOnN6VsRciTIS8nsiI
AiGPIvwo7hi3pcE/uAqBimaF1BjH5wRA/YtPC0oI1+OTgOckaF+pHvgyjKVtGVC9Wc3onupHHBeX5r8aYfmekF9ht5zNDtkNc6Tz
+WSYI37vHPvPtm9z7Mb9I3GBxN/f5tlNnqhH3rfRxDstWAHy7MJjdsT4bYFxKLAhri+TPtec/QFFNlxmN5wE7coqxVDFQbyVkJ4g
nUmsQi1iCaEaIZrWjOdsZmAqalugZG4Vz6Z7qoCjWieTDRzq1iLUVwOFp2AlWCUviflFJweNWupg4IolJqEFYXqZI/G6nOy3Kivk
g6y38ITBIw9U4CAOIXTyntIxUDL160hOiAagPZpqr6QFqnfd9098eHJ/PM3jM8D84ClK+hICcj0LKJigq6IKbXEmxxCY7hDBSx0j
SNKSBqw5xzaBoDsy0QVsLb4H8wK64sgKlcwNybcLyHx4Y1QnM+e2ltWIgEo2aGeuyPNc8C2+ydf5Zi7KzUlayWjaQFezfxgwIggP
OGXGVumAEBs8dUII4cqzuzzy8Beb88FpbVhkd8xNlmny8LriXlfd6H2CcG3ObSrvLbGviD5sleET0oofx/BO/4nMfuGYXeMckebp
VT9aZwjwDca3QVYcyZsEOx4YUo8WU6so3nqQYSc42LmDHc20HTzJC2K8Y1W/T3fBZXq7QDTY1cb9n3RR4eDUF+VY1K9BWh2ORHrs
JNrL9hLB6Xbs60aMEwIsFkaLNrIoRRkv7XIidnYqCwo/7Ozso9zht7CQXiPJL4/ZFSaKptaiWbpWU8eBut8S4McipRXjQpuUoLyO
AqV7xrVj5Usc/E0C2F1Pzc5pqGyT8nSQxiYYKX2BuQRGp5Z84si/77NG6+gE6Lt8omKg72d7mrbAmiMTY9PQBoyWtrnE0/YMx9Kp
dEKLLeUWfOoal3eWiaufv5z1F9gwkt0QG4jeJlhiCDAd361RDAmkDXxYPzh76/rSL2Vr3Yl1Oc7bMs2FmsX/Luu3T226F49C/L9i
vyQzz10f5nmJF/nXuW3+G/8Ge7HEPf6Muz80XLWCIDZRELir5fG34NiQdVdmVxb//qD8lwvhfmrMZOl1+qXbdxcv1aKYK/GnGFOp
sFr6D+1qU6o=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

