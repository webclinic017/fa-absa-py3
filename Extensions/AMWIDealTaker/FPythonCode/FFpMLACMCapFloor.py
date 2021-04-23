"""------------------------------------------------------------------------
MODULE
    FFpMLACMCapFloor -
DESCRIPTION:
    This file is used to map all the Cap/ Floor attributes on the acm.Instrument from the incoming FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtV1tz20QUXvmW2Ena9EJKYTrsFEpNh6aUywvDAMaJi5nEyciBQgbGs5HWiVJZEtKaxEzyQvkbvPBH4XxnLdmkHQgMTrxeSWf3
3L7znZUnpp8yfT+nb/aEBl+IfRod4ZdE6Ih9J5+XxH4pn5fFfln4ZaEdcVwRQ7pZEb8K8VyI7/arkOg3q9jwq5IQD/+nT2N7Z+Pr
rc2GpE+nk2xvtdrbbZV0wjhO5cPGxma/7XZ397o7vY9ZZu8oyOQwCLWk33GmfWliOVKJVGEozZGWtPiRtMuVMWlwMDY6k3HED5U3
Wu9GmUnHIx0ZOUzjEd8PIi8eBdGhhAWNbzbdPhTKe+69hrvZ33O7bVjQfyS3utvdvRZfWHser8tWNJGj2A+GgadMEEcZTMKumZcG
ickeSR156SQxZCzJjUNNt7xQq1QafWqkF/tangTmKLBGenHK3kWxkdk4SeKUVq5LVvf+uo2A3SeX8saZIft/VgehZrEPIIadRkkc
wdORmrDkSZw+kyqT+jTRHgyCXqle8MCnZdaNmTJlEPCUvPFl4+H/9gn+oE/PrBKyLgLAy7Hs0PcLQM/QoAXjVwCbFryYlAFQTCqA
MCbVKX73a8Kv8mRB+DWeLAp/gSd14S/ypCH8Ok+WhN/gybLwl3iyItx+c5kUe87UFMK/aMOcBzSQScf074gzKhVHOPRzzFbhwpRx
e1Cx1YOSzLZpmMOgF6qMEHNE0T0JCMMHGnBOLLB9bVQQZhao/afbWzIeyo7bkklKOfGMNJNEu4hQj0vTXJ+L4kyJWaTbg0EQBWYw
4Eh7qVZGb8WHhzrtqZE2WN1RYabNGmQvZmIw8FTShO+mAid0OGxCLQ/ZjZfkbj2ZuIjTNQjUIFZadVYcrzSNXxHDFRrOOHoD5qk+
q+nx6MKsJkTdWq77gDT8s252KMjozi1IlRhFrLw8/bLyDpQXCXSmmbt9XAbrUQLPS+KsJNKPWKiCObIarfA1cyKuCXD9JsflLgfH
2DoepylV/iQnn6DIR8CWP8Jg61sOia641opF09JOUp0BJsQNrY1+r8lhWEIG49Eojr42BA8DcB5q02lPF3OcQn2YsSQ9KR4sWfuK
61v2egaVLpgwCbXRjNZZ2IfJKOQJLLxE/F+5uHOu8zU8WGRAvOHUnNWSl2fEybMCNZSGPmc+ex8DMbSWBzGRFfySiihyGMbKvMuh
jVOfiMmPdcZcZwyh2tpYOOHCdYPZUG3RFpdw4Yp1AdLdaAcq7hZYKr0I5JvzWJrW/6zs5RwygrnyjyOTKqrkLPhZBxb5jHeuNSS2
PZXok8CsFNyrufl/78P1Ig3z+7w958dlok92U+tE6JlxckQfqIxgSpSECygvJC5G35QtIrksOQGXsH3Zqu60SHyPNn1wIfrYuJpb
/TsNk+/FaZPLWIiNH+6geo2DoqWytvVMft08L4vdH1fEU+SqjKqmR5Sn2+dU3xVU9VnZEjld1NBMcPE0+kxUzIJ41hDpb8I5rxK3
L4rjOme8gU5DtXVWheza8xI9XBbHK+g7dOMXR0SO+JZ6T7+5AFtRG3dzMBAUgmeaCj3wdOCDteDhYd76ODqbaUoEseMxO/jy/r3s
frbLjE0noeIIZKEVmECF8hsVjrXtG4jsutylA0dGpHSkvWc2V+AcXxmFA0c6TtD4e80rRalwplBi5qolka7dmnd2i1awldNMn/3Y
hRsGpP9ERzqlJtNW2RGl9CQzdXhy6mlWxWs467YL8WYbWztPTANQmXUmrh6T8p45Sma7wLZOC62xuMccOSsSdy2nzGxmoQviM3BC
X54I5jz8MC94USo7q86aU3VuUHe75lx17jhefkYo2sxjGk4fzNjhOfB5W5znPQdj3nKcH1fF01n9fYRB/aSnWBkfIKYoQI/iSvk5
kcGQ7xetgp6hDHvckThR7usY7sBl5KATpJlxaZs5Orl1eTohqOU5bR+p6FBnrZw2RGnNKQilknt/qyDGM65GcGN5nhtvTjnG1Rip
1SmCuSIjX8UWKvTGIZ9Ld3UaxP5m5G+Q8faEkPcZXtqNWnZhJ1SHc9S/9i88vPbS/S7Pl+/N8fwwOKXq5IQhIyg4/FKCwKazLvBC
r/o3BucsCV1I6lcvsbVIxQf2sEWpSG9zTopOFVEsmSiP+chqM/XXNL1uk5/gRYkRlx9PLeKyj+n5rtvd3pyeYkw44Z48/yYj+7Tw
SxX5IXahhXhfY18sXu3xkmTcK0UXLMpvfLBhNf63ULk4cfVm59E6VW4RoqKNAwBoGcwP3MOL3L41l1skkl6kEnqxwpSKkCIT0gsU
vYPZFs6HjV01IYZ0K/89v3Wr1G60VyS3zFQ9PdlHRJR0sm/whX1dGwz4+O1CwIVPLhS4KBcXZeXex/AOhncxPMSAALmP/2LX30cU
D/E+kWHLmlOv1cv1xXqF/hr1lXqVZzV7aF1g4/zYI8uYlN7E8AYe3WQSz0lldmR0xeVN4Uh8Yn3/dCk/Y9acZfyV/gTzP7uc""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
