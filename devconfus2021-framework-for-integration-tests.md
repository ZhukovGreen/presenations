[![hackmd-github-sync-badge](https://hackmd.io/dXBUHLpHSH2eRQl01rY5Fg/badge)](https://hackmd.io/dXBUHLpHSH2eRQl01rY5Fg)

---

# Framework for integration tests lifecycle

---

Plan: :world_map: 

 - explain the problem which pushed us to create this framework
 - give a quick overview of tools which are used in the framework
 - provide details on the solution which using this framework

---

## Introduction to the problem

----

- Project: https://github.com/oamg/convert2rhel
- Language: :snake: Python
- Description: Application which converts {CentOS,OracleLinux} > RHEL

----

![](http://theviralcandy.com/wp-content/uploads/2020/05/mandarin_duck_02.jpg)

----

How to approach integration tests?

Some typical needs when building integration tests (technical)
- complex manipulation with the testing environment - OS (i.e. install Red Hat kernel on Oracle Linux, ...)
- the need to reboot the system (maybe even multiple times)
- the need to interact with the user
- adjust files and cleaning after
- install various rpm packages
- resources access (intranet), secrets management

----

Organizational needs:
- Due to complexity of the previous integration tests framework (complex itself, the test language is different from upstream project) project maintainers were unable to cover their features with integration tests
- Organize the contribution process, so new features won't be stacked wating for a verification

----

As a result of these requirements we kept a separate team of QE engineers,
bash-based testing framework, strong separation of duties.

----

At least it was before! :sunglasses: 

----

![](http://comic-news.com/wp-content/uploads/2017/04/20-2.jpg)

---


## New solution tooling overview

- tmt - https://tmt.readthedocs.io
- Testing Farm - https://packit.dev/testing-farm
- Packit - https://packit.dev/

---

## tmt

----

Test Management Tool is an open-source test metadata specification and a command line tool which allows to easily create, discover, execute and debug tests.

----

* The [specification](https://tmt.readthedocs.io/en/latest/spec.html) defines a concise and consistent config
* Command line [tool](https://tmt.readthedocs.io/en/latest/guide.html) provides a user-friendly way to work with tests
* Python [module](https://tmt.readthedocs.io/en/latest/classes.html) allows to work with test metadata from python scripts

----

A unified way of defining, enabling and sharing tests between Github projects, RHEL, Fedora and CentOS Stream.

----

Get quickly started

    $ tmt init --template mini
    Tree '/tmp/git' initialized.
    Applying template 'mini'.
    Directory '/tmp/git/plans' created.
    Plan '/tmp/git/plans/example.fmf' created.

```yaml
summary: Basic smoke test
execute:
    script: tmt --help
```

----

Create new tests

    tmt init --template base
    tmt test create --template shell tests/smoke
    tmt test create --template beakerlib tests/advanced

----

Run tests, review results, debug code

    tmt run
    tmt run --verbose
    tmt run --last report
    
    tmt run --until execute
    tmt run --last login

----

Run tests across different environments

    tmt run --all provision --how container
    tmt run --all provision --how virtual
    tmt run --all provision --how connect
    tmt run --all provision --how local

----

Share test coverage across projects and distros

```yaml
summary: Run integration tests from a remote repo
discover:
    how: fmf
    url: https://github.com/psss/tmt
    ref: fedora
    filter: 'tier: 1, 2'
prepare:
    how: install
    package: [fmf, tmt-all]
```

----

![](https://i.imgur.com/74BEMys.png =400x)

----

See tmt docs for more details and examples

https://tmt.readthedocs.org

---

## Testing Farm

----

Testing System as a Service via an [HTTP API](https://api.dev.testing-farm.io), focusing on testing RHEL-like OS.

Consume a stable testing infrastructure as a service, focus on code/tests instead.

Supports tests defined via [Test Management Tool - tmt](https://tmt.readthedoc.org) via a remote Git reference.

Tests written in any language, integratable via tmt's shell executor.

----

Current users of Testing Farm include [Packit](https://packit.dev), [Fedora CI](https://hackmd.io/@zhukovgreen/BJL0Q8flY#/6/2), [RHEL CI]().

Testing Farm runs currently ~30k jobs per month.

For viewing the resutls Testing Farm provides a simple UI to investigate the test failures.

----

Public requests can be executed on x86_64 and aarch64, infrastrucutre provided by AWS.

Internal Red Hat requests can be executed on all RHEL supported architectures.

Qualify upstream code against unreleased RHEL versions and internal test coverage.

---

## Packit

----

### The problem with distribution testing

* Changes are happening upstream

* Integrating in downstream after a release is "too late"

----

### Packit Dashboard - pipeline view

https://dashboard.packit.dev/jobs

![Packit Dashboard](https://i.imgur.com/X9gTn7V.png)

---

![](https://img.izismile.com/img/img2/20090709/funny_hand_faces_01.jpg)

---

## New solution: how we wire all these together

----

- Based on tmt - tft - packit tools
- Testing environment is declared using Ansible (tmt plans)
- Tests implemented using Pytest (industry standard Python testing framework) (tmt tests)
- All tests stored in the upstream (Secrets are handled as environment variables stored in intranet)

----

- Develop tests locally (runing inside the VMs), submit tests from local to be executed in testing farm (for parallelism)
- Set of convenient testing fixtures which helps very simply solve complex testing problems
- Friendly CI system which executes all the tests in intranet

----

As result:

- Contributors can write features and integration tests
- QE engineers can write features and integration tests
- External contributors can write ...

----

This is a HUGE WIN for our team!

- We got unblocked
- The team performance gradually boosted
- Quality of the application raised (more tests, better tests)

---

## Let's look to the code:

----

- https://github.com/oamg/convert2rhel

- https://github.com/oamg/convert2rhel/blob/51d1acbdea3f24295b303eddbcc61c26814e2383/plans/main.fmf#L13

- https://github.com/oamg/convert2rhel/blob/main/tests/integration/releasever-as-mapping/test_releasever_as_mapping.py

- https://github.com/oamg/convert2rhel/blob/main/plans/integration/conversion/rhsm/main.fmf#L8

- https://github.com/oamg/convert2rhel/blob/main/tests/integration/conversion/rhsm/run_conversion.py

----

![](https://i.imgur.com/8eIXnEK.png)

----

![](https://i.imgur.com/JwZJKd6.png)

----

![](https://i.imgur.com/VJ9nWGJ.png)

----

![](https://i.imgur.com/UHYmA3H.png)

----

---

Slides available:

https://github.com/zhukovgreen/talks/blob/main/devconfus2021-framework-for-integration-tests.md

---

Thank you for your attention!

[zhukovgreen](https://zhukovgreen.pro) - software and data engineer @Absa
:heart: Python :heart: Scala and big data

[mvadkert](https://gitlab.com/mvadkert) - senior principal quality engineer @ Red Hat

[psss](https://github.com/psss) - principal quality engineer @ Red Hat

---

![](http://www.dumpaday.com/wp-content/uploads/2016/12/funny-parenting-16.jpg)

---

It is a time for questions!
:question: 
:question: 
:question: 
:question: 
