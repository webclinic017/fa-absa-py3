""" AbandonClose:1.0.7 """

"""----------------------------------------------------------------------------
MODULE
        FDMCascadeHandler - A module that uses SQL to finds an objects references.

DESCRIPTION
        This module contains some helper class to the main class FDMCascadeHandler
        that can be used to find all references to an object and references to the
        refering objects, ..., so that a whole tree of refererenses can be found.
        In database terms the concept cascade delete exists which means almost the same.

        The FDMCasscadeHandler uses the sql to access record id's to reduce the needed
        memory use.
        A FDMCascadeHandler() first reads the database schema from the database and then keeps
        descriptions of columns,column types, references in/out/same table in dictionaries of
        dictionaries.
        There is many ways these descriptions over the ADM module could be used.
        For example the time type is represented as a float and it is now way to determent
        that an attribute's data type is representing a time compared to a float using the
        types library.

VERSION
        0.2.2

NOTE
        Should be used by care because deleting a instrument record with for example the 'EUR'
        insaddr may delete the whokle database.


DATA-PREP
        Connection to a server must first be establisdh to use this module.

REFERENCES
        <Articles, books, other modules etc>

HISTORY:
        FK 2002-04-02   Improved delete_object so it deletes prices for an instrument using
                        the already implemented cascade delete.
        FK 2002-01-31   Improved delete_object so it now can be called by an ael entity or
                        a list of such. Also handles parent-child relations better.
ENDDESCRIPTION
----------------------------------------------------------------------------"""

import ael
import re
import string


VERSION="0.2.3"

def get_traceback():
    """ returns last traceback as a string """
    import sys, traceback, string
    t, v, tb=sys.exc_info()
    d=traceback.format_exception(t, v, tb)
    msg=string.join(d, '')
    return msg

def get_exception():
    """ returns last exception as string"""
    import sys, traceback, string
    t, v, tb=sys.exc_info()
    d=traceback.format_exception_only(t, v)
    msg=string.join(d, '')
    return msg




"""----------------------------------------------------------------------------
CLASS
        RelationDescr

DESCRIPTION
        Holds a description of a table

CONSTRUCTION
        tablename   - The name from ds_tables.

MEMBERS
        (see constructor)
----------------------------------------------------------------------------"""

class RelationDescr:
    """Simple class for descring a tables relations"""


    built_alias={}
    table_alias={}

    def __init__(self, tablename):
        self.name=tablename # i.e. database table name
        self.alias=self.buildAlias(tablename)
        self.ref={}     # Dictionary of columns that refers to something
        self.rself={}   # Columns refering to itslef.
        self.rfrom={}   # Dictionary <table,[c1,..,cN]> describing reference from other tables
        self.rto={}     # Dictionary <table,[c1,..,CN]> describing reference to other tables
        self.rparent=()   # Tuple (c1,parent table name) describing parent reference to other table
        self.id=''      # Columns name of id
        self.enum={}  # <name,type>
        self.columns=[]  # List of all columns
        self.column_type={} # Dict of column_name : type
        self.queries=[]  #[<id>,<id+string_keys>,<all columns>]
        self.string_keys=[] # List of columns that are string keys.
        self.has_archive_flag=0
        ael_object=self.ael_object=self.toAelObject()
        self.soft_rel=[]  # Relations with soft relations such as additional info etc.
        self.is_soft_table=0 # Is this description to a soft table.
        if not ael_object:
            return

        #
        # Get id and unique string columns
        #
        for values in ael_object.keys():
            col=values[0]
            typ=values[1]
            if typ=='primary':
                self.id=col
            elif typ=='unique':
                self.string_keys.append(col)

    def buildAlias(self, tablename):
        """Build or return an existing alias"""
        # The alias could be used in queries i.e.
        # instrument i, then i is used in queries such as i
        #
        if RelationDescr.table_alias.has_key(tablename):
            return RelationDescr.table_alias[tablename]
        l=string.split(tablename, '_')
        do_cont=1
        i=1
        while do_cont:
            alias=''
            for j in range(len(l)):
                alias=alias+l[j][0:i]
            if RelationDescr.built_alias.has_key(alias):
                #print "ALIAS(%s)>>%s>>%s"% (tablename,alias,RelationDescr.built_alias[alias])
                i=i+1
            else:
                RelationDescr.built_alias[alias]=tablename
                RelationDescr.table_alias[tablename]=alias
                self.alias=alias
                return self.alias


    def pp(self, columns=0):
        """pretty print"""
        format="%-20s::"
        print format % "Tablename", self.name
        print format % "Ael Tablename", self.toAelTableName()
        print format % "Alias", self.alias
        print format % "Id", self.id
        print format % "Relations to Self", self.rself
        print format % "Relations From", self.rfrom
        print format % "Relations To", self.rto
        if self.rparent:
            print format % "Parent Relation To", self.rparent
        print format % "SoftRelations To", self.soft_rel
        print format % "Enum columns", self.enum
        if self.has_archive_flag:
            print format % "Archive_flag", 'Yes'
        else:
            print format % "Archive_flag", 'No'
        if columns:
            cols=self.columns
            cols.sort()
            print format % "Columns", cols[0]
            for i in range(len(cols)):
                if i > 0:
                    print format % "", cols[i]
            print format % "\n\nColumnsAndType"
            keys=self.column_type.keys()
            keys.sort()
            for k in keys:
                print format % "", k, '-->', self.column_type[k]
            for i in range(len(self.queries)):
                s=('Select level(%d)' % i)
                print format % s, self.queries[i]

    def toAelTableName(self):
        """ Converts the table name to the corresponding ael table name """
        n=self.name
        if n=='price_hst':
            return 'Price'
        l=string.split(n, '_')
        o=''
        for i in range(len(l)):
            if i==0 and l[i]=='rf':
                o='RiskFactor'
            elif i==0 and l[i]=='emu':
                o='EMU'
            elif l[i]:
                o=o+string.capwords(l[i])
        return o


    def toAelObject(self):
        """converts the name to corresponding ael object"""
        o = self.toAelTableName()
        try:
            return eval('ael.'+o)
        except:
            return None


    def addRef(self, tn, cn):
        self.ref[cn]=tn

    def getRef(self):
        """ Returns the dictionary of columns refering to something """
        return self.ref



    def addEnum(self, tn, cn):
        self.enum[cn]=tn

    def getTableName(self, cn):
        """Returns the table of a column if it has a reference to a table"""
        return self.ref.get(cn, None)

    def addColumn(self, cn):
        self.columns.append(cn)

    def addColumnType(self, cn, ct):
        if re.search('_time', ct):
            self.column_type[cn] = 'time'
        else:
            self.column_type[cn] = ct



    def buildSelect(self):
        """Creates a select string of columns with id first"""

        # q_level 0
        self.queries=[self.id]

        # q_level 1
        temp=[self.id]+self.string_keys
        skip_columns=temp
        self.queries.append(string.join(temp, ','))

        # q_level 2
        for i in range(len(self.columns)):
            if self.columns[i] not in skip_columns:
                temp.append(self.columns[i])
        self.queries.append(string.join(temp, ','))


    def addSelf(self, cn):
        if not self.rself.has_key(self.name):
            self.rself[self.name]=[]
        self.rself[self.name].append(cn)

    def getSelf(self):
        """ Returns the dictionary of columns refering to itself """
        return self.rself


    def addFrom(self, tn, cn):
        if self.rfrom.has_key(tn):
            self.rfrom[tn].append(cn)
        else:
            self.rfrom[tn]=[cn]

    def getFrom(self,tn=None):
        """ Returns a dictionary of all or a specific table references from FROM other tables """
        if not tn:
            return self.rfrom
        else:
            return self.rfrom[tn]


    def addTo(self, tn, cn):
        if self.rto.has_key(tn):
            self.rto[tn].append(cn)
        else:
            self.rto[tn]=[cn]

    def getTo(self,tn=None):
        """ Returns a dictionary of all or a specific table references from TO other tables """
        if not tn:
            return self.rto
        else:
            return self.rto[tn]

    def addSoftRel(self, softtable):
        """ Do something """
        pass

    def addParent(self, tn, cn):
        self.rparent=(cn, tn)

    def getParentRel(self,tn=None):
        """ Returns the dictionary of columns having a parent reference TO other tables i.e.
             this table is a child in a parent-child relation. """
        return self.rparent

"""========================================================================

 buildTableRef - Help operation for building
                 a description reference structure.
                 For better performance this structure
                 should be stored in a file and then generated
                 when the database schema changes

========================================================================"""

def buildTableRef():
    """Builds a table with references descriptions"""

    s= """select table_name, column_name, column_type from ds_tables"""

    #
    # Build a dictionary with an entry for each table
    # describing:
    # name on id, reference to itself, reference to other tables and
    # references from other tables
    tables={}
    for set in ael.dbsql(s):
        for (tn, cn, ct) in set:
            if not tables.has_key(tn):
                d=RelationDescr(tn)
                if not d:
                    continue
            else:
                d=tables[tn]
            if ct == 'id':
                d.id=cn
            elif cn == 'archive_status':
                d.has_archive_flag=1
            else:
                m=re.search('ref\((\w+)', ct)
                if m:
                    if m.group(1) == tn:
                        d.addSelf(cn)
                    else:
                        d.addTo(m.group(1), cn)
                    d.addRef(m.group(1), cn)
                m=re.search('parent\((\w+)', ct)
                if m:
                    if m.group(1) == tn:
                        d.addSelf(cn)
                    else:
                        d.addTo(m.group(1), cn)
                        d.addParent(m.group(1), cn)
                    d.addRef(m.group(1), cn)
                m=re.search('enum\((\w+)', ct)
                if m:
                    d.addEnum(m.group(1), cn)
            d.addColumn(cn)
            d.addColumnType(cn, ct)
            tables[tn]=d


    for (k, v) in tables.items():
        v.buildSelect()
        for (t, columns) in v.getTo().items():
            for c in columns:
                tables[t].addFrom(k, c)

    return tables




"""----------------------------------------------------------------------------
CLASS
        FDMCascadeHandler

DESCRIPTION
        Main class that can traverse a object backwards finding all
        references to it.
        The class also have some convinient operations built around
        the traverse functionalty such as delete_object, archive_object and
        dearchive_object.
        The traverse is done in deep first order.


CONSTRUCTION
        verbose - 0,1,2
        cp_pre  - callback that will be called before traversing an object id
        cb_post - callback that will be called after traversed an object id.

MEMBERS
        q_level - Query level: 0=id, 1=id+string_keys, 2=all columns
        vervose - 0=No Verbose,1=(table,id,[string key]), 2=also the statement used)
        cp_pre  - See above
        cp_post - See above


----------------------------------------------------------------------------"""

def cmp_level_table(a, b):
    ret=cmp(int(a[0]), int(b[0]))
    if not ret: return ret
    return cmp(a[1], b[1])

class FDMCascadeHandler:
    table_descr=None

    def __init__(self, verbose=None, cb_pre=None,cb_post=None):
        self.q_level=1   # 0=id, 1=id+string_keys 2= all columns
        if not FDMCascadeHandler.table_descr:
            FDMCascadeHandler.table_descr=buildTableRef()
            for (k, d) in FDMCascadeHandler.table_descr.items():
                FDMCascadeHandler.table_descr[d.toAelTableName()]=d # Lookup both through database table name and ael table name
        self.descr=FDMCascadeHandler.table_descr
        self.verbose=verbose
        self.cb_pre=cb_pre        # Called before recursive calls
        self.cb_post=cb_post      # Called after recursive calls
        self.oid_processed={}     # oid already processed
        self.oid_order=[]         # (table,id,level) pre order of object id's processed
        self.oid_path=[]          # To access last object id
        self.version='Version 1'
        self.ignore_curr=0        # Should currency references be ignored


    def printObject(self,ref,level,table,addr,row=None):
        if row and self.q_level > 0 and ref.string_keys:
            print "%s(%d)[" % (table, addr),
            for i in range(len(ref.string_keys)):
                print str(row[i+1]),
                if i+1 < len(ref.string_keys):
                    print ",",
            print "]"
        else:
            print "%s(%s)" % (table, str(addr))



    def oidtos(self,table,addr=None):
        """ table could ael entity """
        #print "oidtos",table,addr
        if type(table) == ael.ael_entity:
            name=''
            if self.table_descr[table.record_type].string_keys:
                c="name=table.%s" % self.table_descr[table.record_type].string_keys[0]
                exec(c)
            id=self.getOID(table)
            if name: s=('%s(%d) [ %s ]' % (table.record_type, id, name))
            else: s=('%s(%d)' % (table.record_type, id))
        else: s=('%s(%d)' % (table, addr))
        #print "oidtos:", s
        return s

    def clear(self):
        self.cb_pre=self.cb_post=None
        self.oid_processed={}
        self.oid_order=[]
        self.oid_path=[]       # To last object

    def buildQuery(self, ref, table, columns, addr):
        q=('select %s from %s where ' % (ref.queries[self.q_level], table))
        cons=''
        for c in columns:
            # Optmization, add more
            if self.ignore_curr and re.search('curr$', c):
                continue
            if cons:
                cons = cons+' or '+c+'='+str(addr)
            else:
                cons=c+'='+str(addr)
        if not cons:
            return ''
        q=q+cons
        return q


    def get_selection_methods(self, parent_name, child_name):
        """ Dirty rule to determent the selection method to use when accessing children
             from the parent. The parent_ and child_name are the ael table names.
             The rule is a follows:
             i) Divide the child_name by uppercase letters.
             ii) Create a new name by adding an s to the last part and then construct names
             by adding an '_' between the parts.
             iii) Pick the max element in the parent class (or any) and check if some of the
             constructed names exists. Then return.
            Example:
            1) YieldCurve,YieldCurvePoint
             from i) and ii)  ['points','curve_points','yield_curve_points']
            2) Volatility,VolBetaPoint
             from i) and ii) ['points','beta_points','vol_beta_points']"""
        import string
        pdescr= self.table_descr[parent_name]
        parts=[]
        suggested=[]
        tmp=''
        methods=[]
        for i in child_name:
            if re.search('[A-Z]', i):
                if tmp: parts.append(tmp)
                tmp=string.lower(i)
            else: tmp=tmp+i
        if tmp:
            if tmp == 'alias':
                parts.append('aliases')
            elif tmp == 'dividend':
                parts.append('historical')
                parts.append(tmp+'s')
            else:
                parts.append(tmp+'s')
        for i in range(len(parts)):
            suggested.append(string.join(parts[i:], '_'))
        stmt='select max(%s) from %s' % (pdescr.id, pdescr.name)
        addr=int(ael.dbsql(stmt)[0][0][0])
        try: o = pdescr.ael_object[addr]
        except: o= pdescr.ael_object.select()[0]
        for m in dir(o):
            # Note: if more than one selection mathod matches pick the first
            # i.e. the longest name except for instruments.
            if m in suggested:
                methods.append(m)
                if parent_name != 'Instrument': return methods
        return methods




    def convert_ael_entity(self,table,addr=None):
        """ If table is an ael_entity it converts it to database table name and addr.
             Always returns a tuple <table,addr>.
             Implemented for backward compatibility """
        if type(table) == ael.ael_entity:
            entity=table
            table=self.table_descr[entity.record_type].name
            s="addr=int(entity.%s)" % self.table_descr[entity.record_type].id
            exec(s)
        return (table, addr)



    def delete_children(self,children,table,level=0):
        """ Deletes all children {addr : None}in the dictionary.
        --- table could be sql tablename or ael table name.
        --- The Operations commits at the end i.e. do not use around transactions"""
        if type(children) == type([]):
            tmp={}
            for c in children:
                tmp[c]=None
            children=tmp
        elif type(children) != type({}):
            msg="Error, children must be a dictionary or a list"
            raise RuntimeError, msg
        clones={}
        processed={}
        del_by_sql=[]
        n_deleted=0 # Counter
        for addr in children.keys():
            if processed.has_key(addr): continue
            child=self.table_descr[table].ael_object[int(addr)]
            if not child:
                del_by_sql.append(addr)
                processed[addr]=1
                continue
            (parent, pid)=self.get_parent(child)
            if not parent: # Error data
                del_by_sql.append(addr)
                processed[addr]=1
                continue
            the_clone=parent.clone()
            if self.verbose: print "%s Cloned: %s" % ("  "*level, self.oidtos(parent))
            for m in self.get_selection_methods(parent.record_type, child.record_type):
                c="elements=the_clone.%s().members()" % m
                exec(c)
                if not elements or elements[0].record_type != child.record_type: # safe test
                    continue
                for e in elements:
                    oid=self.getOID(e)
                    if self.verbose: cstr=self.oidtos(e)
                    if children.has_key(oid):
                        processed[oid]=1
                        e.delete()
                        if self.verbose: print "%s Deleted: %s" % (level*'  ', cstr)
                        n_deleted=n_deleted+1
                break
            the_clone.commit()
            ael.poll()
        if del_by_sql: n_deleted=n_deleted+self.delete_ids_by_sql(table, del_by_sql)
        return n_deleted




    def delete_ids_by_sql(self,tablename,ids,n_max=100,level=0):
        """ Deletes a buch of ids (numbers) by sql """
        if type(ids) == type({}):
            ids=ids.keys()
        i=0
        n_max=100
        descr=self.table_descr[tablename]
        while i < len(ids):
            tmp=ids[i:min(len(ids), i+n_max)]
            i=i+len(tmp)
            tmp=string.join(map(str, tmp), ',')
            s='delete from %s where %s in (%s)' % (descr.name, descr.id, tmp)
            ael.dbsql('begin transaction')
            ael.dbsql(s)
            ael.dbsql('commit')
            if self.verbose: print "%s SQL Deleted %s: %s" % ("  "*level, descr.name, tmp)
        sql_deleted={}
        for i in ids:
            sql_deleted[(descr.name, int(i))]=None
        self.synchronize_with_ads(sql_deleted)
        ael.poll()
        return len(ids)


    def delete_simple_object_by_ael(self,entity,level=0):
        """ Deletes an object and soft relations using ael directly.
             Throws exception on failure """
        try:
            # Try to remove soft relations
            for a in entity.additional_infos():
                a.delete()
            for t in entity.time_series():
                t.delete()
        except:
            pass
        entity_str=self.oidtos(entity)
        entity.delete() # May throw exception
        ael.poll()
        if self.verbose: print "%s Deleted: %s" % ("  "*level, entity_str)
        return 1


    def exists(self, table, addr):
        """check if addr exists"""
        r=self.descr[table]
        s=self.buildQuery(r, table, [r.id], addr)
        if self.verbose == 2:
            print "(S)statement = ", s
        for set in ael.dbsql(s):
            if not set:
                return 0
        return 1


    def getOID(self, entity):
        """ Return the object id, the number of an ael entity """
        c="oid=entity.%s" % self.table_descr[entity.record_type].id
        exec(c)
        return oid



    def get_parent(self, e):
        """ Helper function for delete, parent relation must exists """
        parent=None
        c="parent=e.%s" % self.table_descr[e.record_type].getParentRel()[0] # The column
        exec(c)
        if not parent: return (None, 0)
        pid=self.getOID(parent)
        return (parent, pid)


    def is_traversed(self,table,addr=None,oid_processed=None):
        """ Helper predicate, table could be ael_entity.
        --- To be able to reuse this operation in delete_object the dict.
        --- of processed elements could be passed """
        (table, addr)=self.convert_ael_entity(table, addr)
        if not oid_processed: oid_processed=self.oid_processed
        if oid_processed.has_key(table) and oid_processed[table].has_key(addr):
            return 1
        return 0



    def synchronize_with_ads(self,sql_deleted={},times=60):
        """ Tries to synchronize with ADS if objects are deleted by sql.
             If sql_deleted is used it checks if keys (sql_table_name,int(id)) is found"""
        import time # Could use the threading.Condition() to be able to wait less then a second
        for i in range(times):
            row=ael.dbsql("select count(*) from ds_updates")[0]
            if int(row[0][0]) == 0:
                return 1
            found=0
            rows=ael.dbsql("select table_name,id from ds_updates")[0]
            for table_name, id in rows:
                if sql_deleted.has_key((table_name, int(id))):
                    found=1
                    break
            if not found:
                return 1
            print "+ synchronize (%d elements) against ads ..." % len(sql_deleted)
            time.sleep(1)
        print "- FAILED to synchronize against ADS """
        return 0

    def toEntity(self, table, addr):
        """ Returns the entity (if it exists) as an ael entity """
        if table == 'price_hst':
            mask=1<<30
            addr=((int(addr))&(~mask))|mask
        return self.table_descr[table].ael_object[int(addr)]




    """----------------------------------------------------------------------------
    traverse: Traverses the description recursivly starting from
               [table,addr]
               The cb_pre and cb_post is called in pre or post order.
               This should be used as:
               i) After: If an object should be deleted the the call back should
               called after recusive calls because refering objects
               must be removed before the object itself.
               ii) Before: if AMBA messages should be generated then must
               the object be created before any creation of refering
               objects

               If cb_pre is defined or not cb_post is defined the oid_order
               will be in pre order. Otherwise post order
    ----------------------------------------------------------------------------"""

    def traverse(self,table,addr=None,ignore_children=0):
        """ Main entry, traverse, just for determent if some optimizations can be used.
             If called with one argument it is assumed that table is an ael_entity.
             The parameter ignore_chilren suppresses traverse of chilren in parent-child relations
             and soft relations """
        (table, addr)=self.convert_ael_entity(table, addr)
        self.ignore_curr=1
        self.clear() # If reused
        if table == 'instrument':
            i=ael.Instrument[int(addr)]
            if i and re.search('^curr', i.instype, re.I):
                self.ignore_curr=0
        self.traverse_aux(table, addr, 1, None, ignore_children)
        return


    def traverse_aux(self, table,addr,level=1,row=None,ignore_children=0):
        """ The operations that actually travserses the addr """
        if level==1 and not self.exists(table, addr):
            print "Object "+self.oidtos(table, addr)+" doesn't exists!"
            return

        # check circularity
        for (t, a) in self.oid_path:
            if t == table and a == addr:
                print "OBJECT_PATH=", self.oid_path
                raise 'Circulare reference for '+self.oidtos(table, addr)

        if self.oid_processed.has_key(table):
            if self.oid_processed[table].has_key(addr):
                self.oid_processed[table][addr]=self.oid_processed[table][addr]+1
                if self.verbose:
                    print "  "*level,
                    print "Object "+self.oidtos(table, addr)+" already processed!"
                return # Already processed
            else:
                self.oid_processed[table][addr]=level
        else:
            self.oid_processed[table]={addr:level}

        self.oid_path.append((table, addr))


        ref=self.descr[table]

        # Log object
        if self.verbose:
            for i in range(level):
                print "  ",
            if level == 1:
                s=self.buildQuery(ref, table, [ref.id], addr)
                if self.verbose==2: print "(S)statement = ", s
                row=ael.dbsql(s)[0][0]
            self.printObject(ref, level, table, addr, row)

        # append identifier in pre order if wanted
        if self.cb_pre or not self.cb_post:
            self.oid_order.append((table, addr, level))

        if self.cb_pre:
            self.cb_pre(self, table, addr, level)


        # process the relation, start with reference to self
        # note that row[0] is always id
        for (t, l) in ref.getSelf().items():
            s=self.buildQuery(ref, t, l, addr)
            if not s: continue
            if self.verbose==2: print "(S)statement = ", s
            for aSet in ael.dbsql(s):
                if aSet:
                    for row in aSet:
                        if t == table and addr == row[0]:
                            if self.verbose: print "Object "+self.oidtos(t, row[0])+" is refering to itself!"
                        else:
                            self.traverse_aux(t, row[0], level+1, row, ignore_children)
        for (t, l) in ref.getFrom().items():
            ref2=self.descr[t]
            if ignore_children: # Optimization for delete_object()
                if ref2.is_soft_table or (ref2.getParentRel() and ref2.getParentRel()[1] == table) or (t in ['price', 'price_hst'] and table == 'instrument'):
                    if self.verbose: print "%s Ignore traversing %s<=%s" % ('  '*level, table, ref2.name)
                    continue
            s=self.buildQuery(ref2, t, l, addr)
            if not s: continue
            if self.verbose and self.verbose==2: print "(F)statement=[%s]" % s
            for aSet in ael.dbsql(s):
                if aSet:
                    for row in aSet:
                        if t == table and addr == row[0]:
                            if self.verbose: print "Object "+self.oidtos(t, row[0])+" is refering to itself!"
                        else:
                            self.traverse_aux(t, row[0], level+1, row, ignore_children)


        # add identifier in post order if wanted
        if not self.cb_pre and self.cb_post:
            self.oid_order.append((table, addr, level))

        if self.cb_post:
            self.cb_post(table, addr, level)

        self.oid_path.pop()

        return






    #=======================================
    #Convenient operations using traverse
    #=======================================




    def delete_object(self,objects,addr=None,n_bunch=500, try_simple_delete=1):
        """ Deletes an object and all references to it recursivly.
            Could be called either by:
            ----------------------------------------
            objects=sql table name and addr=>id number, or
            objects=>ael entity a list of ael entities
            n_bunch is how many elements that shall be commited in each
            transaction
            NOTE:
                i) If parent to a parent-child relation are traversed
                (e.g. Trade <- Payment) the children will be deleted when
                the parents are deleted.
                ii) Parents not traversed (e.g. ListNode when Instrument <- ListLeaf)
                must be cloned and then must the child be accessed and deleted by a selection
                operation. For some ael tables such operations are missing!!!

        """

        try: ael.abort_transaction() # To handle invalid state in transactions
        except: pass

        if not objects:
            print "delete_object: called with objects None"
            return 0

        traverse_objects=[] # Objects that need to be travsersed

        if type(objects) != type([]):
            objects=[objects]

        if try_simple_delete: # Should we try to delete the object directly
            for object in objects:
                try:
                    (table, addr)=self.convert_ael_entity(object, addr)
                    if not table:
                        raise RuntimeError, "Nu such object %s:%s" % (str(object), str(addr))
                    descr=self.descr[table]
                    # children must be deleted by cloning the parent
                    if descr.getParentRel():
                        self.delete_children({addr:None}, table)
                    else:
                        obj=descr.ael_object[int(addr)]
                        self.delete_simple_object_by_ael(obj)
                except:
                    traverse_objects.append(object)

            if not traverse_objects:
                ael.poll()
                return 1 # Done!
        else:
            traverse_objects=objects



        # ========================================
        # Need to traverse and then delete
        # ========================================

        table_objects={} # (process_level,table) : {addr:None}, see below
        oid_processed={} # To simulate one oid_processed in is_traversed
            # if many objects should be deleted


        # ----------------------------------------
        # build a dictionary on level,table to be able to delete elements
        # in the same table and level in the same transaction
        # ----------------------------------------
        old_verbose=self.verbose
        #self.verbose=0

        for object in traverse_objects:
            self.traverse(object, addr)          # Build path
            for (t, a, l) in self.oid_order:      # Save paths
                elements=table_objects.get((l, t), {})
                elements[a]=None
                table_objects[(l, t)]=elements
                elements=oid_processed.get(t, {})
                elements[a]=l
                oid_processed[t]=elements

        keys=table_objects.keys()
        keys.sort()
        keys.reverse()
        self.verbose=old_verbose

        if old_verbose: print "%s Start Deleting %s" % ('-'*20, '-'*20)

        # ----------------------------------------
        # Where the work is actually done
        # ----------------------------------------

        clones={} # (record_type,id) : object
        level=(None, None)
        n_deleted=0  # Counter
        n_commited=0 # Commited sofar

        #for lt in keys:
        #   print lt
        for lt in keys:
            l, t=lt
            descr=self.descr[t]
            elements=table_objects[(l, t)].keys()
            n_processed=0
            #print "LEVEL=%d, Table=%s,elements=%s" % (l,t,str(elements))
            if descr.getParentRel():
                # Optimization: Cascade delete of children in parent-child relations
                for addr in elements:
                    entity=self.toEntity(t, addr)
                    parent=self.get_parent(entity)[0]
                    n_skipped=0
                    if entity and parent and not self.is_traversed(parent, oid_processed):
                        n_deleted=n_deleted+self.delete_children(elements, t, l)
                        n_commited=n_deleted
                        break
                    else:
                        n_skipped=n_skipped+1
                n_deleted=n_deleted+n_skipped
                continue
            elif t in ['price_hst', 'price'] and l > 1: #optimization, deleted by instrument
                n_deleted=n_deleted+len(elements)
                continue
            try:
                ael.begin_transaction()
                for addr in elements:
                    if not n_deleted%n_bunch:
                        ael.commit_transaction()
                        ael.poll()
                        level=lt
                        n_commited=n_deleted
                        ael.begin_transaction()
                        #print "AEL Commited:", n_commited
                    entity=self.toEntity(t, addr)
                    self.delete_simple_object_by_ael(entity, l)
                    n_deleted=n_deleted+1
                    n_processed=n_processed+1
                ael.commit_transaction()
                #if n_deleted != n_commited: ael.commit_transaction()
            except:
                #print "-Error when deleting:", t,addr
                #print get_traceback()
                #raise 'TEST'

                # ---------------------------------------
                # Delete all objects on this level by sql
                # ---------------------------------------
                ael.abort_transaction() # Commit here doesn't work
                try:
                    n_deleted=n_deleted+self.delete_ids_by_sql(descr.name, elements)
                    n_commited=n_deleted
                    sql_deleted={} # (table,addr):None
                except:
                    # Delete element by element
                    for e in elements:
                        self.traverse(descr.name, e)
                        tmp=self.oid_order
                        tmp.reverse()
                        ael.dbsql('begin transaction')
                        for (t, a, l) in tmp:
                            stmt="delete from %s where %s=%s" % (t, self.table_descr[t].id, str(a))
                            if self.verbose: print stmt
                            ael.dbsql(stmt)
                        ael.dbsql('commit')
                        self.synchronize_with_ads()
        ael.poll()
        return n_commited


    def archive_object(self,table,addr=None,level=1):
        """ Archives an object but setting archive status to level, if needed
            This operation could be improved if traverse also has a mode for reading the
            archive status directly.
            Could be called with table as an ael_entity"""

        (table, addr)=self.convert_ael_entity(table, addr)

        self.traverse(table, addr) # Build path
        l=self.oid_order
        l.reverse() #Note: Is not the same as post-order!
        #print "L=", l
        for (table, addr, p_level) in l:
            descr=self.descr[table]
            if not descr.has_archive_flag:
                continue # Can't archive that one
            try:
                # Optimization, try using ael first
                o=descr.ael_object[int(addr)]
                if not o:
                    raise 'Use SQL' # Not so pretty but safer
                if o.archive_status < level:
                    o2=o.clone()
                    o2.archive_status=level
                    o2.commit()
                    ael.poll() # refresh
            except:
                res = ael.dbsql('begin transaction')
                r=self.descr[table]
                s=('update %s set archive_status = %d where archive_status < %d and %s = %d ' % (table, level, level, r.id, addr))
                #print "S[%s]" % (s)
                ael.dbsql(s)
                res = ael.dbsql('commit')
        return 1

    def dearchive_object(self,table,addr,level=1):
        """ Dearchives an object but setting archive status to level, if needed
            This operation could be improved if traverse also has a mode for reading the
            archive status directly"""

        self.traverse(table, addr) # Build path
        l=self.oid_order
        l.reverse() #Note: Is not the same as post-order!
        #print "L=", l
        for (table, addr, p_level) in l:
            descr=self.descr[table]
            if not descr.has_archive_flag:
                continue # Can't archive that one
            try:
                # Optimization, try using ael first
                o=descr.ael_object[int(addr)]
                if not o:
                    raise 'Use SQL' # Not so pretty but safer
                if o.archive_status > level:
                    o2=o.clone()
                    o2.archive_status=level
                    o2.commit()
                    ael.poll() # refresh
            except:
                res = ael.dbsql('begin transaction')
                r=self.descr[table]
                s=('update %s set archive_status = %d where archive_status > %d and %s = %d ' % (table, level, level, r.id, addr))
                #print "S[%s]" % (s)
                ael.dbsql(s)
                res = ael.dbsql('commit')
        return 1



    #==========================================
    # Auxillary operations
    #==========================================
    def column_to_str(self, table, columns=None,ael_mode=1):
        """ Transforms a list of columns to a list of columns displaying strings"""
        # Has 2 modes:
        # When ael_mode is used only the list of columns is used.
        # When ael_mode is not used the "string" columnsc,corresponding tables with alias
        # and join constrains will be returned
        # Note: No checks is made that columns actually is part of the table
        d=self.table_descr[table]
        ref=d.getRef()
        rself=d.getSelf()
        ret=[]
        if not columns:
            columns=d.columns
        if ael_mode:
            for c in columns:
                if ref.has_key(c):
                    r2=self.table_descr[ref[c]]
                    if r2.string_keys:
                        ret.append(c+'.'+r2.string_keys[0])
                        continue
                ret.append(c)
            return ret
        else:
            t={d.name+' '+d.alias : None}
            j=[]
            a=d.alias
            used={d.name:0}  #One extract per join in the same table

            for c in columns:
                #print c
                if ref.has_key(c):

                    r2=self.table_descr[ref[c]]
                    if r2.string_keys:
                        n=used.get(ref[c])
                        if n==None:
                            n=''
                            used[ref[c]]=0
                        else:
                            n=n+1
                            used[ref[c]]=n
                            n=str(n)
                        a2=r2.alias+n
                        t[r2.name+' '+a2]=None
                        j.append(a2+'.'+r2.id+'='+a+'.'+c)
                        ret.append(a2+'.'+r2.string_keys[0])
                        continue
                ret.append(a+'.'+c)
            return [ret, t.keys(), j]



"""===============================================================================
    Examples
    1) Printing the relations to instrument 'ABB A'.
    h=FDMCascadeHandler()
    h.q_level=1  # If a unique name exists as key print that name also
    h.verbose=1
    h.traverse('instrument',ael.Instrument['ABB A'].insaddr)

    2) Deleteting the portfolio P1 and all trades etc.
    h=FDMCascadeHandler()
    h.delete_object('portfolio',ael.Portfolio['P1'])

    3) Get the table description for instrument.
    h=FDMCascadeHandler()
    print h.table_descr['instrument']

    4) Display a table of parent-child and corresponding selection methods
    h=FDMCascadeHandler()
    selection=[]
    parent_child=[]
    for (t,d) in h.table_descr.items():
      if d.toAelTableName() != t:
          continue
      if d.getParentRel():
          pname=h.table_descr[d.getParentRel()[1]].toAelTableName()
          cname=d.toAelTableName()
          if not h.get_selection_methods(pname,cname):
              print "FAILED: %s %s" % (pname,cname)
          else:
              for s in h.get_selection_methods(pname,cname):
                  selection.append((pname,s,cname))
                  parent_child.append((cname,s,pname))
    selection.sort()
    print "\n\n"
    print  "%-20s%-20s%-20s\n%s" % ('ael_entity','link method','ael_selection','-'*60)
    for (p,s,c) in selection:
          print "%-20s%-20s%-20s" % (p,s,c)
    print "\n\n"
    parent_child.sort()
    print  "%-20s%-20s%-20s\n%s" % ('child','link method','parent','-')

==============================================================================="""

