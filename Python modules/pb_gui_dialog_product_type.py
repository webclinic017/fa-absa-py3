"""
A module which contains classes for creating a GUI
for adding a new product type.
"""

from FUxCore import LayoutDialog

from at_logging import getLogger
from pb_gui_attribute import (create_attribute,
                              get_checked_state,
                              set_checked_state,
                              WrongValueError)
from pb_gui_core import (CANCEL_BUTTON_ID,
                         OK_BUTTON_ID,
                         show_information_window,
                         show_question_window)
from pb_quirk import get_suggestion_quirks
from pb_storage_attr_def import AttributeDefinitionStorage
from pb_storage_fund import PrimeBrokerageFundStorage


LOGGER = getLogger()


class AddProductTypeDialog(LayoutDialog):

    """
    A class which represents a dialog
    for adding a new product type to a prime brokerage fund.
    """

    def __init__(self,
                 pb_fund,
                 sweeping_class=None,
                 fully_funded=None):
        """
        Initialize the instance.
        """
        self.pb_fund = pb_fund
        if sweeping_class is None:
            sweeping_class = "Cash equity"
        self.sweeping_class = sweeping_class
        if fully_funded is None:
            fully_funded = False
        self.fully_funded = fully_funded
        self.edited = False
        required_attr_ids = ["ps_pswap",
                             "ps_start_date",
                             "ps_swap_portfolio",
                             "ps_pswap_trade_portfolio",
                             "ps_pswap_trade_status"]
        attr_def_storage = AttributeDefinitionStorage()
        attr_def_storage.load()
        self.sweeping_class_attr_def = attr_def_storage.attr_defs[
            "ps_sweeping_class"]
        self.fully_funded_attr_def = attr_def_storage.attr_defs[
            "ps_fully_funded"]
        self.attributes = {}
        suggestion_quirks = get_suggestion_quirks(self.pb_fund)
        for i, attr_id in enumerate(required_attr_ids, start=1):
            gui_id = "quirk{0}".format(i)
            attr_def = attr_def_storage.attr_defs[attr_id]
            attribute_quirk = suggestion_quirks[attr_id]
            attribute = create_attribute(gui_id, attr_def, attribute_quirk)
            self.attributes[attr_id] = attribute


    def update_sweeping_class_callback(self, _ux_control, _unused):
        """
        Fill the GUI parts with the data
        corresponding to the newly selected sweeping class.
        """
        self.sweeping_class = self.w_sweeping_class.GetData()
        self.load_attribute_layout()


    def update_fully_funded_callback(self, _ux_control, _unused):
        """
        Fill the GUI parts with the data
        corresponding to the newly selected fully funded flag.
        """
        self.fully_funded = get_checked_state(self.w_fully_funded)
        self.load_attribute_layout()


    def create_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used at the bottom of the main dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.BeginHorzBox()
        builder.AddOption("sweeping_class",
                          str(self.sweeping_class_attr_def.name),
                          30)
        builder.AddLabel("no_sweeping_classes", "(000)")
        builder.EndBox()
        builder.AddCheckbox("fully_funded",
                            # A space at the end is supposed to ensure
                            # that the bold font would not make
                            # the last part of the label invisible
                            str(self.fully_funded_attr_def.name) + " ")
        builder.AddSeparator()
        for attribute in sorted(self.attributes.itervalues(),
                                key=lambda attribute:
                                attribute.attr_def.attr_id):
            attribute.create_layout(builder)
        builder.BeginHorzBox()
        builder.AddButton(OK_BUTTON_ID, " Add ", False, True)
        builder.AddFill()
        builder.AddLabel("notice", "..... loading  .....", False, True)
        builder.AddFill()
        builder.AddButton(CANCEL_BUTTON_ID, " Close ", False, True)
        builder.EndBox()
        builder.EndBox()
        return builder


    def load_attribute_layout(self):
        """
        Load the values of the GUI attributes
        in the dialog's layout.
        """
        for attribute in self.attributes.itervalues():
            if not attribute.edited:
                attribute.load_attribute(self.sweeping_class,
                                         self.fully_funded)


    def init_attribute_layout(self, layout):
        """
        Initialize the GUI attributes of the dialog's layout.
        """
        for attribute in self.attributes.itervalues():
            attribute.init_layout(layout)
            attribute.set_callbacks(self)


    def init_layout(self, layout):
        """
        Initialize the GUI parts of the dialog's layout.
        """
        import acm
        self.w_sweeping_class = layout.GetControl("sweeping_class")
        self.w_sweeping_class.ToolTip(
            str(self.sweeping_class_attr_def.description))
        self.w_sweeping_class.SetStandardFont("Bold")
        sw_cls_choices = acm.FChoiceList.Select("list = 'PB_Sweeping_Class'")
        for sw_cls in sorted(sw_cls_choices):
            self.w_sweeping_class.AddItem(sw_cls.Name())
        self.w_sweeping_class.SetData(str(self.sweeping_class))
        self.w_sweeping_class.AddCallback("Changed",
                                          self.update_sweeping_class_callback,
                                          self.w_sweeping_class)
        w_no_sweeping_classes = layout.GetControl("no_sweeping_classes")
        w_no_sweeping_classes.SetStandardFont("Bold")
        w_no_sweeping_classes.ToolTip(
            "The number of available sweeping classes")
        greenish = acm.UX().Colors().Create(30, 170, 30)
        w_no_sweeping_classes.SetColor("Text", greenish)
        w_no_sweeping_classes.SetData("({0})".format(len(sw_cls_choices)))
        self.w_fully_funded = layout.GetControl("fully_funded")
        self.w_fully_funded.ToolTip(
            str(self.fully_funded_attr_def.description))
        self.w_fully_funded.SetStandardFont("Bold")
        self.w_fully_funded.AddCallback("Activate",
                                        self.update_fully_funded_callback,
                                        self.w_fully_funded)
        set_checked_state(self.w_fully_funded, self.fully_funded)
        self.w_ok = layout.GetControl(OK_BUTTON_ID)
        self.w_ok.SetStandardFont("Bold")
        self.w_notice = layout.GetControl("notice")
        self.w_notice.SetStandardFont("Bold")
        self.w_notice.SetAlignment("Center")
        reddish = acm.UX().Colors().Create(195, 31, 0)
        self.w_notice.SetColor("Text", reddish)
        self.w_notice.SetData("")
        self.init_attribute_layout(layout)


    def make_edited(self, value):
        """
        Mark the current dialog as edited or not edited.
        """
        if value:
            self.w_notice.SetData("edited")
            self.edited = True
        else:
            self.w_notice.SetData("")
            self.edited = False


    def update_edited_state(self):
        """
        Mark the current dialog as edited if at least one
        of its attributes is marked as edited.
        """
        edited_state = False
        for gui_attribute in self.attributes.itervalues():
            if gui_attribute.edited:
                edited_state = True
                break
        self.make_edited(edited_state)


    def get_input_values(self):
        """
        Check if the entered input values of the suggestion quirks are valid
        and save their values to the appropriate instance attributes.
        """
        self.pswap_name = self.attributes[
            "ps_pswap"].get_string_value(validate=False)
        self.pswap_start_date = self.attributes[
            "ps_start_date"].get_string_value()
        self.pswap_swap_portfolio_name = self.attributes[
            "ps_swap_portfolio"].get_string_value(validate=False)
        self.pswap_trade_portfolio_name = self.attributes[
            "ps_pswap_trade_portfolio"].get_string_value()
        self.pswap_trade_status = self.attributes[
            "ps_pswap_trade_status"].get_string_value()


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        self.layout_dialog = layout_dialog
        self.layout_dialog.Caption("Fund '{0}' | Add Product Type".format(
            self.pb_fund.fund_id))
        self.init_layout(main_layout)
        self.load_attribute_layout()


    def HandleApply(self):
        """
        Obtain the changed fund's attributes from the GUI
        and set them using the underlying Attributes.

        This function handles an event of pressing a button
        with name == "ok".
        """
        shell = self.layout_dialog.Shell()
        message = ("Are you sure you want to create "
                   "the specified product type "
                   "of the prime brokerage "
                   "fund '{0}'?").format(self.pb_fund.fund_id)
        answer = show_question_window(shell, message)
        if answer == "Button1": # The first button (Yes) has been pressed.
            # FIXME: validate entered values and create the new product type
            try:
                self.get_input_values()
            except WrongValueError as exc:
                shell = self.layout_dialog.Shell()
                message = ("Unable to use the entered input values "
                           "for the creation of the new product type. "
                           "Reason: {0}").format(exc)
                show_information_window(shell, message)
                return # Keep the dialog open
            self.pb_fund.add_product_type_pswap(self.sweeping_class,
                                                self.fully_funded,
                                                self.pswap_name,
                                                self.pswap_start_date,
                                                self.pswap_swap_portfolio_name,
                                                self.pswap_trade_portfolio_name,
                                                self.pswap_trade_status)
            product_type_name = self.pb_fund.get_product_type_name(
                self.sweeping_class, self.fully_funded)
            LOGGER.info("Product type '%s' "
                        "with the specified parameters "
                        "of the prime brokerage fund '%s' "
                        "has been created.",
                        product_type_name,
                        self.pb_fund.fund_id)
            # FIXME: Necessary?
            self.make_edited(False)
            return product_type_name
        else:
            # FIXME: update information message
            LOGGER.info("The current product types "
                        "of the prime brokerage fund '%s' "
                        "have been left intact.",
                        self.pb_fund.fund_id)


def demo_launch():
    """
    Launch the attribute edit dialog
    as a standalone application within Front Arena.
    The parent of this dialog will be the session manager.
    """
    import acm
    shell = acm.UX().SessionManager().Shell()
    pb_fund_storage = PrimeBrokerageFundStorage()
    pb_fund_storage.load()
    fund_id = next(pb_fund_storage.stored_funds.iterkeys())
    pb_fund = pb_fund_storage.load_fund(fund_id)
    dialog = AddProductTypeDialog(pb_fund)
    builder = dialog.create_layout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


#demo_launch()
