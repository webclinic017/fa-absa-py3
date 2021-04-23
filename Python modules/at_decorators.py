import collections
import cPickle
import inspect
import time
from functools import wraps


def retry(ExceptionToCheck, tries=4, delay=5, backoff=2, max_delay=900, logger=None):
    """Retry calling the decorated function using an exponential backoff.

    http://www.saltycrane.com/blog/2009/11/trying-out-retry-decorator-python/
    original from: http://wiki.python.org/moin/PythonDecoratorLibrary#Retry
    (modified version)

    :param ExceptionToCheck: the exception to check. may be a tuple of
        exceptions to check
    :type ExceptionToCheck: Exception or tuple
    :param tries: number of times to try (not retry) before giving up
    :type tries: int
    :param delay: initial delay between retries in seconds
    :type delay: int
    :param backoff: backoff multiplier e.g. value of 2 will double the delay
        each retry
    :type backoff: int
    :param max_delay: Maximum delay time
    :type: int
    :param logger: logger to use. If None, print
    :type logger: logging.Logger instance
    """

    def deco_retry(f):
        @wraps(f)
        def f_retry(*args, **kwargs):
            mtries, mdelay = tries, delay
            while mtries > 1:
                try:
                    return f(*args, **kwargs)
                except ExceptionToCheck as err:
                    msg = "%s, Retrying in %d seconds..." % (str(err), mdelay)
                    if logger:
                        logger.warning(msg)
                    else:
                        print(msg)
                    time.sleep(mdelay)
                    mtries -= 1
                    if mdelay < max_delay:
                        mdelay *= backoff
                    else:
                        mdelay = max_delay
            return f(*args, **kwargs)

        return f_retry  # true decorator

    return deco_retry


def pickle_and_memoize(f):
    cache = {}
    @wraps(f)
    def wrapper(*args, **kwargs):
        key = cPickle.dumps(args, 1) + cPickle.dumps(kwargs, 1)
        if key in cache:
            return cache[key]
        result = f(*args, **kwargs)
        cache[key] = result
        return result
    
    return wrapper


def curried(func, *args, **kwargs):
    """Curried decorator.

    Returns partial functions unless all non-default parameters are received.
    Each call is allowed to redefine all kwargs.

    """

    # get the argspec
    argspec = inspect.getargspec(func)

    # the names of args without default value
    non_default = argspec.args[:-len(argspec.defaults)]

    def outer(*args, **kwargs):
        """Context holder for args between calls of the inner function."""
        def inner(*args2, **kwargs2):
            """Accumulate args and run the decorated function if needed."""

            # accumulate args
            acc_args = list(args)
            acc_args.extend(list(args2))

            # accumulate kwargs
            acc_kwargs = dict(kwargs)
            acc_kwargs.update(kwargs2)

            # get names of non-default params that haven't been set yet
            not_set = non_default[len(acc_args):]
            not_set = filter(lambda a: not a in acc_kwargs, not_set)

            # if all non-defaults have been set, run the decorated function
            if not not_set:
                return func(*acc_args, **acc_kwargs)

            # not all non-defaults have been set, return the "partial" function
            return outer(*acc_args, **acc_kwargs)

        # return the inner function, which has all context set due to closure
        return inner

    # set up the closure for partial functions
    return outer(*args, **kwargs)


def sum_over_multiple(argument_name):
    """
    Create a decorator to optionally sum over a collection of arguments.

    sum_over_multiple('foo') is a decorator that will create a wrapper that:
        - Examines the 'foo' argument (if any) to determine if it's an iterable.
        - If it's not an iterable, it will simply forward all the arguments
          to the underlying function and return its result.
        - Otherwise it will call the underlying function repeatedly with
          the elements of the 'foo' collection in place of the underlying
          function's argument 'foo' and return the sum of all the results.

    E.g. sum_over_multiple('a')(lambda a, b: a + b)([1, 2], 3) == 9

    """
    def decorator(fn):
        argspec = inspect.getargspec(fn)
        argnames = argspec.args
        argpos = argnames.index(argument_name) # Raises ValueError in compile time if not found.
        # Get a mapping of default values, if any.
        defaults = dict(list(zip(argspec.args[-len(argspec.defaults):],
            argspec.defaults))) if argspec.defaults else {}

        def wrapper(*args, **kwargs):
            if argument_name not in kwargs and argpos >= len(args):
                # Argument not explicitly specified, therefore it is looked
                # up in the defaults mapping.
                if argument_name in defaults:
                    argument = defaults[argument_name]
                else:
                    raise TypeError('Missing argument %s' % argument_name)
            elif argument_name in kwargs:
                argument = kwargs[argument_name]
            else:
                argument = args[argpos]
            if not isinstance(argument, collections.Iterable):
                return fn(*args, **kwargs)

            def iter_arguments():
                for value in argument:
                    if argpos >= len(args):
                        # Argument either comes from kwargs or from defaults.
                        new_kwargs = kwargs.copy()
                        new_kwargs[argument_name] = value
                        yield args, new_kwargs
                    else:
                        yield (args[:argpos] + (value,) + args[argpos+1:]), kwargs
            return sum(
                fn(*new_args, **new_kwargs)
                for new_args, new_kwargs in iter_arguments()
            )
        return wrapper
    return decorator
