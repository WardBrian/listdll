import ctypes
from ctypes import wintypes
from typing import List, Optional

# https://learn.microsoft.com/windows/win32/api/psapi/nf-psapi-enumprocessmodules
# https://learn.microsoft.com/windows/win32/api/libloaderapi/nf-libloaderapi-getmodulefilenamew

_kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)

_get_current_process = _kernel32["GetCurrentProcess"]
_get_current_process.restype = wintypes.HANDLE

_k32_get_module_file_name = _kernel32["GetModuleFileNameW"]
_k32_get_module_file_name.restype = wintypes.DWORD
_k32_get_module_file_name.argtypes = (
    wintypes.HMODULE,
    wintypes.LPWSTR,
    wintypes.DWORD,
)

_psapi = ctypes.WinDLL("psapi", use_last_error=True)
_enum_process_modules = _psapi["EnumProcessModules"]
_enum_process_modules.restype = wintypes.BOOL
_enum_process_modules.argtypes = (
    wintypes.HANDLE,
    ctypes.POINTER(wintypes.HMODULE),
    wintypes.DWORD,
    wintypes.LPDWORD,
)


def _get_module_filename(module: wintypes.HMODULE) -> Optional[str]:
    name = (wintypes.WCHAR * 32767)()  # UNICODE_STRING_MAX_CHARS
    if _k32_get_module_file_name(module, name, len(name)):
        return name.value
    return None


def _get_module_handles() -> List[wintypes.HMODULE]:
    process = _get_current_process()
    space_needed = wintypes.DWORD()
    n = 1024
    while True:
        modules = (wintypes.HMODULE * n)()
        if not _enum_process_modules(
            process, modules, ctypes.sizeof(modules), ctypes.byref(space_needed)
        ):
            err = ctypes.get_last_error()
            msg = ctypes.FormatError(err).strip()
            raise ctypes.WinError(err, f"EnumProcessModules failed: {msg}")
        n = space_needed.value // ctypes.sizeof(wintypes.HMODULE)
        if n <= len(modules):
            return modules[:n]


def _platform_specific_dllist() -> List[str]:
    modules = _get_module_handles()
    libraries = [name for h in modules if (name := _get_module_filename(h)) is not None]
    return libraries
