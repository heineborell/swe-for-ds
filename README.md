# Code style

## PEP 8

Python style best practices are defined in [PEP 8](https://peps.python.org/pep-0008/).
It includes things such as using spaces instead of tabs, using 4 spaces to indent,
and keeping maximum line length at 79 characters. Following community standards
makes code easier to read, makes the developper appear professional. Code is
read more often than it is written.

One could also look to [google's python style guide](https://google.github.io/styleguide/pyguide.html).


## Naming

- Local variables:
  - Uncapitalized
  - `snake_case` if multiple words
  - Descriptive names that aren't too long
- Functions: same as variables, use verbs consistently
- Classes: `CamelCase` nouns
- Modules a/k/a `.py` files: should be snake case as well
- Packages: same hyphens in the name, but files and directories are snake case

## Comments

- Triple quotes at the top of the module
- Docstrings as part of the method:
  - Single line description
  - Longer description
  - Arguments
  - Returns
- Other comments should be short hints
- DO NOT LEAVE COMMENTED OUT CODE IN VERSION CONTROL

## Tools

### Linters

Common linters include `flake8` and `pylint`. These help catch errors
and style faux pas.

### Code style

Popular auto formatter is `black` which is an opinionated formatter, but 
easy to use.

`isort` will sort your imports alphabetically.

### pre-commit

Can install `pre-commit` and then before committing, linters must not
give errors and can run the auto formatters. Use by installing, setting
up `.pre-commit-config.yaml` file, initializing. Can pre-empt use with
`-n` flag when committing.
