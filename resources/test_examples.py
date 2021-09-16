import logging
import pathlib
import sys
import typing

import pytest

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch


logger = logging.getLogger(__name__)


def test_stupid_example() -> None:
    assert True


def test_a_bit_smarter_example() -> None:
    actual = {1: 2, 3: "a"}
    expected = {1: 2, 3: "b", 4: "c"}
    assert actual == expected


def test_builtin_fixture_demo(tmp_path: pathlib.Path) -> None:
    assert tmp_path == pathlib.Path


def test_builtin_fixture_monkeypatching(monkeypatch: MonkeyPatch) -> None:
    assert sys.version == "sdsdsd"


def test_builtin_fixture_caplog(caplog: LogCaptureFixture) -> None:

    logger.info("Hello caplog")
    assert caplog.records == []


@pytest.fixture()
def some_fixture() -> typing.Generator[None, None, None]:
    logger.info("before test execution!")
    yield
    logger.info("after test execution!")


def test_custom_yield_fixture(
    some_fixture: None,
    caplog: LogCaptureFixture,
) -> None:
    logger.info("-----> executing test......")
    assert len(caplog.records) == 1


def sum_(
    a: int,
    b: int,
) -> int:
    """Function we test."""
    return a + b


@pytest.mark.parametrize(
    (
        "a",
        "b",
        "expected",
        "exp_exception",
    ),
    (
        (
            1,
            2,
            3,
            None,
        ),
        (
            0,
            0,
            0,
            None,
        ),
        (
            0,
            0,
            0,
            None,
        ),
        (
            "1",
            1,
            None,
            TypeError,
        ),
    ),
)
def test_sum_a_b(
    a,
    b,
    expected,
    exp_exception,
):
    if exp_exception:
        with pytest.raises(
            exp_exception,
            match='^can only concatenate str.+',
        ):
            sum_(a, b)
    else:
        assert sum_(a, b) == expected
