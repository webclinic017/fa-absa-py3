"""Abstracts Front Arena infinitely recursive tree-in-a-table model into fixed two-level choiceList - choices model.

Use ChoiceList functions when you want to manage a choice list (FChoiceLists that belong to MASTER).
Use Choice functions to add or remove choices from a ChoiceList.
"""

# SUBMODULE      at_choiceList, part of 'at' module
# For history see 'at' module.
 
import acm                  #@UnresolvedImport
import at_choice as choice

def create(name, owner = None, description = ''):
    """Create a new choice list."""
    if not owner: owner = acm.User()
    choice_list = choice._create_instance(name, choice.MASTER, owner, description)
    choice_list.Commit()
    
    return choice_list

def delete(name):
    """Delete a choice list specified by its name."""
    cl = get(name)
    if cl:
        for choice in cl.Choices():
            choice.Delete() # we assume there are no sub-choices.
             
        cl.Delete()

def get(name):
    """Returns an FChoiceList specified by its name."""
    return choice._get_cl(name)
