# Example Package

This is a simple example package. You can use
[Github-flavored Markdown](https://guides.github.com/features/mastering-markdown/)
to write your content.

https://packaging.python.org/en/latest/tutorials/packaging-projects/


Build dist
```sh
pip install --upgrade pip build
python -m build
```

Run secure container with no capabilities' user:
```shell
docker run -it --rm --cap-drop ALL --user 1000 noname
```

Gunicorn recommends using (2 x <num_of_cores>) + 1 workers.
This mean that a single CPU container, should spawn 3 workers.
By default, Docker container has access to all host's CPU's.
Gunicorn command for container:
```shell
gunicorn -k uvicorn.workers.UvicornWorker --workers 3 -b 0.0.0.0:8080 --worker-tmp-dir /dev/shm noname.main:app
```

For development, we can use uvicorn server with reload
```shell
uvicorn noname.main:app --reload
```

We can test performance by executing:
```shell
ab -n 50 -c 5 -k http://local.awaitq.com:8000/
```

We could use Poetry for dependency management, but only for local (non docker).
In docker, we could export from portainer requirements.txt file and install dependencies by pip.


## Alembic

We can use symbols like head, heads or base, current to specify the current revision(s).

```shell
alembic revision --autogenerate -m "Migration message."
```

```shell
alembic revision -m "Migration message"
```

```shell
alembic upgrade head
```

```shell
alembic upgrade +1
```

```shell
alembic downgrade -1
```

```shell
 alembic upgrade <previous>:<current> --sql
```

```shell
 alembic downgrade <current>:<previous> --sql
```

```shell
alembic downgrade head:base --sql
```

```shell
alembic downgrade base
```
