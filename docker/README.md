# Docker task

In the `app.py` file you're given an implementation of an app. It exposes endpoint allowing users to get n-th [Fibonacci number](https://en.wikipedia.org/wiki/Fibonacci_number#Definition). The app uses Redis as a cache.

Your task is to:
* write `Dockerfile` to run the app in a container,
* write `docker-compose.yml` to run the app together with Redis.

Requirements:
* You **can't** (and don't need to) edit `app.py` file.
* You **can** create any other files you find useful.
* The app should be accessible on port `8000` on host computer (so one should be able to access it eg. via web browser `0.0.0.0:8000/fib/10`).
* In the submission include the whole working solution – after downloading your solution we should be able to run it with `docker compose up`, without making any edits or fixes.

Hints:
* You can use [`redis:alpine`](https://hub.docker.com/_/redis) image to run Redis. It accepts traffic on port `6379` by default.
* Creating `requirements.txt` file might be useful for managing required packages.