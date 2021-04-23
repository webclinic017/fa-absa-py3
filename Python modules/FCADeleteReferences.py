""" CorporateActions:1.2.2 """

import FCAGeneral
import sys, getopt, string
import re, os
import time
import ael

def deleteReferences(instruments, commit = 1):

    ###########################################################
    #Delete listleafs for instruments in instruments.
    #For performance resons each list nodes leafs are handled in
    #one transaction.
    ###########################################################
    FCAGeneral.logme('Reading ListLeafs...')
    list_nodes={}   # nodenbr : (ListNode,[list_leaf lefnbr's])
    n=0             # Counter of number of list leafs
    n_errors=0
    summary={}
    dangling_leafs={}
    for i in instruments:
        for leaf in ael.ListLeaf.select("insaddr=%d" % i.insaddr):
            try: # To avoid problems with dangling list_leafs
                if not leaf.nodnbr or not leaf.insaddr:
                    dangling_leafs[leaf.lefnbr]=None
                else:
                    (ln, ld)=list_nodes.get(leaf.nodnbr.nodnbr, (leaf.nodnbr, {}))
                    ld[leaf.lefnbr]=None
                    list_nodes[ln.nodnbr]=(ln, ld)
                    n=n+1
            except:
                n_errors=n_errors+1
                FCAGeneral.logme('Dangling ListLeaf: %d' % leaf.lefnbr)


    ###########################################################
    # OK, now delete OK elements
    ###########################################################
    FCAGeneral.logme('Deleting %d ListLeafs...' % n)
    n=0 # True number
    for (dummy, (ln, ld)) in list_nodes.items():
        FCAGeneral.logme('+ will delete %-5d leafs for ListNode %s(%d)' % (len(ld), ln.id, ln.nodnbr))
        if commit:
            FCAGeneral.logme('+ deleting %-5d leafs for ListNode %s(%d)' % (len(ld), ln.id, ln.nodnbr))
            ln2=ln.clone()
            for leaf in ln2.leafs().members():
                if ld.has_key(leaf.lefnbr):
                    leaf.delete()
                    n=n+1
            ln2.commit()
    ael.poll() # refresh
    FCAGeneral.logme('Delete of ListLeafs finished!')
    summary['ListLeif']=(n, n_errors, 0)
    if n_errors > 0:
        FCAGeneral.logme('Found %d danglings leafs! See logfile or printout' % n_errors)

    if len(dangling_leafs) > 0:
        FCAGeneral.logme('Deleting %d dangling ListLeafs...' % len(dangling_leafs))
        leafs=map(str, dangling_leafs.keys())
        i=0
        n_max=100
        tmp=[]
        import FDMCascadeHandler
        h=FDMCascadeHandler.FDMCascadeHandler()
        while leafs:
            tmp.append(leafs.pop(0))
            if len(tmp) == n_max:
                stmt="delete from list_leaf where lefnbr in (%s)" % string.join(tmp, ',')
                ael.dbsql(stmt)
                tmp=[]
        if tmp:
            stmt="delete from list_leaf where lefnbr in (%s)" % string.join(tmp, ',')
            ael.dbsql(stmt)
        FCAGeneral.logme('Synchronize with ads')
        h.synchronize_with_ads()
        FCAGeneral.logme('Deleted %d dangling ListLeafs!' % len(dangling_leafs))
        summary['Dangling ListLeif']=(n, n_errors, 0)





    ###########################################################
    # Dropping PriceDefinitions, OrderBooks and OwnOrders is done in the same way
    # except that for an OwnOrders trade references must be checked or ignored.
    # To avoid reading to much data errors in dropping OwnOrders is done by trusting
    # check of reference integrity by server.
    ###########################################################
    table_descr=[('OrderBook', 'order_book'),
        ('PriceDefinition', 'price_definition'),
        ('OwnOrder', 'own_order')]
    ignore_ins={} # dict of insaddr of instruments to ignore because of own order references
    n_errors_own=0 #OwnOrders
    n_errors=0 #
    n_commit_freq=500 # Commit frequence
    for (name, dbsql_name) in table_descr:
        FCAGeneral.logme("Reading the %s's..." % name)
        exec('ael_table=ael.%s' % name)
        entities=[]
        for i in instruments:
            selection=[]
            try:
                sel= ael_table.select('insaddr=%d' % i.insaddr)
                for e in sel:
                    entities.append(e)
            except:
                #############################################
                # Try using dbsql because select doesn't work
                # on OwnOrders
                #############################################
                FCAGeneral.logme('Tries with dbsql for %s on %s' % (name, i.insid))
                id=''
                for k in ael_table.keys():
                    if k[1] == 'primary':
                        id=k[0]
                        break
                if id:
                    stmt='select %s from %s where insaddr = %d' % (id, dbsql_name, i.insaddr)
                    #logW('Tries with dbsql statement: %s' % stmt)
                    try:
                        for id in ael.dbsql(stmt)[0]:
                            entities.append(ael_table[int(id[0])])
                    except:
                        FCAGeneral.logme('ERROR: Failed to select %d for %s' % (i.insaddr, name))
        FCAGeneral.logme("Will Delete %d %s's..." % (len(entities), name))
        n_del=0
        n_err=0
        n_ign=0
        if commit:
            FCAGeneral.logme("Deleting %d %s's..." % (len(entities), name))
            ael.begin_transaction()
            for j in range(len(entities)):
                if not j%n_commit_freq:
                    ael.commit_transaction()
                    FCAGeneral.logme('Commited %d(%d) %s' % (n_commit_freq, j, name))
                    ael.begin_transaction()
                e=entities[j]
                try:
                    e.delete()
                    n_del=n_del+1
                except:
                    if name != 'OwnOrder':
                        FCAGeneral.logme('Failed to delete:\n%s\n\n' % e.pp())
                        n_errors=n_errors+1
                        n_err=n_err+1
                    else:
                        n_errors_own=n_errors_own
                        ignore_ins[e.insaddr.insaddr]=None
                        n_ign=n_ign+1
        else:
            n_del=len(entities) # For test logging
        try:
            ael.commit_transaction()
            FCAGeneral.logme('Commited %d(%d) %n' % (j%n_commit_freq, j, name))
        except: pass
        summary[name]=(n_del, n_err, n_ign)
        ael.poll() #refresh
        if commit:
            FCAGeneral.logme('Delete of %s finished!' % name)




    ###########################################################
    # Log found errors.
    # NOTE: OwnOrder errors should be ignored!
    ###########################################################

    if n_errors+n_errors_own > 0:
        names=[]
        for (n, d) in table_descr:
            names.append(n)
        tables=string.join(names, ',')
        FCAGeneral.logme('Total number of errors when deleting %s: %d' % (tables, n_errors+n_errors_own))
    if n_errors_own > 0:
        FCAGeneral.logme('Total number of OwnOrder errors: %d' % n_errors_own)
        FCAGeneral.logme('Total number of instruments to skipped(by OwnOrder errors): %d' % len(ignore_ins))






