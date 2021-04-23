import ael, SAEQ_Create_CallAccount

def jpCreator(p,*rest):
    
    SAEQ_Create_CallAccount.creat_call(p, ael.date_today(), 1)
    
    return 'Success'
