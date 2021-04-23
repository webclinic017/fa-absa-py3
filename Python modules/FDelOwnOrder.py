""" Standard_Queries:1.0.0 """

#Use this AEL script to delete exp orders from the OwnOrder table.

# Note: ael.connect() and ael.disconnect() lines should be activated if the script is executed outside FRONT ARENA
import ael, os
import time

def log(filename,text,mode='w'):
    try:
        fp=open(filename, mode)
        fp.write(str(text)+'\n')
        fp.close()
    except:
        print "Unable to open file %s in mode=%s!" % (filename, mode)
        raise 'Aborts!'
    
def load_ordnbr(filename):
    first=0
    n=0
    for r in ael.dbsql('select ordnbr from own_order order by ordnbr')[0]:
        n=n+1
        if not first:
            log(filename, r[0]) # Creates file
            first=1
        else:
            log(filename, r[0], 'a')
    return n

def chop(s):
    """ safe way to chop strings of numbers"""
    tmp=''
    for t in s:
        if t in ['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']:
            tmp=tmp+t
    return tmp


#ael.connect('<host>:<port>', '<username>','password') # if executed as script
 
print "-START-"

#
# Define FCS_DIR_TMP variable either as the FCS_DIR_TMP environment variable
# or as a valid path.
#
FCS_DIR_TMP="C:\\Temp"
if os.environ.has_key("FCS_DIR_TMP"):
    FCS_DIR_TMP=os.environ["FCS_DIR_TMP"]
elif not os.path.exists(FCS_DIR_TMP):
    msg="""\nERROR: You must define environment variable FCS_DIR_TMP or
define the variable FCS_DIR_TMP (in this script) to a valid path.\nAbort!"""
    raise msg


#
# Nice constants to use
#
cut_off_time=ael.date_today().to_time()                             # Cut off time for exp_time
sd=ael.date_today().to_string("%y%m%d")                             # Short date string
fname_ordnbr=os.path.join(FCS_DIR_TMP, ("ordnbr_%s.tmp" % sd))       #Filename of ordnbr file
fname_last=os.path.join(FCS_DIR_TMP, ("ordnbr_processed_%s.tmp" % sd))# Filename of last processed
last=None                                                           # Last processed ordnbr
ordnbr=''                                                           # Active ordnbr

# Write the ordnbr's to file if not done today
if not os.path.exists(fname_ordnbr):
    print "+ load OwnOrder nbr's to file...",
    n=load_ordnbr(fname_ordnbr)
    print "OK"
    print "+ saved %d ordnbr's to file..." % n
    if os.path.exists(fname_last):
        os.unlink(fname_last)

# Get last processed ordnbr
if os.path.exists(fname_last):
    fp=open(fname_last)
    last=fp.readlines()[0]
    last=chop(last)
    fp.close()
    print "+ last processed ordnbr was: %s" % last

fp_ordnbr=open(fname_ordnbr, 'r')


# Process each ordnbr and delete the ones the fullfills the criteria
# and skip already processed ordnbr's

print "+ process ordnbr's..."
n=0
n_del=0
n_skip=0
for ordnbr in fp_ordnbr.readlines():
    ordnbr=chop(ordnbr)
    if last:
        if ordnbr != last: # Skip already processed lines
            n_skip=n_skip+1
            continue
        else:
            print "+ skipped %d already processed ordnbr's..." % (n_skip + 1)
            last=None # Done !
            continue  # Next one is the one to process
    if len(ordnbr) <= 0:
        continue 
    o=ael.OwnOrder[int(ordnbr)]
    if not o:
        continue # Strange
    n=n+1
    if not o.insaddr or (o.insaddr and o.exp_time < cut_off_time):
        try:
            o.delete()
            print "Deleted OwnOrder:", o.ordnbr
            ael.poll()
            n_del=n_del+1
        except:
            pass
    log(fname_last, ordnbr) # Save last processed ordnbr in file
fp_ordnbr.close()
print "+ Deteled %d own orders of %d remaining orders" % (n_del, n)
print "-END-"
    
# ael.disconnect()  # If executed as a script
