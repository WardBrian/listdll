# dllist

> [!NOTE]
> This functionality is available [in the standard library](https://github.com/python/cpython/pull/122946) starting in Python 3.14

A very small Python library to list the DLLs loaded by the current process.
This is equivalent to the [`dllist`](https://docs.julialang.org/en/v1/stdlib/Libdl/#Base.Libc.Libdl.dllist) function in Julia.

*Note*: This library is tested on macOS, Linux, and Windows.
Some platforms which provide the same API as Linux (e.g. FreeBSD) also work.

## Installation

`dllist` is [available on PyPI](https://pypi.org/project/dllist/):

```
pip install dllist
```

## Usage
The single function this library provides is `dllist()`, which returns a list of the shared
ibraries loaded by the current process.
The first element is usually a representation of the current process itself (often, the empty string),
and the rest are the shared libraries loaded by the process.
```python
import dllist
print(dllist.dllist())
# ['', 'linux-vdso.so.1', '/lib/x86_64-linux-gnu/libpthread.so.0', '/lib/x86_64-linux-gnu/libdl.so.2', ... ]
```

*Note*: The library paths are not postprocessed by this library. Depending on your usage, you may need to convert them to absolute paths and/or perform case-normalization (Windows).
