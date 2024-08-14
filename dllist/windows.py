import ctypes
import warnings
from ctypes import wintypes
from typing import List, Optional

# https://learn.microsoft.com/windows/win32/api/psapi/nf-psapi-enumprocessmodules
# https://learn.microsoft.com/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
_psapi = ctypes.WinDLL("psapi", use_last_error=True)

GetCurrentProcess =_kernel32["GetCurrentProcess"]
GetCurrentProcess.restype = wintypes.HANDLE

GetModuleFileNameW = _kernel32["GetModuleFileNameW"]
GetModuleFileNameW.restype = wintypes.DWORD
GetModuleFileNameW.argtypes = (
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD,
)

EnumProcessModules = _psapi["EnumProcessModules"]
EnumProcessModules.restype = wintypes.BOOL
EnumProcessModules.argtypes = (
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HMODULE),
    wintypes.DWORD,
    wintypes.LPDWORD,
)


def get_module_filename(hModule: wintypes.HMODULE) -> Optional[str]:
    name = (wintypes.WCHAR * 32767)()  # UNICODE_STRING_MAX_CHARS
    if GetModuleFileNameW(hModule, name, len(name)):
        return name.value
    error = ctypes.get_last_error()
    warnings.warn(
        f"Failed to get module file name for module {hModule}: "
        f"GetModuleFileNameW failed with error code {error}",
        stacklevel=2,
    )
    return None


def get_module_handles() -> List[wintypes.HMODULE]:
    hProcess = GetCurrentProcess()
    cbNeeded = wintypes.DWORD()
    n = 1024
    while True:
        modules = (wintypes.HMODULE * n)()
        if not EnumProcessModules(
            hProcess, modules, ctypes.sizeof(modules), ctypes.byref(cbNeeded)
        ):
            error = ctypes.get_last_error()
            raise RuntimeError(
                f"EnumProcessModules failed with error code {error}"
            )
        n = cbNeeded.value // ctypes.sizeof(wintypes.HMODULE)
        if n <= len(modules):
            return modules[:n]


def _platform_specific_dllist() -> List[str]:
    # skip first entry, which is the executable itself
    modules = get_module_handles()[1:]
    libraries = [name for h in modules if (name := get_module_filename(h)) is not None]
    return libraries
