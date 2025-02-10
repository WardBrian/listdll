import os
import ctypes
from ctypes.util import find_library
from typing import List

# https://developer.apple.com/library/archive/documentation/System/Conceptual/ManPages_iPhoneOS/man3/dyld.3.html

libc = ctypes.CDLL(find_library("c"))
get_image_name = libc["_dyld_get_image_name"]
get_image_name.restype = ctypes.c_char_p


def _platform_specific_dllist() -> List[str]:
    num_images = libc._dyld_image_count()
    libraries = [
        os.fsdecode(name)
        for i in range(num_images)
        if (name := get_image_name(i)) is not None
    ]
    return libraries
