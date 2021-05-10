"""--------------------------------------------------------------------------------------------------------------------------------------
MODULE
    OperationsSTPParameters

DESCRIPTION
    This module contains parameters used to configure Operations STP functionality
    within Front Arena.

-----------------------------------------------------------------------------------------------------------------------------------------
HISTORY
=========================================================================================================================================
Date            Change no       Developer               Requester               Description
-----------------------------------------------------------------------------------------------------------------------------------------
2019-04-05      FAOPS-448       Hugo Decloedt           Kgomotso Gumbo          Initial implementation.
                                Cuen Edwards
                                Stuart Wilson
2019-04-12      FAOPS-483       Cuen Edwards            Kgomotso Gumbo          Migrated confirmation auto-matching.
2019-04-18      FAOPS-425       Cuen Edwards            Kgomotso Gumbo          Addition of term maturity instruction STP.
                                                                                Addition of adjust deposit STP.
2019-05-13      FAOPS-308       Joash Moodley           Kgomotso Gumbo          Implementation Of NetMaturitySettlementsSTPHook.
                                                                                And NetMaturitySettlementsSTPAutoReleaseHook.
2019-05-16      FAOPS-466       Hugo Decloedt           Gasant Thulsie          Add auto-release for SBL fixed cash flows.
2019-06-19      FAOPS-393       Tawanda Mukhalela       Wandile Sithole         Addition of Non Zar Maturities STP
2019-05-27      FAOPS-488       Tawanda Mukhalela       Wandile Sithole         Addition of Capital Markets MT5XX STP
2019-09-12      FAOPS-532       Tawanda Mukhalela       Khanya Modise           Auto Hold of Namibian Bic Settlements
2019-11-21      FAOPS-635       Tawanda Mukhalela       Wandile Sithole         Addition of PICandOasisOutgoingMaturitiesSTPHook
2020-04-29      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Addition of hook to auto-set fields on SARB security
                                                                                transfer trades.
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Relocated list of subscribed tables from ATS module
                                                                                OperationsSTPMain.
2020-04-30      FAOPS-700       Cuen Edwards            Kgomotso Gumbo          Migrated BO Confirming of security trades.
2020-05-05      FAOPS-775       Cuen Edwards            Kgomotso Gumbo          Migrated FX Option approximate load add info population
                                                                                from scheduled task.
2020-05-26      PCGDEV-10       Sihle Gaxa              James Stevens           Addition of SBLAutoBOConfirmSTPHook.
2020-05-28      FAOPS-683       Joash Moodley           Kgomotso Gumbo          EuroClear Custody Funding (MT210 & MT222).
2020-05-28      FAOPS-740       Joash Moodley           Kgomotso Gumbo          EuroClear Custody Funding (MT200).
2020-02-06      PCGDEV-298      Tawanda Mukhalela       Gasant Thulsie          Addition of SBLSettlementsSTPHook
2020-05-04      FAOPS-615       Ntokozo Skosana         Wandile Sithole         Addition of hook to auto-set fields on Internal
                                                                                security transfer trades.
2020-07-23      PCGDEV-532      Sihle Gaxa              James Stevens           Addition of SBL Security Loan Update STP Hook
2020-05-28      FAOPS-685       Tawanda Mukhalela       Nicky Virlijoen         Addition of Security Transfer Stp Hook
2020-08-19      FAOPS-865       Tawanda Mukhalela       Wandile Sithole         Minor Refactor of Euroclear MT210 Payments
2020-09-14      FAOPS-864       Jaysen Naicker          Wandile Sithole         Enable End Cash for Euroclear Repo/Reverse and 
                                                                                incl BSB ins type in Funding
2020-10-19      PCGDEV-598      Sihle Gaxa              Shaun Du Plessis        Addition of Dual booking hook
2020-10-06      PCGDEV-594      Qaqamba Ntshobane       Daveshin Chetty         Addition of AddInfo update hook
2020-11-09      FAOPS-931       Tawanda Mukhalela       Linda Breytenbach       Added Support for MT298 settlements

2020-12-10      FAOPS-925       Metse Moshobane         Wandile Sithole         Auto releasing of Vostro accounts settlements for Prime Service Desk.
2020-11-30      PCGDEV-624      Buhlebezwe Ngubane      Gasant Thulsie          Add hook for Auto Releasing New Security Loan Settlements
2021-03-02      INC2429807      Tawanda Mukhalela       Kgomotso Gumbo          Remove SBL Collateral Auto-Release Hook
                                                                                as per INC2429807
2021-03-11      FAOPS-1030/53   Tawanda Mukhalela       Wandile Sithole         Removed End Cash STP Hook
2021-03-08      FAOPS-1085      Tawanda Mukhalela       Wandile Sithole         Removed Namibia Auto Hold STP Hook and
                                                                                added Autorelease Hook
-----------------------------------------------------------------------------------------------------------------------------------------
"""

from AcknowledgedSecuritySettlementSTPHook import AcknowledgedSecuritySettlementSTPHook
from AdjustCallDepositSTPHook import AdjustCallDepositSTPHook
from AutoMatchConfirmationSTPHook import AutoMatchConfirmationSTPHook
from CMMT5XXSTPHook import CMMT5XXSTPHook
from DematSTPAutoReleaseHook import DematSTPAutoReleaseHook, AuthoriseMT298STPHook
import EnvironmentFunctions
from FXOptionProductTypeChangeSTPHook import FXOptionProductTypeChangeSTPHook
from InternalSecurityTransferSTPHook import InternalSecurityTransferSTPAutoReleaseHook, \
    SetInternalSecurityTransferFieldsSTPHook
from MatchedAdjustDepositConfirmationSTPHook import MatchedAdjustDepositConfirmationSTPHook
from MatchedMT320ConfirmationSTPHook import MatchedMT320ConfirmationSTPHook
from MatchedNonZarMT320ConfirmationSTPHook import MatchedNonZarMT320ConfirmationSTPHook
from MatchedTradeAffirmationSTPHook import MatchedTradeAffirmationSTPHook
from NamibianSettlementsSTPHook import NamibianSettlementsAutoReleaseHook
from NetMaturitySettlementsSTPAutoReleaseHook import NetMaturitySettlementsSTPHook
from NetMaturitySettlementsSTPAutoReleaseHook import NetMaturitySettlementsSTPAutoReleaseHook
from PICandOasisOutgoingMaturitiesSTPHook import PICandOasisOutgoingMaturitiesSTPHook
from SBLCollateralSTPHook import (
    SBLCollateralSTPHook,
    SBLAutoBOConfirmSTPHook,
    SBLDualBookingSTPHook
)
from SBLSettlementsSTPHook import (
    AutoHoldSBLSettlementSTPHook,
    AutoAuthoriseSBLSettlementSTPHook,
    AutoSetCallConfirmationSTPHook,
    AutoReleaseSBLSettlementSTPHook
)
from SecurityTransferSTPHook import (
    SecurityTransferCreationSTPHook,
    SecurityTransferUpdateSTPHook,
    SecurityTransferVoidSTPHook
)
from SetSARBSecurityTransferFieldsSTPHook import SetSARBSecurityTransferFieldsSTPHook
from SSAPremiumNettingSTPHook import SSAPremiumNettingSTPHook
from TermMaturityInstructionSTPHook import TermMaturityInstructionSTPHook
from EuroclearCustom210SettlementSTPHook import EuroClearMT210PaymentCreation, EuroClearMT210PaymentUpdate
from SBLSecurityLoanUpdateSTPHook import SBLTerminateFullReturnSTPHook
from AddinfoUpdateSTPHook import TBillAddinfoUpdateSTPHook, ETNAddinfoUpdateSTPHook
from SwiftSolutionsSTPHook import MT202COVMethodSTPHook
from PSVostroSTPAutoReleaseHook import VostroSTPAutoReleaseHook


ambAddress = '{amb_host}:{amb_port}{amb_login}'.format(
    amb_host=EnvironmentFunctions.get_operations_stp_parameter('Host'),
    amb_port=EnvironmentFunctions.get_operations_stp_parameter('Port'),
    amb_login=EnvironmentFunctions.get_operations_stp_parameter('Login')
)

receiverMBName = EnvironmentFunctions.get_operations_stp_parameter('ReceiverName')

receiverSource = EnvironmentFunctions.get_operations_stp_parameter('ReceiverSource')

eventTables = [
    'CONFIRMATION',
    'INSTRUMENT',
    'SETTLEMENT',
    'TRADE'
]

stpHooks = [
    AutoMatchConfirmationSTPHook(),
    CMMT5XXSTPHook(),
    MatchedTradeAffirmationSTPHook(),
    MatchedMT320ConfirmationSTPHook(),
    MatchedNonZarMT320ConfirmationSTPHook(),
    MatchedAdjustDepositConfirmationSTPHook(),
    TermMaturityInstructionSTPHook(),
    AdjustCallDepositSTPHook(),
    # SBLCollateralSTPHook() Removing Collateral Auto Release to mitigate Prod Incident ,
    SBLDualBookingSTPHook(),
    SBLAutoBOConfirmSTPHook(),
    NetMaturitySettlementsSTPHook(),
    NetMaturitySettlementsSTPAutoReleaseHook(),
    NamibianSettlementsAutoReleaseHook(),
    PICandOasisOutgoingMaturitiesSTPHook(),
    DematSTPAutoReleaseHook(),
    FXOptionProductTypeChangeSTPHook(),
    SSAPremiumNettingSTPHook(),
    AutoHoldSBLSettlementSTPHook(),
    AutoAuthoriseSBLSettlementSTPHook(),
    AutoSetCallConfirmationSTPHook(),
    AcknowledgedSecuritySettlementSTPHook(),
    SetSARBSecurityTransferFieldsSTPHook(),
    SetInternalSecurityTransferFieldsSTPHook(),
    InternalSecurityTransferSTPAutoReleaseHook(),
    EuroClearMT210PaymentCreation(),
    EuroClearMT210PaymentUpdate(),
    SBLTerminateFullReturnSTPHook(),
    SecurityTransferCreationSTPHook(),
    SecurityTransferUpdateSTPHook(),
    SecurityTransferVoidSTPHook(),
    AuthoriseMT298STPHook(),
    TBillAddinfoUpdateSTPHook(),
    ETNAddinfoUpdateSTPHook(),
    MT202COVMethodSTPHook(),
    VostroSTPAutoReleaseHook(),
    AutoReleaseSBLSettlementSTPHook()

]
