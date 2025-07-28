from functools import lru_cache

def cached(maxsize: int = 128):
    def decorator(fn):
        return lru_cache(maxsize=maxsize)(fn)
    return decorator
