
# Example of usage: 
# from CompositeAttributesLib import InstrumentDefinition
from CompositeAttributes import (
    OpenObject,
    MultiEnum,
    SearchList,
    SelectInstrumentsDialog,
    SelectInstrumentField,
    AmortisingDialog,
    BuySell,
    PaymentsDialog,
    OperationsPanel)


from CompositeAddInfoDefinition import (
    AddInfoDefinition)

from CompositeAverageForwardInstrumentDefinition import (
    AverageForwardInstrumentDefinition)
    
from CompositeCashFlowDefinition import (
    CashFlowDefinition)
    
from CompositeCashFlowInstrumentDefinition import (
    CashFlowInstrumentDefinition)

from CompositeCombinationInstrumentDefinition import (
    CombinationInstrumentDefinition)
    
from CompositeDerivativeInstrumentDefinition import (
    DerivativeInstrumentDefinition)

from CompositeFundInstrumentDefinition import (
    FundInstrumentDefinition)
    
from CompositeInstrumentDefinition import (
    InstrumentDefinition)

from CompositeInstrumentIDDefinition import (
    InstrumentIDDefinition)
    
from CompositeTradeIDDefinition import (
    TradeIDDefinition)

from CompositeInstrumentPropertiesDefinition import (
    InstrumentPropertiesDefinition)

from CompositeInstrumentRegulatoryInfoDefinition import (
    InstrumentRegulatoryInfoDefinition)

from CompositeLegDefinition import (
    LegDefinition)
    
from CompositeAutocallLegDefinition import (
    AutocallLegDefinition)
    
from CompositeOptionInstrumentDefinition import (
    OptionInstrumentDefinition)

from CompositePremiumTranslationDefinition import (
    PremiumTranslation)

from CompositeResetDefinition import (
    ResetDefinition)
    
from CompositeSecuritiesDefinition import (
    SecuritiesDefinition)
    
from CompositeTradeBODefinition import (
    TradeBODefinition)
    
from CompositeTradeDefinition import (
    TradeDefinition)
    
from CompositeNDFTradeDefinition import (
    NDFTradeDefinition)
    
from CompositeFxForwardTradeDefinition import (
    FxForwardTradeDefinition)  

from CompositeTradeRegulatoryInfoDefinition import (
    TradeRegulatoryInfoDefinition)

from CompositeExoticDefinition import (
    ExoticDefinition)
    
from CompositeExoticEventDefinition import (
    ExoticEvent)
import importlib

def Reload():
    import CompositeAttributes
    importlib.reload(CompositeAttributes)
    import CompositeAddInfoDefinition
    importlib.reload(CompositeAddInfoDefinition)
    import CompositeCashFlowDefinition
    importlib.reload(CompositeCashFlowDefinition)
    import CompositeExoticDefinition
    importlib.reload(CompositeExoticDefinition)
    import CompositeExoticEventDefinition
    importlib.reload(CompositeExoticEventDefinition)
    import CompositeInstrumentDefinition
    importlib.reload(CompositeInstrumentDefinition)
    import CompositeInstrumentIDDefinition
    importlib.reload(CompositeInstrumentIDDefinition)
    import CompositeTradeIDDefinition
    importlib.reload(CompositeTradeIDDefinition)
    import CompositeInstrumentPropertiesDefinition
    importlib.reload(CompositeInstrumentPropertiesDefinition)
    import CompositeLegDefinition
    importlib.reload(CompositeLegDefinition)
    import CompositeAutocallLegDefinition
    importlib.reload(CompositeAutocallLegDefinition)
    import CompositePremiumTranslationDefinition
    importlib.reload(CompositePremiumTranslationDefinition)
    import CompositeResetDefinition
    importlib.reload(CompositeResetDefinition)
    import CompositeSecuritiesDefinition
    importlib.reload(CompositeSecuritiesDefinition)
    import CompositeTradeBODefinition
    importlib.reload(CompositeTradeBODefinition)
    import CompositeTradeDefinition
    importlib.reload(CompositeTradeDefinition)
    import CompositeInstrumentRegulatoryInfoDefinition
    importlib.reload(CompositeInstrumentRegulatoryInfoDefinition)
    import CompositeTradeRegulatoryInfoDefinition
    importlib.reload(CompositeTradeRegulatoryInfoDefinition)
    import CompositeFundInstrumentDefinition
    importlib.reload(CompositeFundInstrumentDefinition)
    import CompositeAverageForwardInstrumentDefinition
    importlib.reload(CompositeAverageForwardInstrumentDefinition)
    import CompositeCashFlowInstrumentDefinition
    importlib.reload(CompositeCashFlowInstrumentDefinition)
    import CompositeCombinationInstrumentDefinition
    importlib.reload(CompositeCombinationInstrumentDefinition)
    import CompositeDerivativeInstrumentDefinition
    importlib.reload(CompositeDerivativeInstrumentDefinition)    
    import CompositeOptionInstrumentDefinition
    importlib.reload(CompositeOptionInstrumentDefinition)
