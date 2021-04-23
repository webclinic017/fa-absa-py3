"""----------------------------------------------------------------------------
MODULE:
    FSwiftCofirmationInUtils

DESCRIPTION:
    A module for common functions used across Incoming Confirmation solutions.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNrtV/1uG0UQ3zs7TnxNmvSLUD63QMCBErdEgFQBwrET1aVJq7PTSuGP0/l2nVx6vnN313WNnD+gvAAvw6vwBrwGzMzdOU6qAhVB
QoKzdjIzu/ub/fjN7iZg2WdD+RqK3gIhGNsDaTFhs8hie1au22zPZqLAfoQGBSaKpBSZmCFlhokSKSVs3KrMIt46IH98hp+zfa+x
e3fzlsPh22oNw66pJ91Q9XwTJnEz3jVhpB2nsdmqu8377ea9nbRpjfcSMYgk7yaKB0mvl8S8O4gD7KX5QEvB/UAlWvNmDNVhvM/r
STwB5jqJBtR2zXEebLotBOYr7orjuJutttusY6hW9W5zu9mukX7LKd9c47V4hJHDbhj4aSyTcHMguQ5U2DdVGQdq1DcQPh1fNYik
r7iRTw0MU0g+DM1BGFOXIFGSh5rHieF60O8nCvqtOeVP1nj7APzZDLMWwUAbmMh3fieS0GgdGyFGr5/EMja854+o3TBRj7ivuXza
lwEOBCNy/7lxC+iWDv44lG9w6RSXMYzjLLc5/A2+ncACCpWgFKDUkU4SRMjYkcUMY4eMjRl7ZrEjm41tdmixZ1BVYOMC05+Rx848
MUOn8lEeFshZJL1I+gwzM2wMnhn2DJg7toC9GFpfAsnrB368T/wAgghkBqyCCDUssKaV0emORsl+GMDqp4TD776vzAiopw+SQSRw
qaghACUD2AGkItk9MgG1I3nfDwWvAN1E5l+dwPmxyCA3XgpSyUCGT2AGlc5glKOSUdUyimAu0CJluZSQFirpgRYL2Niky7fb6zdu
8C8hxOMBNFSrnFdwT8wrILa229Np8lD5/b5UZpH2Koo8SDM58rpRMjQO+KbMOTBrGSS1z41aOhVzAXz70nh9nLEnpPEhs9PI8yCC
qbBmARwn2pmlrIk3TIfkJZ1DF085CpzPhZrlhpctYgUPRBL6DZxidsjEp0+Ztf7IXDoxSD8Pj259GSGKJWvRmrdRlqx5+C1Y/7P6
X8xqFzfNnAcBQFP0TbmDxKtjIKlox2n/px0Zed0ZpBDhkcCr0EXiHcME0zCXTzn+PhU7ORXf/UMq4nCcaSp+D9wQl5B7KIF1FlND
y1g5J4vIKHgOXD0ibsFFf/WoRFoBtFnSiqDNYU94GDyymfoJHwZHZSSiesTELCrLYCN/S0z9wMZlJubYMhi5u0wjKOcsByiHoH6d
gvr5FNQsU7+w8RzJDHAWytwp0HMZqAF9nkCHVgYKCNISCziqvmOJ89QTQ61aGaJYBMTjkBCsMalamg5mChgPVoyqLrBldMyi4+Ro
LuJoHg+t1APJ28WnE+6Xvg7idhibW3wL+J+niEu0x3z19/Eah8s4S0iDLKvV6/d2d9oGN3SjWTdF+LtT295MKxsNeK20DJ4CNUNM
R7WqUTrU59PPa+RrZFaDrDsaaVytAWKVIHe/ebiT+er1djVTG42bmYohqxnEnZ0KdkmHAgnlnkPrHRAqn4tHc/EgzycnadKnkx0h
tFEVJCnNwQ96eJb/Sf9O3r9EzcwDP6KDX2MCtf19ysgML71uMFAnDGiUsd+TaaUQSmpNlU/86GXS8WaWji8e44aHZ5I3fZGtI/Rt
epCXrBKlqZP95slegHIBSnliz1tXpuwlKFeoXMPe9n85wRH0H0xw+3SC22eR4LUXJ/iGexFvEDznXezvXkGBrzB3GcWriEmZ7F5F
+zUUr6NAsk5lsPvmsf3i7HXfwnytIHHct1Hgg8y9hhmAhHIxAV2O4j0UK5N77n0UH6DAVHFXUXyYJ86ZZU/t+ez59qyzpzI5JTxP
JIHn0UEAJxC9EugcS1flIxTXT8zxL04UD6Uv0v+mvsJXh8a3QcmG69kuL8Gv8js875nZ""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

