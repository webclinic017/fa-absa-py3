"""Abstracts Front Arena infinitely recursive tree-in-a-table model into fixed two-level choiceList - choices model.

Use ChoiceList functions when you want to manage a choice list (FChoiceLists that belong to MASTER).
Use Choice functions to add or remove choices from a ChoiceList.
 
"""
#SUBMODULE      at_choice, part of 'at' module 
#For history see 'at' module. 

import acm              #@UnresolvedImport
import types, time

MASTER = 'MASTER'

def add(choice_list, name):
    """Add a single choice for the specified choice list."""
    add_many(choice_list, [name])

def add_many(choice_list, choices):
    """Add choices for the specified choice list. Does not add duplicate choices."""
    if isinstance(choice_list, (str,)):
        choice_list = _get_cl(choice_list)
        if not choice_list: raise ValueError("Choice list not found!")
    
    existing_choice_names = [choice.Name() for choice in choice_list.Choices()]
    
    for choice_name in choices:
        if choice_name not in existing_choice_names:    
            choice = _create_instance(choice_name, choice_list.Name(), choice_list.Owner(), '')
            choice.Commit()

def delete(choice_list_name, name):
    """Remove a choice from the specified choice list."""
    choice = get(choice_list_name, name)
    if choice:
        choice.Delete()
        return True
    
    return False

def get(choice_list, name):
    """Returns a choice."""
    if isinstance(choice_list, (str,)):
        choice_list = _get_cl(choice_list)
    
    filtered_choices = choice_list.Choices().Filter(lambda x: x.Name() == name)
    if filtered_choices:
        return filtered_choices[0]
    
    return None

def _create_instance(name, parent, owner, description):
    """Create a new choice list instance."""
    master_choice_list = acm.FChoiceList.Select01("name='{0}' and list='{0}'".format(MASTER), None)
    if not master_choice_list: raise Exception("MASTER Choice List not found!")
    
    if isinstance(owner, (str,)):
        owner = acm.FUser.Select01('name="' + owner + '"', None)
        if not owner: raise Exception("User not found")
    
    curr_timestamp = int(time.time())
    
    new_choice_list = master_choice_list.Clone()
    new_choice_list.CreateUser(acm.User())
    new_choice_list.CreateTime(curr_timestamp)
    new_choice_list.Description(description)
    new_choice_list.List(parent)
    new_choice_list.Name(name)
    new_choice_list.Owner(owner)
    new_choice_list.UpdateTime(curr_timestamp)
    new_choice_list.UpdateUser(acm.User())
    
    return new_choice_list

def _get_cl(name):
    """Returns an FChoiceList specified by its name."""
    return acm.FChoiceList.Select01('name="{0}" and list="{1}"'.format(name, MASTER), None) 

