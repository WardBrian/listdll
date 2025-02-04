import platform

import pytest

system = platform.system()

if (
    system.startswith("Linux")
    or system.startswith("FreeBSD")
    or system.startswith("Darwin")
    or system.startswith("Windows")
):
    pytest.skip(reason="Only runs on unknown platforms", allow_module_level=True)


def test_dllist_basic() -> None:
    import dllist
    assert not hasattr(dllist, "dllist")
