import os
import ctypes
from ctypes.util import find_library
from typing import List

# https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/dyld.3.html

libc = ctypes.CDLL(find_library("c"))
get_image_name = libc["_dyld_get_image_name"]
get_image_name.restype = ctypes.c_char_p

def _platform_specific_dllist() -> List[str]:
    libraries = []

    num_images = libc._dyld_image_count()

    # start at 1 to skip executable
    for i in range(1, num_images):
        raw_name = get_image_name(i)
        name = os.fsdecode(raw_name)
        libraries.append(name)

    return libraries
