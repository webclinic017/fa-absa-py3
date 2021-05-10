'''
Purpose              	: Used in the FICA asqls to return the branch code, account number and tel/fax with the +
Department and Desk	: IT - CTB
Requester            	: Karin Bonthuys
Developer            	: Bhavnisha Sarawan
CR Number            	: C514880
'''
import ael, string

# Removes the + sign from the string (tel and fax fields)
def removePlus(temp,st,*rest):
    check = st
    try:
        if check[0] == '+':
            st = check[1:]
    except:
        pass
    return str(st)

# returns the account number
def accNum(temp, st, delimiter, index, *rest):
    check = st
    if check[0] == ' ':
        st = check[1:]
    findSpace = st.find(' ')
    if findSpace == -1:
        return (str)(st)
    else:
        return (str)(st[findSpace+1:])
            
# returns the branch number
def accBranch(temp, st, delimiter, index, *rest):
    check = st
    if check[0] == ' ':
        st = check[1:]
    if st.__contains__(' '):
        list = st.split(delimiter)
        if index < len(list):
            return list[0]
        else:
            return 'error'
    else:
        return ' '

