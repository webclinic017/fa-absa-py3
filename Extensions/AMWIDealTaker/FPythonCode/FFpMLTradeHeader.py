"""------------------------------------------------------------------------
MODULE
    FFpMLTradeHeader -
DESCRIPTION:
    This file is used to get all the details present in the tradeHeader in the FpML
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtVd9vG0UQnju7TuIGyg8hRYiHpVKQRYkrQO0DQlWDk4KlxInObiX8cjpu182W+6XbdVqj5Kn83zAz67PPbqgc1LV2vb6bnflm
vm/WMcxHA+dTnOYRLhJgjKsH0ofEg7FX7X0Y+yAbIO+AbMLfAG8Bfh836N2w06Ljj32Agw802qdnR89PjtsCx7NnxenJqIyk+k3h
UoqD9tHxsBf0z0f9s8FPbDO60EZMdKIEfk+NksLm4qWyIkoSYS+UkMpGOjGiKJVRmRU648e25nb+iKK1XxwHQ3Iu9oP9dnA8HAX9
HkUbPhQn/dP+6JB/uNjfd8VhNhNpLvVEx5HVeWYoPDkzcakLax4KlcXlrLAIDO2micJHcaKiUlj1xoo4l0q81vZijiHOS84ky60w
06LISzzZFRzuh67L1vmprOKpsXmq/4r+SBSb/Uhm5Ckt8owyTqMZW77Oyz9FZIR6U6iYAFFcEb2TgcRjLo1lsMhScUvMRor2wQcb
+h8cA/sJqmid7LhSqYfzF5LZr7goYGUC6ZBk6fGGxUibJgmVNpVWxy3SLW22QLZ4sw3BsLOFvmLyfAcnyhd6FOEBcAdce6ABrtn9
dYPXJliAV6z9K4DQc+qnBjLf0ekkMkx9nGcot4zVVykvnzi1iQtOzFJSgw4FtV9WiZ9HpZ1x9v1skpcpU2E/xtfFypsO4bVNiquS
if0KN+F65cKQwx1FVtn7Nxuw075EdSDvCOnrm80uVWkQh4su/8tqDSGlx4v5/AZau8XMbpOfUGfahiFRb9pk7rc892Feqsm8EFtX
XP9hhx6az3ChJl90spCYLb8LqEJu16yQvB/OrnM2qoq2R8Y+Q4r9+TW5kAi5WkgBJXLlwysPrjx4y7rBDemDpTNkjs0+k7WOtbon
XupLlYnLKJmqAevJLmAe9k57eZrm2XOLMuImKVWaX6qRTtXZZIJOXbKNKlm7Q8uC/Lsk8qWHDUthaqUgfZkWl2LXu7cJM3s1ZlgY
Qi9k5lhp3ZafOdnnq5q9v8aSX2fpI4LlqIAaFQ9qVKyDu5GQJWB/UeN7VVMusWyYhHkniW9qSdyutvPWnCtKSwd167a1/dS5fLHS
6N/+j9Lu1Uq7jm1QA7esI11uqxfMhnjNOt7uEm+HO8BdMFmUKrwL2/zD/Y+FYUAGAT0LiMiAuiogcgIKGXyxUrb3YgnoJfkwlEnL
29neae60cOLHneY0tzi8zGOMTQ0ZcAVg8ziczc8O/5O7VUO2vF1v1/8XNmY0xQ==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
