import os
import sys
import pytest


@pytest.fixture(scope="session")
def import_path() -> None:
    path = os.path.join(os.path.dirname(__file__), "wd/")
    orig_path = sys.path[:]
    try:
        sys.path.insert(0, path)
        yield
    finally:
        sys.path = orig_path
