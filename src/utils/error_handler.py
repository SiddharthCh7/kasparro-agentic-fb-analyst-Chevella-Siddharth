import inspect

def handle_errors(func):
    if inspect.iscoroutinefunction(func):

        async def wrapper(state, *args, **kwargs):
            try:
                return await func(state, *args, **kwargs)
            except Exception as e:
                raise Exception(f"Error in {func.__name__}: {e}") from e

        return wrapper

    else:

        def wrapper(state, *args, **kwargs):
            try:
                return func(state, *args, **kwargs)
            except Exception as e:
                raise Exception(f"Error in {func.__name__}: {e}") from e

        return wrapper
