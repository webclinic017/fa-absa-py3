import acm
import FUxCore  # pylint: disable=import-error

from GenericMandatesAuthorizationApi import requestMandateCreationAuthorization, requestMandateUpdateAuthorization, \
    getMandateAuthorizationStatus
from GenericMandatesAuthorizationCore import loadMandateCustomTextObject, isAuthorizationAuthorized, \
    isAuthorizationRejected
from GenericMandatesDefinition import Mandate, CreateMandateAndLimit, GetAllMandateQFNames, GetAllMandateQFNamesExcept
from GenericMandatesUtils import GetMandateSettingsParam
from GenericMandatesLogger import getLogger
from GenericMandatesConstants import MANDATE_GUI_BLOCKING, MANDATE_GUI_NON_BLOCKING, \
    MANDATE_QUERY_FOLDER_SPECIAL_NAME, MANDATE_QUERY_FOLDER_SELECT_FOLDERS_NAME, FPARAM_LIMIT_OWNER, \
    FPARAM_LIMIT_PROTECTION


MANDATE_TYPES = {"Counterparty": "FParty", "Portfolio": "FPhysicalPortfolio", "Trader Group": "FUserGroup"}
RGB_RED = 255
RGB_GREEN = 65200
RGB_WHITE = 16250871


class DialogEditMandate(FUxCore.LayoutTabbedDialog):
    def __init__(self, mandate=None):
        # pylint: disable=too-many-instance-attributes
        # Reasonable amount for this class
        self.__caption = None
        self.__dialog = None
        self.__shell = acm.UX().SessionManager().Shell()  # pylint: disable=no-member

        # GUI controls
        self.__edtMandateName = None
        self.__edtMandateActive = None
        self.__lstMandateType = None
        self.__edtTargetName = None
        self.__edtMandateStatus = None
        self.__btnSearch = None
        self.__btnSelectTarget = None
        self.__btnSelectQueryFolders = None
        self.__btnCreateQueryFolder = None
        self.__lstBlockTypeDropDown = None
        self.__lstQueryFolders = None
        self.__btnViewQuery = None
        self.__btnClearList = None
        self.__btnOk = None
        self.__limitSheet = None
        self._limits = None
        self._authorizations = None
        self.__edtDescription = None
        self.__modified = False

        # Authorize Tab
        self.__edtCreateTime = None
        self.__edtCreateUser = None
        self.__edtAmendmentTime = None
        self.__edtAmendmentUser = None
        self.__edtApproveTime = None
        self.__edtApproveUser = None
        self.__edtExpiryDate = None
        self.__authorizeSheet = None
        self.__btnRenewMandate = None

        # Mandated Traders tab
        self.__lstTraders = None

        self.__mandateTypeConfig = {}
        self.__mandateNamePrefix = GetMandateSettingsParam('MandateNamePrefix')
        self.__mandateType = None
        self.__mandateTarget = None
        self.__selectedQueryFolders = []
        self.__mandateBlocking = True
        self.__mandate = mandate
        self.__limit = None

        # Permissions related
        self.__user = acm.User()  # pylint: disable=no-member
        self.__newMandate = True

    def __LoadMandate(self):
        """
        Load the mandate details from the limit that was passed to the constructor. This method will populate all
        the fields on the dialog using the information extracted from the limit.
        """
        if self.__mandate:
            self.__newMandate = False
            self.__dialog.Caption('Edit mandate')
            self.__btnOk.Label('Update')
            self.__btnOk.Enabled(False)
            self.__selectedQueryFolders = []
            self.__limit = acm.FLimit[self.__mandate.LimitOid()]  # pylint: disable=no-member

            self.AddQueryFoldersToListView(self.__mandate.QueryFoldersObj())
            self.__selectedQueryFolders = self.__mandate.QueryFoldersObj()

            # Update Mandate name
            self.__edtMandateName.SetData(self.__mandate.Name())
            self.__edtDescription.SetData("%s" % self.__mandate.GetDescription())

            # Set active / inactive
            if self.__mandate.Status() == 'active':
                self.__edtMandateActive.SetData('Active')
                self.__edtMandateActive.SetColor('BackgroundReadonly', self.GetColor('GenericMandatesLightGreen'))
            else:
                self.__edtMandateActive.SetColor('BackgroundReadonly', self.GetColor('GenericMandatesLightRed'))
                self.__edtMandateActive.SetData('Inactive')

            # Update Blocking type on GUI
            if self.__mandate.IsBlocking():
                self.__lstBlockTypeDropDown.SetData(MANDATE_GUI_BLOCKING)
            else:
                self.__lstBlockTypeDropDown.SetData(MANDATE_GUI_NON_BLOCKING)

            # Update Mandate Type
            self.__mandateType = str(self.__mandate.Type())
            self.__lstMandateType.SetData("%s" % str(self.__mandate.Type()))

            # Update Mandated Entity
            self.__mandateTarget = "%s" % self.__mandate.Entity()
            self.__edtTargetName.SetData("%s" % self.__mandate.Entity())

            # Update Authorization Status message
            self.__RefreshStatusMessage()

            # Add Limit to Limit Sheet
            self.__AddLimitToSheet()
            self.__AddAuthorizationSheet()

            # Update Authorization Tab
            self.__edtCreateTime.SetData(self.__mandate.GetCreateTime())
            self.__edtCreateUser.SetData(self.__mandate.GetCreateUser())
            self.__edtAmendmentTime.SetData(self.__mandate.GetAmendTime())
            self.__edtAmendmentUser.SetData(self.__mandate.GetAmendUser())
            self.__edtApproveTime.SetData(self.__mandate.GetAuthTime())
            self.__edtApproveUser.SetData(self.__mandate.GetAuthUser())
            self.__edtExpiryDate.SetData(self.__mandate.GetExpireTime())

            # Load / Update Traders Tab
            if self.__mandate.Type() == 'Trader Group':
                tab3 = self.__dialog.AddPane("Mandated Traders", self.CreateTab3())
                tab3Ctrl = tab3.GetControl
                self.__lstTraders = tab3Ctrl('listMandatedTraders')
                self.__edtProductSupervisor = tab3Ctrl('edtProductSupervisor')
                self.__edtProductSupervisor.Editable(False)
                self.__edtProductSupervisor.SetData(",".join(self.__mandate.GetProductSupervisor()))

                userGroup = acm.FUserGroup[self.__mandate.Entity()]  # pylint: disable=no-member
                if userGroup:
                    self.__lstTraders.Clear()
                    root = self.__lstTraders.GetRootItem()

                    self.__lstTraders.ShowColumnHeaders()
                    self.__lstTraders.AddColumn("Username", 300)
                    self.__lstTraders.AddColumn("Date Accepted", 170)
                    self.__lstTraders.AddColumn("", 25)

                    for user in userGroup.Users():
                        child = root.AddChild()
                        child.Label(user.FullName(), 0) if user.FullName() else child.Label(user.Name(), 0)
                        child.Icon(user.Icon())
                        child.SetData(user)
                        if self.__mandate.IsAcceptedByTrader(user) is True:
                            # pylint: disable=no-member
                            child.Label('%s' % self.__mandate.GetTraderAcceptDate(user), 1)
                            child.Style(2, False, 0, RGB_GREEN)
                        else:
                            child.Style(2, False, 0, RGB_RED)
        else:
            self.__dialog.Caption('Create a new mandate')

    def IsModified(self):
        """
        Check if any of the editable fields on the GUI dialog have been edited.
        :return:
        """
        return self.__modified

    def Touch(self):
        self.__modified = True

    def CreateLayout(self):
        """
        Bottom layout of the GUI.
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('None')
        b.  BeginHorzBox('EtchedIn', '')
        b.    AddFill()
        b.    AddButton('ok', 'Save')
        b.    AddButton('cancel', 'Cancel')
        b.  EndBox()
        b.EndBox()
        return b

    def CreateTopLayout(self):
        """
        Top layout of the GUI.
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('EtchedIn')
        b.  BeginHorzBox('None', '')
        b.    AddInput('mandateName', 'Name', 46, 46)
        b.    AddInput('mandateActivationStatus', 'Active Status:', 10, 10)
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('mandateStatus', 'Authorization Status:', 75, 75)
        b.  EndBox()
        b.  BeginHorzBox('None')
        b.    AddInput('mandateDescription', 'Description:', 75, 75)
        b.  EndBox()
        b.EndBox()
        return b

    def CreateTab1(self):
        """
        Layout for the first tab "Definition".
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('None')
        b.    BeginVertBox('EtchedIn', 'Mandated Entity')
        b.      AddOption('mandateType', 'Type:')
        b.      BeginHorzBox()
        b.        AddInput('targetName', 'Name:')
        b.        AddButton('targetSelector', '...')
        b.      EndBox()
        b.      BeginHorzBox()
        b.      AddOption('mandateLimitType', 'Blocking:')
        b.      EndBox()
        b.      BeginHorzBox()
        b.      EndBox()
        b.    EndBox()
        b.    BeginVertBox('EtchedIn', 'Create query folder containing a custom method:')
        b.      AddFill()
        b.        AddButton('mandateCreateNewRule', 'Create QF')
        b.      EndBox()
        b.    BeginVertBox('EtchedIn', 'Linked query folders:')
        b.      AddFill()
        b.      AddList("listQueryFolders", 5, -1, 50)
        b.      BeginHorzBox('None')
        b.              AddFill()
        b.              AddButton('mandateRuleSelector', 'Select ...')
        b.              AddButton("btnClearList", "Clear List")
        b.              AddButton("btnViewQuery", "View Query")
        b.      EndBox()
        b.    EndBox()
        b.  BeginHorzBox('EtchedIn', 'Limit linked to Mandate:')
        b.    AddCustom('limitSheet', 'sheet.FLimitSheet', 400, 118)
        b.  EndBox()
        b.EndBox()
        return b

    def CreateTab2(self):
        """
        Layout for the 2nd tab "Authorizations".
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('None')
        b.  BeginHorzBox('EtchedIn', 'Business Process linked to Mandate:')
        b.    AddCustom('businessProcessSheet', 'sheet.FBusinessProcessSheet', 400, 118)
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Detail:')
        b.    BeginHorzBox('None')
        b.        AddInput('mandateCreateTime', 'Create Time:')
        b.        AddInput('mandateCreateUser', 'Create User:')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.        AddInput('mandateAmendmentTime', 'Amendment Time:')
        b.        AddInput('mandateAmendmentUser', 'Amendment User:')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.        AddInput('mandateApproveTime', 'Approve Time:')
        b.        AddInput('mandateApproveUser', 'Approve User:')
        b.    EndBox()
        b.    BeginHorzBox('None')
        b.        AddInput('mandateExpiry', 'Date Mandate Expires:')
        b.    EndBox()
        b.  EndBox()
        b.  BeginVertBox('EtchedIn', 'Request recertification:')
        b.      AddButton("btnRenewMandate", "Request")
        b.  EndBox()
        b.EndBox()
        return b

    def CreateTab3(self):
        """
        Layout for the 3rd tab "Traders".
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox('None')
        b.  BeginHorzBox('EtchedIn', 'Product Supervisor:')
        b.    AddInput('edtProductSupervisor', 'Username:')
        b.  EndBox()
        b.  BeginHorzBox('EtchedIn', 'Mandated Traders:')
        b.    AddList("listMandatedTraders", 5, -1, 50)
        b.  EndBox()
        b.EndBox()
        return b

    def GetColor(self, colorName):
        extension = acm.GetDefaultContext().GetExtension("FColor", acm.FColor, colorName)  # pylint: disable=no-member
        if extension:
            return extension.Value()

    def HandleCreate(self, dialog, layout):
        ctrl = layout.GetControl

        # Add the tab panes on the main layout
        topLayout = dialog.AddTopLayout("Top", self.CreateTopLayout())
        topLayoutCtrl = topLayout.GetControl
        tab1 = dialog.AddPane("Definition", self.CreateTab1())
        tab1Ctrl = tab1.GetControl
        tab2 = dialog.AddPane("Authorization", self.CreateTab2())
        tab2Ctrl = tab2.GetControl

        self.__dialog = dialog
        self.__dialog.Caption('Create new Mandate')

        self.__edtMandateName = topLayoutCtrl('mandateName')
        self.__edtMandateName.Editable = True
        self.__edtMandateName.ToolTip('This is the name of the mandate.')
        self.__edtMandateName.AddCallback('Changed', self.__OnChanged, None)

        self.__edtMandateActive = topLayoutCtrl('mandateActivationStatus')
        self.__edtMandateActive.Editable = False
        self.__edtMandateActive.ToolTip('Displays if the mandate is active or not.')
        self.__edtMandateActive.SetAlignment('Center')

        self.__edtMandateActive.SetColor('BackgroundReadonly', self.GetColor('GenericMandatesLightGreen'))

        self.__lstMandateType = tab1Ctrl('mandateType')
        self.__lstMandateType.AddCallback('Changed', self.__OnClickSelectEntityType, None)
        self.__lstMandateType.ToolTip('Select the appropriate type of entity who the mandate will apply to.')

        self.__edtTargetName = tab1Ctrl('targetName')
        self.__edtTargetName.Editable(False)
        self.__edtTargetName.ToolTip('Select the appropriate entity who the mandate will apply to.')
        self.__edtTargetName.AddCallback('Changed', self.__OnChanged, None)

        self.__edtMandateStatus = topLayoutCtrl('mandateStatus')
        self.__edtMandateStatus.Editable(False)
        self.__edtMandateStatus.ToolTip('Displays the current status of the authorization process for the mandate.')

        self.__btnSelectTarget = tab1Ctrl('targetSelector')
        self.__btnSelectTarget.AddCallback('Activate', self.__OnClickSelectTarget, None)
        self.__btnSelectTarget.AddCallback('Changed', self.__OnChanged, None)
        self.__btnSelectTarget.ToolTip('Click here to select an appropriate mandate target entity.')

        self.__btnSelectQueryFolders = tab1Ctrl('mandateRuleSelector')
        self.__btnSelectQueryFolders.AddCallback('Activate', self.__OnClickSelectRulesQueryFolder, None)
        self.__btnSelectQueryFolders.AddCallback('Changed', self.__OnChanged, None)
        self.__btnSelectQueryFolders.ToolTip('Select the query folders that will be used to filter trades that are '
                                             'allowed and not allowed for this mandate. Multiple query folders can be'
                                             'selected. Note: Once a query folder has been selected the permissions on '
                                             'it will be changed to read only for all users except the owner. The '
                                             'owner will also be changed to a system user.')

        self.__btnCreateQueryFolder = tab1Ctrl('mandateCreateNewRule')
        self.__btnCreateQueryFolder.AddCallback('Activate', self.__OnClickCreateQueryFolder, None)
        self.__btnCreateQueryFolder.ToolTip('This opens up the Query Folder application with "special" permission '
                                            'to allow the user to access FCustomMethods on objects. This enables '
                                            'the user to create selection criteria based on custom methods as well.')

        self.__lstBlockTypeDropDown = tab1Ctrl("mandateLimitType")
        self.__lstBlockTypeDropDown.AddCallback('Changed', self.__OnChangeBlockingType, None)
        self.__lstBlockTypeDropDown.ToolTip('Blocking mandates will not allow a trader to book a trade when the trade '
                                            'breaches the mandate. Non-Blocking mandates will allow the trader to book '
                                            'a trade. However, the trader will have to provide a comment or reason for '
                                            'this and a violation record will be created.')

        self.__lstQueryFolders = tab1Ctrl("listQueryFolders")
        self.__lstQueryFolders.ToolTip('This list view contains all the query folders that will be linked to the '
                                       'mandate.')

        self.__btnViewQuery = tab1Ctrl("btnViewQuery")
        self.__btnViewQuery.AddCallback('Activate', self.__OnClickViewQuery, None)
        self.__btnViewQuery.ToolTip('Click here to view the current query folder selected in the list view.')

        self.__btnClearList = tab1Ctrl("btnClearList")
        self.__btnClearList.AddCallback('Activate', self.__OnClickClearList, None)
        self.__btnClearList.ToolTip('Clear all the query folders in the list.')

        self.__edtDescription = topLayoutCtrl("mandateDescription")
        self.__btnOk = ctrl("ok")

        # Get controls for Tab 2
        self.__edtCreateTime = tab2Ctrl('mandateCreateTime')
        self.__edtCreateTime.Editable(False)
        self.__edtCreateUser = tab2Ctrl('mandateCreateUser')
        self.__edtCreateUser.Editable(False)
        self.__edtAmendmentTime = tab2Ctrl('mandateAmendmentTime')
        self.__edtAmendmentTime.Editable(False)
        self.__edtAmendmentUser = tab2Ctrl('mandateAmendmentUser')
        self.__edtAmendmentUser.Editable(False)
        self.__edtApproveTime = tab2Ctrl('mandateApproveTime')
        self.__edtApproveTime.Editable(False)
        self.__edtApproveUser = tab2Ctrl('mandateApproveUser')
        self.__edtApproveUser.Editable(False)
        self.__edtExpiryDate = tab2Ctrl('mandateExpiry')
        self.__edtExpiryDate.Editable(False)
        # self.__btnRequest.AddCallback('Activate', self.__OnClickSelectRulesQueryFolder, None)

        self.__btnRenewMandate = tab2Ctrl('btnRenewMandate')
        self.__btnRenewMandate.AddCallback('Activate', self.__OnClickRenewMandate, None)

        # Create Limit Sheet
        self.__limitSheet = tab1Ctrl("limitSheet").GetCustomControl()
        self.__SetUpLimitSheetColumns()

        # Create Business Process sheet on Authorize tab
        self.__authorizeSheet = tab2Ctrl('businessProcessSheet').GetCustomControl()
        self.__SetUpAuthorizationSheetColumns()

        self.__InitialiseControls()
        self.__LoadMandate()
        # self.__EnableOkButton()
        self.__btnOk.Enabled(False)
        self.__btnRenewMandate.Enabled(self.__EnableRenewMandateButton())

    def __EnableRenewMandateButton(self):
        """
        Check if the Renew Mandate button should be enabled or disabled.
        :return: bool
        """
        from GenericMandatesConstants import OPERATION_MODIFY
        if acm.User().IsAllowed(OPERATION_MODIFY, 'Operation'):  # pylint: disable=no-member
            if self.__mandate:
                return True if self.__mandate.Status() == 'active' else False
        else:
            return False

    def __EnableOkButton(self):
        """
        Enable and disable the 'Save' / 'Update' button on the dialog.
        """
        # Check if user has permission to create a new mandate
        from GenericMandatesConstants import OPERATION_CREATE, OPERATION_MODIFY
        if self.__newMandate is True:
            if not self.__user.IsAllowed(OPERATION_CREATE, 'Operation'):
                self.__btnOk.Enabled(False)
            else:
                self.__btnOk.Enabled(True)
        else:
            self.__edtDescription.Editable(False)
            if not self.__user.IsAllowed(OPERATION_MODIFY, 'Operation'):
                self.__btnOk.Enabled(False)
            else:
                self.__btnOk.Enabled(True)

    def __SetUpLimitSheetColumns(self):
        columns = self.__limitSheet.ColumnCreators()
        columns.Clear()

        # Populate the limit sheet columns
        extContext = acm.GetDefaultContext()  # pylint: disable=no-member
        col = ('Limit Specification Name', 'Limit Path L1', 'Mandate Blocking Type')
        defaultColumns = acm.GetColumnCreators(col, extContext)  # pylint: disable=no-member
        for i in range(defaultColumns.Size()):
            columns.Add(defaultColumns.At(i))

    def __AddLimitToSheet(self):
        # Insert the query folder into the limit sheet
        self.__InitialiseLimit()
        self.__limitSheet.RemoveAllRows()
        self.__limitSheet.InsertObject(self._limits, 'IOAP_LAST')
        self.__limitSheet.PrivateTestSyncSheetContents()

    def __SetUpAuthorizationSheetColumns(self):
        extContext = acm.GetDefaultContext()  # pylint: disable=no-member
        columns = self.__authorizeSheet.ColumnCreators()
        columns.Clear()
        col = ('Product Support Approval', )
        bpColumns = acm.GetColumnCreators(col, extContext)  # pylint: disable=no-member
        for i in range(bpColumns.Size()):
            # columns.Add(bpColumns.At(i))
            self.__authorizeSheet.ColumnCreators().Add(bpColumns.At(i))

    def __AddAuthorizationSheet(self):
        # Insert item into business process sheet (Authorization)
        self.__InitialiseBusinessProcess()
        self.__authorizeSheet.RemoveAllRows()
        self.__authorizeSheet.InsertObject(self._authorizations, 'IOAP_LAST')
        self.__authorizeSheet.PrivateTestSyncSheetContents()

    def __InitialiseLimit(self):
        """
        Create FASQLQueryFolder that will be used to populate the limits in the limit sheet that is displayed in the
        pre-deal check window.
        """
        getLogger().debug("__InitialiseLimits() executing")
        limit = acm.FLimit[self.__mandate.LimitOid()]  # pylint: disable=no-member
        if limit:
            self._limits = acm.FASQLQueryFolder()
            self._limits.Name('Temp_Query')
            query = acm.CreateFASQLQuery('FLimit', 'OR')  # pylint: disable=no-member

            getLogger().debug('Add limit to query: %s' % limit.Oid())
            query.AddOpNode('OR')
            query.AddAttrNode('Oid', 'EQUAL', limit.Oid())

            self._limits.AsqlQuery(query)

    def __InitialiseBusinessProcess(self):
        """
        Create FASQLQueryFolder that will be used to populate the limits in the limit sheet that is displayed in the
        pre-deal check window.
        """
        getLogger().debug("__InitialiseBusinessProcess() executing")
        # pylint: disable=no-member
        limit = acm.FLimit[self.__mandate.LimitOid()]
        if limit:
            mandate = acm.FCustomTextObject.Select01("name=\"%s\"" % limit.Oid(), "Could not load mandate")
            if mandate:
                self._authorizations = acm.FASQLQueryFolder()
                self._authorizations.Name('Authorization')
                query = acm.CreateFASQLQuery(acm.FBusinessProcess, 'OR')
                node = query.AddOpNode('AND')
                node.AddAttrNode('Subject_seqnbr', 'EQUAL', mandate.Oid())
                self._authorizations.AsqlQuery(query)

    def HandleApply(self):
        getLogger().debug('HandleApply() executed')

        # Check if there is a pending authorization process currently
        if self.__mandate:
            # pylint: disable=no-member
            selection = acm.FBusinessProcess.Select('subject_seqnbr = %i' % self.__mandate.LimitOid())
            bp = selection[0]
            if isAuthorizationRejected(bp) is False and isAuthorizationAuthorized(bp) is False:
                getLogger().info("Authorization pending on Mandate.")
                msg = "There is currently an authorization process pending on this mandate. Do you want to save the " \
                      "Mandate and restart the authorization process?"
                if self.__MessageBoxYesNo("Question", msg) is not True:
                    return None

        # Check if a mandate already exists with this name
        if acm.FLimit[self.__edtMandateName.GetData()] and self.__newMandate is True:  # pylint: disable=no-member
            msg = "A mandate with this name already exists. Please choose a different name."
            self.__ShowMessageBoxInformation(msg)
            return None

        # Check if all the fields are filled in
        if self.__mandateType and self.__mandateTarget and self.__selectedQueryFolders and self.__edtMandateName:
            # Check if the query folders are used in other mandates
            getLogger().debug("Check if query folder is used in other mandates.")
            if self.__mandate:
                queryFolderNames = GetAllMandateQFNamesExcept(self.__mandate.Name())
            else:
                queryFolderNames = GetAllMandateQFNames()
            for folder in self.__selectedQueryFolders:
                selected = acm.FStoredASQLQuery.Select('name="%s"' % folder.Name())  # pylint: disable=no-member

                # Check if the Query Folder is linked to another mandate
                if folder.Name() in queryFolderNames :
                    self.__ShowMessageBoxInformation("Error: The query folder that you have selected is already "
                                                     "linked to another mandate.")
                    return None
                # Check if the protection rights are correct on the mandate
                elif folder.MayChangeProtection() is False:
                    self.__ShowMessageBoxInformation("Error: You do not have permission to change ownership or "
                                                     "permissions on this query folder. Please select another query "
                                                     "folder.")
                    return None
                elif len(selected) > 1:
                    self.__ShowMessageBoxInformation("Error: There are duplicate copies of the query folder in the "
                                                     "database. Please remove the duplicates before linking this query "
                                                     "folder to the mandate.")
                    return None


            # Retrieve the Limit / Query Folder owner and protection
            protection = int(GetMandateSettingsParam(FPARAM_LIMIT_PROTECTION))
            owner = acm.FUser[GetMandateSettingsParam(FPARAM_LIMIT_OWNER)]  # pylint: disable=no-member

            # If update request. i.e when existing data is available and mandate is currently active
            if self.__mandate and (self.__limit or acm.FLimit[self.__mandate.LimitOid()]):
                # Prompt the user to confirm overwriting the existing mandate in the DB
                msg = "A %s mandate already exists for %s. Are you SURE you want to overwrite this existing " \
                      "mandate with these changes?" % (self.__mandateType, self.__mandateTarget)

                # If user confirm override prompt
                if self.__MessageBoxYesNo("Question", msg) is True:
                    reason = self.__MessageBoxPromptText('Reason for change', 'Reason for change ...')
                    if reason:
                        # Load mandate as text object
                        mandateTextObj = loadMandateCustomTextObject(self.__mandate.LimitOid())

                        # Start authorization process for update
                        # pylint: disable=no-member
                        getLogger().debug("Updating Authorization Time stamp on mandate")
                        self.__mandate.SetAmendTime(acm.Time.TimeNow())
                        self.__mandate.SetAmendUser(acm.User().Name())
                        self.__mandate.SetName(self.__edtMandateName.GetData())
                        # self.__mandate.SetOwnerAndProtectionOnQueryFoldersAndLimit(owner, protection)
                        self.__mandate.Commit()
                        result = requestMandateUpdateAuthorization(mandateTextObj,
                                                                   self.__mandateTarget,
                                                                   self.__mandateType,
                                                                   self.__selectedQueryFolders,
                                                                   self.__mandateBlocking,
                                                                   True, reason)
                        # If request was successful
                        if result is True:
                            self.__ShowMessageBoxInformation("The mandate update request was successfully submitted "
                                                             "for approval.")

                            # Close the dialog
                            return True
                        else:
                            self.__ShowMessageBoxInformation("Error: The mandate update request was not submitted for "
                                                             "approval. \nDetails:\n%s" % result)

            # If creation request. i.e. no existing data is available
            else:
                # Create a brand new mandate
                getLogger().debug("Creating a new mandate.")
                limitOid = CreateMandateAndLimit(str(self.__edtMandateName.GetData()),
                                                 self.__mandateType,
                                                 self.__mandateTarget,
                                                 self.__selectedQueryFolders,
                                                 self.__mandateBlocking)
                # If mandate created in ADS
                if limitOid > 0:
                    # pylint: disable=no-member
                    limit = acm.FLimit[limitOid]
                    self.__mandate = Mandate(limit)
                    self.__mandate.SetType(self.__mandateType)
                    self.__mandate.SetEntity(self.__mandateTarget)
                    self.__mandate.SetBlocking(self.__mandateBlocking)
                    self.__mandate.SetCreateTime(acm.Time.TimeNow())
                    self.__mandate.SetCreateUser(acm.User().Name())
                    self.__mandate.SetName(self.__edtMandateName.GetData())
                    #JS>use default protections
                    #self.__mandate.SetOwnerAndProtectionOnQueryFoldersAndLimit(owner, protection)
                    #JS>END
                    
                    if self.__edtDescription.GetData():
                        self.__mandate.SetDescription(str(self.__edtDescription.GetData()))
                    else:
                        self.__mandate.SetDescription("No description provided.")

                    getLogger().debug("Commit Mandate text object to DB")
                    self.__mandate.Commit()
                    getLogger().debug("Done committing text object.")

                    # Load mandate as text object
                    mandate = loadMandateCustomTextObject(self.__mandate.LimitOid())
                    #mandate.Owner(owner)
                    #mandate.Protection(protection)
                    
                    # Initialize the authorization process for creation
                    result = requestMandateCreationAuthorization(mandate,
                                                                 self.__mandateType,
                                                                 self.__selectedQueryFolders,
                                                                 self.__mandateBlocking,
                                                                 self.__mandateTarget,
                                                                 'New mandate - No comment required.',
                                                                 self.__mandate.Name(),
                                                                 self.__mandate.GetDescription())

                    # If request was successful
                    if result:
                        # Close dialog
                        return True
                    else:
                        getLogger().debug("Removing mandate and limit.")
                        self.__ShowMessageBoxInformation("Error: The mandate creation request was not submitted for"
                                                         " approval. See log.")
        else:
            msg = "Could not create mandate. Not all fields are filled in."
            self.__ShowMessageBoxInformation(msg)
            getLogger().warn(msg)

    def OnCancel(self, _params, _cd):
        del _params
        del _cd
        getLogger().debug("OnCancel() executed")

    def __InitialiseControls(self):
        self.__edtMandateName.SetData('%s/' % self.__mandateNamePrefix)

        # Init mandate types
        for mandateType in list(MANDATE_TYPES.keys()):
            self.__lstMandateType.AddItem(mandateType)
        self.__lstMandateType.SetData(list(MANDATE_TYPES.keys())[0])

        # Init block types
        self.__lstBlockTypeDropDown.AddItem(MANDATE_GUI_BLOCKING)
        self.__lstBlockTypeDropDown.AddItem(MANDATE_GUI_NON_BLOCKING)
        self.__lstBlockTypeDropDown.SetData(MANDATE_GUI_BLOCKING)

    # def __OnClickSearch(self, _params, _cd):
    #     """
    #     Credit Limits Check button handler.
    #     :param _params:
    #     :param _cd:
    #     """
    #     del _params
    #     del _cd
    #
    #     getLogger().info('__OnClickSearch() executing')
    #     getLogger().debug('GUI has been edited: %s' % self.IsModified())
    #     mandateNames = acm.FArray()
    #
    #     limitOids = GetAllMandateLimitOids()
    #
    #     for limitOid in limitOids:
    #         limit = acm.FLimit[limitOid]
    #         if limit:
    #             mandateNames.Add(limit.Name())
    #
    #     selected = acm.UX().Dialogs().SelectObject(acm.UX().SessionManager().Shell(),
    #                                                "Select mandate",
    #                                                "Mandate description",
    #                                                mandateNames,
    #                                                "A")
    #     if selected:
    #         self.__mandate = Mandate(acm.FLimit[selected])
    #         self.__LoadMandate()

    def __OnChanged(self, _params, _cd):
        del _params
        del _cd
        getLogger().debug('OnChanged executing')
        self.__EnableOkButton()

    def __OnClickSelectEntityType(self, _params, _cd):
        """
        OnClick event handler for the dropdown list containing the Mandate types.
        :param _params:
        :param _cd:
        """
        del _params
        del _cd
        getLogger().debug('OnClickSelectEntityType() executed')
        self.__EnableOkButton()
        self.__mandateType = self.__lstMandateType.GetData()

    def __OnClickSelectTarget(self, _params, _cd):
        """
        On click event handler for the "Select Target" button.
        :param _params:
        :param _cd:
        """
        del _params
        del _cd

        getLogger().debug('OnSelectTarget() executed')
        self.__mandateType = self.__lstMandateType.GetData()

        if self.__mandateType:
            # Check if the user has selected a "Target Type"
            associatedTargetType = MANDATE_TYPES[self.__mandateType]
            # pylint: disable=no-member
            selectedObject = acm.UX().Dialogs().SelectObjectsInsertItems(acm.UX().SessionManager().Shell(),
                                                                         associatedTargetType,
                                                                         False)
            if selectedObject:
                # Check if the user has selected a Target
                self.__mandateTarget = selectedObject.Name()
                getLogger().debug("Selected target: %s" % selectedObject.Name())
                self.__edtTargetName.SetData("%s" % self.__mandateTarget)


                self.__edtMandateName.SetData("%s/%s/%s" % (self.__mandateNamePrefix,
                                                            self.__mandateType,
                                                            self.__mandateTarget))
                self.Touch()
                getLogger().debug('GUI has been edited: %s' % self.IsModified())
        else:
            getLogger().warn("Please select a mandate and try again.")
            msg = 'Please select a Mandate Type and try again.'
            acm.UX().Dialogs().MessageBoxOKCancel(self.__shell, 'Warning', msg)  # pylint: disable=no-member

    def __OnClickCreateQueryFolder(self, _params, _cd):
        """
        On CLick event handler for the create new query folder button.
        :param _params:
        :param _cd:
        """
        del _params
        del _cd

        getLogger().debug('__OnClickCreateQueryFolder() executed')
        # pylint: disable=no-member
        mandateQueryTemplate = acm.FStoredASQLQuery[MANDATE_QUERY_FOLDER_SPECIAL_NAME]

        if mandateQueryTemplate is None:
            # Create Trade Filter Template
            query = acm.FASQLQuery()
            query.AsqlQueryClass = 'FTrade'

            mandateQueryTemplate = acm.FStoredASQLQuery()
            mandateQueryTemplate.Query = query
            mandateQueryTemplate.SubType = 'tradeFilterConfig'
            mandateQueryTemplate.Name = MANDATE_QUERY_FOLDER_SPECIAL_NAME
            mandateQueryTemplate.Commit()
            getLogger().info("Created template query folder (%s)" % MANDATE_QUERY_FOLDER_SPECIAL_NAME)

        newMandateRuleSetName = self.__edtMandateName.GetData()
        newMandateQf = acm.FStoredASQLQuery[MANDATE_QUERY_FOLDER_SPECIAL_NAME]

        if newMandateQf is None:
            newMandateQf = mandateQueryTemplate.StorageImage()
            newMandateQf.StorageSetNew()
            newMandateQf.Name = newMandateRuleSetName
            newMandateQf.Commit()
        acm.StartApplication('Insert Items', newMandateQf)

    def __OnClickSelectRulesQueryFolder(self, _params, _cd):
        """
        On CLick event handler for the create query folder button.
        :param _params:
        :param _cd:
        """
        del _params
        del _cd
        getLogger().debug("__OnClickSelectRulesQueryFolder() executing")
        # pylint: disable=no-member
        query = acm.FStoredASQLQuery[MANDATE_QUERY_FOLDER_SELECT_FOLDERS_NAME]

        if query is None:
            # Create Trade Filter Template
            query = acm.CreateFASQLQuery(acm.FStoredASQLQuery, 'OR')
            node = query.AddOpNode('OR')
            node.AddAttrNode('Name', 'RE_LIKE_NOCASE', "%s*" % self.__mandateNamePrefix)
            getLogger().info("Created template query folder (%s)" % MANDATE_QUERY_FOLDER_SELECT_FOLDERS_NAME)

        panel = InsertItemsPanel(self)
        parentDialog = acm.StartFASQLEditor("Add Query Folders to Mandate Definition", None, None, query, None, '',
                                            True, panel)
        panel.SetParentDialog(parentDialog)

    def __OnClickRenewMandate(self, _params, _cd):
        """
        OnClick event for the "Renew Mandate" button.
        :param _params:
        :param _cd:
        :return:
        """
        getLogger().debug('__OnClickRenewMandate() executing')
        del _params
        del _cd

        selection = self._authorizations.AsqlQuery().Select()
        if len(selection) > 1:
            getLogger().error('[ERROR] More than one authorization business process is linked to this Mandate.')
        else:
            msg = "Are you sure you want to recertify this Mandate? \n\nThis will follow the same authorization " \
                  "process as amending mandates."
            if self.__MessageBoxYesNo("Question", msg) is True:
                getLogger().debug('Recertify mandate (%s)' % self.__mandate.LimitOid())

                reason = 'Mandate Recertification requested.'
                mandateTextObject = loadMandateCustomTextObject(self.__mandate.LimitOid())
                requestMandateUpdateAuthorization(mandateTextObject, '%s' % self.__mandate.Entity(),
                                                  self.__mandate.Type(), self.__mandate.QueryFoldersObj(),
                                                  self.__mandate.IsBlocking(), False, reason)
                requestMandateUpdateAuthorization(mandateTextObject, '%s' % self.__mandate.Entity(),
                                                  self.__mandate.Type(), self.__mandate.QueryFoldersObj(),
                                                  self.__mandate.IsBlocking(), True, reason)
                getLogger().debug('Mandate Recertification requested.')

    def AddQueryFoldersToListView(self, queryFolders):
        """
        Add the array of Query Folders to the list view in the dialog.
        :param queryFolders: array of FStoredASQLQuery
        """
        getLogger().debug("AddQueryFoldersToListView() executing")
        self.__lstQueryFolders.Clear()
        root = self.__lstQueryFolders.GetRootItem()
        self.__selectedQueryFolders = queryFolders

        for qf in queryFolders:
            child = root.AddChild()
            child.Label(qf.Name())
            child.Icon(qf.Icon())
            child.SetData(qf)

        self.Touch()
        self.__OnChanged(None, None)
        getLogger().debug('GUI has been edited: %s' % self.IsModified())

    def __OnChangeBlockingType(self, params, cd):
        del params
        del cd
        getLogger().debug("__OnChangeBlockingType() executing")
        self.__EnableOkButton()
        blockingMap = {MANDATE_GUI_BLOCKING: True, MANDATE_GUI_NON_BLOCKING: False}
        selection = self.__lstBlockTypeDropDown.GetData()
        self.__mandateBlocking = blockingMap[selection]

        getLogger().debug('GUI has been edited: %s' % self.IsModified())

    def __OnClickViewQuery(self, params, cd):
        del params
        del cd
        getLogger().debug("__OnClickViewQuery() executing")

        if self.__lstQueryFolders.GetSelectedItem():
            queryFolder = self.__lstQueryFolders.GetSelectedItem().GetData()
            acm.StartApplication('Insert Items', queryFolder)  # pylint: disable=no-member
        else:
            self.__ShowMessageBoxInformation('Select a Query Folder to view.')

    def __OnClickClearList(self, params, cd):
        del params
        del cd
        getLogger().debug("__OnClickClearList() executing")
        self.__lstQueryFolders.Clear()
        self.Touch()
        getLogger().debug('GUI has been edited: %s' % self.IsModified())

    def __ShowMessageBoxInformation(self, message):
        """
        Display a dialog with a message and a single 'OK' button.
        :param message: string - Message to display
        :return: None
        """
        acm.UX().Dialogs().MessageBoxInformation(self.__shell, message)  # pylint: disable=no-member

    def __MessageBoxYesNo(self, title, message):
        """
        Display a dialog showing a message with a 'Yes' and a 'No' button.
        :param title: string - Title of the dialog
        :param message: string - Message of the dialog
        :return: boolean
        """
        answer = acm.UX().Dialogs().MessageBoxYesNo(self.__shell, title, message)  # pylint: disable=no-member
        if answer == 'Button1':
            return True
        return False

    def __MessageBoxPromptText(self, caption, initialText):
        """
        Display a dialog prompting the user to type in a reason for requesting a Mandate change.
        :param caption:
        :param initialText:
        :return: string
        """
        msg = acm.UX().Dialogs().GetTextInput(self.__shell, caption, initialText)  # pylint: disable=no-member
        if msg:
            # Check if the user clicked on Cancel
            return msg

    def __RefreshStatusMessage(self):
        # pylint: disable=no-member
        if self.__limit or acm.FLimit[self.__mandate.LimitOid()]:
            # Load mandate if not yet loaded
            if not self.__mandate:
                self.__mandate = Mandate(acm.FLimit[self.__mandate.LimitOid()])

            status = getMandateAuthorizationStatus(loadMandateCustomTextObject(self.__mandate.LimitOid()))

            if status is None:
                status = "Mandate authorization status not available"

        else:
            status = "Mandate not created yet"

        self.__edtMandateStatus.SetData(status)

    def SetSelectedQueryFolders(self, queryFolders):
        self.__selectedQueryFolders = queryFolders
        getLogger().debug('Added: %s' % self.__selectedQueryFolders)


class InsertItemsPanel(FUxCore.LayoutPanel):
    """
    This class defines the panel that will be displayed at the bottom of the Insert Items dialog when the user selects
    query folders to add to the mandate definition.
    It will consist of a "Open" button and an Edit Box that displays the amount of items selected.
    """
    def __init__(self, createGuiDialog):
        self._selected = []
        self.m_open = None
        self.m_selectedCount = None
        self.parentDialog = None
        self.createGuiDialog = createGuiDialog

    def GetSelected(self):
        return self._selected

    def UpdateControls(self):
        self._selected = self.Owner().Selection()
        self.m_selectedCount.SetData(self._selected.Size())
        self.m_open.Enabled(1 <= self._selected.Size())

    def ServerUpdate(self, sender, aspect, parameter):
        del sender, parameter
        if str(aspect) == str('SelectionChanged'):
            self.UpdateControls()

    def HandleCreate(self):
        layout = self.SetLayout(self.BuildLayout())
        self.m_open = layout.GetControl('buttonOpen')
        self.m_selectedCount = layout.GetControl('selectedCount')

        self.m_selectedCount.Editable(False)
        self.m_open.Enabled(False)
        self.m_open.AddCallback("Activate", self.OnClickInsertItems, self)

        self.Owner().AddDependent(self)
        self.UpdateControls()

    def BuildLayout(self):
        """
        Layout panel that will be docked at the bottom of the "Insert Items" dialog.
        :return: FUxLayoutBuilder
        """
        b = acm.FUxLayoutBuilder()  # pylint: disable=no-member
        b.BeginVertBox()
        b.  BeginHorzBox('EtchedIn', 'Mandates - Insert Query Folders')
        b.      AddButton('buttonOpen', 'Select')
        b.      AddInput('selectedCount', 'Selected items')
        b.  EndBox()
        b.EndBox()
        return b

    def OnClickInsertItems(self, a, b):
        del a, b
        if len(self._selected) > 0:
            self.createGuiDialog.AddQueryFoldersToListView(self._selected)
            self.createGuiDialog.SetSelectedQueryFolders(self._selected)
        self.parentDialog.Close()

    def SetParentDialog(self, parent):
        self.parentDialog = parent


def LaunchFromMenu(eii):
    """
    Method called from button in the ribbon. Displays the GUI interface.
    :param eii: FExtensionInvokationInfo
    """
    shell = eii.Parameter('shell')
    dialog = DialogEditMandate()
    acm.UX().Dialogs().ShowCustomDialogModal(shell, dialog.CreateLayout(), dialog)
