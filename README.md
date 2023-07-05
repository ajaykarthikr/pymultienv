# New Env Reader

A python library that provides an easy way to load environment variables from a `.env` or `.ini` file along with type hint support in your IDE.

## Motivation

Since the introduction of type hints in python, it is possible for IDEs to provide type checking. Type hints is very useful in improving developer experience and preventing possible bugs due to type mismatch. However, existing libraries for reading environment variables does not provide exact type hint support. This library aims to provide a easy way to read environment variables with type hint support.

## Credits

This library takes inspiration from a great library [python-decouple](https://github.com/HBNetwork/python-decouple).

## Installation

```bash
pip install newenvreader
```

## Usage

It is recommended to store configuration in the environment separate from code as per [12 Factor App](https://12factor.net/config) methodology. So, let's start by creating a configuration file in the root of your project. This library supports both `.env` and `.ini` file formats.

### Env file

Create a `.env` file in the root of your project. This file will contain all your environment variables.

```text
STR_ENV=hello
INT_ENV=123
FLOAT_ENV=123.456

DB_URL=postgres://user:password@localhost:5432/dbname
```

### Ini file

Incase you prefer `.ini` file over `.env` file, you can create a `settings.ini` file in the root of your project. This file will contain all your environment variables.

```init
[settings]
STR_ENV=hello
INT_ENV=123
FLOAT_ENV=123.456

DB_URL=postgres://user:password@localhost:5432/dbname
```

### Loading environment variables

Import the module in one single place in your application. This will automatically load the environment variables from `.env` file. Then use `get_env` function to read environment variables.

```python
from newenvreader import get_env

val = get_env("STR_ENV")
print(val) # "hello"

# Parse as int
val = get_env("INT_ENV", cast=int)
print(val) # 123

# Provide a default value if environment variable is not set
val = get_env("MY_VAR", default="default value")
print(val) # "default value"
```

Hint: It is recommended to use `get_env` function in one single place to get all your environment variables as constants and then import these constants anywhere you need them.

### Casting

You cast the environment variable to any type you want. All available types in python are supported.

```python
from newenvreader import get_env

# Cast as int
val = get_env("INT_ENV", cast=int)
print(val) # 123

# Cast as float
val = get_env("FLOAT_ENV", cast=float)
print(val) # 123.456

# Cast as bool
val = get_env("BOOL_ENV", cast=bool)
print(val) # True
```

When casting as boolean, the following values are considered as `True`: `true`, `t`, `yes`, `y`, `1`, `on`. And similarly for `False`: `false`, `f`, `no`, `n`, `0`, `""`.

You can also cast to your custom types. For example, if you have a custom type `MyType`, you can cast to it like this:

```python
from newenvreader import get_env

val = get_env("MY_VAR", cast=MyType)
```

Note: when casting int and float types incase the environment variable is not a valid number, it will raise a `ValueError`.


## Caveats
- Undefined environment variables will raise a `KeyError` exception. You can provide a default value by passing `default` argument to `get_env` function.
- Environment present in configuration files takes precedence over environment variables present in the system.
- No multiline support for environment variables.