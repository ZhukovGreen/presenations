import logging
import pathlib
import sys

import pytest

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch

logger = logging.getLogger(__name__)


def test_stupid_example():
    assert True


def test_a_bit_smarter_example():
    actual = {1: 2, 3: "a"}
    expected = {1: 2, 3: "b", 4: "c"}
    assert actual == expected


def test_builtin_fixture_demo(tmp_path: pathlib.Path):
    assert tmp_path == 1


def test_builtin_fixture_monkeypatching(monkeypatch: MonkeyPatch):
    assert sys.version == "sdsdsd"


def test_builtin_fixture_caplog(caplog: LogCaptureFixture):

    logger.info("Hello caplog")
    import pdb;pdb.set_trace()
