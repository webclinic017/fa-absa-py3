"""------------------------------------------------------------------------
MODULE
    FSWMLUTIPriorTradeDiv -
DESCRIPTION:
    This file returns the prior UTI details on the trade. These values are then reflected on the ClearingTab GUI 
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtU99v0zAQdjooKEwgDSHg7V4m9aWdNt4QQlRtQZHabkpSfgmp8mJ3NaR2ZDvbisYT/OHcOa2AwQMPs+RPzvm7++6SLwXbrAj3
K9zuIYJg7CNixH7gIWKixbLODl1+aDHWvaEVT46Hs/EoBlyvs3eT8SxPTqwyNrdcyKE6h248HGWDNDnJk+Pp80DMl8rBQpUSrPS1
1Q78UkJFaYD5IKTnqnRgdLjwVKqHWdJJOOdlLR1wK+lOY4VFKQsvxZY9KCW3Sp/l/BTezBKI347SjKRhP92P01GWp8mAeskOYJxM
krwfHprODnvQ12tYGaEWquBeGWrOhMKusKry7gCkLuy6Iknk1aXEUEGi4OWlh8IICRfKL1XTT2GwVZxXGw+uripjMbMHQe6o17yL
ps6WVdTOm5X6yk9LGWjPwvBYaVUZLbWHFV8H5oWxX4A7kJdV8w5IF/hfEwhMa8b4JcY91E5anEZA3L2xVZAHW5s9ILt9arz4LWJX
jH2O2HfEFqHtXo8gR7PfgjuB9p5dRdeDjzfUCE1NitPOLURPMMVh/X089IVQND8vE70wIRSsiRabH1bc+j9DRxTqUNv+NgG5zj/A
UzDmzKthY8sO/WkB3BOEf7q+V639Hl6eSb+tv8nepbzd8LO2o73oEe6n0bSRvYMwnwtTzOdpeyvyv3J38fJF821f3iM2lWxHPwHK
XweY""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
