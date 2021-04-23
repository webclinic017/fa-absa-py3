"""------------------------------------------------------------------------
MODULE
    FFpMLLogger -
DESCRIPTION:
    This file is used for logging all messages within the component
VERSION: 1.0.30
RESTRICTIONS/ LIMITATIONS:
    1. Any modifications to the scripts/ encrypted modules/ clear text code within the core is not supported. 
    2. This module is not customizable
    3. The component may not work as expected with any modifications done to this module at user end 
--------------------------------------------------------------------------"""
import base64, zlib, imp, marshal
if imp.get_magic() == '\x03\xf3\r\n':
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
eNqtWF9z28YRP5AURVKUKFGWZcd/CjdVy8a1FNtNpvV4NKVJUOGYfxSAsmp1OhiIOEmQQIAGjo6VkV7iTB/6BfrQL9CHPuQlT3nr
l+gH6Qdod/cICqREZzoRKBzu9rd3t7d7u7enLhs+SXj/AG/4AxQ2Y3tQKsxOMFdhPYXtKUzBdpK5CbaXYHaK7SWZPcP2UsxOs70Z
Zs+yvTQyWBnGs2wvx07vUnOODTvm2V6e8XmEdr1ZpiiKp7A/2hn2LUy3wOwsVQrMzlFlkdnQNc++hdmXqD5P9SLVF6i+TPUC1W/g
JEZpERfxIMHYo2t6cs12daeh5VR4arV+s9HwDw95oD7KVTWjote3O/V26xnBnSMnVA8cl6vwHYTcVg/8QHWB3/EOVct11R4PQ+uQ
h+pXjjhyPFUccbXr9/q+xz2Re6XpBg6mrulrOV0zOnq9gqMbG2qj3qx3ytSQcz1eV8veqdrzbefA6VrC8b1QFT6NGHYDpy/CDZV7
3eC0L0AQ4Bu4HEhdl1uBKvg7ARPbfFyQgCT3fKGGg37fD6DnukrTPVmXq5PjRFzdQSj8nvO1te9yYnuKbLElqT3rlDi/8oMT1QpV
/q7PuygQzqtal1ZgQze5jIvJLIHKDGA1tpp7dG2P8194SgrsFzELRU3atRV+Dg1cxFqodi0Phd/nasC7/qHnfA2S75+q5aqxrlb5
gTVwBZpWEPt6uPHhrlf2eYpzl+sNrfpMrbdelRv1qvp8LdxUn0P5eHPzUicgP9lcDw3oB/MI61DtOWGI6EHg91Rjt9nYwH26rn4B
9kdjeKFj8wA5bDmU2rcCq8cFD2AnHvEAhXwzcAIQsQuuw/BdgreCzvRP1BB87zChsOMEuvOZwt4zxWLMk9CfEZJ0CBlnDF1RJDFK
CIoSgqIE1mepzGCIec8yoxGO09DEjidJFvyDKLP/11Czo6GMUhYEbgEfUHCRM1Bx+VvuEumE8z7ZG9yyDeoReVnv+BXQk+9ykYsI
24ED3W9FzRo4dlkYsH9hv3J72xJHNBA4PCqylEE9pSU3bCQdw6pAWb6wQrm3SJSa5YacROkEA1lpwaYnrEFiokQ6dzxHOJYL+6aE
5hALULzlwb4fOuJUMuZGk7VgoSWckIoQeWOxar1/SoIcciEJ95DpJrIm0sqKklbuK3mlCL879O3iaYArSUV74F9QnJHp0UDfYf2Y
oYHeU2xH4t+JqAyJ52Sy8xR7J9gZ2A5MmUT6CWPB39CO5zNIB56TFAvE0KZAAZ5VMO0q4GBP2FDHKXY2g70BvP0+wc4V6pgBlhR7
83u2++a7IRucICCCZPFoN8FRsgrY6jltTaM0RzuDDIN+/4xCgEMqw6Wi24VJWSGGTQfLMEGuRp9nagkNRWY7cDybzBb2XUeIJO0z
j76hCGhvBLzvWl1eQmWSuUJ/EHQ5biXCh+cBjUI+KeaimikGfeBCARyiwphmNN4HTY1HYDfgluBAa8oZHiLvR9gDLLyiFBRp97yy
qtxUlhIriQWFPB8FKUZW30hJ50QHY+eJyMAKWf237CTNgvsKEikhGKIziIIRIiAdAbMTQCYCshNALgLmJoB8BMxPAAsRUJgAFiNg
aQIoRsDyBHAjAlZ+VFyvqIxp5DPSyKeJSY3cmqaR29Om+GiaRu5M08jdaRq5N00j96dp5GfTNKL+qLgei0hpJIV6YrRk+0HEYf8c
owO4SdBPDrnJ7cGd0bE/ZicJFnyTsH+BFI98DZ17LRo6Q8r+ZdTMUfNXUTNPzRIN9euIWCTiJ1HzBjUfRs0Fav4mai7SauBwmqEQ
8ojkuZ0EH4VT6oxMrbx5mEJsnbDPCJudwDYI+5KwzAT2KWEPU4hlY5j3A0aJuArjawb9gUz2YxbX2vEcOicO933SfoKaHYY+Kfe/
af48ncxPZQyGvLvDLqT/D3HMR1J4v2MX0hdIwoURdpdNSl8YYXRtMEqfU4idh1LmzabR3tErGlHKzd16lVtuxzqBw3ApRqnTYScg
4yxgT80wyluaCfnwi7ahiRWMcZjXmJMIcst6vfPabGivtEaMexLBKNpob21putkqNzWSQHLGqRgla612p157bdKnXqHEGyav1suU
D8hOV4A3JvtGU0/pJcHlWK8dA+TQmpAQGjH5iECYMcZtNDvbJlBhpaI4wT0k34yxR+p7obdfAvRg2lLGuOYnpDNiM42R8ZAr41Hk
kOQVvGlA0lmDvLIaOK4rLYMM5pUWJmTSZksjJG6jWyPqNAtdBifHi+u0OEEd6u7BtGnGFFQc5xqqw8HjlHILOul3y3qr3tqixAHr
Ol08sCtcE0YXILPHbfCDfEQ+NWXmOj/M9ECdQ8rCRfZg7gc+OhQOjRcl2udYMXnPctxQZg890TeB9nbIqIE6qVKNKrtYSUoXoYSk
qr3Y2aIMSGBuy991Tcc78CkdDS/5c3ilP0vmi50RXrkz6NYudypyQSZ+4BxuYxakcwuuLrRaSJNMyozeWi4kzkgKx0ko034rpk5i
qpXHSJmRyocJuabrbfjDpLsSpXb1Vq2to3FkfifgPq2/RI4GFk0sWpiCzUTKORh43Qrc8EmBvfCQ9lmX1mFeXLbIRfY7AaRwlJCD
SaU5P5zQYeJ4kco9J4lkKpdYUW5f+t2dQi0oy5DupyH5yytZ5RZ8C9TCXxFoi7F3OVGg60AW6jdjdB2jD90PkvH7wcfyjnhGGTsm
4UlMwkeXQjz56XTA3dAiJVJVRwfTTWzicPodLP6Exb1IH9OUQoOcR5k7U4qJnypV6zqkwkG+iUml/FSpXl6HVDjIX65TquZ1SIWD
/DUuVWklipamaftd06Q7tP4lUhGC8GrqWqW91aobWtV88dosVw3y8XGESMP/pZjyfyvkQ53ylll+YWitjo6hQkcX1DE46h0sXmGx
gwXdwItjy5Oej+aVgaA5tryproux4bn8P9YmheFP8GqNrkSuCD/6JukuloNvKpFdyC5ly/mZfCqf+h+2SXLg""")))
else:
    __pyc = marshal.loads(zlib.decompress(base64.b64decode("""
The system cannot find the path specified.""")))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
