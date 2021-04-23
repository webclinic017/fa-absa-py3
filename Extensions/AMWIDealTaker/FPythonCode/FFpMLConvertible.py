"""------------------------------------------------------------------------
MODULE
    FFpMLConvertible -
DESCRIPTION:
    This file is used to map the convertible details from the instrument
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVN1rG0cQn7vT5yUlximBQB+2DwFBa4e0UEopJY4sB1FbKSulUL2I896qWuW+erdqrJI8Jf93OzN7J9l1CHnIHhrtx+x8/OY3
q6AeAf6e4q96jiIGmKP0IPYh8WDuNXMf5n4zD2AeQByA9mDtwRI3W/Ae4B3AH/MWaUwHbTL4jQ9w9JlGePHi9OX5KBQ4zs6Ki/Nh
nv2tS2suEy2OwtPRdCjHv83GLyY/sc5sZSqxNHiI/5tKx8LmIo0KYVdaqGt3Y20jk6Bumad8aLLKlptUZzb8fSSnZFE8ko9COZrO
5HhILqaPxfn4Yjw74YVz+ORYnGRbkeaxWRoVWZNnFfkkk5UqTWGrx0JnqtwWFqNBvU2icUslOiqF1VcWw4q1eG3symR1mCWHn+VW
VJuiyEu8eSzY3XfHLkVnp9FSm8rmqfknwsxY7XtSI0tpkWeYEkKwZc3XeflKRJXQV4VWFBD5FdGtDGK85tLYO4ssIVpiNrEIjz7b
MP/imNgDpM7/K6wasiKj4Blx61sUGpigUFMTKUi8ZAa+R+62iaO02QFZM/JHFCqJKqzMCrP4ADWu0wrLcHJ6QacUjvLwslfHMCRr
pygswBqoDd5gA3jgYTQ4WwRQT1pg27BuU3PQsgO2C+tus+yR2nRAVieDPplrN9nbHs4WC5MZu1jYFmlgKWyIkz1DWd2WEZK431x8
lmcx61/SJGy2pzZXr2yHYPtrY+yWnbJepZPlgMBlUd3/AP7HxVZS2oekQCbBO/D6+N3zVFC/IUEDy6/ALwjlh1m6CUqfJyzXAaxb
fOTDOx882mrXW+sOg+MO+C0hw9UPHKi91b6UJBLSluZyYzV3nCp1ZDVrMpD3KLD9FcJnMuhS9ndQFCWSWtnZttCS0JAEqeTjrvN5
VqSJ5OJQ5i+zWJfJ1mR/cmCS9uwXKCKVjveF6bmdGdXmE8AlAw934Pp9Bve+A7d9HdwJMKZrhghRRpTeBowpbvqMaeAwdUoBdQMp
tW4C33L4Bogvc0CQAwcchSeWeXkLZ0ZS3USS23Wzw2TE3JpwtzG8rhjDlUliB+qXO0d0/WRXOYfwg92ps7Q/Z5MObSLxVZo8R5wp
9iXWhxtBkUV52ID9UcS5ls4T3f+aVHuM/SHifujVDHFNmEWpxiYMeeEeQVx2eRnnarHg5pDMB6qkfHgjho+Xng4PGvcdr+P1u3d7
LtuvSFCfSkpZkoKETzfN0f/s4v3lzt7FXfr8/wCRvM2o""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
