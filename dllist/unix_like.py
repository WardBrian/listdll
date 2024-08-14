import os
import ctypes
from ctypes.util import find_library
from typing import List

# this uses functions common to Linux and a few other Unix-like systems
# https://man7.org/linux/man-pages/man3/dl_iterate_phdr.3.html
# https://man.freebsd.org/cgi/man.cgi?query=dl_iterate_phdr
# https://man.openbsd.org/dl_iterate_phdr
# https://docs.oracle.com/cd/E88353_01/html/E37843/dl-iterate-phdr-3c.html


class dl_phdr_info(ctypes.Structure):
    _fields_ = [
        ("dlpi_addr", ctypes.c_void_p),
        ("dlpi_name", ctypes.c_char_p),
        ("dlpi_phdr", ctypes.c_void_p),
        ("dlpi_phnum", ctypes.c_ushort),
    ]


@ctypes.CFUNCTYPE(
    ctypes.c_int,
    ctypes.POINTER(dl_phdr_info),
    ctypes.c_size_t,
    ctypes.POINTER(ctypes.py_object),
)
def info_callback(info, _size, data):
    libraries = data.contents.value
    name = os.fsdecode(info.contents.dlpi_name)
    libraries.append(name)

    return 0


libc_path = find_library("c")
if libc_path is None or not hasattr(
    (libc := ctypes.CDLL(libc_path)), "dl_iterate_phdr"
):
    raise ImportError("dl_iterate_phdr not found")


def _platform_specific_dllist() -> List[str]:
    libraries: List[str] = []
    libc.dl_iterate_phdr(info_callback, ctypes.byref(ctypes.py_object(libraries)))

    # remove the first entry, which is the executable itself
    return libraries[1:]
