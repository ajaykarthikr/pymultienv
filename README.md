# newenvreader
A python library to read environment variables with typing support.

# Installation
```bash
pip install newenvreader
```

# Usage
```python
from newenvreader import get_env

val = get_env("MY_VAR")

# Parse as int
val = get_env("MY_VAR", cast=int)
```

