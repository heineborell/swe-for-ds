# Object oriented programming

One style of programming that is fairly popular within the
python community is that of __object oriented programming__ (OOP).
In object oriented programming, one seeks to express the
complexity of programs by encapsulating different types of data
and the behaviors that are permitted on the data by
using classes and then creating instances of those classes
called objects.

A standard example is that you have a class called something
like `Entity` which has a name property and a method called `speak`
and the entity introduces itself using its name. You can then
create a child class `Person` that inherits the structure of
the `Entity` and a child class `Dog` both of which will `speak`
in a different way.

In a more realistic example, one might have a `Dataset` class
with various standard transformations. Instances of the class
would be instantiated with different sets of data but the
transforms are the same and the object keeps track of the current
state of the dataset.

## Liskov substitution principle

The [Liskov substitution principle](https://en.wikipedia.org/wiki/Liskov_substitution_principle),
named after Barbara Liskov from a keynote address she gave in at a
conference in 1988, says that subclasses must be interoperable with
their parent classes.

At first glance this makes sense: both `Dog` and `Person` from
the example above are child classes of `Entity` and if a function
expects an abstract `Entity`, it will be happy to receive a `Dog` or a
`Person` since they both have names and the ability to `speak`. The
child classes `Person` and `Dog` can each have additional properties
that a basic `Entity` does not have as long as they fulfill the
interface and assumptions of an `Entity` as well.

However, this requirement that child classes obey the behaviors of
parent classes in some way requires that a `Square` cannot be a child
class of a `Rectangle`. While the set of squares may be a subset of the
set of rectangles, squares are stricter than rectangles. One can edit
the length of rectangle and keep its height the same, but the same is
not true for a square. If a function that uses a `Rectangle` requires
this property, the function will break if it is given a `Square`.
data.

## Drawbacks

The idea that data and the methods to transform it are encapsulated together
is intuitive, but it does introduce some difficulties. In OOP, objects
are generally assumed to be __mutable__. So if you have an object `x` with
a property `foo`, then running `x.foo()` might change the data in `x`.
This can make bugs hard to find, because it is difficult to guarantee that
`x` is in a given state at a given time. This is in contract to __functional
programming__ which we will talk about in the next video.

In reality, many languages such as python do not impose a paradigm upon
the programmer. Object oriented ideas are used when they are useful
and classes can be defined in ways that their underlying data is immutable.
