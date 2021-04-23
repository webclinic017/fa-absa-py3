from __future__ import print_function
import acm

#
# return textual description of obj together with its type
#
def describe(obj):
    d = ''
    t = ' '
    acmObj = hasattr(obj, 'Class')
    if not acmObj:
        t = ' '
        d = str(obj)
    elif obj.IsString() and str(obj) != '.root':
        # symbols are used internally for native c functions
        t = 'c'
    elif obj.IsEvaluator():
        t = 'e'
    elif obj.IsKindOf('FFunction'):
        t = 'f'
    elif obj.IsKindOf('FMethod'):
        t = 'm'
        rc = obj.ReceiverClass()
        if rc:
            d = str(rc.Name()) + '.'
        else:
            d = str(obj.ClassName()) + ': ?.'

    if acmObj:
        try:
            d = d + obj.StringKey()
        except:
            d = d + '?'
    return [d, t]

# length of info text
textLen = 95

#
# print (top list)
#
def dumpTop(tlist, count):
    tcount = len(tlist)
    print ('\ntop %d(%d):' % (count, tcount))
    print ('-' * (textLen + 56) + '\n' + ' ' * (textLen + 17), 'count       T ms')
    if count <= 0 or tcount < count:
        count = tcount
    for n in range(count):
        pd = tlist[n]
        descr, type = describe(pd.Object())
        print ('%3d' % n, '%-*.*s' % (textLen, textLen, descr) + ' ' + type + ' %16d' % pd.Count() + ' %10.3f' % ((pd.Tacc() - pd.Dacc()) * 1000))

#
# dump measurements sorted by Tacc (T+D)
# '~' denotes recursive call
#
def dumpImpl(pd, count, visited, level):
    descr, type = describe(pd.Object())
    txt = '%-*.*s' % (textLen + 4 - level, textLen + 4 - level, descr) + ' ' + type + ' %16s' % ('(%d)%d' % (count, pd.Count()))
    if visited.Includes(pd):
        print ('~' * level + txt)
        return
    visited.Add(pd)
    if level == 0:
        print ('-' * (textLen + 56) + '\n' + ' ' * (textLen + 17), 'count     T+D ms       D ms     P cost')
    print ('>' * level + txt, '%10.3f' % (pd.Tacc() * 1000), '%10.3f' % (pd.Dacc() * 1000), '%10.3f' % (pd.TPacc() * 1000))
    da = pd.Descendants().AsArray().SortByProperty('Tacc', False)
    for d in da:
        dumpImpl(d, pd.DescendantCount(d), visited, level + 1)
    
def dump(pd):
    visited = acm.FIdentitySet()
    dumpImpl(pd, 1, visited, 0)

#
# dump snapshot since last call
#
tp = None
def snapshot(verbose):
    global tp
    tp = acm.FTimeProfiler.Select01('.Name = "snapshot"', '')
    if not tp:
        print ('creating profiler, resolution is %.3fus' % (1000000.0 / acm.FTimeProfiler.TicksPerSecond()))
        acm.AEF.EnablePythonProfiling()
        tp = acm.FTimeProfiler()
        tp.Name = 'snapshot'
    else:
        shot = tp.Snapshot()
        if verbose:
            dump(shot)
        dumpTop(shot.Items(), 25)
    tp.PrepareSnapshot(-1)

def snapshotVerboseMenuHook(eii):
    snapshot(True)

def snapshotBriefMenuHook(eii):
    snapshot(False)

def snapshotMenuHook(eii):
    snapshot(False)



