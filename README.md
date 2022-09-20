# Trunk Based Development

Perhaps the most common way to develop code as a
team is the (scaled) trunk based development model.
In this model there is the __trunk__ branch which is
assumed to be in a good, deployable state. This is typically called
either `main` (GitHub's preferred term since ~2020) or
`master`.

[source](https://trunkbaseddevelopment.com/)

New code is not pushed directly to the trunk brunch,
but instead created in __feature__ branches which
are where development happens. When the code is ready,
a pull request (PR) is opened which gives another person the
opportunity to comment and approve the changes. If everything
looks good, the feature branch is merged into the trunk branch.
In this model, the trunk branch can always serve as the reference.

Even for an individual project, doing your development on branches
and only merging changes that are confirmed to work can help keep
your code presentable if you want to use your GitHub account on
your resume. PRs don't really make sense as there will not be
someone else to review your work, but you can
`git checkout main; git merge feat/some-feature` and then delete
the feature branch.

## Small PRs

A crucial idea is that feature branches should be well-scoped and
short lived. A pull request that features changes to 500 lines of
code across 7 files is hard for a reviewer to understand and can
lead to accidental introduction of bugs.

Also, work should be well-coordinated enough that PRs do not
really get rejected in a typical work flow. What happens is that
a reviewer will leave comments that then get resolved. Rejected
PRs are more common for open source projects where it's really up
to the author to convince the core maintainers that their changes
are worth adding.

Different teams will assign reviewers in different ways. Some teams
will have a rotating on-call person tasked with reviewing PRs. Small
teams might work with a "whoever has time grabs it" method.

Upon completion, the branch is deleted and work starts again on
a french branch.

## Pair coding

A somewhat common practice for ensuring that changes to the codebase
are good and share knowledge is to use pair coding. One person codes
while sharing their screen with a second developer. The person watching
dictates what changes to make while the person sharing their screen
implements the changes. This forces code to always have been seen
by two people and makes sure ideas are clearly communicated, because
if not, the implementation will be off and the person dictating will
be forced to revise their description of what should be happening. It
might sound painful, but can be very useful and after some practice
can feel fairly natural.

## Other Models

### Trunk based development (small teams)

Another way to work is to have all developers commit directly to
the trunk and then peel off releasable code into release branche
which live forever and do not get updated. This is primarily used
by smaller teams.


### Gitflow

An older model is called [Gitflow](https://www.atlassian.com/git/tutorials/comparing-workflows/gitflow-workflow). This model involves long lived feature branches
which are only deployed once a feature -- typically a larger chunk
of code -- is complete. The longer lived branch will then be merged
via PR into the trunk branch. Developers may even create branches off
the feature branch which are PR'd into it. As can be seen at that link,
it is common in this workflow to have a main branch where releases
are done, and a development branch which is really the trunk branch
from which features are derived. The development branch is occasionally
PR'd into the main branch when releases are done.

The main issue with this and why it has fallen out of favor is that
with multiple features in development at the same time, the PRs will
often have many conflicts that are costly to resolve. On the other hand,
the now standard trunk based development leads to features being sort of
half-implemented as multiple PRs are needed to enable larger features.
However, as long as the code is always in a runnable state, this is
not usually a problem.

### Infrastructure repositories

A big exception to the above is for repositories that handle
infrastructure as code (IaC). Imagine declarative code which describes a
desired set of infrastructure such as
virtual machines or databases which are then deployed via some tool
(see [terraform](https://www.terraform.io/) or [pulumi](https://www.pulumi.com/)
for examples). In this case different environments (development versus
production) might be represented by different long running branches,
each of which can sort of be considered a trunk branch with
short lived feature branches off of them.

## Naming

### Feature branches

On a team, work is usually associated with a ticket that will have a number,
so branches are named something like `<ticket number>/<type>/<decription>`.
The type will be something like `feat`, `refactor`, `fix`, `tests`, `docs`,
while the description is short, hypen separated, and informative. The order
of course can change and different teams will have different conventions.

### Commits

Related to this, there are many opinions on how to format commit messages.
The [conventional commit](https://www.conventionalcommits.org/en/v1.0.0/)
suggests using the format `type: description` where the type is as above.
Some people (like me) will insist that commits should always be imperative
`add class to handle datasets` instead of `adding class to handle datasets`.
Regardless, the most imortant thing is to keep the commit message informative.

Generally upon merging to the trunk the commits will be squashed into one
merge commit which will have both an informative short message like
one adds with `git commit -m "feat: add short message"` and a much longer
description that one gets one using just `git commit`. This helps keep the
trunk branch's history clean. The commits are still generally viewable in
the PR which is remains in source control's history.
