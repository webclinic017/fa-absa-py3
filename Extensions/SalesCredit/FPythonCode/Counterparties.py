
from at_logging import getLogger
import acm

LOGGER = getLogger(__name__)

def getCounterparties():
    parties = None
   
    try:
        partyTypeEnum = acm.FEnumeration["enum(PartyType)"]
        types_filter = [partyTypeEnum.Enumeration("Counterparty"), partyTypeEnum.Enumeration("Client")]
        select_string = "type in {types}".format(types=tuple(types_filter))
        parties = acm.FParty.Select(select_string)
    except Exception as error:
        LOGGER.exception(error)

    return parties
