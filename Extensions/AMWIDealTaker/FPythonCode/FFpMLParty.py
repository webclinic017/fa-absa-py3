"""------------------------------------------------------------------------
MODULE
    FFpMLParty -
DESCRIPTION:
    This file is used to map the party details from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtV1tv2zYUpu+2nHt62aXduG7e3Iek6IY9bNiGZXECGEjcjkoGNMAgaCKdaJMlQWTaZujb9o/2B8dDirJkO/ClkWHms0gefvzO
4eGJh9KnIr8/yy9/LBuK0IVsS4hWES2jfxH6B6FXF/J3BdndGgx7UkZo744e6/RF7/zkyMLyOT6OT09euom4wXtW78g+JP2XZ/0X
g+9V79mVz/HQDxiWf685o1hEeOTGWFwxHKtZlAnXD+SoJBqp137oRSM/vMRg2frtiNhgDndIxyJH9hnpH4J9+xk+6Z/2zw7UD73a
8318EN7gUUT9oe+5wo9CDguCVe4lfiz4M8xCL7mJhaQix10HTL7yAuYmWLC3AnsRZfiNL678UE3zokRxDyOB+XUcR4mcuY/Vcl/v
6/1pO2aUd82F5P+3+0fA1LBvYBhYGsVRyEIh93+jRr6Jkr+wyzF7GzMPCMG62J3aAZXT9DbGi7kC5Ezkbii29u7sEZaMlbFLPRNt
Jfn9BcLoP9kwGW0liDkZZxdlCDsAlTTyLqoQdQBqEI4A6ojWFGggWlegiWhDgRaiTQUsRFsKtBG1FFhDtK3AOqJrCmwguq7AJqIb
CmwhuqnANqJbCuwguq3ALqI7CtxDxO7uSt5eKd2JPAroEHZzjtSpeYeQk4GSAWUDKgZUDagZUDeggS6RAk2Qwe7C8eQdWCdwuQpC
LwploIfYDYIs5qOhPgQCNB50W7IVH8jGGbvAcYbxKFCw3xP3JjvjtOPBzI6BO2Lio1ldvufHbijkzPuT3SJxKUtkz8czbRI2ZIk8
REzsTvZzn7I+nb2gJGl7V2wmH5bwKOxpTbrgIFEF+Vgw7IIwquHrhcjcj29EEww5fugLx4FevgMDy61S8ZO5vWTc3kDKV38i6Sh4
yUGDSybUiQe509TU76luAvGiUdvQuY3ThrZ0PPbZhzCwrJh55TT4sgAEA+9yAWh3oYt31fZn8DHZ7NJ/zUL82g2u2SDHsWw4Cmhy
gTOXMy9wfpzjPF+9rZx6ReEqiwtnaSMpgc9WEO3znGjz9aoU9YJNxQtoZelFUpqdpXTamdIplOdT06kurtRaTik44E9X0KozpRVQ
uV2talGtllEL1p9LlufI7i2l2IMJxdKslcVXbXHVtsaqZbnv+VJkHuXIQKbDPoUEnkmoiTQXp9TSBm2VNb9dwYuPcl6cxWiQozR2
Xh1mqTXnsuOG3XcrsHs6EWNj590eZ7Ui1fU0zjKPzXUxn3Dxj0u5eDvnYn0NZqFWX9yvbW3lLL1HD1bQ7oucdhmR22WrF2UDh5tb
fC5TPmZ6tJRYD6fSWWJKA82qsbhk27mclhUY/RWEeziV2DJSgxyrsVYbJpVly84lyieJnr6nbtK1XNVGmmFrpayWFVi/3olsGadB
jtT0ycxWXfRkZhPO3zPhaZq6djQFdcrVKnIFnxVqzBOfi4X45ie9WvmymMU0R3Q5T+cp/T6m1L1vDr7jwFUuy3hL/dD/LzoOgZuY
gF2yCQ3YI1CRECjjCUwncN0SCAUCRSuB+p/ARsgn0HwKDRRm5Ak0kKLIl9B8VeB+ywYIvFbVAMypl1prreq8z0AbLJsCzXFo5Mmt
oEUWVGL8oLf/U9soVS/9D9ovc+Q=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
