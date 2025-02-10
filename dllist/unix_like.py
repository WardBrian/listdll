import os
import ctypes
from ctypes.util import find_library
from typing import List

# this uses functions common to Linux and a few other Unix-like systems
# https://man7.org/linux/man-pages/man3/dl_iterate_phdr.3.html
# https://man.freebsd.org/cgi/man.cgi?query=dl_iterate_phdr
# https://man.openbsd.org/dl_iterate_phdr
# https://docs.oracle.com/cd/E88353_01/html/E37843/dl-iterate-phdr-3c.html


class _dl_phdr_info(ctypes.Structure):
    _fields_ = [
        ("dlpi_addr", ctypes.c_void_p),
        ("dlpi_name", ctypes.c_char_p),
        ("dlpi_phdr", ctypes.c_void_p),
        ("dlpi_phnum", ctypes.c_ushort),
    ]


_dl_phdr_callback = ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(_dl_phdr_info),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.py_object),
)


@_dl_phdr_callback
def _info_callback(info, _size, data):
    libraries = data.contents.value
    name = os.fsdecode(info.contents.dlpi_name)
    libraries.append(name)
    return 0


if not hasattr((libc := ctypes.CDLL(None)), "dl_iterate_phdr"):
    raise ImportError("dl_iterate_phdr not found")

_dl_iterate_phdr = libc["dl_iterate_phdr"]
_dl_iterate_phdr.argtypes = [
    _dl_phdr_callback,
    ctypes.POINTER(ctypes.py_object),
]
_dl_iterate_phdr.restype = ctypes.c_int


def _platform_specific_dllist() -> List[str]:
    libraries: List[str] = []
    _dl_iterate_phdr(_info_callback, ctypes.byref(ctypes.py_object(libraries)))

    return libraries
