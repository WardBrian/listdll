"""A reimplementation of Julia's dllist"""

import platform
from typing import List

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
    pass
else:
    def dllist() -> List[str]:
        """
        List the dynamic libraries loaded by the current process.

        This is a wrapper for platform-specific APIs on Windows, Linux, and macOS.

        Returns
        -------
        List[str]
            The names of the dynamic libraries loaded by the current process.
        """
        return _platform_specific_dllist()
