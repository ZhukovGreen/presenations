# TMT - PYTEST integration tests framework

---

## Directory structure


----

```
➞  tree -d plans                                                                      [git:feature/tft-integration] ✖  
plans
└── integration
    ├── changed-yum-conf
    ├── check-custom-repo
    ├── conversion
    │   └── basic-conversion
    ├── inhibit-if-kmods-is-not-supported
    ├── inhibit-if-oracle-system-uses-not-standard-kernel
    ├── releasever-as-mapping
    ├── remove_all_submgr_pkgs
    ├── remove-excluded-pkgs
    ├── resolve-broken-ol8-rollback
    └── resolve-dependency

```

----

```
➞  tree -d tests                                                                      [git:feature/tft-integration] ✖  
tests
├── ansible_collections
│   ├── group_vars
│   └── roles
│       ├── install-testing-deps
│       │   └── tasks
│       ├── oracle-linux-specific
│       │   └── tasks
│       ├── packaging
│       │   └── tasks
│       └── update-system
│           └── tasks
└── integration
    ├── changed-yum-conf
    ├── check-custom-repo
    ├── conversion
    │   └── basic-conversion
    ├── inhibit-if-kmods-is-not-supported
    ├── inhibit-if-oracle-system-uses-not-standard-kernel
    │   └── ansible
    ├── releasever-as-mapping
    ├── remove_all_submgr_pkgs
    │   └── ansible
    ├── remove-excluded-pkgs
    ├── resolve-broken-ol8-rollback
    └── resolve-dependency

```

----


---

## Plans metadata

----

cat plan/main.fmf

```yaml=
execute:
    how: tmt
discover:
    how: fmf
prepare:
    - name: main preparation step
      how: ansible
      playbook: tests/ansible_collections/main.yml
environment-file:
  - .env
adjust:
  - environment-file-:
    - .env
    when: distro != ""
  - environment-file-url:
      - https://gitlab.cee.redhat.com/oamg/convert2rhel/convert2rhel-secrets/-/raw/main/.env
    when: distro != ""
```

----

cat plans/integration/conversion/main.fmf

```yaml=
# fmf inheritance mechanism (adding filter to discover section)
discover+:
    filter:
        - 'tag: conversion'

prepare+:
    # here you can run tests which will be executed before the conversion
    - name: main conversion preparation
      how: shell
      script: pytest -svv tests/integration/conversion/run_conversion.py
    - name: reboot machine
      how: ansible
      playbook: tests/ansible_collections/reboot.yml
```

----

cat plans/integration/conversion/basic-conversion/main.fmf
```yaml=
discover+:
    filter+:
        - 'tag: basic-conversion'
provision:
    how: libvirt
    develop: true

/centos7:
    discover+:
        filter+:
            - 'tag: centos7'
    provision+:
        origin_vm_name: c2r_centos7_template

```

----

```
➞  tmt plans show --verbose plans/integration/conversion/basic-conversion/centos7     [git:feature/tft-integration] ✖  
/plans/integration/conversion/basic-conversion/centos7
    discover 
         how fmf
      filter tag: conversion
             tag: basic-conversion
             tag: centos7
   provision 
         how libvirt
origin_vm_name c2r_centos7_template
     develop true
     prepare 
        name main preparation step
         how ansible
    playbook tests/ansible_collections/main.yml
     prepare 
        name main conversion preparation
         how shell
      script pytest -svv tests/integration/conversion/run_conversion.py
     prepare 
        name reboot machine
         how ansible
    playbook tests/ansible_collections/reboot.yml
     execute 
         how tmt
      report 
         how display
      finish 
         how shell
      script 
environment DEBUG: True
            ...
enabled true
sources /home/azhukov/Documents/convert2rhel/plans/main.fmf
        /home/azhukov/Documents/convert2rhel/plans/integration/conversion/main.fmf
        /home/azhukov/Documents/convert2rhel/plans/integration/conversion/basic-conversion/main.fmf
```

----

---

## Tests metadata

----

cat tests/main.fmf
```yaml=
summary: Integration tests
duration: 30m
```
cat tests/conversion/main.fmf
```yaml=
tag+:
  - conversion
```

----

cat tests/conversion/basic-conversion/main.fmf
```yaml=
summary: basic-conversion
tag+:
  - centos7
  - centos8
  - oracle7
  - oracle8
  - basic-conversion
# needed for packit integration
adjust:
  enabled: false
  when: >
    distro != centos-7 and
    distro != centos-8 and
    distro != oracle-7 and
    distro != oracle-8
test: |
  pytest -svv
```

----

➞  tmt tests show --verbose /tests/integration/conversion/basic-conversion
```
     summary basic-conversion
        test pytest -svv
        path /tests/integration/conversion/basic-conversion
      manual false
    duration 30m
     enabled true
      result respect
         tag conversion
             centos7
             centos8
             oracle7
             oracle8
             basic-conversion
     sources /home/azhukov/Documents/convert2rhel/tests/integration/main.fmf
             /home/azhukov/Documents/convert2rhel/tests/integration/conversion/main.fmf
             /home/azhukov/Documents/convert2rhel/tests/integration/conversion/basic-conversion/main.fmf
      fmf-id name: /tests/integration/conversion/basic-conversion
             url: https://github.com/ZhukovGreen/convert2rhel.git
             ref: feature/tft-integration
```

----

---

## Plans to tests relation

----

Plan contains:
```
    discover 
         how fmf
      filter tag: conversion
             tag: basic-conversion
             tag: centos7
```
Test contains:
```
         tag conversion
             centos7
             centos8
             oracle7
             oracle8
             basic-conversion
```
This test will be selected, because **ALL** filter tags in plan contains in
test.

----

---

## Tools for writing tests

----

Shell, convert2rhel fixtures

```python=
def test_do_not_inhibit_if_module_is_not_loaded(shell, convert2rhel):
    assert shell("modprobe -r -v bonding").output == "rmmod bonding\n"
    with convert2rhel(
        ("-y --no-rpm-va --serverurl {} --username {} --password {} --pool {} --debug").format(
            env.str("RHSM_SERVER_URL"),
            env.str("RHSM_USERNAME"),
            env.str("RHSM_PASSWORD"),
            env.str("RHSM_POOL"),
        )
    ) as c2r:
        c2r.expect("Kernel modules are compatible.")
        c2r.send(chr(3))
    assert c2r.exitstatus != 0

```

----

c2r_config fixture

```python=
def test_releasever_as_mapping_config_modified(convert2rhel, os_release, c2r_config):
    """Test if config changes takes precedence."""
    with c2r_config.replace_line(pattern="releasever=.*", repl=f"releasever=333"):
        with convert2rhel(
            ("-y --no-rpm-va --serverurl {} --username {} --password {} --pool {} --debug").format(
                env.str("RHSM_SERVER_URL"),
                env.str("RHSM_USERNAME"),
                env.str("RHSM_PASSWORD"),
                env.str("RHSM_POOL"),
            )
        ) as c2r:
            c2r.expect("--releasever=333")
            c2r.send(chr(3))
    assert c2r.exitstatus == 1

```

----

config_at, os_release fixtures

```python=
def test_releasever_as_mapping_not_existing_release(convert2rhel, config_at, os_release):
    """Test unknown release."""
    with config_at(Path("/etc/system-release")).replace_line(
        "release .+",
        f"release {os_release.version[0]}.1.1111",
    ):
        with convert2rhel(
            ("-y --no-rpm-va --serverurl {} --username {} --password {} --pool {} --debug").format(
                env.str("RHSM_SERVER_URL"),
                env.str("RHSM_USERNAME"),
                env.str("RHSM_PASSWORD"),
                env.str("RHSM_POOL"),
            )
        ) as c2r:
            c2r.expect(
                f"CRITICAL - {os_release.name} of version {os_release.version[0]}.1 is not allowed for conversion."
            )
        assert c2r.exitstatus == 1
```

----

---

## local interaction with tft script

----

```
➞  python ./scripts/run_tmt_tests_on_tft.py --help                                    [git:feature/tft-integration] ✖  Usage: run_tmt_tests_on_tft.py [OPTIONS]

Options:
  -p, --plans TEXT          Plan names. i.e. -p /plan/name. Could be multiple
                            [default: /plans/]

  -r, --remote-name TEXT    Git remote name from which the content of the repo
                            will be cloned at current commit. Warning: changes
                            should be pushed to the remote before running this
                            script.  [default: origin]

  -b, --copr-build-id TEXT  Use specified builds ids instead of creating a new
                            copr builds.

  -v, --verbose
  --help                    Show this message and exit.
```

Show live!

----

---

## References:

1. Integration tests https://github.com/oamg/convert2rhel/tree/main/tests/integration
2. Fixtures https://github.com/oamg/convert2rhel/blob/main/tests/integration/conftest.py
3. tft script https://github.com/oamg/convert2rhel/pull/297
4. 

---

With :heart: to Python :snake: and Pytest

[zhukovgreen](https://zhukovgreen.pro)