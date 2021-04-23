"""
A module which contains a class and functions
used to create a GUI for maintaining the data
about the prime brokerage funds.
"""

from FUxCore import LayoutTabbedDialog

from pb_attr_def import AttributeDefinition
from pb_gui_attribute import (create_attribute,
                              GUIChronicleAttribute,
                              GUIPortfolioSwapQuirkAttribute,
                              GUIQuirkAttribute,
                              WrongValueError)
from pb_gui_core import (CANCEL_BUTTON_ID,
                         OK_BUTTON_ID,
                         show_information_window,
                         show_question_window)
from pb_gui_dialog_product_type import AddProductTypeDialog
from pb_gui_dialog_text_object import TextObjectEditDialog
from pb_storage_attr_def import AttributeDefinitionStorage
from pb_storage_fund import PrimeBrokerageFundStorage


class FundDetailsDialog(LayoutTabbedDialog):

    """
    A class which represents a dialog
    with the details about a single Prime Brokerage fund.
    """

    def __init__(self,
                 fund_id=None,
                 pb_fund_storage=None,
                 attr_def_storage=None):
        """
        Initialize the instance.
        """
        if attr_def_storage is None:
            attr_def_storage = AttributeDefinitionStorage()
        attr_def_storage.load()
        self.attr_def_storage = attr_def_storage
        if pb_fund_storage is None:
            pb_fund_storage = PrimeBrokerageFundStorage()
        pb_fund_storage.load()
        self.pb_fund_storage = pb_fund_storage
        if fund_id is None:
            fund_id = pb_fund_storage.stored_funds.iterkeys().next()

        self.attributes = {}
        self.load_fund(fund_id)
        self.edited = False


    def load_fund(self, fund_id):
        """
        Load the prime brokerage fund with the provided ID
        from the prime brokerage fund storage
        and initialize the GUI attributes from its attributes and quirks.
        """
        self.pb_fund = self.pb_fund_storage.load_fund(fund_id)
        self.text_object_id = str(self.pb_fund_storage.stored_funds[fund_id])
        attr_ids = sorted(self.pb_fund.attributes.keys())
        quirk_ids = sorted(self.pb_fund.quirks.keys())
        gui_attr_ids = sorted(attr_ids + quirk_ids)
        if self.attributes and sorted(self.attributes.keys()) != gui_attr_ids:
            exception_message = ("The prime brokerage fund '{0}' "
                                 "has different GUI attributes ({1}) "
                                 "than the originally loaded prime "
                                 "brokerage fund ({2}).".format(
                                     self.pb_fund.fund_id,
                                     repr(gui_attr_ids),
                                     repr(sorted(self.attributes.keys()))))
            raise RuntimeError(exception_message)

        if not self.attributes:
            # FIXME: Simplify this function
            for i, attr_id in enumerate(attr_ids, start=1):
                gui_id = "attr{0}".format(i)
                attr_def = self.attr_def_storage.attr_defs[attr_id]
                chronicle_attribute = self.pb_fund.attributes[attr_id]
                attribute = create_attribute(gui_id, attr_def, chronicle_attribute)
                self.attributes[attr_id] = attribute
            for i, attr_id in enumerate(quirk_ids, start=1):
                gui_id = "quirk{0}".format(i)
                attr_def = self.attr_def_storage.attr_defs[attr_id]
                quirk_attribute = self.pb_fund.quirks[attr_id]
                attribute = create_attribute(gui_id, attr_def, quirk_attribute)
                self.attributes[attr_id] = attribute
        else:
            for attr_id, gui_attribute in self.attributes.iteritems():
                if isinstance(gui_attribute, GUIChronicleAttribute):
                    gui_attribute.attribute = self.pb_fund.attributes[attr_id]
                elif isinstance(gui_attribute, GUIQuirkAttribute):
                    gui_attribute.attribute = self.pb_fund.quirks[attr_id]


    def save_edited_quirks(self):
        """
        Save the quirk attributes which have been marked as edited.
        """
        for gui_attribute in self.attributes.itervalues():
            # FIXME: This condition needs to be checked before
            # the condition for GUIQuirkAttribute,
            # because GUIPortfolioSwapQuirkAttribute is a subclass
            # of GUIQuirkAttribute.
            # Maybe it would be better to create a common superclass
            # for both of those classes.
            if isinstance(gui_attribute, GUIPortfolioSwapQuirkAttribute):
                acm_portfolio_swap = self.portfolio_swaps[
                    self.product_type_index]
                gui_attribute.save_from_input(acm_portfolio_swap)
            elif isinstance(gui_attribute, GUIQuirkAttribute):
                gui_attribute.save_from_input()


    def make_attributes_not_edited(self):
        """
        Mark the chronicle attributes as not edited.
        """
        for gui_attribute in self.attributes.itervalues():
            if isinstance(gui_attribute, GUIChronicleAttribute):
                gui_attribute.make_edited(False)


    def fund_id_callback(self, _ux_control, _unused):
        """
        Fill the GUI parts with the data of a newly selected fund.
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Discard the changes made to "
                       "the currently selected fund '{0}'?").format(
                           self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button2": # The second button (No) has been pressed.
                current_index = self.fund_ids.index(self.pb_fund.fund_id)
                self.w_fund_id.SetData(current_index)
                return

        selected_fund_id = self.w_fund_id.GetData()
        self.load_fund(selected_fund_id)
        self.load_product_types()
        self.load_fund_attributes()
        self.make_edited(False)


    def select_product_type_callback(self, _ux_control, _unused):
        """
        Fill the GUI parts with the product-type specific details
        of the newly selected product type.
        """
        # FIXME: Only check if the product type details are edited.
        if self.edited:
            shell = self.layout_dialog.Shell()
            current_product_type = self.product_types[self.product_type_index]
            message = ("Discard the changes made to "
                       "the currently selected product type ({0}) "
                       "of the fund '{1}'?").format(
                           current_product_type,
                           self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button2": # The second button (No) has been pressed.
                self.w_product_type.SetData(self.product_type_index)
                return

        selected_product_type = self.w_product_type.GetData()
        try:
            product_type_index = self.product_types.index(
                selected_product_type)
        except ValueError:
            product_type_index = 0
        self.load_product_type(product_type_index)
        self.update_edited_state()


    def add_product_type_callback(self, _ux_control, _unused):
        """
        Create a new product type
        for the currently selected prime brokerage fund.
        """
        import acm
        # FIXME: Only check if the product type details are edited.
        if self.edited:
            shell = self.layout_dialog.Shell()
            current_product_type = self.product_types[self.product_type_index]
            message = ("Discard the changes made to "
                       "the currently selected product type '{0}' "
                       "of the fund '{1}'?").format(
                           current_product_type,
                           self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button2": # The second button (No) has been pressed.
                self.w_product_type.SetData(self.product_type_index)
                return

        shell = self.layout_dialog.Shell()
        dialog = AddProductTypeDialog(self.pb_fund)
        builder = dialog.create_layout()
        product_type = acm.UX().Dialogs().ShowCustomDialogModal(
            shell, builder, dialog)
        if product_type is not None:
            self.load_product_types(product_type)
            self.update_edited_state()


    def remove_product_type_callback(self, _ux_control, _unused):
        """
        Remove the currently selected product type
        of the currently selected prime brokerage fund.
        """
        shell = self.layout_dialog.Shell()
        current_product_type = self.product_types[self.product_type_index]
        # FIXME: Only check if the product type details are edited.
        if self.edited:
            message = ("Discard the changes made to "
                       "the currently selected product type '{0}' "
                       "of the fund '{1}'?").format(
                           current_product_type,
                           self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button2": # The second button (No) has been pressed.
                self.w_product_type.SetData(self.product_type_index)
                return

        message = ("Are you sure you want to remove "
                   "the currently selected product type '{0}' "
                   "of the fund '{1}'?").format(
                       current_product_type,
                       self.pb_fund.fund_id)
        answer = show_question_window(shell, message)
        if answer == "Button2": # The second button (No) has been pressed.
            return

        acm_portfolio_swap = self.portfolio_swaps[self.product_type_index]
        self.pb_fund.remove_product_type_pswap(acm_portfolio_swap)
        information_message = ("Product type '{0}' "
                               "of the prime brokerage fund '{1}' "
                               "has been removed.").format(
                                   current_product_type,
                                   self.pb_fund.fund_id)
        print information_message
        self.load_product_types()
        self.update_edited_state()


    def generate_report_callback(self, _ux_control, _unused):
        """
        Launch the task for generating a report with the current values
        of all the accessible attributes of all the available
        prime brokerage funds.
        """
        import acm
        acm.RunModuleWithParameters("pb_fund_report", acm.GetDefaultContext())


    def view_text_object_callback(self, _ux_control, _unused):
        """
        Launch the window for viewing the text object
        representing the current prime brokerage fund.
        """
        import acm
        shell = self.layout_dialog.Shell()
        dialog = TextObjectEditDialog(self.text_object_id)
        builder = dialog.create_layout()
        acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


    def delete_text_object_callback(self, _ux_control, _unused):
        """
        Delete the text object representing the current prime brokerage fund.
        """
        shell = self.layout_dialog.Shell()
        if self.edited:
            message = ("Discard the changes made to "
                       "the currently selected fund '{0}'?").format(
                           self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button2": # The second button (No) has been pressed.
                return

        message = ("Are you sure you want to delete the text object '{0}' "
                   "representing the currently selected fund '{1}'?").format(
                       self.text_object_id,
                       self.pb_fund.fund_id)
        answer = show_question_window(shell, message)
        if answer == "Button2": # The second button (No) has been pressed.
            return

        self.pb_fund_storage.delete_fund(self.pb_fund.fund_id)
        self.pb_fund_storage.clean_up()
        self.pb_fund_storage.save()

        fund_id = self.pb_fund_storage.stored_funds.iterkeys().next()
        self.load_fund(fund_id)
        self.init_top_layout(self.top_layout)
        self.load_product_types()
        self.load_fund_attributes()
        self.make_edited(False)


    def make_edited(self, value=True):
        """
        Mark the current dialog as edited or not edited.
        """
        import acm
        if value:
            reddish = acm.UX().Colors().Create(195, 31, 0)
            self.w_notice.SetColor("Text", reddish)
            self.w_notice.SetData("edited")
            self.w_ok.Enabled(True)
            self.edited = True
        else:
            self.w_notice.SetData("")
            self.w_ok.Enabled(False)
            self.edited = False


    def update_edited_state(self):
        """
        Mark the current dialog as edited if at least one
        of the currently selected fund's attributes is marked as edited.
        """
        edited_state = False
        for gui_attribute in self.attributes.itervalues():
            if gui_attribute.edited:
                edited_state = True
                break
        self.make_edited(edited_state)


    def create_top_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used at the top of the main dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.BeginHorzBox()
        builder.AddOption("fund_id", "Fund ID")
        builder.AddLabel("number_of_funds", "(000)")
        builder.AddButton("generate_report", " Generate report...", False, True)
        builder.EndBox()
        builder.BeginHorzBox()
        builder.AddInput("text_object_id", "Text object ID")
        builder.AddButton("view_text_object", " View...", False, True)
        builder.AddButton("delete_text_object", " Delete...", False, True)
        builder.EndBox()
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddLabel("log_note",
                         "Please see the Python log for warnings and errors.")
        builder.AddFill()
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_top_layout(self, top_layout):
        """
        Initialize the GUI parts of the top layout.
        """
        import acm
        self.w_fund_id = top_layout.GetControl("fund_id")
        # remove the old list of the available Prime Brokerage funds
        self.w_fund_id.Clear()
        self.w_fund_id.ToolTip("The ID of the edited Prime Brokerage fund")
        self.w_fund_id.AddCallback(
            "Changed", self.fund_id_callback, self.w_fund_id)
        self.fund_ids = []
        for fund_id in sorted(self.pb_fund_storage.stored_funds):
            self.w_fund_id.AddItem(str(fund_id))
            # This is required for getting an index
            # of the currently selected fund ID.
            self.fund_ids.append(fund_id)
        index = self.fund_ids.index(self.pb_fund.fund_id)
        self.w_fund_id.SetData(index) # set the current fund as active
        self.w_fund_id.SetFocus()

        w_number_of_funds = top_layout.GetControl("number_of_funds")
        w_number_of_funds.ToolTip("The number of currently available "
                                  "prime brokerage funds")
        w_number_of_funds.SetData("({0})".format(len(self.fund_ids)))
        w_number_of_funds.SetStandardFont("Bold")
        w_number_of_funds.SetAlignment("Center")
        greenish = acm.UX().Colors().Create(30, 170, 30)
        w_number_of_funds.SetColor("Text", greenish)
        w_generate_report = top_layout.GetControl("generate_report")
        w_generate_report.ToolTip("Generate a report with the current values "
                                  "of all the accessible attributes of all "
                                  "the available prime brokerage funds.")
        w_generate_report.SetStandardFont("Bold")
        w_generate_report.AddCallback(
            "Activate", self.generate_report_callback, w_generate_report)

        self.w_text_object_id = top_layout.GetControl("text_object_id")
        self.w_text_object_id.ToolTip("The ID of the underlying "
                                      "custom text object")
        self.w_text_object_id.Editable(False)
        self.w_text_object_id.SetData(self.text_object_id)
        w_view_text_object = top_layout.GetControl("view_text_object")
        w_view_text_object.AddCallback(
            "Activate",
            self.view_text_object_callback,
            w_view_text_object)
        w_delete_text_object = top_layout.GetControl("delete_text_object")
        w_delete_text_object.AddCallback(
            "Activate",
            self.delete_text_object_callback,
            w_delete_text_object)
        w_log_note = top_layout.GetControl("log_note")
        w_log_note.SetAlignment("Center")


    def create_bottom_layout(self):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout that will be used at the bottom of the main dialog.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.BeginHorzBox()
        builder.AddFill()
        builder.AddLabel("quirks_note",
                         ("Star (*) indicates an attribute "
                          "which does not support history."),
                         False,
                         True)
        builder.AddFill()
        builder.EndBox()
        builder.BeginHorzBox()
        builder.AddButton(OK_BUTTON_ID, "Save")
        builder.AddFill()
        builder.AddLabel("notice", "..... loading  .....", False, True)
        builder.AddFill()
        builder.AddButton(CANCEL_BUTTON_ID, "Close")
        builder.EndBox()
        builder.EndBox()
        return builder


    def init_bottom_layout(self, bottom_layout):
        """
        Initialize the GUI parts of the bottom layout.
        """
        self.w_ok = bottom_layout.GetControl(OK_BUTTON_ID)
        self.w_ok.SetStandardFont("Bold")
        self.w_ok.Enabled(False)
        self.w_notice = bottom_layout.GetControl("notice")
        self.w_notice.SetStandardFont("Bold")
        self.w_notice.SetAlignment("Center")
        self.w_notice.SetData("")
        w_quirks_note = bottom_layout.GetControl("quirks_note")
        w_quirks_note.SetAlignment("Center")


    def create_product_type_layout(self, product_type_attributes):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout for the product-type-specific attributes.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        builder.BeginHorzBox("EtchedIn", "Product type")
        builder.AddOption("product_type", "", 30)
        builder.AddLabel("number_of_ptypes", "(000)")
        builder.AddFill()
        builder.AddButton("add_product_type",
                          " Add new...", True, True)
        builder.AddFill()
        builder.AddButton("remove_product_type",
                          " Remove selected ", True, True)
        builder.EndBox()
        for attribute in sorted(product_type_attributes,
                                key=lambda attribute:
                                attribute.attr_def.attr_id):
            attribute.create_layout(builder)
        builder.EndBox()
        return builder


    def init_product_type_layout(self,
                                 product_type_layout,
                                 product_type_attributes):
        """
        Initialize the GUI parts of the product type layout.
        """
        import acm
        self.w_product_type = product_type_layout.GetControl("product_type")
        self.w_product_type.ToolTip("A product type")
        self.w_product_type.AddCallback(
            "Changed", self.select_product_type_callback, self.w_product_type)
        self.w_number_of_ptypes = product_type_layout.GetControl(
            "number_of_ptypes")
        self.w_number_of_ptypes.ToolTip("The number of product types "
                                        "available for the currently selected "
                                        "prime brokerage fund")
        self.w_number_of_ptypes.SetStandardFont("Bold")
        self.w_number_of_ptypes.SetAlignment("Center")
        greenish = acm.UX().Colors().Create(30, 170, 30)
        self.w_number_of_ptypes.SetColor("Text", greenish)
        self.w_add_ptype = product_type_layout.GetControl(
            "add_product_type")
        self.w_add_ptype.AddCallback("Activate",
                                     self.add_product_type_callback,
                                     self.w_product_type)
        self.w_remove_ptype = product_type_layout.GetControl(
            "remove_product_type")
        self.w_remove_ptype.AddCallback("Activate",
                                        self.remove_product_type_callback,
                                        self.w_product_type)
        for attribute in product_type_attributes:
            attribute.init_layout(product_type_layout)


    def load_product_type(self, product_type_index):
        """
        Load the details about the product type with the provided index
        of the currently selected prime brokerage fund.
        """
        self.product_type_index = product_type_index
        product_type_name = self.product_types[self.product_type_index]
        print "Loading product type '{0}'".format(product_type_name)
        acm_portfolio_swap = self.portfolio_swaps[self.product_type_index]
        for attribute in self.product_type_attributes:
            attribute.load_attribute(acm_portfolio_swap)


    def load_product_types(self, product_type_to_select=None):
        """
        Load the product type layout with values
        of the currently loaded prime brokerage fund.
        Optionally, select the desired product type
        and load its attributes.
        """
        # remove old items relevant to the previously
        # selected prime brokerage fund
        self.w_product_type.Clear()
        # TODO: Handle situation when there are no product types.
        self.portfolio_swaps = self.pb_fund.get_product_type_pswaps()
        product_type_names = {}
        self.product_types = []
        for pswap in self.portfolio_swaps:
            name = self.pb_fund.get_pswap_product_type_name(pswap)
            if name in product_type_names:
                product_type_names[name] += 1
                name += " {0}".format(product_type_names[name])
            else:
                product_type_names[name] = 0
            self.product_types.append(name)
        indices = list(range(len(self.product_types)))
        indices.sort(key=lambda idx: self.product_types[idx].lower())
        self.portfolio_swaps = [self.portfolio_swaps[i] for i in indices]
        self.product_types = [self.product_types[i] for i in indices]
        for product_type in self.product_types:
            self.w_product_type.AddItem(product_type)
        self.w_number_of_ptypes.SetData("({0})".format(len(self.product_types)))
        if product_type_to_select is None:
            product_type_index = 0 # select the first product type
        else:
            try:
                product_type_index = self.product_types.index(
                    product_type_to_select)
            except ValueError:
                product_type_index = 0
        self.w_product_type.SetData(product_type_index)
        self.load_product_type(product_type_index)


    def create_attributes_layout(self, attributes):
        """
        Return a new instance of FUxLayoutBuilder
        with a layout for the provided attributes.
        """
        import acm
        builder = acm.FUxLayoutBuilder()
        builder.BeginVertBox()
        for attribute in sorted(attributes,
                                key=lambda attribute:
                                attribute.attr_def.attr_id):
            attribute.create_layout(builder)
        builder.EndBox()
        return builder


    def init_attributes_layout(self, attribute_layout, attributes):
        """
        Initialize the GUI parts of the provided attribute layout.
        """
        for attribute in attributes:
            attribute.init_layout(attribute_layout)


    def init_fund_layout(self):
        """
        Initialize the fund-specific parts of the GUI
        with values from the currently loaded prime brokerage fund.
        """
        if self.main_attributes:
            self.init_attributes_layout(self.main_pane_layout,
                                        self.main_attributes)
        if self.references_attributes:
            self.init_attributes_layout(self.references_pane_layout,
                                        self.references_attributes)
        if self.ids_attributes:
            self.init_attributes_layout(self.ids_pane_layout,
                                        self.ids_attributes)
        if self.rates_attributes:
            self.init_attributes_layout(self.rates_pane_layout,
                                        self.rates_attributes)
        if self.spreads_attributes:
            self.init_attributes_layout(self.spreads_pane_layout,
                                        self.spreads_attributes)


    def load_gui_attributes(self, attributes):
        """
        Load the values of the provided GUI attributes.
        """
        for attribute in attributes:
            attribute.load_attribute()


    def load_fund_attributes(self):
        """
        Load the GUI attributes with values
        from the currently loaded prime brokerage fund.
        """
        self.w_text_object_id.SetData(self.text_object_id)
        if self.main_attributes:
            self.load_gui_attributes(self.main_attributes)
        if self.references_attributes:
            self.load_gui_attributes(self.references_attributes)
        if self.ids_attributes:
            self.load_gui_attributes(self.ids_attributes)
        if self.rates_attributes:
            self.load_gui_attributes(self.rates_attributes)
        if self.spreads_attributes:
            self.load_gui_attributes(self.spreads_attributes)


    def set_fund_callbacks(self):
        """
        Set the callbacks on the fund-specific parts of the GUI.
        """
        for gui_attribute in self.attributes.itervalues():
            gui_attribute.set_callbacks(self)


    def HandleCreate(self, layout_dialog, main_layout):
        """
        Handle the dialog's create event.
        """
        self.layout_dialog = layout_dialog
        self.layout_dialog.Caption("Prime Brokerage Fund Maintenance Tool")

        # FIXME: Properly divide attributes and quirks into these categories
        self.product_type_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.PRODUCT_TYPE_CATEGORY]
        self.main_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.MAIN_CATEGORY]
        self.references_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.REFERENCES_CATEGORY]
        self.ids_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.IDS_CATEGORY]
        self.rates_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.RATES_CATEGORY]
        self.spreads_attributes = [
            attr for attr in self.attributes.itervalues()
            if attr.attr_def.category == \
                    AttributeDefinition.SPREADS_CATEGORY]

        self.top_layout = self.layout_dialog.AddTopLayout(
            "The TOP layout",
            self.create_top_layout())
        self.product_type_layout = self.layout_dialog.AddPane(
            "Product types",
            self.create_product_type_layout(self.product_type_attributes))
        if self.main_attributes:
            self.main_pane_layout = self.layout_dialog.AddPane(
                "Main",
                self.create_attributes_layout(self.main_attributes))
        if self.references_attributes:
            self.references_pane_layout = self.layout_dialog.AddPane(
                "References",
                self.create_attributes_layout(self.references_attributes))
        if self.ids_attributes:
            self.ids_pane_layout = self.layout_dialog.AddPane(
                "IDs",
                self.create_attributes_layout(self.ids_attributes))
        if self.rates_attributes:
            self.rates_pane_layout = self.layout_dialog.AddPane(
                "Rates",
                self.create_attributes_layout(self.rates_attributes))
        if self.spreads_attributes:
            self.spreads_pane_layout = self.layout_dialog.AddPane(
                "Spreads",
                self.create_attributes_layout(self.spreads_attributes))

        self.init_top_layout(self.top_layout)
        self.init_bottom_layout(main_layout)
        self.init_product_type_layout(self.product_type_layout,
                                      self.product_type_attributes)
        self.init_fund_layout()
        self.set_fund_callbacks()
        self.load_product_types()
        self.load_fund_attributes()


    def HandleApply(self):
        """
        Obtain the changed fund's attributes from the GUI
        and set them on the appropriate places (in a transaction).

        This function handles an event of pressing a button
        with name == "ok".
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Are you sure you want to save "
                       "the entered attributes "
                       "of the Prime Brokerage "
                       "fund '{0}'?").format(self.pb_fund.fund_id)
            answer = show_question_window(shell, message)
            if answer == "Button1": # The first button (Yes) has been pressed.
                try:
                    self.save_edited_quirks()
                except WrongValueError as exc:
                    print exc
                    show_information_window(shell, str(exc))
                    return
                self.pb_fund_storage.save_fund(self.pb_fund)
                self.make_attributes_not_edited()
                self.make_edited(False)
            else:
                information_message = "No changes have been saved."
                print information_message


    def HandleCancel(self):
        """
        If the current dialog has been edited,
        ask the user if they really want to close it.

        This function handles an event of pressing a button
        with name == "cancel".
        """
        if self.edited:
            shell = self.layout_dialog.Shell()
            message = ("Are you sure you want to close "
                       "the dialog and lose all changes?")
            answer = show_question_window(shell, message)
            if answer == "Button1": # The first button (Yes) has been pressed.
                information_message = "No changes have been saved."
                print information_message
                return True # The dialog will be closed
        else:
            return True # The dialog will be closed


def menu_launch(eii):
    """
    Launch the fund details dialog from the menu.

    The only provided parameter is of type FExtensionInvokationInfo.
    """
    import acm
    extension_object = eii.ExtensionObject()
    shell = extension_object.Shell()
    dialog = FundDetailsDialog()
    builder = dialog.create_bottom_layout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


def standalone_launch():
    """
    Launch the fund details dialog
    as a standalone application within Front Arena.
    The parent of this dialog will be the session manager.
    """
    import acm
    shell = acm.UX().SessionManager().Shell()
    dialog = FundDetailsDialog()
    builder = dialog.create_bottom_layout()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, builder, dialog)


#standalone_launch()
