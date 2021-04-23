"""
------------------------------------------------------------------------------------------------------------------------
PURPOSE              :  Utility classes for Static Data changes for Upgrade and Rollback Scripts
DEVELOPER            :  Ncediso Nkambule
------------------------------------------------------------------------------------------------------------------------

HISTORY
========================================================================================================================
Date         Change no      Developer              Requester           Description
------------------------------------------------------------------------------------------------------------------------
2021-03-27   FAOPS-1127     Ncediso Nkambule       Cuen Edwards        Initial implementation
"""


import os
import acm
import ael
import csv
import logging


LOGGER = logging.getLogger(__name__)


class AbstractBase:

    def __init__(self):
        pass

    def _run(self):
        raise NotImplementedError("No Implementation")

    def execute(self):
        self._run()


class DecoratorMeta:

    def __init__(self):
        pass

    @classmethod
    def run_in_ael_transaction(cls, func):

        def wrapper(*args, **kwargs):
            try:
                message = "Running the function {func_name} in AEL Transaction"
                LOGGER.info(message.format(func_name=func.__name__))
                ael.begin_transaction()
                result = func(*args, **kwargs)
                ael.commit_transaction()
                message = "Successfully committed AEL Transaction for changes carried out by the function {func_name}\n"
                LOGGER.info(message.format(func_name=func.__name__))
                return result
            except Exception as error:
                ael.abort_transaction()
                message = "Aborting AEL Transaction for the function {func_name}\n"
                LOGGER.info(message.format(func_name=func.__name__))
                LOGGER.exception(error)
            return None

        return wrapper

    @classmethod
    def run_in_acm_transaction(cls, func):

        def wrapper(*args, **kwargs):
            try:
                message = "Running the function {func_name} in ACM Transaction"
                LOGGER.info(message.format(func_name=func.__name__))
                acm.BeginTransaction()
                result = func(*args, **kwargs)
                acm.CommitTransaction()
                message = "Successfully committed ACM Transaction for changes carried out by the function {func_name}\n"
                LOGGER.info(message.format(func_name=func.__name__))
                return result
            except Exception as error:
                acm.AbortTransaction()
                message = "Aborting ACM Transaction for the function {func_name}\n"
                LOGGER.info(message.format(func_name=func.__name__))
                LOGGER.exception(error)
            return None

        return wrapper


class FileHandlerMeta:

    def __init__(self):
        pass

    @staticmethod
    def is_existing_file_path(path_to_file):
        return os.path.exists(path_to_file)

    @classmethod
    def create_directory(cls, file_directory):
        if cls.is_existing_file_path(file_directory) is False:
            os.makedirs(file_directory)
            LOGGER.info("Successfully created file path {file_dir}".format(file_dir=file_directory))

    @classmethod
    def dict_to_file(cls, data_dict, absolute_path, headers=None):

        if data_dict and headers is None:
            headers = data_dict[0].keys()

        if data_dict:
            directory, file_name = os.path.split(absolute_path)
            if directory and cls.is_existing_file_path(directory) is False:
                cls.create_directory(directory)

            with open(absolute_path, 'wb') as file_obj:
                file_writer = csv.DictWriter(file_obj, fieldnames=headers)
                file_writer.writeheader()
                file_writer.writerows(data_dict)
                LOGGER.info("Successfully created data file. File Path: {file_path}".format(file_path=absolute_path))

    @classmethod
    def read_csv_to_list_of_dict(cls, absolute_path, headers=None):
        file_data = list()
        if cls.is_existing_file_path(absolute_path) is False:
            LOGGER.info("File {file_path} could not be Found".format(file_path=absolute_path))
            return file_data

        with open(absolute_path, 'r') as file_obj:
            if headers:
                file_reader = csv.DictReader(file_obj, fieldnames=headers)
            else:
                file_reader = csv.DictReader(file_obj)
            file_data = list(file_reader)
            message = "Successfully read data ({rows} Rows) from file {file_path}"
            LOGGER.info(message.format(rows=str(len(file_data)), file_path=absolute_path))

        return file_data

    @classmethod
    def read_csv_to_list_of_list(cls, absolute_path, headers=None):
        file_data = list()
        if cls.is_existing_file_path(absolute_path) is False:
            LOGGER.info("File {file_path} could not be Found".format(file_path=absolute_path))
            return file_data

        header_indices = list()
        with open(absolute_path, 'r') as file_obj:
            file_headers = file_obj.readline().strip().split(",")

            for header_item in headers:
                index = file_headers.index(header_item)
                if index != -1:
                    header_indices.append(index)
            header_indices.sort()
            file_obj.seek(0, 0)
            file_reader = csv.reader(file_obj)
            if header_indices:
                for line_data in file_reader:
                    file_data.append(line_data[index] for index in header_indices)
            else:
                file_data = list(file_reader)
            message = "Successfully read data ({rows} Rows) from file {file_path}"
            LOGGER.info(message.format(rows=str(len(file_data)), file_path=absolute_path))

        return file_data


class BaseReaderUtils(object):

    @staticmethod
    def get_user_profile_by_name(name):
        """
        Get an existing user profile by name.

        If a user profile with the specified name is not found then an
        error is raised.
        """
        user_profile = acm.FUserProfile[name]
        if user_profile is None:
            raise ValueError("A user profile with the name '{name}' does not exist.".format(name=name))
        return user_profile

    @classmethod
    def get_multiple_user_profile_by_name(cls, user_profile_names):
        """
        Get an existing user profile by name.

        If a user profile with the specified name is not found then an error is raised.
        """
        user_profiles = list()
        for user_profile_name in user_profile_names:
            user_profile = cls.get_user_profile_by_name(user_profile_name)
            if user_profile is None:
                message = "User profile '{user_profile_name}' not found, skipping "
                message += "addition of profile components."
                LOGGER.warning(message.format(user_profile_name=user_profile_name))
                continue
            user_profiles.append(user_profile)
        return user_profiles

    @staticmethod
    def get_user_group_by_name(name):
        """
        Get an existing user group by name.

        If a user group with the specified name is not found then an error is raised.
        """
        user_group = acm.FUserGroup[name]
        if user_group is None:
            raise ValueError("A user group with the name '{name}' does not exist.".format(name=name))
        return user_group

    @staticmethod
    def find_component_by_name_and_type(component_name, component_type):
        """
        Find a component by name and type.
        """
        select_expression = "name = '{component_name}' and type = '{component_type}'".format(
            component_name=component_name,
            component_type=component_type)
        select_exception_message = "Expecting zero or one component '{component_name}' "
        select_exception_message += "of type '{component_type}'."
        select_exception_message = select_exception_message.format(
            component_name=component_name,
            component_type=component_type)
        return acm.FComponent.Select01(select_expression, select_exception_message)

    @staticmethod
    def find_group_profile_link_by_group_and_profile(user_group, user_profile):
        """
        Find a group profile link component by user group and user profile.
        """
        select_expression = "userGroup = {user_group_oid} and userProfile = {user_profile_oid}".format(
            user_group_oid=user_group.Oid(),
            user_profile_oid=user_profile.Oid())
        select_exception_message = "Expecting zero or one group profile link for user group"
        select_exception_message += "{user_group_oid} and user profile {user_profile_oid}."
        select_exception_message = select_exception_message.format(
            user_group_oid=user_group.Oid(),
            user_profile_oid=user_profile.Oid())
        return acm.FGroupProfileLink.Select01(select_expression, select_exception_message)

    @staticmethod
    def find_profile_component_by_profile_and_component(user_profile, component):
        """
        Find a profile component by name and type.
        """
        select_expression = "userProfile = {user_profile_oid} and component = {component_oid}".format(
            user_profile_oid=user_profile.Oid(),
            component_oid=component.Oid())
        select_exception_message = "Expecting zero or one profile component for user "
        select_exception_message += "profile {user_profile_oid} and component "
        select_exception_message += "{component_oid}'."
        select_exception_message = select_exception_message.format(
            user_profile_oid=user_profile.Oid(),
            component_oid=component.Oid())
        return acm.FProfileComponent.Select01(select_expression, select_exception_message)

    @staticmethod
    def _get_database_string_column_size(table_name, column_name):
        """
        Get the size of a given string column in the ADM database.
        """
        column_domain = acm.FTable[table_name].GetColumn(column_name).Domain()
        if column_domain.BaseDomain().Class() != acm.FStringDomain:
            exception_message = "Column '{column_name}' in table '{table_name}' "
            exception_message += "is not a string."
            raise ValueError(exception_message.format(column_name=column_name, table_name=table_name))
        return column_domain.Size()

    @classmethod
    def validate_component_name(cls, component_name):
        """
        Validate a component name.
        """
        column_size = cls._get_database_string_column_size('ADM.Component', 'compname')
        if len(component_name) > column_size:
            exception_message = "The length of component name '{component_name}' is "
            exception_message += "greater than the database column size of {column_size}."
            exception_message = exception_message.format(component_name=component_name, column_size=column_size)
            raise ValueError(exception_message)

    @staticmethod
    def get_choice_list(choice_list_name, parent_list="MASTER"):
        choice_list = acm.FChoiceList[choice_list_name]
        if choice_list:
            if choice_list.List() == parent_list:
                return choice_list
            else:
                message = "The found choice does not belong to the specified parent list. "
                message += "Could not remove ChoiceList {child_choice_list} from Parent ChoiceLis {parent_choice_list}"
                LOGGER.warning(message.format(child_choice_list=choice_list_name, parent_choice_list=parent_list))
                return None
        message = "Could not find ChoiceList {child_choice_list} to Parent ChoiceList {parent_choice_list}"
        LOGGER.warning(message.format(child_choice_list=choice_list_name, parent_choice_list=parent_list))
        return None

    @staticmethod
    def get_extension_context_by_name(extension_context_name):
        """
        Get an existing extension context by name.

        If an extension context with the specified name is not found then an error is raised.
        """
        extension_context = acm.FExtensionContext[extension_context_name]
        if extension_context is None:
            message = "An extension context with the name '{name}' does not exist."
            raise ValueError(message.format(name=extension_context_name))
        return extension_context

    @staticmethod
    def get_extension_module_by_name(extension_module_name):
        """
        Get an existing extension module by name.

        If an extension module with the specified name is not found then
        an error is raised.
        """
        extension_module = acm.FExtensionModule[extension_module_name]
        if extension_module is None:
            message = "An extension module with the name '{name}' does not exist."
            raise ValueError(message.format(name=extension_module_name))
        return extension_module

    @staticmethod
    def get_netting_rule_links(party_name, netting_rule_name):
        select_string = "nettingRule='{n_rule}' and party='{party}'"
        select_string = select_string.format(n_rule=netting_rule_name, party=party_name)
        matching_links_list = acm.FNettingRuleLink.Select(select_string)
        return matching_links_list


class BaseValidations(BaseReaderUtils):

    @staticmethod
    def is_correct_add_info_spec(record_type, add_info_name):
        if isinstance(add_info_name, str) is False:
            return False

        add_info_spec = acm.FAdditionalInfoSpec[add_info_name]
        if add_info_spec and record_type == add_info_spec.RecType():
            return True

        return False

    @classmethod
    def add_info_exists(cls, acm_object, add_info_name):
        if cls.is_correct_add_info_spec(acm_object.RecordType(), add_info_name) is False:
            return False
        add_info_spec = acm.FAdditionalInfoSpec[add_info_name]
        select_query = "addInf = %i and recaddr = %i " % (add_info_spec.Oid(), acm_object.Oid())
        add_info = acm.FAdditionalInfo.Select01(select_query, "")
        return True if add_info else False


class BaseWriterUtils(BaseValidations):

    def __init__(self):
        super(BaseWriterUtils, self).__init__()

    @classmethod
    def create_component(cls, component_name, component_type):
        """
        Create a component.
        :param component_name:
        :param component_type:
        :return:
        """
        cls.validate_component_name(component_name)
        component = cls.find_component_by_name_and_type(component_name, component_type)
        if component is None:
            try:
                message = "Component '{component_name}' of type '{component_type}' "
                message += "does not exist - creating."
                LOGGER.info(message.format(component_name=component_name, component_type=component_type))
                component = acm.FComponent()
                component.RegisterInStorage()
                component.Name(component_name)
                component.Type(component_type)
                component.Commit()
            except Exception as error:
                LOGGER.exception(error)

        return component.OriginalOrSelf()

    @classmethod
    def update_component(cls, component_name, component_type):
        """
        Update a component.
        :param component_name:
        :param component_type:
        :return:
        """
        component = cls.find_component_by_name_and_type(component_name, component_type)

        message = "Component '{component_name}' of type '{component_type}' "
        message += "exists - updating."
        if component:
            try:
                LOGGER.info(message.format(component_name=component_name, component_type=component_type))
                component = component.StorageImage()
                component.Name(component_name)
                component.Type(component_type)
                component.Commit()
            except Exception as error:
                message = "Could updated component {comp_name}. {error_msg}."
                LOGGER.exception(message.format(comp_name=component_name, error_msg=error.message))

        return component.OriginalOrSelf()

    @classmethod
    def create_profile_component(cls, user_profile, component, allow_create=None, allow_write=None):
        """
        Create or update a profile component.
        :param user_profile:
        :param component:
        :param allow_create:
        :param allow_write:
        :return:
        """
        profile_component = cls.find_profile_component_by_profile_and_component(user_profile, component)
        if profile_component is None:
            message = "Component '{component_name}' of type '{component_type}' "
            message += "does not exist on user profile '{user_profile_name}' - creating."
            LOGGER.info(message.format(
                component_name=component.Name(),
                component_type=component.Type(),
                user_profile_name=user_profile.Name()))
            try:
                profile_component = acm.FProfileComponent()
                profile_component.UserProfile(user_profile)
                profile_component.Component(component)
                if allow_create is not None:
                    profile_component.AllowCreate(allow_create)
                if allow_write is not None:
                    profile_component.AllowWrite(allow_write)
                profile_component.Commit()
            except Exception as error:
                LOGGER.exception(error)
        else:
            message = "Component '{component_name}' of type '{component_type}' "
            message += "exists on user profile '{user_profile_name}' - nothing "
            message += "to create."
            LOGGER.info(message.format(
                component_name=component.Name(),
                component_type=component.Type(),
                user_profile_name=user_profile.Name()))

    @classmethod
    def create_group_profile_link(cls, user_group, user_profile):
        """
        Create a group profile link giving a user group the specified user profile.
        :param user_group:
        :param user_profile:
        :return:
        """
        group_profile_link = cls.find_group_profile_link_by_group_and_profile(user_group, user_profile)
        if group_profile_link is None:
            try:
                message = "User profile '{user_profile_name}' does not exist "
                message += "on user group '{user_group_name}' - creating."
                LOGGER.info(message.format(user_profile_name=user_profile.Name(), user_group_name=user_group.Name()))
                user_profile_link = acm.FGroupProfileLink()
                user_profile_link.UserProfile(user_profile)
                user_profile_link.UserGroup(user_group)
                user_profile_link.Commit()
            except Exception as error:
                LOGGER.exception("Could not create Group Profile Link. {err_msg}".format(err_msg=error.message))
        else:
            message = "User profile '{user_profile_name}' exists on user "
            message += "group '{user_group_name}' - nothing to create."
            LOGGER.info(message.format(user_profile_name=user_profile.Name(), user_group_name=user_group.Name()))

    @staticmethod
    def _create_choice_list(choice_list_name, description, parent_list="MASTER"):
        """
        Creates a Choice List Item to the given parent Choice List
        :param choice_list_name:
        :param description:
        :param parent_list:
        :return:
        """
        try:
            choice_list_entry = acm.FChoiceList(choice_list_name)
            choice_list_entry.List(parent_list)
            choice_list_entry.Name(choice_list_name)
            choice_list_entry.Description(description)
            choice_list_entry.Commit()
            message = "Successfully added ChoiceList {child_choice_list} to Parent ChoiceList {parent_choice_list}"
            LOGGER.info(message.format(child_choice_list=choice_list_name, parent_choice_list=parent_list))
        except Exception as error:
            message = "Could not create/add ChoiceList {child_choice_list} to Parent ChoiceList {parent_choice_list}"
            LOGGER.error(message.format(child_choice_list=choice_list_name, parent_choice_list=parent_list))
            LOGGER.exception(error)

    @classmethod
    def remove_choice_list(cls, choice_list_name, parent_list="MASTER"):
        """
        Deletes a Choice List Item from the given parent Choice List
        :param choice_list_name:
        :param parent_list:
        :return:
        """
        choice_list = cls.get_choice_list(choice_list_name, parent_list)
        try:
            if choice_list:
                choice_list.Delete()
                message = "Successfully removed ChoiceList {child_list} from Parent ChoiceList {parent_list}"
                LOGGER.info(message.format(child_list=choice_list_name, parent_list=parent_list))
            else:
                message = "Could not find ChoiceList {child_choice_list} to remove"
                LOGGER.warning(message.format(child_choice_list=choice_list_name))
        except Exception as error:
            LOGGER.exception(error)

    @classmethod
    def add_choice_list(cls, choice_list_name, description, parent_list="MASTER"):
        """
        Creates a Choice List Item to the given parent Choice List if Choice List Item does not exist
        :param choice_list_name:
        :param description:
        :param parent_list:
        :return:
        """
        choice_list = cls.get_choice_list(choice_list_name, parent_list)
        if choice_list:
            message = "The ChoiceList {child_list} for Parent ChoiceList {parent_list} already exist"
            LOGGER.info(message.format(child_list=choice_list_name, parent_list=parent_list))
        else:
            cls._create_choice_list(choice_list_name, description, parent_list)

    @classmethod
    @DecoratorMeta.run_in_acm_transaction
    def setup_access_control(cls, user_profile_names, required_operations):
        """
        Setup access control - Creates a component and link component to the give user profile.
        :param user_profile_names: User Profiles to assign access to.
        :param required_operations: Component to create and assign to user profiles
        :return:
        """

        user_profiles = cls.get_multiple_user_profile_by_name(user_profile_names)
        for required_operation in required_operations:
            component = cls.create_component(required_operation, 'Operation')
            for user_profile in user_profiles:
                cls.create_profile_component(user_profile, component)

    @staticmethod
    def remove_extension_module_from_context(extension_module_name, extension_context):
        """
        Remove an extension module from an extension context if present.
        :param extension_module_name:
        :param extension_context:
        :return:
        """
        if extension_module_name not in extension_context.ModuleNames():
            message = "Extension module '{ext_module_name}' not found in context '{ext_context_name}' - "
            message += "nothing to remove."
            LOGGER.info(message.format(ext_module_name=extension_module_name, ext_context_name=extension_context.Name()))
        else:
            message = "Extension module '{ext_module_name}' found in "
            message += "context '{ext_context_name}' - removing."
            try:
                LOGGER.info(
                    message.format(ext_module_name=extension_module_name, ext_context_name=extension_context.Name()))
                extension_context = extension_context.StorageImage()
                extension_context.RemoveModule(extension_module_name)
                extension_context.Commit()
            except Exception as error:
                LOGGER.exception(error)

    @staticmethod
    def delete_extension_module(extension_module_name):
        """
        Remove an extension module if present.
        :param extension_module_name:
        :return:
        """
        extension_module = acm.FExtensionModule[extension_module_name]
        if extension_module is None:
            message = "Extension module '{extension_module_name}' does not "
            message += "exist - nothing to remove."
            LOGGER.info(message.format(extension_module_name=extension_module_name))
        else:
            message = "Extension module '{extension_module_name}' exists - "
            message += "removing."
            LOGGER.info(message.format(extension_module_name=extension_module_name))
            extension_module.Delete()

    @staticmethod
    def __add_extension_module_to_context(extension_module, extension_context, index):
        """
        Add an extension module to an extension context at the specified index.
        :param extension_module:
        :param extension_context:
        :param index:
        :return:
        """
        module_name_to_add = extension_module.Name()
        extension_context = extension_context.StorageImage()
        module_names = list(extension_context.ModuleNames())
        # Remove added module if already in list and re-add to ensure in correct position.
        try:
            if module_name_to_add in module_names:
                message = "Extension module '{module_name}' already in "
                message += "context '{context_name}' - removing before add."
                LOGGER.info(message.format(module_name=extension_module.Name(), context_name=extension_context.Name()))
                current_index = module_names.index(extension_module.Name())
                if current_index < index:
                    index += 1
                module_names.remove(module_name_to_add)
            module_names.insert(index, module_name_to_add)
            # Update context.
            extension_context.Clear()
            for module_name in module_names:
                extension_context.AddModule(module_name)
            extension_context.Commit()
            message = "Added extension module '{extension_module_name}' to context "
            message += "'{extension_context_name}' at index {index}"
            LOGGER.info(message.format(
                extension_module_name=extension_module.Name(),
                extension_context_name=extension_context.Name(),
                index=index))
        except Exception as error:
            LOGGER.exception(error)

    @classmethod
    def add_extension_module_to_context(cls, extension_module_name, next_to_module_name, context_name='Standard'):
        """
        Add Extension Module to the Standard context.
        :param extension_module_name:
        :param next_to_module_name:
        :param context_name:
        :return:
        """
        extension_module = cls.get_extension_module_by_name(extension_module_name)
        extension_context = cls.get_extension_context_by_name(context_name)
        index = list(extension_context.ModuleNames()).index(next_to_module_name)
        cls.__add_extension_module_to_context(extension_module, extension_context, index)

    @classmethod
    def create_add_info_spec(cls, record_type, add_info_spec_name, data_type, description=None):
        """
        Creates Additional Info Specification.
        :param record_type:
        :param add_info_spec_name:
        :param data_type:
        :param description:
        :return:
        """
        if cls.is_correct_add_info_spec(record_type, add_info_spec_name) is False:
            add_info_spec = acm.FAdditionalInfoSpec()
            try:
                if description is None:
                    description = add_info_spec_name
                add_info_spec.RecType(record_type)
                add_info_spec.DataTypeType(data_type)
                add_info_spec.Name(add_info_spec_name)
                add_info_spec.Description(description)
                add_info_spec.Commit()
                return add_info_spec
            except Exception as error:
                LOGGER.exception(error)
                add_info_spec.Undo()
                return None
        else:
            add_info_spec = acm.FAdditionalInfoSpec[add_info_spec_name]
        return add_info_spec

    @classmethod
    def _create_add_info(cls, acm_object, add_info_name, add_info_value):
        """
        Creates and Additional Info "add_info_name", "add_info_Value".
        :param acm_object:
        :param add_info_name:
        :param add_info_value:
        :return:
        """

        return_val = None
        try:
            if cls.is_correct_add_info_spec(acm_object.RecordType(), add_info_name):
                add_info_spec = acm.FAdditionalInfoSpec[add_info_name]
                select_query = "addInf = %i and recaddr = %i " % (add_info_spec.Oid(), acm_object.Oid())
                add_info = acm.FAdditionalInfo.Select01(select_query, "")
                if add_info is None:
                    add_info = acm.FAdditionalInfo()
                    add_info.Recaddr(acm_object.Oid())
                    add_info.AddInf(add_info_spec)
                    add_info.FieldValue(add_info_value)
                    add_info.Commit()
                    return_val = add_info
                    message = "Successfully created Additional Info on object {oid}. {name} : {val}"
                    LOGGER.info(message.format(oid=str(acm_object.Oid()), name=add_info_name, val=str(add_info_value)))
            else:
                message = "No Additional Info Spec {name} on object {rec_type}"
                LOGGER.info(message.format(name=add_info_name, rec_type=acm_object.RecordType()))
        except Exception as error:
            LOGGER.error(" Error: Creating an additional info {name}".format(name=add_info_name))
            LOGGER.exception(error)
        finally:
            return return_val

    @classmethod
    def _update_add_info(cls, acm_object, add_info_name, add_info_value):
        """
        Updated ACM Additional Info with a given Additional Info Value (add_info_value).
        :param acm_object:
        :param add_info_name:
        :param add_info_value:
        :return:
        """

        add_info_spec = acm.FAdditionalInfoSpec[add_info_name]
        try:
            if cls.is_correct_add_info_spec(acm_object.RecordType(), add_info_name):
                acm_object.AddInfoValue(add_info_name, add_info_value)
                acm_object.Commit()
                message = "Successfully updated Additional Info on object {oid}. {name} : {val}"
                LOGGER.info(message.format(oid=str(acm_object.Oid()), name=add_info_name, val=add_info_value))
            else:
                message = "No Additional Info Spec {name} on object {rec_type}"
                LOGGER.info(message.format(name=add_info_name, rec_type=acm_object.RecordType()))
        except Exception as error:
            message = "{err_msg}. Failed to Create 'additional info' {name}"
            LOGGER.exception(message.format(err_msg=error.message, name=add_info_spec.Name()))

    @classmethod
    def set_add_info_value(cls, acm_object, add_info_name, add_info_value):
        """
        Create or Updated AddInfo on ACM object.
        :param acm_object:
        :param add_info_name:
        :param add_info_value:
        :return:
        """

        if cls.is_correct_add_info_spec(acm_object.RecordType(), add_info_name):
            if cls.add_info_exists(acm_object, add_info_name):
                cls._update_add_info(acm_object, add_info_name, add_info_value)
            else:
                cls._create_add_info(acm_object, add_info_name, add_info_value)

    @classmethod
    def create_netting_rule(cls, netting_rule_name, definition_by_values, definition_values, netting_rule_type,
                            query_folder):
        """
        Creates a Netting Rule.
        :param netting_rule_name:
        :param definition_by_values:
        :param definition_values:
        :param netting_rule_type:
        :param query_folder:
        :return:
        """
        netting_rule = acm.FNettingRule[netting_rule_name]
        if netting_rule:
            message = "Netting Rule {name} already exists. Will use existing Netting Rule"
            LOGGER.warning(message.format(name=netting_rule_name))
            if not netting_rule.NettingDefinitionByValues() == definition_by_values:
                LOGGER.warning("Netting Rule By Value don't match existing Netting Rule By Value.")
            if not netting_rule.NettingDefinitionValues() == definition_values:
                LOGGER.warning("Netting Rule Value don't match existing Netting Rule Value.")
            if not netting_rule.NettingRuleType() == netting_rule_type:
                LOGGER.warning("Netting Rule Type don't match existing Netting Rule Type.")
            if not netting_rule.Query() == acm.FStoredASQLQuery[query_folder]:
                LOGGER.warning("Netting Rule Query Folder don't match existing Netting Rule Query Folder.")
        else:
            try:
                netting_rule = acm.FNettingRule()
                netting_rule.Name(netting_rule_name)
                netting_rule.NettingDefinitionByValues(definition_by_values)
                netting_rule.NettingDefinitionValues(definition_values)
                netting_rule.NettingRuleType(netting_rule_type)
                netting_rule.Query(query_folder)
                netting_rule.Commit()
                LOGGER.info('Created Netting Rule {name}'.format(name=netting_rule_name))
            except Exception as error:
                LOGGER.exception(error)

        return netting_rule

    @classmethod
    def create_netting_rule_link(cls, netting_rule_name, party_name):
        """
        Creates a Netting Rule Link given a Party Name and Netting Rule Name
        :param netting_rule_name:
        :param party_name:
        :return:
        """
        matching_links_list = cls.get_netting_rule_links(party_name, netting_rule_name)
        if acm.FNettingRule[netting_rule_name] is None:
            raise ValueError("No Netting rule found matching the name {name}".format(name=netting_rule_name))

        if matching_links_list.Size() == 0:
            netting_rule_link = acm.FNettingRuleLink()
            netting_rule_link.NettingRule(netting_rule_name)
            netting_rule_link.Party(party_name)
            netting_rule_link.Enabled(True)
            netting_rule_link.OrderNumber(0)
            netting_rule_link.Commit()
            message = 'Created Netting Rule Link for {pty} and Netting Rule {name}'
            LOGGER.info(message.format(pty=party_name, name=netting_rule_name))
        else:
            message = 'Netting Rule {name} is already linked to party {pty}'
            LOGGER.warning(message.format(name=netting_rule_name, pty=party_name))


class UpgradeAndRollbackManager(BaseWriterUtils, AbstractBase):
    """
    This it the main class to be extended whn you are using these utils.

    This class aims to stantardises the structure of upgrade script, such that the implementation steps may be be
    added in the _run function and execution will be kicked of by the function execute from AbstractBase Class.
    """

    def __init__(self):
        BaseWriterUtils.__init__(self)
        AbstractBase.__init__(self)

    def _run(self):
        raise NotImplementedError("Not Implemented")


class UsageExample(UpgradeAndRollbackManager, FileHandlerMeta):
    """
    This is an example of the how you can use the base scripts.
    """

    @DecoratorMeta.run_in_ael_transaction
    def func1(self, name):
        LOGGER.info("I am creating AEL : {name}".format(name=name))

    @DecoratorMeta.run_in_acm_transaction
    def func2(self, name):
        LOGGER.info("I am creating ACM UpdateClients: {name}".format(name=name))

    def _run(self):
        name = ""
        self.func1(name)
        self.func2(name)


if __name__ == "__main__":
    user_case1 = UsageExample()
    user_case1.execute()
