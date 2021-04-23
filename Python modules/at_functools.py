import inspect

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
            not_set = [a for a in not_set if not a in acc_kwargs]

            # if all non-defaults have been set, run the decorated function
            if not not_set:
                return func(*acc_args, **acc_kwargs)

            # not all non-defaults have been set, return the "partial" function
            return outer(*acc_args, **acc_kwargs)

        # return the inner function, which has all context set due to closure
        return inner

    # set up the closure for partial functions
    return outer(*args, **kwargs)


def cache_first_result(method):
    """Lazy initialization decorator.

    This method cashes the result and returns the cached value in subsequent
    calls.

    """
    def decorated(*args, **kwargs):
        if not hasattr(method, '_cached'):
            method._cached = method(*args, **kwargs)
        return method._cached
    return decorated
