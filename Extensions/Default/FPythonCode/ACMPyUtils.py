
"""
Utilities that make working with ACM more Pythonic.
"""

from contextlib import contextmanager
import acm

@contextmanager
def Transaction():
    """
    Perform a transaction around the scoped block. Propagates exception to caller.
    Example:
    
    with Transaction():
        a.Commit()
        b.Commit()
        c.Delete()
    """
    acm.BeginTransaction()
    try:
        yield None
        acm.CommitTransaction()
    except:
        acm.AbortTransaction()
        raise

