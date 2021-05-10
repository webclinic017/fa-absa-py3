""" Compiled: 2020-09-18 10:38:53 """

#__src_file__ = "extensions/operations/etc/FOperationsRollbackWrapper.py"
import FBDPRollback
import FBDPCommon
import acm, ael

class FOperationsRollbackWrapper(FBDPRollback.RollbackWrapper, object):

    def __init__(self, createRollback = True, rollbackName=None, testmode = 0, arguments = {}):
        super(FOperationsRollbackWrapper, self).__init__(rollbackName, testmode, arguments)
        self.rollback = createRollback
        self.testmode = testmode

    def add(self, e, attribs=[], op=None, modified_child_entities=None):
        """
        Only add to transaction list
        """
        if 'transaction_list' in dir(self):
            op = (op or (attribs or modified_child_entities) and 'Update' or
                  'Create')
            if modified_child_entities and op == 'Update':
                for ca in modified_child_entities:
                    (c, c_attribs) = ca
                    c_op = c_attribs and 'Update' or 'Create'
                    c_orig = eval(self.encapsulateAttribute(c))
                    c_id = FBDPCommon.getPrimaryKey(c)
                    c = ((c_op == 'Update') and
                             FBDPCommon.clone(c_orig) or c)
                    rd1 = None
                    if self.rollback:
                        rd1 = self.createRollbackData(c_id, c, c_attribs, c_op)
                    tpl = (None, c_id, c, c_attribs, c_op, rd1)
                    self.addToTransactionList(tpl)

            orig = eval(self.encapsulateAttribute(e))
            e_id = FBDPCommon.getPrimaryKey(e)
            orig_copy = (op == 'Update') and FBDPCommon.clone(orig) or e
            rd = None
            if self.rollback:
                rd = self.createRollbackData(e_id, orig_copy, attribs, op)
            tpl = (e, e_id, orig_copy, attribs, op, rd)
            self.addToTransactionList(tpl)
            return True
        # Commit and add rollback data to the rollback spec directly.
        self.beginTransaction()
        self.add(e, attribs, op, modified_child_entities)
        try:
            self.commitTransaction()
        except:
            self.abortTransaction()
            return False
        return True

    def commitList(self, tr_list):
        try:
            acm.BeginTransaction()
        except Exception as error:
            Logme()('Rollback failed to begin transaction. \n%s.' %
                    (str(error)), 'ERROR')
            raise error
        try:
            for tpl in tr_list:
                e = tpl[0]
                op = tpl[4]
                rd = tpl[5]
                if e:
                    commit_function = self.commitFunction(op)
                    arg = [e]
                    orig = eval(self.encapsulateAttribute(e))
                    if orig and op == 'Update':
                        arg.append(orig)
                    if not self.testmode:
                        try:
                            commit_function(*arg)
                        except Exception as error:
                            Logme()('Failed to %s object. %s.' % (op,
                                    str(error)), 'ERROR')
                            raise Exception("Rollback unable to commit "
                                    "object. " + str(error))
                        if op != 'Delete':
                            if rd:
                                try:
                                    rd.commit()
                                except Exception as e:
                                    Logme()('Failed to commit rollback data. %s.' %
                                            (op, str(error)), 'ERROR')
                                    raise Exception("Rollback unable to commit "
                                            "rollback data. " + str(error))
        except Exception as e:
            acm.AbortTransaction()
            raise e

        try:
            acm.CommitTransaction()
        except Exception as e:
            acm.AbortTransaction()
            raise e
        acm.PollDbEvents()
        try:
            self.logAndUpdateRollbackData(tr_list)
        except Exception as e:
            raise Exception("Failed to log and update Rollback Data. %s." %
                    str(e))
