# Continuous Integration

Continuous integration is the philosophy that we should constantly
be seeking to implement small changes into the production version of the
code / the application defined by the code. In CI, implemented changes should
be as small as possible.

Enabling CI is difficult, how does one ensure that in a multi-developer
team that changes do not break the code / application? And even if the code
a developer is proposing works, how do we ensure quality? Obviously the PR
is an important step, but it also slows the process down. To speed up
the pace of changes in search of "continuous" integration, there is
usually an automated testing component. This testing component is sometimes
referred to as CI itself, even if its purpose is really to enable continuous
integration.

For this repository, we are using GitHub Actions as our CI tool. In
the parlance of Actions, we have defined a CI workflow via a [YAML](https://yaml.org/)
file, which is just a structured text file and placed it in the
`.github/workflows/` directory. Going over that file, the workflow
tells GitHub Actions to pull down this repository, use `pip` to install
the package that is defined in the repo, check for style using `flake8`, and
run tests using `pytest`.
Note that all of these actions are occurring not
on your local machine, but on GitHub's servers! This helps to ensure that
the code is not working due to some local quirk, but is robust enough
to be deployed elsewhere. Ideally, your CI environment has the same conditions
as where the code is deployed and used.

A companion to CI is _Continuous Deployment_ or _Continuous Delivery_  (CD),
and it is common to refer to the two together as CI/CD. This is not implemented
here, but CD is about very often deploying the changes that are merged into the
trunk branch. GitHub Actions can also accomplish this deployment process in
some cases.

There are many CI/CD tools in addition to GitHub Actions including Jenkins,
Travis, Circle CI.

- [GitHub Actions quickstart](https://docs.github.com/en/actions/quickstart)
- [Simple workflows](https://github.com/actions/starter-workflows)


## Branch protections

In GitHub and other remote repository hosts there is the ability to
impose branch protections where you require certain conditions before allowing
a trunk branch to be updated. Typical restrictions include:

- Only allowing changes to the trunk branch via PR
- Requiring the PR to approved by N reviewers other than the PR author
- Requiring CI to pass before PRs can be merged

In GitHub this can be accomplished the repository's Settings and selecting
"Branches" in the left sidebar.
