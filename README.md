# Simple-Config

A simple Config class for interacting with yaml configuration files.

## Examples
The following examples assume a file names `example_config.yaml` exists with the following contents:
```yaml
top:
  middle:
    bottom: value

```

Basic Usage:
```python
>>> from config import Config
>>> CONFIG = Config("example_config.yaml")
>>> CONFIG.get("top/middle/bottom")
'value'
# Or use __getitem__ syntax instead
>>> CONFIG["top/middle/bottom"]
'value'
```

The `Config` class also supports supplying custom separators if the default "/" is not acceptable.

```python
from config import Config

>>> CONFIG = Config("example_config.yaml", ".")
>>> CONFIG.get("top.middle")
{'bottom': 'value'}
```

The Config class supports reloading without needing to fully reconstruct the object. This can be handy for implementing a hot-reload with a single CONFIG instance that gets throughout a project.
```python
from config import Config

>>> CONFIG = Config("example_config.yaml")
>>> with open("example_config.yaml", "a") as config_file:
...   print("foo: bar", file=config_file)
...
>>> CONFIG.get("foo")
>>> CONFIG.reload()
>>> CONFIG.get("foo")
'bar'
```

The `Config` class also makes use of a simple caching mechanism to speed up repeat requests for multi-part keys.

```python
>>> from timeit import timeit

# No cache mechanism
>>> timeit('for _ in range(100): CONFIG.get("top/middle/bottom")', setup="from config import Config; CONFIG=Config('example_config.yaml')")
51.61055869999999

# With cache mechanism
>>> timeit('for _ in range(100): CONFIG.get("top/middle/bottom")', setup="from config import Config; CONFIG=Config('example_config.yaml')")
18.241426
```

## Installing
The project currently isn't published to pypi yet, but you can install it using the git url.

`python -m pip install git+ssh://git@github.com/Jordan-Cottle/Simple-Config`

Adding the git url to a `requirements.txt` file also works.
```
$ cat requirements.txt
git+ssh://git@github.com/Jordan-Cottle/Simple-Config
$ python-m pip install -r requirements.txt
```
