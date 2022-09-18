# Packages

We have now reconfigured our repository to be a pip
installable packages with our packaging managed by `setuptools`.

To this end we have put our source code under `src/someproject`
and created a `setup.py` with information about the package
and `pyproject.toml` with metadata about how to build the
package indicating that we want to use `setuptools`.

One thing to note is the namespacing. When adding modules to
`src/someproject`, other modules are imported using full
paths such as `from someproject.utils import some_function`.

## Dependencies and installation

The `setup.py` file is used to indicate what packages are in
the repository and what requirements are required by the
project as well as packages which are optionally installable,
either for development purposes or to enable fuller funtionality.
The `setup.py` file can also indicate scripts that are installable
and then accessible via command line arguments.

The package can then be installed locally with `pip install -e ".[dev"]`
where the `.` indicates the path (we are installing from the current
directory) and the `[dev]` indicates that we want to install the
optional `dev` requirements as indicated in `setup.py`. The `-e` means
to watch changes, i.e., we do not need to re-install upon making
changes to the modules comprising the package.

To install from github using ssh credentials, one can do
`pip install git+ssh://git@github.com/TheErdosInstitute/swe-for-de` since
this is where it is hosted. HTTP can also be used, although note that
the URL will change and you may be asked for your username and password.

Packages are also commonly hosted by [pypi](https://pypi.org/) and it
is not too hard to build a package and upload it following the instructions
there. It is best not to spam your packages into the pypi package repository.
Your company might have its own package repository similar to pypi where
packages are installed and not available fo rhte wider world.

## Semantic versioning

Note that we have provided a version number of the form `0.1.0`.
This is a [symantic version](https://semver.org/) which has a standard format
of `Major.Minor.Patch`. Major changes mean the API, a/k/a how people use the
package, is fundamentally changing in a backward incompatible way. Minor
changes are used for additions which are backwards compatible,
and the patch number is incremented for bug fixes, style, and other less essential changes.
Note that one can tag a repository with the semantic version, typically either as
`0.1.0` or `v0.1.0`.

Going alongside this, one should [keep a changelog](https://keepachangelog.com/en/1.0.0/)
describing what has been added, changed, removed, and fixed under each version,
including changes which are unpublished.
