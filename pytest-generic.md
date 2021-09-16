# Pytest introduction (technical talk)

---

Do we need to test our software?

----

Not properly tested software is a poor quality software.
Poor quality software damage company reputation (in a very optimistic scenario).
:-1::-1::-1::-1::money_with_wings: :money_with_wings: :money_with_wings::money_with_wings: 

---

Pytest is a software testing framework. 
https://docs.pytest.org/en/stable/

----

:hearts: Pytest is awesome: :hearts:
- It is the most popular testing framework in the world
In according with 2020 python developer [survey](https://www.jetbrains.com/lp/python-developers-survey-2020/):
![](https://i.imgur.com/bxK3j56.png)
And the adoption is very rapid. Starting from 2017 pytest is strongly dominating over other frameworks

----

except the percent of people who is not testing their software at all. Those percent was always big

:rolling_on_the_floor_laughing: 

---

## Technical part

---

Installation:
```bash
$ pip install pytest
```

----

Project tree

```
├── README.md
├── poetry.lock
├── pyproject.toml               # pytest configuration
├── src
│   └── wlb_bot
│       ├── __init__.py
│       ├── __main__.py
│       └── app.py
└── tests                        # place for tests
    ├── __init__.py
    ├── conftest.py              # fixtures
    ├── handlers
    │   └── test_start.py        # pytest automatically discovering tests in nested dirs
    └── test_app.py              # testing module
```

----

How does test look like?
```python=
def test_basic():
    assert True
```

---


## How execute tests

From top of my head the most frequently used commands are:

```bash=
$ pytest    # to run the pytest session
$ pytest --collect-only    # to list collected tests
$ pytest -k 'some pattern or expression here'    # to run tests matching the pattern
$ pytest --lf    # run last failed tests only
$ pytest --pdb   # fall into python debugger if test fails
$ pytest /some/path     # run tests in the /some/path
```

----

Otherwise check `pytest --help` or https://docs.pytest.org

---

## How to write tests

----

Open terminal:
cd $CODE/talks/

---

## Interesting things about fixtures

----

A lot of nice examples are in the documentation (https://docs.pytest.org/en/stable/fixture.html), like:

- Fixtures as factories
- Parametrizing fixtures (by adding a fixture your test will be parametrized)
https://github.com/oamg/convert2rhel/blob/main/convert2rhel/unit_tests/conftest.py#L64
- Test parametrization https://docs.pytest.org/en/stable/parametrize.html#pytest-mark-parametrize-parametrizing-test-functions

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
- pytest-xdist (test parallelization, isolation, remote execution)
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

Talk is available at:
https://github.com/zhukovgreen/talks/blob/main/pytest-generic.md

---

## :question: Questions :question: 

---

Thank you for your attention!

---

with :heart: to Python
https://zhukovgreen.pro
