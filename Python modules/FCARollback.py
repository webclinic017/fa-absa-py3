""" CorporateActions:1.2.2 """


"""----------------------------------------------------------------------------
MODULE
    FCARollback - Saves data about Corporate Actions to the database so they
    can be rollbacked.

    (c) Copyright 2003 by Front Capital Systems AB. All rights reserved.
    
DESCRIPTION
    This module includes classes for creating database records to be saved to
    the ca_rollback_data table. This table has columns for storing the CorpAct
    seqnbr to which it refers, what database action to be performed in case of
    rollback (one of Delete or Update), what entity to perform the rollback on
    (normally a table name), and a text field where a dictionary with any
    relevant data is stored (such as trade number).

----------------------------------------------------------------------------"""

import ael
import string
import FCAGeneral
import FCAMisc
        

NotFound = "NotFound"

"""----------------------------------------------------------------------------
CLASSES / DESCRIPTIONS
    RollbackInfo - Class for maintaining rollback information for corporate
    actions.  Rollback (undo) information is stored in the database, one row
    for each object.  Attributes are stored in a dictionary with each object.
    The database table is included in the ADM 3.4.0. If an earlier version is
    used, the table can be created as follows using isql:
     
    > create table ca_rollback_data (id numeric(9) identity primary key, 
        ca_seqnbr int, op char(10), entity char(64), attribs text);
    > grant all on ca_rollback_data to public;
    
TODO:
    - Use ael.dbproc() to solve security issues (problems with procs and text).
    - Purge old rollback lists.
    
MEMBERS
    List of member functions:
    add(self,op,e,attribs=[])   Add an object to the rollback list. op can be 
                                'Update' or 'Delete'.
                                Update Time and User are automatically added
                                for 'Update' operations. attribs is a list of
                                field names that should be restored by
                                rollback.
    commit(self)                Commit the rollback list to the database.
    getdata(self)               Return the rollback data for the Corporate
                                Action. Delete the returned data from the
                                database.
    rollback(self)              Rollback (undo) a Corporate Action from the 
                                rollback data in the database.
----------------------------------------------------------------------------"""
class RollbackInfo:
    """Class for maintaining rollback information for corporate actions."""

    class RollbackData:
        """Rollback data for one object. Just for encapsulating purposes."""
        
        def __init__(self, op, entity, attribs):
            self.op, self.entity, self.attribs = op, entity, attribs
        def __repr__(self):
            s = 'RollbackData instance: op=%s, entity=%s, attribs=%s' \
                % (self.op, self.entity, self.attribs)
            return s

    class RollbackAttrib:
        """Class for encapsulating an attribute. Needed to convert entity
        references and dates to strings that can be stored in the database. An
        entity reference is converted to `ael.Table[nbr]` and a date to
        `ael.date(date)`.  Other types are converted to `str(object)`."""

        def __init__(self, o):
            ### Have to add apostrophes in order to get eval(.) right later on.
            if type(o) == type(''):
                o = "'%s'" % o
            self.o = o
                
        def __repr__(self):
            if type(self.o) == ael.ael_entity:
                for i in eval('ael.%s.keys()' % self.o.record_type):
                    if i[1] == 'primary':
                        _id = getattr(self.o, i[0])
                        return 'ael.%s[%d]' % (self.o.record_type, _id)
                raise TypeError, 'No primary key for' + self.o
            elif type(self.o) == ael.ael_date:
                return 'ael.date(\'%s\')' % self.o
            else:
                return str(self.o)

    def __init__(self, ca):
        """Constructor. Store corporate action object, initialize list of
        rollback objects."""

        self.ca = ca
        self.rb_list = []

    def add(self, op, e, attribs = []):
        """Add an object to the rollback list."""

        if op == 'Update':
            if not 'updat_usrnbr' in attribs: attribs.append('updat_usrnbr')
            if not 'updat_time' in attribs: attribs.append('updat_time')
        d = {}
        for i in attribs:
            d[i] = self.RollbackAttrib(getattr(e, i))
        rd = self.RollbackData(op, e, d)
        self.rb_list.append(rd)
        
    def commit(self):
        """Commit the rollback list to the database."""

        for rd in self.rb_list:
            ca_seqnbr = self.ca.seqnbr
            op = rd.op
            entity = self.RollbackAttrib(rd.entity)
            attribs = rd.attribs
            if len(str(attribs)) > 2:
                attribs = string.replace(str(attribs), "'", '"')
            caClone = self.ca
            try:                
                crd = ael.CaRollbackData.new(caClone)
                crd.op = rd.op
                crd.entity = str(entity)
                crd.set_attribs(str(rd.attribs))
            except AttributeError, msg:
                if str(msg) in ('set_attribs', 'CaRollbackData'):
                    ael.dbsql("insert ca_rollback_data (ca_seqnbr,op,entity, "\
                        "attribs) values (%d, '%s', '%s', '%s')" % \
                        (ca_seqnbr, op, entity, attribs)) # FIXME dbproc()
                else:
                    raise 'AttributeError: ' + str(msg)
            else:
                crd.commit()
            print '\n### ROLLBACK DATA ###\nCommitted to Rollback Table:' \
                '\nSeqnbr: %s' \
                '\nOperation to be performed when doing rollback: %s' \
                '\nEntity on which to perform rollback: %s' \
                '\nAttributes to update when doing rollback: %s\n' \
                % (ca_seqnbr, op, entity, attribs)
        return self.rb_list
        
    def getdata(self):
        """Return the rollback data for the corporate action. Delete the
        returned data from the database."""

        rb_list = []
        attribsWarning = 'The Attribs field in CaRollbackData is empty.'
        entityWarning  = 'The Entity field in CaRollbackData is empty.'
        dictError = 'The Attribs Field in CaRollbackData is not a dictionary.'
        try:
            for i in ael.CaRollbackData.select().members():
                if self.ca.seqnbr == i.ca_seqnbr.seqnbr:
                    if i.entity:
                        if i.get_attribs():
                            rd = self.RollbackData(i.op, eval(i.entity),
                                                eval(i.get_attribs()[:i.size]))
                            rb_list.append(rd)
                        else:
                            FCAGeneral.logme(attribsWarning) 
                    else:
                        FCAGeneral.logme(entityWarning)
        except AttributeError, msg:
            if str(msg) in ('get_attribs', 'CaRollbackData'):
                for i in ael.dbsql('select op, entity, attribs from '\
                                   'ca_rollback_data where ca_seqnbr = %d '\
                                   'order by id desc' % self.ca.seqnbr)[0]:
                    if i[1]:
                        if i[2]:
                            assert '{' in str(i[2]), dictError
                            rd = self.RollbackData(i[0], eval(i[1]),
                                                         eval(i[2]))
                            rb_list.append(rd)
                        else:
                            FCAGeneral.logme(attribsWarning)
                    else:
                        FCAGeneral.logme(entityWarning)

        return rb_list

    def rollback(self, void = 'Void'):
        """Rollback (undo) a corporate action from the rollback data in the 
        database."""
        
        rb_list = self.getdata()
        if not rb_list:
            print NotFound, "No rollback data for " + str(self.ca.seqnbr)
        for rd in rb_list:
            if rd.op == 'Update':
                try:
                    e = rd.entity.clone()
                    for i in rd.attribs.keys():
                        setattr(e, i, rd.attribs[i])
                        print 'Attribute:', i
                    e.commit()
                    print 'Update done.'
                except AttributeError:
                    pass
                except RuntimeError:
                    try:
                        e = rd.entity.trdnbr.clone()
                        p = e.payments()
                        for i in p:
                            if i.paynbr == rd.entity.paynbr:
                                i.delete()
                        e.commit()
                    except AttributeError:
                        pass
                    except:
                        print 'Uncaught RuntimeError in FCARollback.' ; raise
                except Exception, e:
                    print 'Failed to update' + rd.entity + e
            elif rd.op == 'Delete' and void == 'Void':
                try:
                    if rd.entity != None:
                        e = rd.entity.clone()
                        if e.record_type == 'Trade':
                            e.status = 'Void'
                            e.commit()
                        if e.record_type in ('Instrument', 'Payment'):
                            pass
                    else:
                        print 'Cannot void None entity.'
                except Exception, e:
                    print 'Failed to void' + str(rd.entity) + str(e)
                else:
                    print 'Voided:', self.RollbackAttrib(rd.entity), rd.attribs
                    
            elif rd.op == 'Delete':
                try:
                    rd.entity.delete()
                except AttributeError, msg:
                    if str(msg) ==\
                    "'NoneType' object has no attribute 'delete'":
                        print 'Not possible to delete None entities'\
                              ' (FCARollback).'
                    else:
                        raise
                except RuntimeError, msg:
                    print 'Not possible to delete %s, %s. Possible reason: '\
                    'BO Confirmed.' % (self.RollbackAttrib(rd.entity), msg)
                except:
                    print 'Uncaugt exception in FCARollback.' ; raise
                else:
                    print 'Deleted:', self.RollbackAttrib(rd.entity), rd.attribs
                
        FCAMisc.script_update(seqnbr = self.ca.seqnbr)
        ### Delete data in the ca_rollback_data table:
        ael.dbsql('delete from ca_rollback_data where ca_seqnbr = %d' \
                  % self.ca.seqnbr)

def test():     
    try:
        ael.dbsql('select id from ca_rollback_data')
    except RuntimeError:
        print '''\nA rollback-table must be created to be able to run the\
corporate action scripts (contact your database administrator):

1. Log in to your ARENA database, for example:

dsql -S<server> -U<user> -P<password>

2. Make sure you are in the ARENA database:

use <ARENA database>;

3. Create the table:

create table ca_rollback_data (id numeric(9) identity primary key,\
ca_seqnbr int, op char(10), entity char(64), attribs text);

4. Grant rights:

grant all on ca_rollback_data to public;
''' ; raise









