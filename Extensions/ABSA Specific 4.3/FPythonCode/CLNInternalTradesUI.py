"""--------------------------------------------------------------------------
MODULE
   CLNInternalTradesUI

DESCRIPTION
    This module is used to the extension button for the for Credit Linked Note (CLN) deal structure.

HISTORY
Date: 2020-10-28
Author: Snowy Mabilu
Jira:  https://absa.atlassian.net/browse/ARR-74

-----------------------------------------------------------------------------"""

import acm
import FUxCore
import CLNInternalTradesStructure
from FUploaderUtils import CreateOutput
from at_ux import msg_box
from at_logging import getLogger

lOGGER = getLogger(__name__)
CD_CDS_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject', 'CLN_CD_Trade_Parameters').Value()
DEPO_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
                                                   'CLN_Funding_Desk_Trade_Parameters').Value()
CLIENT_CDS_PARAMS = acm.GetDefaultContext().GetExtension('FParameters', 'FObject',
                                                         'CLN_Client_Trade_Parameters').Value()


class CLNTradesCreator(FUxCore.LayoutDialog):

    def __init__(self, client_trade):
        self.client_trade = client_trade
        self.CreateLayout()

    def render_output(self, trades):
        """
        This function is used to desplay the trades to a user.
        It creates a gui pop -up with the trades.

        :param trades: Trades to be displayed on the GUI
        """
        shell = acm.UX().SessionManager().Shell()
        dlg = CreateOutput('CLN Trades', trades)
        acm.UX().Dialogs().ShowCustomDialogModal(shell, dlg.CreateLayout(), dlg)

    def create_CLN_structure(self, rate, credit_ref):
        """
        This method creates the deal structure for CLN trades  using the input FRN trade,
        and the rate and credit ref information from FO user. The deal structure constitute three trades,
        i.e Two CDS trades  and One deposit
        :param rate:
        :param credit_ref:
        :return:
        """
        trades = []
        try:
            client = self.client_trade        
            depo = CLNInternalTradesStructure.create_deposit(client, DEPO_PARAMS)
            depo.TrxTrade(depo)
            depo.Commit()
            trades.append(depo)
            if client.Status() not in ['Void']:
                client.TrxTrade(depo)
                client.AddInfoValue('Approx. load', CLIENT_CDS_PARAMS['approx_load'].Text())
                client.AddInfoValue('Approx. load ref', CLIENT_CDS_PARAMS['approx_load_ref'].Text())
                client.AddInfoValue('InsOverride', CLIENT_CDS_PARAMS['ins_override'].Text())
                client.Commit()

            client_cds = CLNInternalTradesStructure.create_cds_trade(client, rate, credit_ref, CLIENT_CDS_PARAMS, depo)
            trades.append(client_cds)
            cd_cds = CLNInternalTradesStructure.create_cds_trade(client, rate, credit_ref, CD_CDS_PARAMS, depo)
            trades.append(cd_cds)
            self.render_output(trades)
        except Exception as error:
            message = "Deleting commited trades \n"
            try:
                for trade in trades:
                    instrument = trade.Instrument()
                    trade.Delete()
                    instrument.Delete()
                    
            except Exception as error:
                lOGGER.exception(error)
            lOGGER.info(message)
            raise error

    def HandleApply(self):
        try:
            rate = float(self.rate.GetData())
        except ValueError as e:
            msg_box('Please ensure rate is number', 'Invalid Rate')
            return False

        credit_ref = acm.FInstrument[self.credit_ref.GetData()]
        if not credit_ref:
            msg_box('Invalid Credit Ref provided, please rectify', 'Invalid Credit Ref')
            return False
        try:
            self.create_CLN_structure(rate, credit_ref.Name())
        except Exception as e:
            lOGGER.exception(e)
            msg_box('Failed to Book CLN trades', 'Error')
            return False
        return True


    def HandleCreate(self, dlg, layout):
        gc = layout.GetControl
        self.fux_dialog = dlg
        self.fux_dialog.Caption('CDS Trade Parameters')
        self.rate = gc('rate')
        self.credit_ref = gc('credit_ref')
        gc("ok").SetFocus()


    def CreateLayout(self):
        b = acm.FUxLayoutBuilder()
        b.BeginVertBox('None')
        b.BeginHorzBox()
        b.AddInput('credit_ref', 'CreditRef')
        b.EndBox()
        b.BeginHorzBox()
        b.AddInput('rate', 'Rate')
        b.EndBox()
        b.BeginHorzBox()
        b.AddButton('ok', 'OK')
        b.AddButton("cancel", "Cancel")
        b.EndBox()
        b.EndBox()
        self.layout = b


def book(eii):
    object = eii.ExtensionObject().CurrentObject()
    if object is None:
        msg_box('No Object selected', 'Error')
        return
    elif object.IsKindOf(acm.FTrade):
        shell = eii.ExtensionObject().Shell()
        custom_dlg = CLNTradesCreator(object)
        acm.UX().Dialogs().ShowCustomDialogModal(shell,
                                                 custom_dlg.layout,
                                                 custom_dlg)
