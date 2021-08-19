[![hackmd-github-sync-badge](https://hackmd.io/dXBUHLpHSH2eRQl01rY5Fg/badge)](https://hackmd.io/dXBUHLpHSH2eRQl01rY5Fg)

---

# Framework for integration tests lifecycle

---

## Tooling overview

- TMT - tmt.readthedocs.io/
- Testing Farm (TFT) - @mvadkert which url to use?
- Packit - https://packit.dev/

---

## TMT

----

Test Management Tool is an open-source test metadata specifiction created by Red Hat. It was created to help 

----

---

## Testing farm

----

* Testing System as a Service, focusing on testing RHEL-like OS

* HTTP API for public and Red Hat users

* Removes the burden of maintaining a stable infrastructure for teams, focus on code/tests instead

* Test metadata defined using Test Management Tool (TMT), an open-source test metadata specification & tool

* Tests written in any language, integratable via shell executor, built in support for beakerlib test framework & Ansible

* Integrations: Packit (GitHub), Fedora CI (Jenkins, Zuul), RHEL CI (Jenkins), CentOS Stream (Zuul)

Speaker: Miro

----

---

## Packit

----

## The problem with distribution testing

* Changes are happening upstream

* Integrating in downstream after a release is "too late"

----

## Is it easy to use?

* Manual steps are dreadful

* Feedback loop

----

---

## How we wire all these together?

----

- Project: https://github.com/oamg/convert2rhel
- Language: :snake: Python
- Description: Application which converts {CentOS,OracleLinux} > RHEL

----

How to approach integration tests?

Some typical needs when building integration tests (technical)
- Complex manipualiton with the initial system (i.e. install RH kernel on Oracle Linux, ...)
- A need to reboot the machine (maybe even multiple times)
- A need to interact with the user
- Manipulate with configs
- Install various rpm packages
- Due to secrets management the test should be stored in intranet

----

Organizational needs:
- Due to complexity of the integration tests a separate team of QE engineers is needed for covering new features with integration tests
- Organize the contribution process, so new features won't be stacked wating for a verification

----

As a result of these requirements we kept a separate team of QE engineers,
own testing framework (bash based), strong separation of duties.

----

At least it was before! :sunglasses: 

----

---

## New solution results

----

- Based on tmt - tft - packit tools
- Testing environment is defined using Ansible
- Tests are defined using Pytest (industry standard Python testing framework)
- All tests stored in the upstream (Secrets are handled as environment variables)

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

## Walk through framework

- Possibility to develop and run integration tests locally in the VM (with help of libvirt)
- Possibility to submit plans to be excuted via testing farm
- CI system (based on packit) which runs tests for each MR
- set of convinient testing fixtures which helps very simply solve complex testing problems

----

Let's look to the code:
https://github.com/oamg/convert2rhel

----

---

Slides available:

https://github.com/ZhukovGreen/talks/blob/main/devconfus2021-framework-for-integration-tests.md

---

Thank you for your attention!

[zhukovgreen](https://zhukovgreen.pro) - software and data engineer @Absa
:heart: Python :heart: Scala and big data

[mvadkert](gitlab.com/mvadkert) - senior principal quality engineer @ Red Hat

Petr

~~Tomas~~

---

It is a time for questions!
:question: 
:question: 
:question: 
:question: 

---

## Ideas, questions goes here

- [ ] Should we talk all together?
- [ ] Who will do Tomas's talk about Packit (as he is not around)

outputs of our meeting:
- [ ] show the live example (asciinema)
- [ ] add couple more sentences at the begining
- [ ] rearange structure, so the problem goes first
- [ ] Run tests in intranet from the github (very important)
- [ ] Add more interaction (pictures, ascicinema samples)
- [ ] Show how the ci works on real project (hope it will be convert2rhel, fallback to tmt)
- [ ] Add timeframes

---



## TBD

