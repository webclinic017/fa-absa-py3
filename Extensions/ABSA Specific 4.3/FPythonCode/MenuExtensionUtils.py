import acm


def run_user_search(f_object):
    caption = 'Front User Lookup'
    query = acm.CreateFASQLQuery(acm.FUser, 'AND')
    query.AddAttrNode('Inactive', 0, 'EQUAL')
    query.AddAttrNodeNumerical('Name', None, None)
    query.AddAttrNodeNumerical('FullName', None, None)
    query.AddAttrNodeNumerical('Email', None, None)
    query.AddAttrNodeNumerical('UserGroup.Name', None, None)
    query.AddAttrNodeNumerical('Oid', 0, None)
    acm.StartFASQLEditor(caption, None, None, query, None, '', True)
