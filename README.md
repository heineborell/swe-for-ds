# DRY code and unit testing

## DRY code

One of the principles of programming is to write code which is DRY,
a/k/a Don't Repeat Yourself. If you find yourself typing something more
than once, it probably belongs in a function.

## Function scope

Building off that, it's worth thinking about the scope of functions
and how complicated they should be. The complicated a function is,
the more likely it has a bug and the harder that bug can be to
track down. Thus functions should be as simple as possible -- one
unit of code, one set of logic that can be easily tests. So even
if breaking a function into multiple function doesn't necessarily make
code more DRY, it can still be helpful.

## Unit testing

Unit testing is used to test the individual units of code. We'll
see how to do that with python. By installing and running `pytest`
we will setup and run any tests in a `tests` directory. Tests
are discovered if they are in modules with `test` in the name
and the function also starts with `test`. Test discovery happens
somewhat more loosely than this, but we can start here.


### Coverage

The idea of having a good suite of tests is that as we make changes
we can be sure that we did not break anything as long as tests
continue to pass. This of course depends on the tests having sufficient
coverage. We can test this by installing `pytest-cov` alongside
`pytest` and running `pytest --cov=src` to indicate that we want
to check coverage in the `src/` directory. Note that 100% test coverage
is not the goal, but robust code is. Your code will probably have some
function or scripts that truly are used to encapsulate business logic and
require successive function calls. This is a situation where your code
might not really be unit testable, but as long as the components of these
functions are tested, this should be sufficient.

Note that if you find a function is hard to unit test, this is usually a
sign of "code smell" and you probably want to refactor your code so that it
is more easily unit-testable, as opposed to setting up a very complicated unit
test.

### Mocking

In testing, there is the idea of __mocking__ which means that instead of
instantiating full versions of complicated classes, you create a mock
version with simplified behavior that can be tests. Mocking is important
because we want to test each unit of code in isolation from other resources
and logic as much as possible.
Examples of how to
do this in python using `unittest.mocking.Mock` are included. Python
unit testing also has the idea of fixtures, whereby common objects are
shared across tests. These can be setup in the test modules themselves or
in a `fixtures.py` and imported and made available via `conftest.py` that
helps setup the test environment.

### Test Driven Development

One ideal to strive for is to use __test driven development__. This involves
setting up just the interfaces (call signatures, return types) of
each unit of code and then writing complete unit tests before writing any
actual code. This forces the developer to understand the flow of data
and how a component should work before actually coding it. While not
used so often in practice, this is an ideal to strive for. Another name
for this is __red/green development__ as the tests start out failing (red)
and end up passing (green).

## Other types of testing

### Functional tests

Consider a unit of code being embedded into a component of an application.
In unit testing, we focus on the unit itself and other units of code in the component
including the unit is mocked out. In functional testing, we will not mock out
these other units and test overall behavior of the component. However,
other components of the application will be mocked. The goal is to test
behavior of the component containing the unit of code as a black box, not
digging into the units of the component.

### End to End (e2e) tests

Expanding the scope again, end to end tests will test the application behavior
overall treating each component as a black box. However, external applications
that are called by the application or which call the application will still
be mocked in some simplified way.

### Integration tests

Finally, integration testing uses no mocked components at all. The environment
might be the real production environment, but no applications, components, or
units will be mocked.

After integration testing, there is typically nothing left other than to promote
the code into the production environment. If something goes wrong, code will be
rolled back.
