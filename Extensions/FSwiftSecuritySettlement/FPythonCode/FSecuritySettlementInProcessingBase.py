"""----------------------------------------------------------------------------
MODULE:
    FSecuritySettlementInProcessingBase

DESCRIPTION:
    Base class for logic to be executed in each state. User can override/extend
    the default behavior in the FSecuritySettlementInProcessing class
    derived from this class.

FUNCTIONS:
    process_state_ready():
        Pairing is performed in this state and either the 'Identified'/
        'NotIdentified'/'SecurityTransfer' event is triggered.

    process_state_paired():
        Matching/Partial matching is performed in this state and either the
        'Match'/'NoMatch'/'PartialMatch' event is triggered.

    process_state_partialmatch():
        Partial settlement is handled in this state and the 'Identified' event
        is triggered.

VERSION: 3.0.0-0.5.3344

RESTRICTIONS/LIMITATIONS:
	1. Any modifications to the script/encrypted module/clear text code within the core is not supported.
	2. This module is not customizable.
	3. The component may not work as expected with any modifications done to this module at user end.
----------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNrNPFlw3OZ5wN67PMVLlCjJkGNGtGNJjh2rsaOqoXjEdCSKBWnL1cTdAQEsBWoJrAAsrfWQyUyVo+nh9HCTeKaZNE6bXjNpHpK6
M2nca9JJm7w0T33pS6fTmT4kPdKHTiat+x3/j4O7q2MpRxFFEPjPD///3d/3w1TEvyz8vh9+g2/BxVKUK3BVFSuj1FVlDe+ySj2j
XMkodkbZzChWTrHyyk0oySqiNqdcycn7vHIlL+8LypWCvC8qV4ryvqRcKcn7snKlLO8rypWKYhUUu0+pQUlR+aii3FSUn7vSr1gl
WVqOSgcUqyJL+6LSQRxqdaYf3+jDOUU5eQ//VS5emn/uwsLTFQ3+La7aZtN3wtaqHYZ1e8t2wyV3xfdMOwgcd+O8EdiVyvzC6py+
tLK2dGmZe2GxZtaNINBqnq/VvQ3H1EJPW7c1+wYMGNqW5riabZhXtSA0QvuU9lxg+5ppuJq3bfu+Y9mn7Ruh7Vo0XnjV1iy7ZjTr
IYxx1dh2YFQYAMtvAyGDQaNYtu9sw8w139uCrk7AdacqlcXnlucQ+lUGv8G9qwRa1bcNqzXzMFfhvxXD8XFkGKBh+/CCW/w6NCT1
0QzX0mwHwPMJxhNLFoDl1BzbOnE6GufEshcmK07IN1nzDTeo2f4Jzd6Gapwo9J2NDdu3LYC2HcQGQGRbSRgvGqF5FYA8vWL4oWPU
tS1RcOdQx3DSYADfsifvxKj8eOdQUieCJL2eDGIQbSCOdRWgqXcEce+K8vzRcHvgeH5BX0XE1Kb16UpFX1hd05d4s09fWLq4tDYr
Nr787lParNvStjwLhjWN0PHcAJEWpwtM32mEp23X9FsNxF5o1azbp826bcBiAapqpmfZ2kuwegIvTc+3ERbXC7Wg2Wh4fojwlB8/
pa3h+/AIsoXZDEJvy3nZWK/b0OgJbIRjbDU8Fxdky2hRu5c8/5pmBEBGDdtEQHBGWJW9cFvQjYGPpzJCrYlUBlR1qnIvOYbzFvyb
UYEZhXh5ZDnsgz+AzUCS9TnPrYUPwnNHQgUScGqtKjZyNsJ3dGuW5jim5Oo423nkgU/CxQauriJvByYJjBzYLd5kkcnjTQ5ZJt7k
kbvjTUHRV2fy0NPMwEX+zuF4CO+OquwoSpVeCkQC3G8C9+XCLM6zSq+8PJPDFx+Gy3oTIER8F3gfDtD7vOTUwosXngudehAewemA
owA5AJI4ftVb34SNrCJPqq43/LCAg2FNMIPQhDh4YNdrIUowaDCD702X4J13tlqnGq2wBE2rVcd1wmr1Yeybo+Urqya+Aq5BSb76
azBt61ImhNdVcRHhjVV8d5CLWRQ+/t8qoi5DdeIhSwuUUzbz2EjcF/A+VVKkkhJdy3dcXsEtg8m4qpZXJmjmPmWzXzSEegHkgHIz
q6ggvVdFwSBBfVwCWmCoh5TNYdEFnndV3G7/4ypcNw/I+TPi/loWq8IRZTejXP+46tpKOKpsjiW6ZxUccFyU7GRRdYjHzMqRJ3A0
EPliQGh8EIU+VtEi0WsB6NDVJQT0/5ggPSTeklEyfkv303Ivym/z8ldus/yVNGACqj5a68vunJILDyvXKor/akbdzSny1fuVcErZ
oa2dkLh0JC6zQPmB3VNV1VWVF3BLZ4YQRSfhImWLBjQhZAMJ6uAQVCbE//kVHarthqZT7UmoXXKBr2LdFrQxNrBjw7cDIJ1Ak+QE
IoRlcHAVeQwMMm1pC6CR+C5IKiZaLHpaW2NZg+OxHNwrxTXP1VYJwOngFPxqJ0/O7G3z8MmT56CKuMjeuuXgp28D9MINE6QllEEX
C2SCbjc8jViqv0XygLjIyqy+FrzYaSgQEV5NC1sNW2u0y2IUuVCMHcR717wmlMHbC+ElO9MM63e7XiktqNNipRrIlULWmqoIUHjM
gcCs2ygXG11R4HFot+D7oEF6Jqy0j0L0qgPysWuXp3FCZJD2DROYaM1zkGvOHEX+jMWuRyD4tMxLy4uX9CJWjeBTsHc7dRIXyM0v
OVaIDVebtDwkNOcQIDdchblDZMu0FjTusrFlU5M1w9+wQ6rQsQkthdB4qrSkYQWpBMVO1TKg3QMEiMQSQhJEkRSGoCmxeHENdVvS
6sLjUADzkG4JSxIJKs8HjbjhVU3oHZC4mt0CfAgJyDW/aYcTPNST73lB0OFi0zVJLSHAnEBqgrRC7XOE44it3CQWa2uAYbQkC7p+
SeclASWHhrS8at1xr8EQYRlb3DBh+fCtcJmD0Kd+8wvnn/sAyXsdNy0cJMkqh8e5ifxClM5VIwayTDALeEjBsXsTwqPQtINpgSwp
OIODZbLqQGZIHVB/Rn2feiSTU/F+RD2u9mdG8uOZY+pBtZwpqA9kqD57AOoPsgTPCClOEtyHS2tG6SDBgXurKeHNrDlLrHlLUXcF
DyZdCRZtR02x5kJcJgxkyZoLwJoRlYn7dmDNbKAEh7vw5hWufui2FCwaPnE3JMx9kIZ13HKHlTaEVkdpotOm450wiyQ26ri1OnIV
/QRecL9JJyP00R+VKHDXeDDWhge8PJdxnEFGhMqAWlETG5xNbvBv4wbr6Q0OST9jacwKDewV7BiWFNPqQ5Ekfa4jKpQJFT4DqJDh
+gqhQp+yk0mhQn9c1g0VTnZBha42YaB1RY/Y2gweuQMkSTR/6u5QJe65F2EGUgjDnPeg4F+GubVXkSc2ryPnDZEm2JqVr1uN+Q6J
Ch2bdMS3bIRvD+8P6Q53QLp46TdxtGHJg4DnPJhEvnIS+ZaghBEnqT0DD9lkFTxPJRlxzzroblY+kkLp/SLKTcA1YN6o+/Zh4U3C
Y1HIjRPlk3FdVhRdyym7kdbfT4rqAF1J4d8cIl1bRV17N4+oGryJaqX/T8pOHq8I8bCYSbwJoLx7VQkPoNq/OSKhGCV9WCWVHuip
IDX/vChUQV6BZi+KClj0IWhaVHZLNMnB1CQ7QIxMfUB3q7S/wSmklBXmPprgPuzpYKnOzhsNcNj1+J7EdRJbl2cmJVbqj+ElQj8d
qYoVEmQ8LPi3YPPtNa9ug1Ji2vphqZIY6wGpJPO26WwZdUZE1HN07Muz+va24zUDVFF0lNQ6yvsUfrVjOUlp0AkWDTP0/BbJ3jky
gy+uXWKhj0hGpvI8qiw48Ky12QzCRceuW8GaBFqfwtn6WOhLpxY1lyoQFVZdj/1M5RQBhVOsgDhCBa4KFTilkbB6s9WohnKBwmnu
Fik+Um2qGqT7wGxh1b7ehAGOs5lOJWIOYglyTXj7cHe8ph/Qi+BUQdMkj0FFPINq36yHPZG6jujUxD4TRNAj+REg5RfUE0DWh0CJ
GFWnVOLQwivggmJZrdLM1Sq7iqpVHR91ZOH6abyg0kwDxyDdNVxZ0SnAsQtqOVd+pDxa7guf6jwEarjNIB5m1tp2TLurLygjfUF/
ene+oFFyB6nkuc9TYQmdBHhTFu55dNiX6KZPuObRWV+hmwHhlkeXfD/dDKHdijfDaL3izQHFGqKbEcUaphuY9ADdjCnWCN2MozNq
LOmMykqO+797nFF4k0lw3MgrRRxJWP1FYcVXKQiBN2XZt0Kymzoy37xJSgDwU/+VVDks0iHmqbBE1zKiswukMIhrBat0Bv8U+U8J
/pRxWc7AisBanGHznf4MwZ9hfOcz8Lqw5PRnDP6MK9YE/DmoWJPw55BiHYY/U4p1RDmDsw2ynw050HKoSGHs/N9bb73FtgBKdiKi
WfOa671Ut60NW1i7cx+kmzl5s7KizxFzE25sNiEuzq7RSHHRxdm5Z6jdiu1ayFyo88LyvBhueYVqFw2nnqhdJFNIt4mXEfNdeHaN
buaxK1bOISupy1HmSeec3XItLNeBe9gB97yIgCYrk4BcvLSyTHaKrJS6kKidnyMfCVuZeYKzDnwYNRXTqNeraR2gVjc2WGgUIilR
kWbn3FXgWQQ5PTJzQt4W8CMycZPtVSoCZn2A7C0c2aiFaI7S/iAm16EVqlDPO4EDihuPyKJjTHRqBsBx2YKtWo4ZJpTtcs9MB2H+
JSlk0eNZVsfhB/9OqdOg7RS7/rQr3q8qpFKAvtM6JylFJXIj24odpLuqULfBqGPJ78/RDRGmCuRz2V0CVbtIqvanhKpdQu8aUCFQ
MCo5pFfVMkLhLqEuFBUDWZI7VCjcSCB5IhBGbl7a03ej904HaW2XAousQpDOEIl53cKLI70bUuS69o2QN46V2KFbabKEBkm8sfeh
1iJkIGa3QBQ7SAfYjiTz70UarVpQs7DXI6TRHlWJvyJS5+SufkFRUpupigfa013p+Rebm8VNiBiv8PSSaQWIcTBSeg+izplwrOLO
UkAZ/cBYURYM9iwOV4mHQ89nNgKBNGCVtpi4VYC7U8H1V/RnUxtFpLfo+SaodbTv7Dkix4dj+C1W4HD9P2CHC24IJZHlQa2WPaRp
bDALKx3YPittoGSi48n2uW6lyZ2ZocHCO+FMIdpZvNS9jSoGxEihQ25h4fSkOsabLrxbNg3Vxy40O6jSc2+IwJzH821AxpekWvcV
LBwhJEDHypA6nhlTJ9Rh+I2IO4r5PLkHDdh/D7v6AAvcHcKBzVzC7skgMqwSn1p2foRBsHwbG20Gc55l6+hG1utSzwYhlSCIvpgB
YhSR2DuzQeCHgsZ6J4+YOBPDvYkDlWhl0Mk03oEs3qmS2gHId62k+FP02nJh3ChAQlSBPgcZaYBFAeTYpDyIHcHAkm2RgrKKf4AI
ISuCDtcKiv/XaOBtykCC8FVQjAEIAkkMOOqgyiwSBkbmuMtW1QDRFjLKAlp/4uH6oHqdZhFv8C8ySDWU6O4OU+goOWJqkNTw8Nbi
1fLRqxFtFog2J7q4L6YD8jmDsEZnufSIsPP7xHRwghMSBHEILwmVBx8gl6rhgsgElka5FBSNJly5dd+9kWcWCLefU/TbNuqORQ6Z
W/tapoMZcoeg606/2U1qxH42RPXncWwCJWDdY1ISDftBPizjnpdn9WUinJjF6L+AFw9blJPaCOlLAsll8F9v9aw1wE4r35R9lEy/
OpSZUg8ACymAHDkG12EgmlEoz6qj2eHMgDqciRhKFEl9L5S0vt/dTRfmE2HCZxWsivx1UodA8sBA3xfjoKtw4UVhuiISTSpwVxSC
I+kVuaNySivCQN9AKtAXxUqLiThvKRnoyyVciAdIr3lCjVyII0gv4eheF+JYXAaWBFgRkUZTApIq7zPQ9+MJQ+moy7zNkaekE3I8
7YREb4Z+PKKeY3iZjoiQiAmlnz7agSYPRv6iybfb+Uh+hH/GPlrkYhynQAaqZsfUSfh5h3ok0y2g8QL6uwelratIRFMJ0VZF2III
C6gszKXCFhkUS1EZkA9huEC0nFCdu4Ut7l24gRiYGy300NsTWiBfzf9IFwsu9GCXJf0VXNLznWJEwYNC0/Fncd2E47KQ4DyCJaEd
E4cMPhFHj6KQgdohZNApehSL0G40zXYkW9jboJre3Zaw4b3HxNnjz48MmwRN5NJy6e2KB7XHBel1MbuJw0Eq++TfEe+l/J2TIaOY
NhKJSXjVGwiSKsG8V8EDI3a3WGUENEOA3g/gJtuAAwWG3Ky21X9/QRtvA03ANXR/4XqgPRjELqbYYz/ykwZhjf1tMYTj9xfCiQ7R
/E3KyZy8v4A92E6s0NQyiQn67Ge0ran7C6R2KyAFMh77CV5HU6p7x+8vkAfbgGT4gDM/9JMGmXiyrRMxZMszpIwu4gWtXY47NaQZ
yCblQ5HyFAekPokXdOzqv4wX1Gf0X8XLK3j5FF5+DS+/jpffwMtv4uXV/YWwnoGmn5R9Cmp5qtxXHiwX+4+WJ8qlcrmcbf8JUXde
nKs7IqRFY1+qPePVEcdvn9r8lWQ46w7zmkUgqygDWSUZyCrLQFZFBrL6ZCCrXwayBmQga1AGsoZkIGtYBrIOyEDWiAxkjcpA1hgG
slClCXBTE6dAEprZul333A28Cz3NhDXZ8PyW1m2NAq09QXvxtgnaDoe/cjL8lZclBXlT5OASe+8IHUqR1rcnJkJZ2Zg3x4mHpJ9V
TQz9gjJaiUowakGP1PbeBjFOItH0iyAGBzAS6duRYq+i0+ENpWv6dhSd2InrEolCsqio9PsfkeGLjyCuoV+PghQ7pOLvZKQHsE+m
feTQt+c+gvh4h407eA/6yZr4kRKlCQ+Q92Bwb5rwUFx2770H5K2mPElOUrAoRhUXOJ6L4b+mb/8Ybf/htMFSlF6yJehLGro8V0B4
ylkHlh0CnIH+mkTiZsPCgMtnOxg6XW2cOGWSUyEdt1p3gpBdcZ/Yv2fgSTXlGUB/9Cj8FOBuMoPX8WQykppkA+jxSPvXkiltdEaO
DlAcuWUuGpj4R7ulnkUtTtw+70y2XWaij/Zqn6KUhBamXfGpjczAPhaii6MDletb5GcucvXt8zO54T1+/w4JkwzvcmpNsiJ4EQUw
/hyjtXnkMxb5WDHI8ICI6RxCVkUBN/+zUn5klUO+R+G9bKKIFpP8IMIDUkgdl4AmMkx7/c/IYVImJ2m2Q1vZ0NVkw1yHVhwxyQif
COEdGD3k+DfM603Ht/HsoziYhiJGc2qcks/RO9GGTg3IB/RnYnPiDSSN5/DAmeUYrnZ2OjgHEpkOBBiNBuwsjI2FlEgsohZQQwN0
HtAIUkc0cRgcDvZs28EDCTRFh1ktz+Zwg30DGAoe9ZudXw1+fp/TihBGNHv7xMszFalXctqbuUXccRFT6lr6FyLsnYk4bZmS88Ug
7EEl1M5FzBFlhgCFFYF+UgSsedv0fCP0fNoeuYW9UcIgJWkFlHLK46yqgr0pwCr7gXUW4HcMVAONnKt4Pcy0kU/Sxtc70MYbCdpA
wng1QQUcf/OvCfJgwXundPHVO6SL62/cli6QZiPSmEmQBka5al7d8brRBm7gimwUnEs+9UYdQTuadhnx3pJHdb/z3hV96K/LZI/F
lautwDGNejSb/ofthKL/bhRhGE4pDzpmZOhfkrQU7Rcp1NETplH3RhpDEWlEg9VUIRmZNipEG/ibpI6jd0gdHSTHZ9oJxO2JQN54
OwQHrp22KsiDEKKr3ChI7dYP3hfd9kYVjXbs7DTcvSWJD+1r0h7ogRLr8JMF+pd7I4HIoPRje9HvHfn7I+TnkV5OY/5AR8zvJBe+
i5hfuC3mf1lgvqUmUqAA/WsiLdVK5/+LbNQY4933UsNSAuPTbaPUNzkNGok8TYbsSqYvJAgeJ99hkJgg6EDKu9oIQiRSdKGKPkkK
nMYTvD/93Bt9vNYFVTuNeU+J5JT2jO2a0WiE+CGBtepsNeto5Z7jJHz5GBj7h7UH2kIdZ8Ftbi2CAbsa0kmsW9JXlKHaDDqSWn/k
j0kkqSYLqjbM1nvWWYLueLxXYntWEt8I/ErSOwpPwzH5FZOp3r8fmXGcVMrGnPCUcPIZJWjs5sTxrpDPdpVE9gefjBG5h5UoiSlH
+aMUgwVyOCTLBnCx5QOfl4Faccgl7l2g9I9oKCZjcXTlbJKmHDcI/SYfGg5h59abISAihhwwJC7xJZBHrOuewedO5VpfgAJ2xB2I
sGGATqMY9TmjETYRGShcym6ZZfulpWhKcjgvnhefYLiAn5yJNW9Escu+0RBnTUjnt+uUaGeRPYnOkoCR7USk8yMizUP1mrNlM2mE
YB9gCQ34nAuctt5CmJBVLCZgKVKepWv7jqmb0lFzwd7g0zULroWD8BnEkqxGxwpNCctIhzIITFzTfv6bNiQI7m2jLrKrN3o3rRmB
cdZ4176IODxGODxOKU9oVAxQ2tNAB7x9eW/uZFZJJdGSFxbREmTHTxHHR0TLK+7jJDYcmWnAaZUFpOmdnMTVHanmjGMP8vsCwkuE
VIULN5hKouL1JuAWIhkiHTGoZT4KFG3sz4oWtLGLhmk/b9SbNvMhOtw3KQ73xVjNaEL7hC1qgMBs5c15LkxihqvOyzYtqRz8Ui1G
kni7iS/p35LoLWFlqxHZXw3A2UZwuKiUaMRHqCOQ9mtGymG/Eu835skWhMKACdMDarv7/ak9+w3mLO6KmiokAT2gRJk56e2aSG6X
cKXjIamWFqyk5U6qUu7nKW3WpAqsrlskZdbthLT17TqsIdRTv1MzUTKH2LF4TBYvH0unc3ypZ2/VSLS4ScC/ocqEW1jgQxmxqKkE
5DNK+mQlO+xFnrFKzD8jFzEiFl5RdLAFjyVXNHIV4TlCwiXNMlpajU7TxVTBiUl/gZe/jOTrX8n8ZeF2mTf4CzJEIfCQSAwjTP7O
vhJLUv6MKoBbJXAB2m/GazbJjKdtzZ7qtmaYXylPo2JmvljDQmrZMvKQAC8brUgIzF4LkClo73786cceg/9MuZ0WCZuFnpAcLC9m
1xaqS6uXqIq0JZQee1aMKomB42z7tXcJbhzoO7heBVqvGcmm+5PBoe+pkmw541kcVaX0ata0+RQLa9eYC62Kj8owt2XOzLnd+FhE
VrpTpLS6MqVpl5SWJg6o1CvKVp+yW4a1LtOZVxWrL7tnoyjPm4q6W4HqkhL8AbLCzUFOC2O2wc/8uR4YHfpieAca+7bKadygliDv
sam6T0kWio/4lMiAOYBTtNcegj4oTvrkiCN4zyd4dzkgNtpWMtZWMp4quW6rIjl+Agvjc8P0xZudglhGfJxMPx5KPMIiH6bs+CkC
97Bkp1hxhHblKMa8rBKOLipYL8ORjuG0Z2FRVkm3Jrc+Yjgp/UJdj/UzwiT8XscTTy658ktcg6R2kS5/kVX5xEe+EKfqDnA2o15F
ORV8lc6PCDYTNGyTk2hR2V+MDpBo6fH2mALIppwwwM+m+XbQ8CgDJPL7Phq7uB5N2SDYjU39U9oHHdeqt4Dx40d3LM9sRoeBosz5
6LNpeNTaCMnDzVE5DsaZnovphTh1d8DBnkKxDOMafquXaRO8AT9qQqmPWFFfnqEPBqBzsnrHKQOd1DfSnfWvS3MqUpf52y/fwMo3
oxDgNjYrsraDQyT84kGo/2s6afVj7VZY+N4e4JXyiU7/3m3n2Hl4pofewu/yvl67CjOyl7eOtLizPXROqhPhfO9rnpKxPa1/JHFI
5PE3i8yW/jfSlEG01r+G+PHp6JBaSeq8+t/h5dt4+XuJaKFvsWBEhGwg4ZFtZkr2UK173rVmg5HxUWnf927yRC+RoJnvovR8Wmgb
aPQMwW8WTJ5hUojxlEcFygvqlHqETHr8maR2+HMIfkx5/iOSuF+LPMmhKrxX5Ekj9U1Y25iHLTUX4vA5vsvLO05ip0StLEpi9nHt
8AFRGPqy+1R0nvRzIFOL0JASPFg634waAuNBSZ8RJ0YoX0J8xi3LYoRkfy3yIePZAo25h/Rz0cdT6VYkF2hOdDCb2hOP0c5OW+c0
zkhgQbC0urTM7in6hAtzXWCl1CYWTOmmmAMhPr1ChpkZ+QUQPc7bG45L56MMYsf8NS1jGzkduWb4gGKiBR+HeGeU33BMDjW7Diwl
2TAOXpdS2Cu+tkXpPfz+hMBbwQafaMTXYq342/vLCu/fk9Hxg6RXqQCoWAHkrIifw4CAE1A6qIrkgIL4JST8k3YlWXwoKBPnSO2q
yo2PivL5F1vxJ1xE8o4wxxMaIx7I2xVnlifYuOegBKDoWXEgFka9fkqeHeIDstWibEnu37Acpx4dPAuNL8fHMoZi9AsEfjCelSSe
Vac5ekHoVGVfIjElUGieAZ4RhEcpvBSE1Thfobpu1/CkqEnokcjwR26lZ2AGSpjRP4OXz0pkSZxzZe+9VXXYSYzfMRbf/9ExLUPH
JCxCB4K5t/0f2JvRU8xEJvqxDJ5Ae4DQAOyizHB8fDPiPJg+2VqJ1X22I288Rl+ByAhdHwrnXzyS2FJW/9kCyCjq9Wnl8o4836le
dh8CPpMnPrMNfCbPJy75qKc4LEY6Ou2tMK8oC2vOqAOjMJOMxGg4GiU3pDlBx/wlZAPkvqHvt5BTBrOQtoOkc4ZcJTlSTYOQVh9U
1K1A/yHl3qkpLYZ8ya+lTxZ+Xn7RqcvYCeHVe77T56DpRCbxsaUh2MYxOqYjzuCWkpSLmppDZ2odcqrd+CPcyvkXXyeXWh5NtNaj
MgopjTb8vtGzJCeyIuwCVWfpvM5jsH852r9d2L8C7B9JE4vOpKMvuZD87gDtZV4JRonIc0DkxZhuD/LHRXa4KApJlpSJs9dHFfh/
eScrxQgyfO2iHV71hGsmbPous/ntIOk2pgBMMJvEig1htyRa0TePcZdEBARFEkU4uNPTHGl5D33qMt0pliztMRL8VOI6bFPMYZip
TFvJEAVpzP8QBSA6neaK2EZCdHw+YiUDqtSD/lGiEvF6ziBlT0KPWaIw8vFMIvDHPrwsqS8H4XqcGMYwfv9nPJV1TYKzWgXjJfXl
H8w7038HL9/Dy/fx8u94+Q+8/Bte/hMv/4WXH+Dlv/Hyw4iLEtV9jtK61X3lXf8WNH2XGuVdF9RyqTxWzsPPKPwdK4+XB+CnVC6W
C+Xj8DxU7uPPoOBBG3o7i79oxZkM9J0pTLK0/QseHgPlLXw9cvPko9OVT1F+pCq/5YboLDg9uXQwIZyg6/3lSFyd5Q8vnTsqWSbu
VD8pmP3yJzNhTLz+/4nOgh4=""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc

