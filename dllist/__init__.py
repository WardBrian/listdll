"""A reimplementation of Julia's dllist"""

import platform
import warnings
from typing import List, Optional

__version__ = "2.0.0"

_system = platform.system().lower()
try:
    if _system.startswith("darwin"):
        from .macos import _platform_specific_dllist
    elif _system.startswith("windows") or _system.startswith("microsoft"):
        from .windows import _platform_specific_dllist
    else:
        # just try the Unix-like implementation
        from .unix_like import _platform_specific_dllist
except ImportError:
    # thrown by unix_like if dl_iterate_phdr is not found
    def _platform_specific_dllist() -> Optional[List[str]]:
        warnings.warn(
            f"Unable to list loaded libraries for unsupported platform {_system}"
        )
        return None


def dllist() -> Optional[List[str]]:
    """
    List the dynamic libraries loaded by the current process.

    This is a wrapper for platform-specific APIs on Windows, Linux, and macOS.
    On other platforms, this function will return an empty list.

    Returns
    -------
    List[str]
        The names of the dynamic libraries loaded by the current process.
    """
    try:
        return _platform_specific_dllist()
    except Exception as e:
        warnings.warn(
            f"Unable to list loaded libraries: {e}",
        )
        return None
