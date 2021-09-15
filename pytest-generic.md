# Pytest introduction

---

Pytest is a software testing framework. 
https://docs.pytest.org/en/stable/

----

I'd better focus on practical aspects to let you write Pytest compatible tests easier.

----

:hearts: But pytest is awesome: :hearts:
- It is the most popular testing framework in Python
In according with 2020 python developer [survey](https://www.jetbrains.com/lp/python-developers-survey-2020/):
![](https://i.imgur.com/bxK3j56.png)
And the adoption is very rapid. Starting from 2017 pytest is strongly dominating over other frameworks

----

except the percent of people who is not testing their software at all. Those percent was always big :rolling_on_the_floor_laughing: 

---

## How run tests

From top of my head the most frequently used commands are:

```bash=
$ pytest    # to run the pytest session
$ pytest -k 'some pattern or expression here'    # to run tests matching the pattern
$ pytest --lf    # run last failed tests only
$ pytest --pdb   # fall into python debugger if test fails
$ pytest /some/path     # run tests in the /some/path
```

----

Otherwise check `pytest --help` or https://docs.pytest.org

---

## How test looks like

----

Open terminal:
cd $CODE/talks/

---

## Other interesting things about fixtures

----

Cleanup - yield fixtures

```python=
@pytest.fixture
def sending_user(mail_admin):
    # Runs when fixture invoked at test run
    user = mail_admin.create_user()
    yield user
    # Runs when fixture scope teardown initiated
    # (i.e. after particular test run )
    admin_client.delete_user(user)
```

----

A lot of interesting examples are in the documentation (https://docs.pytest.org/en/stable/fixture.html)

- Fixtures as factories
- Parametrizing fixtures (by adding a fixture your test will be parametrized)
https://github.com/oamg/convert2rhel/blob/main/convert2rhel/unit_tests/conftest.py#L64
- ...

---

## Test parametrization

One cool feature of pytest is [parametrization](https://docs.pytest.org/en/stable/parametrize.html?highlight=fixtures)

----

```python=
@pytest.mark.parametrize(
    (
        "has_openjdk",
        "can_successfully_apply_workaround",
        "mkdir_p_should_raise",
        "check_message_in_log",
        "check_message_not_in_log",
    ),
    [
        # All is fine case
        (
            True,
            True,
            None,
            "openjdk workaround applied successfully.",
            "Can't create %s" % OPENJDK_RPM_STATE_DIR,
        ),
        # openjdk presented, but OSError when trying to apply workaround
        (
            True,
            False,
            OSError,
            "Can't create %s" % OPENJDK_RPM_STATE_DIR,
            "openjdk workaround applied successfully.",
        ),
        # No openjdk
        (False, False, None, None, None),
    ],
)
def test_perform_java_openjdk_workaround(
    has_openjdk,
    can_successfully_apply_workaround,
    mkdir_p_should_raise,
    check_message_in_log,
    check_message_not_in_log,
    monkeypatch,
    caplog,
):
    mkdir_p_mocked = (
        mock.Mock(side_effect=mkdir_p_should_raise())
        if mkdir_p_should_raise
        else mock.Mock()
    )
    has_rpm_mocked = mock.Mock(return_value=has_openjdk)

    monkeypatch.setattr(
        special_cases,
        "mkdir_p",
        value=mkdir_p_mocked,
    )
    monkeypatch.setattr(
        special_cases.system_info,
        "is_rpm_installed",
        value=has_rpm_mocked,
    )
    perform_java_openjdk_workaround()

    # check logs
    if check_message_in_log:
        assert check_message_in_log in caplog.text
    if check_message_not_in_log:
        assert check_message_not_in_log not in caplog.text

    # check calls
    if has_openjdk:
        mkdir_p_mocked.assert_called()
    else:
        mkdir_p_mocked.assert_not_called()
    has_rpm_mocked.assert_called()
```

---

## Pytest markers


----

Pytest markers helps you categorize your tests into groups and then decide which
groups to run.

```python=
@pytest.mark.webtest
def test_send_http():
    pass
```

```bash=
$ pytest -m webtest
```

Will execute only tests marked as `webtest`

----

Usecases:
- Runnig tests in different environments (some group in container, some in VM etc.)
- Running long duration tests separately
- What you invent

----

There are builtin markers:

```pytest
@pytest.mark.skip()
@pytest.mark.skipif(condition)
```

---

## Pytest plugins

----

You can see it as a pytest fixture provisioned from another package.

----

Most popular plugins for me:
- pytest-cov (coverage report)
- pytest-xdist (test parallelization, isolation)
- pytest-asyncio (for running coroutines in easy way)
- pytest-sugar (for beautiful test session reports)
- pytest-mock (pytest friendly Mock with nice reports)

More on https://github.com/augustogoulart/awesome-pytest

---

## Pytest configuration

----

pyproject.toml or pytest.ini

check https://docs.pytest.org/en/stable/customize.html

----

Example:
```
[tool.pytest.ini_options]
minversion = "6.0.0"
addopts = "-vv -s --tb=native"
testpaths = "tests/"
log_cli = true
log_cli_level = "DEBUG"
log_cli_format = "| %(asctime)s | %(name)s | %(levelname)s | %(filename)s | %(message)s"
```

---

## :question: Questions :question: 

---

Thank you for your attention!

---

with :heart: to Python
https://zhukovgreen.pro
