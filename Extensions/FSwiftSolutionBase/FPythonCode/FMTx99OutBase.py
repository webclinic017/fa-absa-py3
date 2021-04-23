"""----------------------------------------------------------------------------
MODULE:
    FMTx99OutBase

DESCRIPTION:
    OPEN EXTENSION MODULE
    This is a READ ONLY module opened to display the logic to extract attributes
    from swift message and an acm object but the user should NOT edit it.
    User can extend/override default mapping in derived class i.e. FMTx99
    Base class for mapping attributes.
    Default logic for extracting attributes from confirmation object.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
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
JMsadG8oLV/I79+3TptSKtalowCWyCZfc+Fsqg1cwRQuZFbr4ySi06XMVgSHtA3SG0lCfg+5TPEOwoAJ2Sj0GnFc1Vq21aqHcxww
71QPd+b/OpsrWzY/i8My1XdY8p3/zTd3SO7M9w4Jc//XORQXzKHID/Jvs8NApnVt9lLPnY39Vuh57JZ4ngoZex4HadgFdb+HBI6o
u4pEGL+Yu+XYIufI9vHg0Li/BKkakk9NYFgL3FICHt5tMQMg2e2XujOvpBA2cp/2TfclzvJ1s94w/crW8EClVLlQqV4uVcqVtzgd
qJQvl1QkOV95TemBj0LykpIsomKZiMqHvYiK4KiFbcIpBRNOKZpwSkmHUHD3peInAyZ+MohYB4eSitqhyWIdixlAPA4g61iHfUas
IyMpFs4iHgrW5czZHO2FHRAw9ndSDk64t5AkZm97DkcvfuGm51huVP6HLDZhnxWbwIzVWNUIU2yzo5fcgepVoYpLXyVo4f4KFf5z
duaK3G0hv6T/LfqN7HygQkcdvpfzAoUmv/hH/ZIq9vCrLFnslwz6JYss+ROcC1UelHTQdRrXmgWuc7O/DpvnyT9x6wPm1aA2SSHP
xnT6rwgoKeP9t5T5ybY5DNMKh3E1S1eNSnMebKg7qSh1dv0kQD6AVlrke7SU7DQyQ911rDbMR7eO5D1jc65tsNqqs9gHq0vKjsTr
+kptecX1qEzdUrb8mKiwnRw421HYDLj1et9t4y4fKon9WeRrEYWyzALMYhRqUKm3FTVyIQ/5xgte581r97Us6DZhriVIhCP5HBVh
hltsPOtGCY0D81rZb4SsZtmw5etFsgtJgbU4MOgHQYKbg0w1saVy8jXboblBvYqQr2Ti3lk9fgmRN3IW4iX7ElLrCv1/3UJ0ZMI6
jfT/fTXSv4991agsaPNmOigaVP64v06J68iX1/m0v06Z6/wJeGqv1H9OvvsizP/Ly1tXuP8vuLMncT/wdXD/5AzcS+NRuGEjJCXJ
aM8Og8L9Ahs8SyurH39t5D/phQAV8jPQKi/oAMnnSA4zE4sZ+cjoxUSP71xYu5qrcCba/uMk2q7oRyGO0GZPqHuuUt5i/kONNlZ9
uCSyRPIHsJ6lpS5NOfigaHOxV0h7Nn1YFNNU79lpccWdv65vZ68guGHpD87pyjZTqyWmergomFAvFsxpJCEuncyMHT1j3iMY7cwL
1UplgS9pHEUpQbiAnNPefpFMU2oRhtephhJ2CRYoy+Bip/jJkycRtj1ipoBBthqz7egARHevpffeVjv9KHN6AQG+U1C8M6guO7ln
ji3rUShYoNmtxI/5CioIX6Uxgaz/wVugUJTVLdNla5qeqvW6ffGsa4XM93mApV0mFm2oL1moddJon8utAnyfBWeVVymKG23ahJ13
nHX+3Nb32iTOJ2P9K15WjPGFeacrvXbiUWOUG7BOmwEVM4V/y6wPfUdhveiO4t3cHYVtAlMn7ige5+4obBOYOnFH8XnujsI2galM
RqH8T3MXF8x0ADO7migfNKRY5kwFfEkMeHVah6ezAsSi6rN8z/Qkb1DxtzwyD3h27ZH7NggrRfhJfztF+U7O/cWl6/WVH9Q+cLGX
eZ16/WMVnF5ddk6YB4oRoWg/v3XzvYV8APyIyVRd9GIL1OXrZBbLeXnM58PMBOyRH8e9PzmnW2ZiOexfZvMfsbLLhbGTQRW7YH3H
4hV0m0hambcD49L9DSTHhpPd30byO+d1RWBd/72JtJctcjwGKhfpd6JSZs+/r0ItlPhqj0tOV3ra+5jOex9518PV5xK6xNFtOAm+
7KM9VP4yUOZsvMAb9bIbVst4HXb+HrFgvPz+q1FcaY6cLOWdzvkSv4fk9w0EzuNLXLUy/x2ehGor2xnmP88L2g1yTG+fdx9+lwrf
tDSVEeHZHLR1f5R98SgXvnjQ3tkhfT1zorjPOXS3UT3OoqX3XtTQSrwTxSE7yS4Tm23IPMZXliJqhvU/7v3ZaWW48IWhCk7ysM8z
P270rvLX7100Ch1fVun9Ttnj9kShMlyZmjqa+fT/AQ1T0pU=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
