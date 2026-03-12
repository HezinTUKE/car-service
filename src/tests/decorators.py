import time
from functools import wraps

from celery.backends.database import retry


# Task 1 solution
def log_calls(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"Calling function {func.__name__}")
        return func(*args, **kwargs)

    return wrapper


# Task 2 solution
def retry(n):
    def decorator(function):
        @wraps(function)
        def wrapper(*args, **kwargs):
            res = None
            for i in range(n):
                try:
                    res = function(*args, **kwargs)
                except Exception:
                    print(f"Attempt {i+1} failed")
            return res

        return wrapper
    return decorator


# Task 3 solution
def timer(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        func(*args, **kwargs)
        print("Execution time: ", time.time() - start)
    return wrapper


# Task 4 solution
def require_auth(func):
    @wraps(func)
    def wrapper(user: dict):

        if user["authenticated"]:
            print("Sensitive data")
            return func(user)
        else:
            print("Access denied")
    return wrapper


# Task 5 solution
def cache_result(func):
    cache = {}

    @wraps(func)
    def wrapper(*args, **kwargs):

        key = (args, tuple(kwargs.items()))

        if key in cache:
            return cache[key]

        result = func(*args, **kwargs)
        cache[key] = result
        return result

    return wrapper


def rate_limit(max_calls, period):
    def decorator(function):
        calls = []

        @wraps(function)
        def wrapper(*args, **kwargs):
            nonlocal calls
            now = time.time()

            while calls and now - calls[0] > period:
                calls.pop(0)

            if len(calls) < max_calls:
                calls.append(now)
                return function(*args, **kwargs)

            print("Rate limit exceeded")
            return None
        return wrapper
    return decorator


@log_calls
def greet():
    print("Hello!")


@timer
def slow_function():
    time.sleep(2)


@require_auth
def get_data(user):
    print("Sensitive data")


@cache_result
def slow_add(a, b):
    print("Calculating...")
    return a + b


@cache_result
def slow_add(a, b):
    print("Calculating...")
    return a + b


@retry(3)
def unstable():
    raise Exception("Unstable")


@rate_limit(3, 10)
def send_request():
    print("Request sent")


send_request()
send_request()
send_request()
send_request()
