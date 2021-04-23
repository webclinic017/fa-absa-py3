"""----------------------------------------------------------------------------
MODULE:
    FFXMMPairingViews

DESCRIPTION:
    This module implements the pairing views and menu items on it for
    FSwiftFXMM ConfirmationIn solution.
    There are 2 pairing views in this solution 'Pairing View 300' and
    'Pairing View 305'. Menu items defined in this module are as follows.

    Display name : Insert Confirmations
        A menu item defined on the Operations Manager frame to insert
        confirmation records into the docked confirmation sheet of the
        pairing view.

    Display name : Pair Confiramtion
        A menu item defined on the Business Process and the Confirmation record
        to pair the selected records.

VERSION: 3.0.1-0.5.3470

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNrtWktzFNcVvj0zmtEMEhJCkgG/OjbYg20EMRZJiOOK0AOmrAfuERirnHSa6TuiRU/30H0HoVhUHrgqu2ThRZbZZJVNfkF22WSX
qlSlKqn8l+R853b3PCRAElQWqWiYy+37Oueex3fPPT0Nkfzl6ftD+sajhhCuEBtUGsLNCd8QG0Zaz4mNnJA5sZUTbl64BfGEWvJp
b0FsFNL6kNgYSutFsVHk+pDwS6JVEhslYeC5KPxhse6WhCyLJj0Pi6+FeCLEFxsV4ZbT1krWeky4x4Qc4daRrHVUuKNp6/Gs9bhw
x4Qc49bxrHVcuCfwsHFCuBNcmRDuSa6cFO4kVyaFO8WVKXBfr05DLPMFIS68xL/KytrCreXFqxWT/paW7qys3HS8yAs2b3tyO65U
Fhbr81bt5nptbVWPWb/nxWYrdDu+NL1W25ctGajYVPek2dYzzYeYajqBa1Jfx/SUbMVmGFDFbIaRplTf9poK5Mz5MGh6UctRXhjU
AjMO/Q6qMwk1GUnToe+HA8t7AdEkVtLx5rsJ4yY4Ny9fuvQuWOBVBrtm350xV7qsubLpBdLNlkx2B6pOTCz7frgdz1R4qQUvbvvO
jhk4LWleNWtBLCPVt4eYx+Fvrrv/jEYYsKjW2jLSo80VJ3A2ZWQ2IyypQmIDa2arNHrWNiPZCCMXu6eBWMgNG/dp2b5B8T0plRk2
MSBbpld6++8FQkp24rSw0EE2cq0T02McmzejsIH/oXZ0zO9lO1uPeAc7PC6WvmwoWjDZGvF2e9Gqw97Mc9a5SsVarK9btXlYYP3i
cm2ltj7H9auV8rdnzLlgB/ryml4jkWcimLgReW11UQaNaKeN9bVWLzZ86RBl+UiR0Fxpbnukc70Xok82HZtBqMy4026HEc2bqZQ/
nOm3ej2i0YlV2PJ+6tz1JQ26jEFYo9UOA3IJswXJ0rjtMLoPO5KP2nqjoEhiGuTbpWma+R4TVGaHjMGUAfHxMt3e+zf9raoKQQqc
EMqqEc94TJ+7PrkaKq+5Y3PjZpVwWagxjFx8pGQUOP7a3S3ame5A8Z46TmUPjpAzNlKAx4BrQLK3qZCCQV0wzOWAzajkgXeoFIRV
r+JEaGDWMH0J/cQ8Zv+Til0hthhPHxsgvMULPDHE4xw/5sWuIXZzOBsMVUj7qDUvoh+LR++jsvCjk+JxQaghHsvniPFgQXwejApV
FFslcEKzDJAaZlJDvHZ5D6mhjFQl7SuK3aKI/sKkippUiUnRv5Im9cdeUnkmRdKoV7HPVRoqxMo6SS/+CgIly40JZaPwoUeG+9Dx
Pdecq3+2bD7oyEi7cTU+D6NZuukATUg9Zo8art20PuORZO9LvG4tSLQKYDb90HEBEXdTn25rn6Z/v3wZ9OcaLTKVA7EgfW/TI8fq
A7a4egwmhnPwulR1oNxSFLZutQlMbzqB9NU4zHJlfZ7OhFYwH0lHkQ+/Q42bUtkJAtpAQPtuO7IbPCy2m7SIrXbaUk3SUMd1sx4V
2gymT18DW/dk7xqv0FAN4dy5YwOrk2VgwgG8yaNu6PjzOWt1z4aWw+10Q+/tR9dptOzw7tY+/D9z+B5Wq2CH2SAQbqoyVbAlzWoJ
bqcJqFNUf9rOGUOk07ind6smeF5Xaclyrw0uMcAVs4FlqgAJLuLJFI56Q5KZ9o4agTWG7Y7vKIlGbDs2GV1GjDFjPDeSKxqjxmRu
lGq9z4wj6ZdxBGTJXevVHDzOKqTEGc2sE9njsxmCIPGwSka/gJE5ZiYjl0/JgUkvDU6v6Nj1CsWjFIJeofiTIs8r9WqZnR+CXOoF
YrYPFjeLVGv8Vazc6yPrIZhbCiP2Lh7ehinZcM/4zcHh5nqoD36aYeoprHmnjW4CJkLrUNFBx3tsh7GH9iOICDa0wMEK70P7fEcH
QddTTQjjhFEF6jE1m3m2bd6Ebesz0bat06B7BsVbfcSfzUGm2xibKubKZ8r5vQfV7P8Pqhc4qGb/dw+q2UMfVBbszII3WbAIC25t
wZQt7gWIWaMoYIQWIioL5xejMruVBQiwTqKAUVtTKHBYqDPPQtMd69QBPQKOtPpc7DQOiJ3njoSd7MibLwczLaChhaPmObg4a72B
lZ+PhrMWxlhgwfrW0fYHjNraA3AWUMU6i+KIcAZxL/fA2WmCsw+oqq+kNdxs10ONuHtOEVx+MWIv2J15BthZWtN7DaGkDWHzhc/R
oeQcjR/sYxB95BQJFeTQuMpEFQyG/ECNDh6ch+MBHqoBYB0HbJcRxroevSHqsC4cRmXnqSNMTYFUllcXD6mwfQ+ol6SzI/ovxLBz
eHVZ76P44NDkLujz9OUpZYY6tvuU8n4SFHCOaoUOFWdTfk6X9l6tkHk83YmuHyRiICBDZQhwhkoReUlUSkA2VIahvVKv9nKpTCsi
zYtuIjWYz5zuRbT4i/+uFr/uIZdLQqYsbPqeJrerU74UPOURwlDkQvX7ZRHNCk9wjJRDsLPLcv2Y/qtzVMLy4OC1rhzVifn6oZ1a
NpRuuybpHJcJYxpBSvr65Cilb2erYSC1gZ1Iu5ODVuEIj3kdu9kJGhxIpoewbj8I1oxrgvOdKJJBwtevUv0KY8LQhy9ro5REliye
n1PLzhUjCyy/zCG2hIQMqOgJy0blOODjaG0riysLCB8hxWER3e4PHiE7TBrmCNPgGLIstiqQMsWCFAhGswZmHIP10sJbIyz9XFJp
5sQ0B6F5MLGrF8WCowkX6eQC86knpwx3H4/z4xiX4wdoPAHPwR65vTmkmQDdCTYgDhXIgIyALtzBvCiok+J+RURfGQaFvszTpKBI
Qk0h/KW50ymr0902CjPcMlUMIzDEHbayClsZX8iAFLbrKCc+z3ajTCeJOwdjVI4ek9htJgb+L3vBfYSSaTrNDNlKzXNJqrAvk3rO
jb8EzNy00L/PlKvmeuRtbkpO9sqHyETWXCqRc+CsLaxMmufiGfqaFy5Uu73nL1z4hBp5R93WGIHqihN0iAwx0bgXIwRdfNSQfEVE
gMwh01VMhYHKRw3bC5qhB6utIh3Cdn5dKu1+SSjG7lTvcJM+szXeLt9Snq89FqkMmWzRJnF2pA1pbtqO9BU8dk5Zl/tiac6lYFpL
3491soPVw1kDCuVBewX7UAi8WElZ+Ey6SXMnDAC11aU1jivWPJc30QhbLU/ZTuDakVTRDuNA5r4kkaEEc6QGENwtMGTdiYgr3cF8
ah3ZrCDOvGQC5SUWLWvNYsoxYRFaFhav3brOp4EGo0qSrdGatz5KL80kLxuJeuu7aBnNjDMRCCdo5UGwqZCcgr/GqLOMR3lGpFP0
HTUKdFmYMN6m2qhxxZg1zuTHjFc0UkHQQylS/dZI77/RN8bOXAJZCUYZSdcWozjuqIzoBFbw6yGUT/gEuJ9jQOOb8v69Bb4u1wxC
LpT9wwjfTm8Vk2vxAIGeviJQjuAwu0QDA0tPn0BDNT5iHIHmMJMucclAl8EaISBm5pnVMuD3cQVZdIIswFcBhAmn1AQNy1HXLh1x
S8ZuRYzQf9Raf1Bj9HrwjZGi128IvY4RTE2KrSkAHJn+7rEuelHzK9023JMMRi9a4Q6tpE4RgMFeVtlNPZHaz60ADiBdbVGwXcf3
7eTlTPzOoOvX74Ud310M8BaEPQsvigAF1lWY2Ol0Wb6lkq3qy24xjdd9Mn9Yf53fAsH6x7Mn4iHcnpc+gQFfncNtjR+8Xi3+1Avc
tSZHEhyF6ORv+j4qeR1lLaEb8Zh1AwWjxQ8wejJDnP7XGOrkIPBoD2N/WI860vo0Qxxcv6wVFLhFs5suOX4sqyOZm472xgWI5PlS
z+i2Fvg7a4GkfaX7XQsI13Wa782nDNBBjB4zooOarmDQcK0ddRvAwm0gXN+w19PWQWFlIyb0QrUgtQaNXMcSfNESiS3rgFcqdOxn
KL/HrPcYWsoELmP0eYM+I8Zr9JkyqlR7gwKgV/OjxnED8GJqgMn3hsKf9CbYoqtcNwZjIrT3JN7okcyvHnD6O73/IOTUd3Nc163v
Q0+w1nknuEGA78tFgLVlo/MnGJvPEjVrKD46oDSA4VoO7p+6sd4IoemUUdIbLPYi6B9wwdoQg8BpJKhJId4Tvgyc1iCFDeuhQ0kc
iHBs/6GFJB4qMqL8ThgEjwYxSOhHKEdutzvURZQSkC5rS353kcRDCBALiP/qLMFVxpP4rUG0GIwBukihgwVOjN3Ocmd3UHyBYiPL
kz3N+6rF/rQZq8RJ9XJQU2Wt/xkjJpITb4xMcYwMD+b3usF5pv2um9Z3UNQz6/FTEzrwPRSh4M8w4nhyD6VPqTxdPl0u7X//U/y6
9clAFuRkf0Y7vaTqjIyR4q70vIMm7XvzjJcvXbLxUwAEGH/d57b4fP6sVnZJ5QtjcIjXB/2czGac/O0AnOyKXk6Y9MVDM3E2YcJO
QiqdGrARpdu9+d+/H42h84dmCJDVwGtOaSevHPkXLXhvqX8YYu99FZeJ7R9H43Lm0Fx+/CJckqL/1ZPumU4v4jbm2rY++ieyw9yS
jiuj5RDRtYaJUnrkW3Mo2ElO6KtA8gOYG9Jvyyjm462H924+hX8YsU+ari81x+pj6WQ+mOSOshEXOYxB0UaBJKcVoYgPARQc/nys
X4Z9ciYNzov5kdwIh+f4jBuV/PTZ6benh+nzGUMJff4D+Mm1bQ==""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

