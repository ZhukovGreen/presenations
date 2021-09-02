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
- complex manipualiton with the testing environment - OS (i.e. install RH kernel on Oracle Linux, ...)
- the need to reboot the machine (maybe even multiple times)
- the need to interact with the user
- adjust files and cleaning after
- install various rpm packages
- resources access (intranet), secrets management

----

Organizational needs:
- Due to complexity of the integration tests (complex, the test language is different from upstream project) a separate team of QE engineers is needed for covering new features with integration tests
- Organize the contribution process, so new features won't be stacked wating for a verification

----

As a result of these requirements we kept a separate team of QE engineers,
own testing framework (bash based), strong separation of duties.

----

At least it was before! :sunglasses: 

----

![](http://comic-news.com/wp-content/uploads/2017/04/20-2.jpg)

---


## New solution tooling overview

- tmt - tmt.readthedocs.io
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

Get quickly started:

    $ tmt init --template mini
    Tree '/tmp/git' initialized.
    Applying template 'mini'.
    Directory '/tmp/git/plans' created.
    Plan '/tmp/git/plans/example.fmf' created.

Simple plan example:

```yaml
summary: Basic smoke test
execute:
    script: tmt --help
```

----

Create new tests, review test results, debug test code:

    tmt init --template base
    tmt test create --template beakerlib tests/smoke
    tmt run
    tmt run --until execute
    tmt run --last report
    tmt run --last login

----

Safely and easily run tests across different environments

    tmt run --all provision --how container
    tmt run --all provision --how virtual
    tmt run --all provision --how connect
    tmt run --all provision --how local

----

Share test coverage across projects and distros:

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

For more information see https://tmt.readthedocs.org

----

---

## Testing Farm

----

Testing System as a Service with and HTTP API, focusing on testing RHEL-like OS

Removes the burden of maintaining a stable infrastructure for teams, focus on code/tests instead

Supports tests defined via [Test Management Tool - tmt](https://tmt.readthedoc.org)

Tests written in any language, integratable via tmt's shell executor.

----

Current users of Testing Farm include Packit, Fedora CI, RHEL CI.

Testing Farm runs around 50k jobs per month currently.

All tests are executed on AWS. Supported architectures are x86_64 and aarch64.

For Red Hat projects we support delegating tasks to internal infrastructure, which makes it very easy to test upstream code against RHEL versions in development.

----

For viewing the resutls Testing Farm provides a simple UI to investigate the test failures.



----

---

## Packit

----

## The problem with distribution testing

* Changes are happening upstream

* Integrating in downstream after a release is "too late"

----

## Packit pipeline view

![Packit Dashboard](https://i.imgur.com/X9gTn7V.png)

----

---

![](https://img.izismile.com/img/img2/20090709/funny_hand_faces_01.jpg)

---

## New solution: how we wire all these together

----

In no way! It is impossible and too complex.

Thank you

----

- Based on tmt - tft - packit tools
- Testing environment is declared using Ansible (tmt plans)
- Tests implemented using Pytest (industry standard Python testing framework) (tmt tests)
- All tests stored in the upstream (Secrets are handled as environment variables stored in intranet)
- Possibility to develop tests locally, submit tests from local to be executed in testing farm
- Friendly CI system which executes all the tests in intranet

----

- Contributors can write features and integration tests
- QE engineers can write features and integration tests
- External contributors can write ...

----

This is a HUGE WIN for our team!

- We were unblocked
- The team performance gradually boosted
- Quality of the application raised (more tests, better tests)

----

---

## Walk through the framework

- Possibility to develop and run integration tests locally in the VM (with the help of libvirt)
- Possibility to submit plans to be excuted via testing farm (still from the local env)
- CI system (based on packit) which runs tests for each MR
- Set of convenient testing fixtures which helps very simply solve complex testing problems

---

![](http://s3.awkwardfamilyphotos.com/wp-content/uploads/2015/08/22184002/8-photo-u1.jpg)

---

## Let's look to the code:

----

https://github.com/oamg/convert2rhel

----

![](https://i.imgur.com/8eIXnEK.png)

----

![](https://i.imgur.com/JwZJKd6.png)

----

---

Slides available:

https://github.com/ZhukovGreen/talks/blob/main/devconfus2021-framework-for-integration-tests.md

---

Thank you for your attention!

[zhukovgreen](https://zhukovgreen.pro) - software and data engineer @Absa
:heart: Python :heart: Scala and big data

[mvadkert](https://gitlab.com/mvadkert) - senior principal quality engineer @ Red Hat

[psss](https://github.com/psss) - senior principal quality engineer @ Red Hat

---

![](http://www.dumpaday.com/wp-content/uploads/2016/12/funny-parenting-16.jpg)

---

It is a time for questions!
:question: 
:question: 
:question: 
:question: 

---

## Ideas, questions goes here

- [x] Should we talk all together?
yes
- [x] Who will do Tomas's talk about Packit (as he is not around)
no

outputs of our meeting:
- [x] show the live example (asciinema)
just print screen from tmt. convert2rhel is not yet there
- [X] add couple more sentences at the begining
- [X] rearange structure, so the problem goes first
- [ ] Run tests in intranet from the github (very important)
- [ ] Add more interaction (pictures, ascicinema samples)
- [ ] Show how the ci works on real project (hope it will be convert2rhel, fallback to tmt)
- [ ] Add timeframes

---
- [ ] ask Michal to provide asciirec of tmt run in libvirt
- [ ] too much possibility world
- [ ] fix the view of the tmt part (fit into the screen)
- [ ] mention in tft and packit the internal infra

---



## TBD

