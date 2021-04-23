"""
    PackageTaggerAMBA
    
    (C)2012-2013 SunGard Front Arena
    
    Handles the AMBA file export
    
    20120514 Richard Ludwig


    Extension Manager extension type FAMBADefinition it is possible to have AMBA settings per Object type.
    
    An example for FInstrument:
    
    [PackageTagger]FInstrument:Configurator =
      add_fields={{instrument,strike_price},{instrument,free_text}}
      add_referring={leg,insaddr}
      add_ref_fields={{trade,insaddr,instrument,instype}}
      nice_enum_names=1
      remove_fields={{instrument,free_text}}
      remove_ref_fields={{instrument,settle_calnbr,calendar,calid}}
      show_all_fields=0
      show_protection=1
      show_seqnbr=0
      use_regional_settings=0
      utc_timestamps=1
    
"""
import base64, zlib, imp, marshal
if imp.get_magic().encode('hex') != '03f30d0a': raise ImportError('This module needs Python version 2.7')
__pyc = marshal.loads(zlib.decompress(base64.b64decode('eJy1WF9v2zYQ73Nf9wVYBAWlwhPa1w4eYDtSFsyOg9jpWhRFwci0o07/JlKrA+ST7dPtjqQkUpETp9j4Ipm6//c73tHin59evEiysqgkYXFGXpr36KrOV3GVlPLs+rzdvWTxn2zHJ4vpZJukfJZylvOq/TyrOJN8efONx3KeCNlJK9K0+H7KS55veC6uZZKK9uOqLnm1gjeU9HLDtyTc44dZkWVFrqVNxMfFfDb1eJL478lLAitWn4ubb2RMYDsI9xJEJw2H52syccvT1JBcsoplHPR4VG1TQ7NV5gGRkBWqCBY8r1t5nh9MpEeodoL6PhmPCV1XNaea/aG5nhI/6mwcdTr0i/+Uq1FVZJOyREue5XUwq6uK5/L5UTjCjcbqHZeIgVO+TfJEYoxaEmDrbM0l30tQC8gKzrgEelanoELtN7YB2TbZXYBNQGl4kLpLAI1amwUdQSa0efg6U8x1xWRRUT/4wNKa64TRyDURFaCrSmfJqsPKXD5q+Q9Kg1nKhPD8kWW2cSTZolzjPK6Ky7rKlTK1x1PBrc88K+XdpbIEA9TT24THpgxQnUdD/Nn6YmlqJeo0/VElkq+LCErVSZAYbYsqYxLiGaM3IyzmHERj5pTMHc9tqxZcCKj7Mw7VjpFubJNst+ObDL62AhXCbeFeFx0sr1ZVAGeB+J7IW48G+wxQ+N7yh2U3LNNKxYAhdmxs0mB9V0J8FuFqNTkLV9QiA6OcPJIkd34LKzG4TsiKw8Hl5sQl0SB6ohZcFohrV3/CAwkNZO1s4gJ246zSkQcm+Pwx8SYOGAXg6kSoelh/ugxpj8EiueJZ8Tf/nd+tZJXkuyfpJ/KybqSO6PnFKrxaf30t6GvLiL5TTq4mm02Tzk6szSGru15SilqWdXOgRLNbiGQMgVyqbYQ52M5Z1oHMZR+AaxCpN8On5Y8cO20MJTlL075RAGxj16sxuShy3vveGQ5nRyFa8OrToFn/n9fPRT6uI9CP6wcqANfxVaDc/5FKwPXsanC1HVcRPZ4fqQpcR0PTKZU2xf8ZMA9NJQ8nmlLPgkSLbgacccQA1vArScEFNQRqAgJVlaZamDB7zaAAhuaF7GRbdiLkrz9CRz9NWFrsoJsExv1psT/PdbAQcsY+elGQyDYcgJzCg29e2Zkz/VLnAetGUyHIx+7sG1hl1tB4FPFO1HCDzIJ4bwK5l/69etzDAEeiZh96G+7D434CM1hL/wZ339zfN2YV3dgMa0w+45CHtYtPu2QxXLdMAEYqPDhHVE0kerz5gpULaC3JLWcb6MZCQdcIF8ZhEOBZyWD5hsDJYW355Ffy1rfSAPwml5+/uD3VWNfx9kGYx2m9QZgMXQKCSOGk2ZTC08Nyix7/AaSNwCEsayMDVqI0T8+rA7YO4exJ/hMrP2P7zhLgw/juGRG+E7mObTAEyG8uVhb/0MDoQgTk9S9cwaRNg9cRN7XZi6sSe2JkEEbyJOak6SEdUpo6f3iGOHUTNHWmpk3D1PkBghBinVHqFvXuPRiA8LPwbL5/fvtlRDWoLZVxKvRR3lE1A/mjgwOoB9bgOk/+qjlKnYC25KaGJuIPIAka022xwRvCISa8MywUFbyrqbyH1F7qHpF8rFS+j3kpezJbeVQ3KehW1IoEfJ4xdfODJj0QYTWSaxm+pQrC1XIOto4n5dJlsrEP3LoNIvAYbidnLfAG02ticeLR10K1U+8g0ahT5ftBxcuUxXAnINCOvzoXgsPo7Q1SCr2HjRo7Fv/8zvl6XLkcFN6V6RLODCUCehe4J9S/JSZXA01yWhXfBYcJQsk3zdFtdA7w7dQ317QDxvqDVzcbHfa90zqG1Pi6VoOO6eHQKKNm3Bk9qtIqg4eFdbS+xfTZ6lT0lxfzT2S9JFfhYvkhJKvlIiSXV8vpPFysYFxYLogaCKLzefgLWf22vJ6fkmkIvz+Gp2Q+WYdXrsDh/9GCGJ/N5qMpCNbqDxT/X4RP9xU=')))
del base64, zlib, imp, marshal
exec(__pyc)
del __pyc
