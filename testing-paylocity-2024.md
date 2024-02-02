# Software testing

By zgreen @Paylocity 2024

---

## Disclaimer

This presentation is aimed at developing the understanding of "why-s"
behind testing. As well as writing software that is easy to test.

However how to write tests technically is not covered at full scale,
because this information is available on the internet and most of
articles about testing cover exactly the technical side of a problem.

---

## About me

Zgreen (Artem Zhukov), Data Engineer, working @Paylocity
[https://github.com/zhukovgreen](https://github.com/zhukovgreen)
![](https://hackmd.io/_uploads/Sy7TbE_qT.png)


---

# Chapter I (theoretical)

---

## Why should I write automated tests

----

1. It is your automated army that protects you and your code from bugs 24/7
   ![](https://hackmd.io/_uploads/B1Kd_WK9T.jpg)

----

2. Only tests ensure relatively safe and fast refactoring of the existing code
   base

- Bumping dependencies versions frequently
- Easier adopting new technologies
- Components refactoring
- Harder to break existing things by new contributors (knowledge transfer
  mechanism)
  ![](https://hackmd.io/_uploads/SJB0iWY5p.jpg =500x)

---

## Types of bugs in a sense where they appear

----

- A. Type-checking errors (the best type of errors)

Provided by mypy, pyright tools (see corresponding ide plugins)

![](https://hackmd.io/_uploads/BkE5gfKqT.png)

- caught immediately when you're writing the code
- thus, easy to find the root cause (the price of a bug is the smallest)
- do not get to the customer
- error is captured for all the dimension space of possible inputs

----

- B. Import time explosion

Your app starts, performs initialization, and fails immediately. This
could be on the level of running a test suite, CI system, or, at worse,
on the deployment stage.

- still easy to find the root cause
- hardly gets to the customer
- running some health check suits reduces the chance of getting such bugs
- on the other side longer health checks increase start-up time

----

- C. Runtime explosion

Your app was deployed and initialized. Then when external systems
the state has changed - it fails with an exception.

- might be expensive (need to debug, fix, redeploy)
- likely customer-facing
- the good thing is that exception is raised so something bad is prevented

----

- D. Doing the wrong thing silently (the worst type of error)

All works fine from things which are tracked by the engineer, but
something goes wrong and it was missed until a certain moment. Consequences
could be waste of computational power, reputation damage due to bugs

- takes a large amount of time or infinitely to reveal the error
- very expensive
- maybe impossible to fix or long to fix
- very hard to avoid future errors without changing conceptually how the team
  builds the software

---

## Concepts of addressing errors A..D

----

The universal idea behind reducing the number of errors and the impact of
them is:

**converting error risks into types as close as possible to the type A errors**

Thinking in this direction, surprisingly starts affecting the way
you write the software.

----

Some ideas here:

----

When converting to type A:

- Sanitizing the application inputs as early as possible to get maximum degree
  of type safety of your inputs before starting to process them in
- Having inputs processing pipelines as type-safe as it is feasible to achieve
  capturing max amount of errors due to typing incompatibilities

----

When converting to type B:

- run health-check routines at the initialization phase
- ensure external systems are in a healthy state
- validate static inputs (i.e. configurations) as early as possible (i.e.
  test suite, CI)
- good meaningful unit/integration test coverage
- good meaningful e2e test coverage

----

When converting to type C:

- Assert for invariants more often to avoid undesired states to propagate
  further to the logic
- Be explicit in states that your logic can handle (forbid unknown states
  early)
- validate before interacting with components whose states are hard to
  revert. I.e. using of dry-run

----

Minimizing chances occur type D errors and their consequences:

- use all the previous recommendations
- do not let technical debt grow and invest in keeping it at some level (
  documentation, update dependencies, runtimes, refactoring, new approaches)
- have an inner group of manual testers and real, versatile inputs
- easy system for end users to report problems and shorten the feedback loop as
  much as possible

---

## Types of tests

![](https://hackmd.io/_uploads/HJzDcmY5a.jpg)

----

Unit tests:
![](https://hackmd.io/_uploads/HyhypmF96.jpg =500x)

----

Testing the simplest component of your software architecture. 99% of this is a
function/method in class. Sometimes it could be a group of functions

----

- Ideal case when the function is pure (how to make my function pure?). Then
  the
  testing logic is: vary inputs and check expected outputs
- If the function is not pure (doing some kind of IO: interact with the OS,
  network, API). In this case, external systems should be patched (frozen,
  controllable state)
- generally, unit tests do not use any connection to external services
- should be performed in an isolated environment and do not modify the system
  where it runs (teardown)

----

Integration tests:
![](https://hackmd.io/_uploads/ByGfpXKcT.jpg =500x)

----

Testing how components of the software system interact together. In this case,
the components itself shouldn't be modified. They are combined and the
environment outside of this combination is modified and expected behavior is
asserted.

----

Examples:

- integration tests between low-level and high-level API within the same
  application
- integration tests between some 3rd party library and the client wrapper code
- installing the library into the client code and testing the library by
  modeling the scenarios from the client code

----

e2e tests:
![](https://hackmd.io/_uploads/S1oX6XF56.jpg =500x)

----

Testing the whole software system, by modifying inputs only at the client input
layer and validate the final state of the system (i.e. response)

----

real-world tests:
![](https://hackmd.io/_uploads/BJqBTXYca.jpg =650x)

A subset of customers are testing the software


---

## Writing code for tests and not tests for code

An indirect indicator of the code quality is the level of complexity in
covering the
code by tests. So thinking upfront about how the code will be
tested will result in a better code quality, fewer errors, and fewer
maintenance
cycles.

----

Example of a bad code (from the perspective of testing)

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
This simple 30-line code would require many hours to write a complex test suite
with a lot of patching/mocking. Also, the tests will be very sensitive to
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

This approach is called functional composition, where no unit tests are needed
for this
function at all. Each of these elementary functions
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

BDD - behavior-driven development

At the heart of this approach are questions:
`Given...When...Then`. You're forming the questions to your function using
these 3 words and tests start describing the behavior of your function, rather
than its implementation details. A very good library for BDD
is <https://github.com/zhukovgreen/pytest-when>. Also, show test examples there

----

TDD - test-driven development

This is a more generic definition of the process when writing tests should go
before the implementation. Not for all, including me. But I know big
evangelists of this approach.

----

It is fun to practice this approach in pair
programming.

- Player 1 - writes the test, and Player 2 - implements the code to satisfy the
  test
- Player 2 - writes the test, Player 1 - implements the code to satisfy the
  test

The goal of each other is to implement at the end some application with minimum
efforts

---

## Intro to the pytest

<https://hackmd.io/@zhukovgreen/S1nk_Vkmt#/>
<https://github.com/zhukovgreen/talks/blob/main/pytest-presentation.md>

---

## Writing tests tips and tricks

The main trick is always to decompose the logic into small single-purpose
functions and combine them using a variety of Python functools instruments.

- Avoid if/else (each if means additional test + patching)
- Avoid for loops, especially nested (using map + test a single map function is
  a way easier than controlling the iterables of each loop)

----

- passing constants as args with defaults (to make function pure)

```python=
CONST = "something"

def foo(a, *, kwarg=CONST): ...
    # do something using kwarg (not CONST)

```

----

- avoid `__post_init__` hooks in classes (to avoid patching)

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
![](https://hackmd.io/_uploads/S1dNWEO9p.png)
