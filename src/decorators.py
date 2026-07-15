import functools


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                result = func(*args, **kwargs)
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{func.__name__} ok\n")
                else:
                    print(f"{func.__name__} ok")
                return result
            except Exception as e:
                if filename:
                    with open(filename, "a", encoding="utf-8") as f:
                        f.write(f"{func.__name__} error {type(e).__name__}: {e}\n")
                else:
                    print(f"{func.__name__} error {type(e).__name__}: {e}")
                raise

        return wrapper

    return decorator
