import redis
import uvicorn
import logging

from fastapi import FastAPI


logger = logging.getLogger()
app = FastAPI()
cache = redis.Redis(host="redis", port=6379)


def _add_to_cache_and_log(n, result):
    cache.set(n, result)
    logger.info(f"Added to cache: {n}: {result}.")


def _fib(n: int):
    """This function calculates n-th Fibonacci number."""
    if n < 0:
        raise Exception(f"Invalid argument: {n}.")
    elif n == 0:
        _add_to_cache_and_log(0, 0)
        return 0

    result = 1
    prev = 0
    for i in range(n - 1):
        tmp = result
        result = result + prev
        prev = tmp

    _add_to_cache_and_log(n, result)
    return result


@app.get("/fib/{n}")
def get_fib(n: int):
    if cache.exists(n):
        logger.info(f"Getting result for n = {n} from cache.")
        return cache.get(n)
    else:
        logger.info(f"Cache for {n} not found.")

    return _fib(n)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    uvicorn.run(app, host="0.0.0.0", port=3000)
