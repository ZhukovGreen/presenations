# Software testing

By zgreen @Paylocity 2024

---

## Disclaimer

This presentatation is aimed to develop the understanding of "why-s"
behind testing. As well as writing software which is easy to test.

However how to write test technically is not covered at full scale,
because this information is available on the internet and most of
articles about testing covers exactly techical side of a problem.

---

## About me

Zgreen (Artem Zhukov), Data Engineer, working @Paylocity
[https://github.com/zhukovgreen](https://github.com/zhukovgreen)
![image](https://hackmd.io/_uploads/Sy7TbE_qT.png)


---

# Chapter I (theoretical)

---

## Why should I write automated tests

----

1. It is your automated army which protects you and your code from bugs 24/7
   ![](https://hackmd.io/_uploads/B1Kd_WK9T.jpg)

----

2. Only tests ensures relatively safe and fast refactoring of the existing code
   base

- Bumping dependencies versions frequently
- Easier adopting new technologies
- Components refactoring
- Harder to break existing things by new contributors (knowledge transfer
  mechanism)
  ![](https://hackmd.io/_uploads/SJB0iWY5p.jpg)

---

## Types of bugs in a sense where they appears

----

- A. Type-checking errors (best type of errors)

Provided by mypy, pyright tools (see corresponding ide plugins)

![image](https://hackmd.io/_uploads/BkE5gfKqT.png)

- catched immidiately when you're writing the code
- thus, easy to find the root cause (price of a bug is smallest)
- do not get to customer
- error is captured for all the dimension space of possible inputs

----

- B. Import time explosion

Your app starts, performs initialization and fails immidiately. This
could be on the level of running test suite, CI system or, at worse,
on the deployment stage.

- still easy to find the root cause
- hardly gets to the customer
- running some health check suits is reducing the chance to get such bugs
- from other side longer health checks increases start up time

----

- C. Runtime explosion

Your app was deployed and initialized. Then when external systems
state has changed - it fails with exception.

- might be expensive (need to debug, fix, redeploy)
- likely customer facing
- good thing is that exception is raised so something bad was prevented

----

- D. Doing wrong thing silently (the worsest type of error)

All works fine from things which are tracked by the engineer, but
something goes wrong and it was missed until a certain moment. Consiquences
could be waste computational power, reputation damage due to bugs

- takes big amount of time or infinitely to reveal the error
- very expensive
- maybe impossible to fix or long to fix
- very hard to avoid future errors without changing conceptually how team
  builds the software

---

## Concepts of addressing errors A..D

----

Unviversal idea behind reducing the number of errors and the impact of
them is:

**converting error risks into types as close as possible to the type A errors**

Thinking towards this direction, surprisingly starts affecting the way
you write the software.

----

Some ideas here:

----

When converting to type A:

- Sanitizing the application inputs as early as possible to get maximum degree
  of type safety of your inputs before starting process them in
- Having inputs processing pipelines as type safe as it is feasible to achieve
  capturing max amount of errors due to typing incompatibilities

----

When converting to type B:

- run health-check routines at the initialization phase
- ensure external systems are in a healthy state
- validate static inputs (i.e. configurations) as early as possible (i.e.
  test suite, CI)
- good a meaningful unit/integration test coverage
- good a meaningful e2e test coverage

----

When converting to type C:

- Assert for invariants more often to avoid undesired states to propogate
  further to the logic
- Be explicit in states which your logic can handle (forbid unknown states
  early)
- validate before interacting with components which states are hard to
  revert. I.e. using of dry-run

----

Minimizing chances to occur type D errors and its consiquences:

- use all the previoius recommendations
- do not let technical debt to grow and invest into keeping it at some level (
  documentation, update dependencies, runtimes, refactoring, new approaches)
- have inner group of manual testers and real, versatile inputs
- easy system for end users to report problems and shorten the feedback loop as
  much as possible

---

## Types of tests

![](https://hackmd.io/_uploads/HJzDcmY5a.jpg)

----

Unit tests:
![](https://hackmd.io/_uploads/HyhypmF96.jpg =250x)

Testing a simplest component of your software architecture. 99% this is a
function/method in class. Sometimes it could be a group of functions

- Ideal case when function is pure (how to make my function pure?). Then the
  testing logic is: vary inputs and check expected outputs
- If function is not pure (doing some kind of IO: interact with the OS,
  network, API). In this case external systems should be patched (frozen,
  controlable state)
- generally unit tests are not using any connection to external services
- should be performed in the isolated environment and do not modify the system
  where it runs (teardown)

----

Integration tests:
![](https://hackmd.io/_uploads/ByGfpXKcT.jpg =250x)

Testing how components of the software system interacts together. In this case
the components itself shouldn't be modified. They are combined together and the
environment outside of this combination is modified and expected behaviour is
asserted.

Examples:

- integration tests between low level and high level API within the same
  application
- integration tests between some 3rd party library and the client wrapper code
- installing the library into the client code and testing the library by
  modeling the scenarious from the client code

----

e2e tests:
![](https://hackmd.io/_uploads/S1oX6XF56.jpg =250x)

Testing the whole software system, by modifying inputs only at the client input
layer and validate the final state of the system (i.e. response)

----

real world tests:
![](https://hackmd.io/_uploads/BJqBTXYca.jpg =650x)

Subset of costumers are testing the software


---

## Writing code for tests and not tests for code

Indirect indicator of the code quality is the level of complexity to cover the
code by tests. So thinking towards how the code I am currently writing will be
tested will result in a better code quality, less errors, less maintainence
cycles.

----

Example of a bad code (from perspective of testing)

```python=
...
        for fmt, sources in subscribed_data_sources.items():
            valid_sources = list(
                filter(
                    lambda source: all(
                        [
                            source not in excluded_paths,
                            not re.match(
                                checkpoint_file_pattern, source.split("/")[-1]
                            ),
                        ]
                    ),
                    sources,
                )
            )
            if len(valid_sources) > 0:
                if fmt == _SOURCE_FORMAT_DELTA:
                    for path in valid_sources:
                        converted_table = self._spark_client.convert_to_table_format(
                            path
                        )
                        if converted_table == path:
                            paths.add(path)
                        else:
                            tables.add(converted_table)
                            excluded_paths.add(path)
                else:
                    paths.update(valid_sources)
...

```

What things are bad here - many if/else, for loops and not isolated logic.
This simple 30 line code would require many hours to write complex tests suite
with a lot of patching/mocking. Also the tests will be very sensitive to
changes

----

Example of complex code, which is easy to test:

```python=
def validate_hashes_and_table_meta_mismatch(
    target: DeltaTable,
    table_meta: DT.TableMeta,
) -> Iterable[Exception]:
    
    actual_hash = compute_columns_meta_hash(get_columns_meta(target))
    expected_hash = get_columns_meta_hash(target, default=actual_hash)

    try:
        assert actual_hash == expected_hash
        yield from ()
    except AssertionError:
        yield AssertionError("Error description")
        yield from map(
            render_exc,
            map(
                create_simple_meta_repr,
                map(
                    handle_nones_in_cols_descr,
                    filter(
                        meta_mismatch,
                        zip_longest(
                            sorted(
                                filter(
                                    has_not_empty_description,
                                    get_columns_meta(target),
                                )
                            ),
                            sorted(
                                filter(
                                    has_not_empty_description,
                                    table_meta.columns_description,
                                )
                            ),
                        ),
                    ),
                ),
            ),
        )
```

This approach called functional composition, where no tests are needed for this
function at all. Each this elementary functions
like `has_not_empty_description`,
`handle_nones_in_cols_descr` should be tested instead

---

# Chapter II (practical)

---

## Why mocking indicates that code is better to refactor

----

```python=
def complex_foo(a, b, c):
    ext_output = do_some_io_stuff()
    if a is None and b:
        # some logic to test here
    if a and b is None:
        # some other logic here
    for item in ext_output:
        if not c:
            # some other than other logic here
        else:
            # ...
```

Problems:

- Each time we want to test some logic in this function we need to isolate
  other parts of the functions with patching
- hard to name as it does many things

----

Anything which can lead to a simple functional composition with
small functions doing one thing

```python=
func_map = {
    (None, True): logic_a,
    (True, None): logic_b,
}
func_map[(a, b)]
if c:
    map(logic_for_c, ext_output)
else:
    map(logic_for_not_c, ext_output)
```

---

## Structuring your tests

here is a simple rule of mimicking the structure of your project. This helps
others to quickly orient where to find relevant tests. Example:
<https://github.com/Paylocity/dst-pcty_features_donkey/tree/main>

---

## Writing tests, BDD or TDD?

----

BDD - behaviour driven development

In the heart of this approach is questions:
`Given...When...Then`. You're forming the questions to your function using
these 3 words and tests starts describing behavior of your function, rather
than its implementation details. Very good library for BDD
is <https://github.com/zhukovgreen/pytest-when>. Also show tests examples there

----

TDD - test driven development

This is more generic definition of the process, when writing tests should go
first of the implementation. Not for all, including me. But I know big
evangelists of this approach. It is fun to practice this approach in a pair
programming.

- Player 1 - write test, Player 2 - implements the code to satisfy the test
- Player 2 - write test, Player 1 - implements the code to satisfy the test

Goal of each other to implement at the end some application with minimum
efforts

---

## Intro to the pytest

<https://hackmd.io/@zhukovgreen/S1nk_Vkmt#/>

---

## Writing tests tips and tricks

The main trick is always decompose the logic into small single purpose
functions and combine them using all variety of python functools instruments.

- Avoid if/else (each if means additianal test + patching)
- Avoid for loops, especially nested (using map + test a single map function is
  a way easier than controlling the iterables of each loop)

----

- passing constants as args with defaults

```python=
CONST = "something"

def foo(a, *, kwarg=CONST): ...
    # do something using kwarg (not CONST)

```

----

- avoid `__post_init__` hooks in classes

```python=
@dataclass
class Klass:
    complex_resource: Resource
    
    @classmethod
    def apply(cls, *args, **kwargs) -> Self:
        res: Resource = construct_complex_resource(args, kwargs)
        return cls(res)
```

---

## Thank you

---

## Questions

Link to the presentation:
![](https://github.com/zhukovgreen/talks/blob/main/testing-paylocity-2024.md)
![image](https://hackmd.io/_uploads/S1dNWEO9p.png)
