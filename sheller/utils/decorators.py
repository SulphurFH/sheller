import functools


def validate_parser(parser_class):
    def decorator(view_func):
        @functools.wraps(view_func)
        def wrapper(request, *args, **kwargs):
            params = parser_class.validate()
            return view_func(request, params, *args, **kwargs)
        return wrapper
    return decorator
