import acm

from at_addInfo import save as ai_save
from at_logging import getLogger


LOGGER = getLogger(__name__)


PSWAP_PREFIX = "RTM_"
PF_PREFIX_ACS = "PSWAP_RTM_"
PF_PREFIX_BANK = "ABSA RTM - "
ACQUIRER = "ACS"
CTRPTY = "PRIME SERVICES DESK"


#config = {}
#config["cfdAccount"] = "55558"
#config["startDate"] = "2018-06-06"


def create_pswap(pswap_name, pf_acs, pf_synthetic, pf_bank,
                 acquirer, ctrpty, start_date, exp_date):
    # <pf_acs> portfolio name under ABSA CAPITAL SECURITIES where the pswap will be booked
    # <pf_synthetic> portfolio name under ABSA CAPITAL SECURITIES containing the stocks
    # <pf_bank> portfolio name under ABSA CAPITAL where the pswap with opposite sign will be booked
    LOGGER.info("Create pswap with name {}".format(pswap_name))
    acm.BeginTransaction()
    try:
        # Create pswap
        pswap = acm.FInstrument[pswap_name]
        if pswap is None:
            template = acm.FInstrument["RTM_TEMPLATE"]
            pswap = template.Clone()
            pswap.Name(pswap_name)
        else:
            LOGGER.info("Instrument {} already exists".format(pswap_name))
            existing_pswap = acm.FPortfolioSwap[pswap_name]
            if not existing_pswap:
                msg = "{} is not a portfolio swap!".format(pswap_name)
                LOGGER.error(msg)
                raise RuntimeError(msg)
            if existing_pswap.Trades().Size() != 2:
                msg = "Number of trades is not 2, check pswap {}!".format(pswap_name)
                LOGGER.error(msg)
                raise RuntimeError(msg)
            return
        pswap.MtmFromFeed(False)
        pswap.FundPortfolio(pf_synthetic)
        pswap.StartDate(start_date)
        pswap.ExpiryDate(exp_date)
        pswap.Commit()
        LOGGER.info("Instrument - pswap done")
        # Create meta leg
        meta_leg = acm.FInstrument["ML_" + pswap_name]
        if meta_leg is None:
            template = acm.FInstrument["ML_RTM_TEMPLATE"]
            meta_leg = template.StorageNew()
            meta_leg.Name("ML_" + pswap_name)
        else:
            LOGGER.info("Instrument {} already exists".format("ML_" + pswap_name))
        meta_leg.MtmFromFeed(False)
        meta_leg.Commit()
        LOGGER.info("Instrument - meta leg done")
        # Create rate index
        rate_index = acm.FInstrument["CL_" + pswap_name]
        if rate_index is None:
            template = acm.FInstrument["CL_RTM_TEMPLATE"]
            rate_index = template.StorageNew()
            rate_index.Name("CL_" + pswap_name)
        else:
            LOGGER.info("Instrument {} already exists".format("CL_" + pswap_name))
        rate_index.MtmFromFeed(False)
        rate_index.Commit()
        LOGGER.info("Instrument - rate index done")
        # Create instrument package
        ins_package = acm.FInstrumentPackage[pswap_name]
        if ins_package is None:
            template = acm.FInstrumentPackage["RTM_TEMPLATE"]
            ins_package = template.StorageNew()
            ins_package.Name(pswap_name)
        else:
            LOGGER.info("Instrument package {} already exists".format(pswap_name))
        ins_package.InstrumentLinks()[0].Instrument(pswap)
        ins_package.InstrumentLinks()[1].Instrument(meta_leg)
        ins_package.InstrumentLinks()[2].Instrument(rate_index)
        ins_package.Commit()
        LOGGER.info("Instrument package done")
        # Create trade - ACS
        template = acm.FDealPackage.Select01("instrumentPackage='RTM_TEMPLATE'", None)
        trade = template.TradeLinks()[0].Trade().StorageNew()
        trade.Instrument(pswap)
        trade.Portfolio(pf_acs)
        trade.Counterparty(ctrpty)
        trade.Acquirer(acquirer)
        trade.ValueDay(start_date)
        trade.AcquireDay(start_date)
        trade.TradeTime(start_date)
        trade.Quantity(-1.0)
        trade.Commit()
        LOGGER.info("Trade ACS done")
        # Create trade - bank
        trade_bank = template.TradeLinks()[0].Trade().StorageNew()
        trade_bank.Instrument(pswap)
        trade_bank.Portfolio(pf_bank)
        trade_bank.Counterparty(acquirer)
        trade_bank.Acquirer(ctrpty)
        trade_bank.ValueDay(start_date)
        trade_bank.AcquireDay(start_date)
        trade_bank.TradeTime(start_date)
        trade_bank.Quantity(1.0)
        trade_bank.Commit()
        LOGGER.info("Trade bank done")
        acm.CommitTransaction()
        LOGGER.info("Transaction done")
    except:
        acm.AbortTransaction()
        LOGGER.exception("Transaction aborted due to errors")
        raise
    # Create deal package
    dp = acm.DealPackage.NewAsDecoratorFromInstrumentPackage(ins_package)
    dp.TradeLinks()[0].Trade(trade)
    dp.Commit()
    ins_package.Commit()
    LOGGER.info("Deal package done")
    for leg in list(pswap.Legs()):
        leg.Delete()


def setup_rtm(config):
    bda_acc_nr = config["cfdAccount"]
    start_date = config["startDate"]
    exp_date = acm.Time.DateAddDelta(config["startDate"], 1, 0, 0)
    # Update the additional infos for the ABSA CAPITAL SECURITIES portfolio
    pf = acm.FPhysicalPortfolio[PF_PREFIX_ACS + bda_acc_nr]
    ai_save(pf, "Reg_Classification", "Trading")
    ai_save(pf, "Portfolio Status", "Active")
    ai_save(pf, "RTMRestricted", "Yes")
    ai_save(pf, "prt_BDA AccountNum", bda_acc_nr)
    # Update the additional infos for the ABSA CAPITAL portfolio
    pf = acm.FPhysicalPortfolio[PF_PREFIX_BANK + bda_acc_nr]
    ai_save(pf, "Reg_Classification", "Trading")
    ai_save(pf, "Portfolio Status", "Active")
    ai_save(pf, "RTMRestricted", "Yes")
    # Create the pswap with the trades
    create_pswap(PSWAP_PREFIX + bda_acc_nr,
                 PF_PREFIX_ACS + bda_acc_nr,
                 bda_acc_nr,
                 PF_PREFIX_BANK + bda_acc_nr,
                 ACQUIRER,
                 CTRPTY,
                 start_date,
                 exp_date)
    # Set the add info Portfolio Status back to Pending
    ai_save(acm.FPhysicalPortfolio[PF_PREFIX_ACS + bda_acc_nr], "Portfolio Status", "Pending")
    ai_save(acm.FPhysicalPortfolio[PF_PREFIX_BANK + bda_acc_nr], "Portfolio Status", "Pending")


#setup_rtm(config)

