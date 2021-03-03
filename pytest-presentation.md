# Pytest introduction for convert2rhel
![](https://i.imgur.com/eLypzrd.png)

---

Pytest is a framework for tests. Details are on [Pytest web](https://docs.pytest.org/en/stable/)

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

## How test looks like

----

```python
def test_logger_custom_logger(tmpdir, caplog):
    """Test CustomLogger."""
    log_fname = "convert2rhel.log"
    logger_module.initialize_logger(log_name=log_fname, log_dir=tmpdir)
    logger = logging.getLogger(__name__)
    logger.task("Some task")
    logger.file("Some task write to file")
    with pytest.raises(SystemExit):
        logger.critical("Critical error")
```

----

```python    
def test_logger_custom_logger(tmpdir, caplog):
```
Pytest test function should start with `test_` to be automatically added to the test session execution.

----

```python    
def test_logger_custom_logger(tmpdir, caplog):
```
`tmpdir` and `caplog` are [pytest fixtures](https://docs.pytest.org/en/stable/fixture.html#fixture). In this case they are builtin. But you can create your own, i.e. we did in `conftest.py` (special file configuring the pytest session and sharing fixtures across tests):

```python=
@pytest.fixture(scope="session")
def is_py26():
    return sys.version_info[:2] == (2, 6)


@pytest.fixture(scope="session")
def is_py2():
    return sys.version_info[:2] <= (2, 7)


@pytest.fixture()
def tmpdir(tmpdir, is_py2):
    """Make tmpdir type str for py26.

    Origin LocalPath object is not supported in python26 for os.path.isdir.
    We're using this method when do a logger setup.
    """
    if is_py2:
        return str(tmpdir)
    else:
        return tmpdir
```

----

```python
# def test_logger_custom_logger(tmpdir, caplog):
#     """Test CustomLogger."""
#     log_fname = "convert2rhel.log"
#     logger_module.initialize_logger(log_name=log_fname, log_dir=tmpdir)
#     logger = logging.getLogger(__name__)
#     logger.task("Some task")
#     logger.file("Some task write to file")
    with pytest.raises(SystemExit):
        logger.critical("Critical error")
```
This is how you check if exception is raised

----

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

Otherwise check `pytest --help` or https://docs.pytest.org

---

## Already available fixtures

----

```python=
@pytest.fixture(scope="session")
def is_py26():
    return sys.version_info[:2] == (2, 6)


@pytest.fixture(scope="session")
def is_py2():
    return sys.version_info[:2] <= (2, 7)
    

def test_tools_opts_debug(tmpdir, read_std, is_py2):
    log_fname = "convert2rhel.log"
    logger_module.initialize_logger(log_name=log_fname, log_dir=tmpdir)
    logger = logging.getLogger(__name__)
    tool_opts.debug = True
    logger.debug("debug entry 1")
    stdouterr_out, stdouterr_err = read_std()
    # TODO should be in stdout, but this only works when running this test
    #   alone (see https://github.com/pytest-dev/pytest/issues/5502)
    try:
        assert "debug entry 1" in stdouterr_out
    except AssertionError:
        if not is_py2:
            assert "debug entry 1" in stdouterr_err
        else:
            # this workaround is not working for py2 - passing
            pass
    tool_opts.debug = False
    logger.debug("debug entry 2")
    stdouterr_out, stdouterr_err = read_std()
    assert "debug entry 2" not in stdouterr_out
```

----

```python=
@pytest.fixture()
def tmpdir(tmpdir, is_py2):
    """Make tmpdir type str for py26.

    Origin LocalPath object is not supported in python26 for os.path.isdir.
    We're using this method when do a logger setup.
    """
    if is_py2:
        return str(tmpdir)
    else:
        return tmpdir
```

----

```python=
@pytest.fixture()
def read_std(capsys, is_py2):
    """Multipython compatible, modified version of capsys.

    Example:
    >>> def test_example(read_std):
    >>>     import sys
    >>>     sys.stdout.write("stdout")
    >>>     sys.stderr.write("stderr")
    >>>     std_out, std_err = read_std()
    >>>     assert "stdout" in std_out
    >>>     assert "stderr" in std_err

    :returns: Callable[Tuple[str, str]] Factory that reads the stdouterr and
        returns captured stdout and stderr strings
    """

    def factory():
        stdouterr = capsys.readouterr()
        if is_py2:
            return stdouterr
        else:
            return stdouterr.out, stdouterr.err

    return factory


def test_logger_handlers(tmpdir, caplog, read_std, is_py2, capsys):
    """Test if the logger handlers emmits the events to the file and stdout."""
    # initializing the logger first
    log_fname = "convert2rhel.log"
    tool_opts.debug = True  # debug entries > stdout if True
    logger_module.initialize_logger(log_name=log_fname, log_dir=tmpdir)
    logger = logging.getLogger(__name__)

    # emitting some log entries
    logger.info("Test info")
    logger.debug("Test debug")

    # Test if logs were emmited to the file
    with open(os.path.join(tmpdir, log_fname)) as log_f:
        assert "Test info" in log_f.readline().rstrip()
        assert "Test debug" in log_f.readline().rstrip()

    # Test if logs were emmited to the stdout
    stdouterr_out, stdouterr_err = read_std()
    assert "Test info" in stdouterr_out
    assert "Test debug" in stdouterr_out
```

----

```python=
@pytest.fixture()
def pkg_root(is_py2):
    """Return the pathlib.Path of the convert2rhel package root."""
    if is_py2:
        import pathlib2 as pathlib  # pylint: disable=import-error
    else:
        import pathlib  # pylint: disable=import-error
    return pathlib.Path(__file__).parents[2]


def test_package_version(pkg_root):
    # version should be a string
    assert isinstance(__version__, str)
    # version should be separated with dots, i.e. "1.1.1b"
    assert len(__version__.split(".")) > 1
    # versions specified in rpm spec and convert2rhel.__init__ should match
    with open(str(pkg_root / "packaging/convert2rhel.spec")) as spec_f:
        for line in spec_f:
            if RPM_SPEC_VERSION_RE.match(line):
                assert __version__ == RPM_SPEC_VERSION_RE.findall(line)[0]
                break
```
Pay attention to a possiblity to use exisiting fixtures to create another fixtures

----

```python=
@pytest.fixture(autouse=True)
def setup_logger(tmpdir):
    initialize_logger(log_name="convert2rhel", log_dir=tmpdir)
```
With `autouse=True` the fixture added automatically for each test run

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
- ...

---

## Test parametrization

One cool feature of pytest is [parametrization](https://docs.pytest.org/en/stable/parametrize.html?highlight=fixtures)

----

Example in our codebase
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

## Pytest hooks (advanced topic)


----

Documentation https://docs.pytest.org/en/stable/reference.html#hooks

----

Example:
```python=
def pytest_collectstart(collector):
    if collector.nodeid:
        current_repo_basedir = find_repository_basedir(collector.nodeid)
        # loading the current repo
        if (
            not hasattr(collector.session, "leapp_repository")
            or current_repo_basedir != collector.session.repo_base_dir
        ):
            repo = find_and_scan_repositories(
                find_repository_basedir(collector.nodeid), include_locals=True
            )
            repo.load(skip_actors_discovery=True)
            collector.session.leapp_repository = repo
            collector.session.repo_base_dir = current_repo_basedir

        # we're forcing the actor context switch only when traversing new
        # actor
        if "/actors/" in str(collector.fspath) and (
            not hasattr(collector.session, "current_actor_path")
            or collector.session.current_actor_path + os.sep
            not in str(collector.fspath)
        ):
            actor = None
            for a in collector.session.leapp_repository.actors:
                if a.full_path == collector.fspath.dirpath().dirname:
                    actor = a
                    break

            if not actor:
                logger.info("No actor found, exiting collection...")
                return
            # we need to tear down the context from the previous
            # actor
            try:
                collector.session.current_actor_context.__exit__(
                    None, None, None
                )
            except AttributeError:
                pass
            else:
                logger.info(
                    "Actor %r context teardown complete",
                    collector.session.current_actor.name,
                )

            logger.info("Injecting actor context for %r", actor.name)
            collector.session.current_actor = actor
            collector.session.current_actor_context = actor.injected_context()
            collector.session.current_actor_context.__enter__()
            collector.session.current_actor_path = (
                collector.session.current_actor.full_path
            )
            logger.info("Actor %r context injected", actor.name)
```

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

## Random adjacent thoughts

----

In 2021 it is very important to use/reuse popular tools. It is not enough to build something beautiful, what has 0 support in modern developement environments. Think about that before starting bulding something new.

----

 
In 2021 it seems any popular project is popular because of user friendly way to
write plugins :rolling_on_the_floor_laughing:

Examples:

1. Unittest -> Pytest
2. Pylint -> Flake8
3. Django -> Flask -> FastAPI

..........

---

## :question: Questions :question: 

---

Thank you for your attention!

---

with big :heart: to Python
https://zhukovgreen.pro
