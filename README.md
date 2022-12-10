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

Run secure container with no capabilities user:
```shell
docker run -it --rm --cap-drop ALL --user 1000 noname
```
