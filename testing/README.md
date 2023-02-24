# Unit testing task

In the `app.py` file you're given an implementation of an app. It exposes endpoint allowing users to get n-th [Fibonacci number](https://en.wikipedia.org/wiki/Fibonacci_number#Definition). The app uses Redis as a cache.

Your task is to:
* write unit tests for `app.py`.

Requirements:
* You **can't** (and don't need to) edit `app.py` file.
* Your tests should achieve 100% code coverage.
* Provide full working solution as a submission (we should be able to successfully run your tests with `pytest .`, without making any edits to it). Include a screenshot of how you run the tests in your submission as well.
* You don't need to **directly** call `get_fib`, `_add_to_cache_and_log` or `_fib` from your tests. You only need to run test client and make a requests to it (the functions above should be called as an effect of this request).
* Remember to test expected behaviour – response status code, content (what value was returned) and logging.

Hints:
* Mock `cache`.
* You can access response content with `response.content`. It's type is `bytes` (eg. `b"1"`). If you want to compare it to an int, you can convert it with `int(response.content)` (so you can directly compare eg. `int(response.content) == 1`).
* You can test if an exception is raised with [`pytest.raises(Exception)`](https://docs.pytest.org/en/stable/reference/reference.html#pytest.raises). See snippet below. Then you can get the exception itself with `err.value`.
```python
with pytest.raises(Exception) as err:
    # Run some code that raises an exception here.
```