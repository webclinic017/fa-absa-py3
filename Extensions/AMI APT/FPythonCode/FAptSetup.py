
import acm
import FLogger

logger = FLogger.FLogger.GetLogger('APT')


class FAPTSetup(object):
    DATASTREAM = 'DATASTREAM'
    SEDOL = 'SEDOL'
    RECORD_TYPE = 'Instrument'
    APT_BORROWER_CLASS = 'APT Borrower Classification'
    APT_BORROWER_CLASS_MASTER = "Party Choice Lists"
    APT_BORROWER_CLASS_CHOICES = ['Banks', 'Consumer Services', 'Financial Services', 'Government',
                                  'Insurance', 'Manufacturing', 'Public authorities', 'Real Estate', 
                                  'Resources', 'Supranationals', 'Swap', 'Technology', 'Transportation',
                                  'Utilities']
    APT_BBG_INDUSTRY = ['BB_Industry_Group', 'BB_Industry_Sector', 'BB_Industry_SubGrp']

    APT_EXPORT_TYPE = 'APT Export Type'
    APT_EXPORT_TYPE_CHOICES = ['CONTRACT PARAMS', 'DELTA APPROX', 'SYNTH APPROX', 'UNDERLYING']

    APT_RECON_ID_TYPE = 'APT Recon Id Type'
    APT_RECON_ID_TYPE_CHOICES = ['DATASTREAM', 'ISIN', 'SEDOL', 'OTC']

    APT_SERVICE_FEE = 'APT Service Fee'

    APT_MBS_TYPE = 'APT MBS Type'
    APT_MBS_TYPE_CHOICES = ['CONV15', 'CONV30', 'GNMA1', 'GNMA2']

    @classmethod
    def _get_choice_list(cls, cl_name, cl_master_name):
        cl = acm.FChoiceList.Select01('name = "%s" and list = "%s"' % (cl_name, cl_master_name), '')
        return cl

    @classmethod
    def _create_alias_spec(cls, alias_spec_name, alias_spec_descr):
        alias_spec = acm.FInstrAliasType()
        alias_spec.Name(alias_spec_name)
        alias_spec.AliasTypeDescription(alias_spec_descr)
        try:
            alias_spec.Commit()
            logger.info('Created Alias Type Spec: %s', alias_spec_name)
        except Exception as err:
            raise err

    @classmethod
    def _create_add_info_spec_str(cls, add_info_spec_name, record_type):
        add_info_spec = acm.FAdditionalInfoSpec()
        add_info_spec.Name(add_info_spec_name)
        add_info_spec.FieldName(add_info_spec_name)
        add_info_spec.RecType(record_type)
        add_info_spec.DataTypeGroup('Standard')
        add_info_spec.DataTypeType(3)
        try:
            add_info_spec.Commit()
            logger.info('Created Additional Info Spec: %s', add_info_spec_name)
        except Exception as err:
            raise err

    @classmethod
    def _create_add_info_spec_double(cls, add_info_spec_name, record_type):
        add_info_spec = acm.FAdditionalInfoSpec()
        add_info_spec.Name(add_info_spec_name)
        add_info_spec.FieldName(add_info_spec_name)
        add_info_spec.RecType(record_type)
        add_info_spec.DataTypeGroup('Standard')
        add_info_spec.DataTypeType(4)
        try:
            add_info_spec.Commit()
            logger.info('Created Additional Info Spec: %s', add_info_spec_name)
        except Exception as err:
            raise err

    @classmethod
    def _create_add_info_spec_cl(cls, add_info_spec_name, record_type):
        add_info_spec = acm.FAdditionalInfoSpec()
        add_info_spec.Name(add_info_spec_name)
        add_info_spec.Description(add_info_spec_name)
        add_info_spec.FieldName(add_info_spec_name)
        add_info_spec.RecType(record_type)
        add_info_spec.DataTypeGroup('RecordRef')
        add_info_spec.DataTypeType(32)
        try:
            add_info_spec.Commit()
            logger.info('Created Additional Info Spec: %s', add_info_spec_name)
        except Exception as err:
            raise err

    @classmethod
    def _update_choice_list_name(cls, free5_chlnbr):
        free5_chlnbr_name = free5_chlnbr.Name()
        free5_chlnbr.Name(cls.APT_BORROWER_CLASS)
        try:
            free5_chlnbr.Commit()
            logger.info("Updated Choice List name %s to %s", free5_chlnbr_name, cls.APT_BORROWER_CLASS)
        except Exception as err:
            raise err
        cl = cls._get_choice_list(free5_chlnbr_name, "MASTER")
        if cl:
            cl.Name(cls.APT_BORROWER_CLASS)
            try:
                cl.Commit()
            except Exception as err:
                raise err

    @classmethod
    def _create_choices(cls, choices, list_name):
        for order, cl_name in enumerate(choices):
            choice = cls._get_choice_list(cl_name, list_name)
            if not choice:
                choice = acm.FChoiceList()
                choice.Name(cl_name)
                choice.List(list_name)
                choice.SortOrder(order)
                try:
                    choice.Commit()
                    logger.info("Added choice %s to Choice List %s", cl_name, list_name)
                except Exception as err:
                    raise err

    @classmethod
    def _create_free_choice_list(cls, cl_name, list_name):
        cl = cls._get_choice_list(cl_name, list_name)
        if not cl:
            new_cl = acm.FChoiceList()
            new_cl.Name(cl_name)
            new_cl.List(list_name)
            try:
                new_cl.Commit()
                logger.info("Created Choice List %s", cl_name)
                return new_cl

            except Exception as err:
                raise err

    @classmethod
    def _create_party_choice_list(cls):
        cl_name = cls.APT_BORROWER_CLASS_MASTER
        list = cls._get_choice_list(cl_name, "MASTER")
        if not list:
            list = cls._create_free_choice_list("%s"%cl_name, "MASTER")
        choices = list.Choices()
        if choices.Size() > 4:
            free5_chlnbr = choices.At(4)
            if free5_chlnbr.Choices():
                print ('Error adding APT Borrower Classification to Party Choices Lists at position 5. '\
                       'Party Choices Lists already contains a choice list in that position: %s '\
                       'with choices in it' % free5_chlnbr.Name())
                raise Exception('Error adding APT Borrower Classification to Party Choices Lists at position 5. See python log for details')
            cls._update_choice_list_name(free5_chlnbr)
        else:
            cl_name = cls.APT_BORROWER_CLASS
            cls._create_free_choice_list(cl_name, list.Name())

    @classmethod
    def _create_choice_list(cls, cl_name):
        if cl_name == cls.APT_BORROWER_CLASS:
            cls._create_party_choice_list()
        else:
            list = cls._get_choice_list(cl_name, "MASTER")
            if not list:
                list = cls._create_free_choice_list("%s"%cl_name, "MASTER")

    @classmethod
    def _append_choice_list_to_master(cls, cl_name):
        choice_list = cls._get_choice_list(cl_name, "MASTER")
        if not choice_list:
            new_cl = acm.FChoiceList()
            new_cl.Name(cl_name)
            new_cl.List('MASTER')
            try:
                new_cl.Commit()
                logger.info("Added choice %s to MASTER Choice List", cl_name)
                return new_cl
            except Exception as err:
                raise err
        return choice_list

    @classmethod    
    def _populate_choice_list(cls, cl_name, choices):
        if cl_name == cls.APT_BORROWER_CLASS:
            choice_list = cls._get_choice_list(cl_name, cls.APT_BORROWER_CLASS_MASTER)
            if not choice_list:
                raise Exception('%s not found' % cl_name)
            choice_list_master = cls._append_choice_list_to_master(choice_list.Name())
        else:
            choice_list = cls._get_choice_list(cl_name, "MASTER")
            if not choice_list:
                raise Exception('%s not found' % cl_name)
            choice_list_master = cls._append_choice_list_to_master(cl_name)
        cls._create_choices(choices, choice_list_master.Name())

    @classmethod
    def _get_add_info_spec(cls, name):
        return acm.FAdditionalInfoSpec[name]

    @classmethod
    def _get_alias_spec(cls, name):
        return acm.FInstrAliasType[name]

    @classmethod
    def _datastream(cls):
        datastream_alias_spec = cls._get_alias_spec(cls.DATASTREAM)
        logger.info("Checking that %s Alias Type Spec exists", cls.DATASTREAM)
        if not datastream_alias_spec:
            cls._create_alias_spec(cls.DATASTREAM, 'APT Alias Type')

    @classmethod
    def _sedol(cls):
        sedol_alias_spec = cls._get_alias_spec(cls.SEDOL)
        logger.info("Checking that %s Alias Type Spec exists", cls.SEDOL)
        if not sedol_alias_spec:
            cls._create_alias_spec(cls.SEDOL, 'APT Alias Type')

    @classmethod
    def _id_types(cls):
        cls._datastream()
        cls._sedol()

    @classmethod
    def _apt_borrower_class(cls):
        apt_borrower_class_cl = cls._get_choice_list(cls.APT_BORROWER_CLASS, cls.APT_BORROWER_CLASS_MASTER)
        logger.info("Checking that %s Choice List exists", cls.APT_BORROWER_CLASS)
        if not apt_borrower_class_cl:
            cls._create_choice_list(cls.APT_BORROWER_CLASS)
            logger.info("Created %s choice list", cls.APT_BORROWER_CLASS)
        cls._populate_choice_list(cls.APT_BORROWER_CLASS, cls.APT_BORROWER_CLASS_CHOICES)

    @classmethod
    def _apt_bbg_industry(cls):
        GROUP = cls.APT_BBG_INDUSTRY[0]
        SECTOR = cls.APT_BBG_INDUSTRY[1]
        SUBGROUP = cls.APT_BBG_INDUSTRY[2]
        group_add_info_spec = cls._get_add_info_spec(GROUP)
        logger.info("Checking that %s AdditionalInfo Spec exists", GROUP)
        if not group_add_info_spec:
            cls._create_add_info_spec_str(GROUP, cls.RECORD_TYPE)
        sector_add_info_spec = cls._get_add_info_spec(SECTOR)
        logger.info("Checking that %s AdditionalInfo Spec exists", SECTOR)
        if not sector_add_info_spec:   
            cls._create_add_info_spec_str(SECTOR, cls.RECORD_TYPE)
        subgroup_add_info_spec = cls._get_add_info_spec(SUBGROUP)
        logger.info("Checking that %s AdditionalInfo Spec exists", SUBGROUP)
        if not subgroup_add_info_spec:   
            cls._create_add_info_spec_str(SUBGROUP, cls.RECORD_TYPE)

    @classmethod
    def _apt_export_type(cls):
        apt_export_type_add_info_spec = cls._get_add_info_spec(cls.APT_EXPORT_TYPE)
        logger.info("Checking that %s AdditionalInfo Spec exists", cls.APT_EXPORT_TYPE)
        if not apt_export_type_add_info_spec:
            cls._create_add_info_spec_cl(cls.APT_EXPORT_TYPE, cls.RECORD_TYPE)
        apt_export_type_cl = cls._get_choice_list(cls.APT_EXPORT_TYPE, "MASTER")
        logger.info("Checking that %s Choice List exists", cls.APT_EXPORT_TYPE)
        if not apt_export_type_cl:
            cls._create_choice_list(cls.APT_EXPORT_TYPE)
            logger.info("Created %s choice list", cls.APT_EXPORT_TYPE)
        cls._populate_choice_list(cls.APT_EXPORT_TYPE, cls.APT_EXPORT_TYPE_CHOICES)

    @classmethod
    def _apt_recon_id_type(cls):
        apt_recon_id_type_add_info_spec = cls._get_add_info_spec(cls.APT_RECON_ID_TYPE)
        logger.info("Checking that %s AdditionalInfo Spec exists", cls.APT_RECON_ID_TYPE)
        if not apt_recon_id_type_add_info_spec:
            cls._create_add_info_spec_cl(cls.APT_RECON_ID_TYPE, cls.RECORD_TYPE)
        apt_recon_id_type_cl = cls._get_choice_list(cls.APT_RECON_ID_TYPE, "MASTER")
        logger.info("Checking that %s Choice List exists", cls.APT_RECON_ID_TYPE)
        if not apt_recon_id_type_cl:
            cls._create_choice_list(cls.APT_RECON_ID_TYPE)
            logger.info("Created %s choice list", cls.APT_RECON_ID_TYPE)
        cls._populate_choice_list(cls.APT_RECON_ID_TYPE, cls.APT_RECON_ID_TYPE_CHOICES)

    @classmethod
    def _apt_mbs_type(cls):
        apt_mbs_type_add_info_spec = cls._get_add_info_spec(cls.APT_MBS_TYPE)
        logger.info("Checking that %s AdditionalInfo Spec exists", cls.APT_MBS_TYPE)
        if not apt_mbs_type_add_info_spec:
            cls._create_add_info_spec_cl(cls.APT_MBS_TYPE, cls.RECORD_TYPE)
        apt_mbs_type_cl = cls._get_choice_list(cls.APT_MBS_TYPE, "MASTER")
        logger.info("Checking that %s Choice List exists", cls.APT_MBS_TYPE)
        if not apt_mbs_type_cl:
            cls._create_choice_list(cls.APT_MBS_TYPE)
            logger.info("Created %s choice list", cls.APT_MBS_TYPE)
        cls._populate_choice_list(cls.APT_MBS_TYPE, cls.APT_MBS_TYPE_CHOICES)

    @classmethod
    def _apt_service_fee(cls):
        apt_service_fee_add_info_spec = cls._get_add_info_spec(cls.APT_SERVICE_FEE)
        logger.info("Checking that %s AdditionalInfo Spec exists", cls.APT_SERVICE_FEE)
        if not apt_service_fee_add_info_spec:
            cls._create_add_info_spec_double(cls.APT_SERVICE_FEE, cls.RECORD_TYPE)

    @classmethod
    def _setup_fa_objects(cls):
        cls._id_types()
        cls._apt_borrower_class()
        cls._apt_bbg_industry()
        cls._apt_export_type()
        cls._apt_recon_id_type()
        cls._apt_mbs_type()
        cls._apt_service_fee()
        logger.info("APT Setup done!")

    @classmethod
    def Setup(cls):
        cls._setup_fa_objects()
        #acm.PollDbEvents()
        #acm.AEF.RegisterCustomMethods()
        #acm.AEF.RegisterCustomFunctions()

def setup(eii):
    FAPTSetup.Setup()
