# coderetreat-aiohttp

Here we stored our PoC implementation of the Dependency Injection for the `aiohttp` stack. This code was made during the summer'24 [https://coderetreat.me](CodeRetreat).

Implemented features:

- [x] injection of request attributes
- [x] injection of "generic" dependencies stored in the `aiohttp.web.Application`

Homework (if anyone will ever want to dig deeper):

- [ ] teach the `inject` decorator to work with middlewares too
- [ ] check the types of `Injectable` args during the handler wrapping
- [ ] make possible to have the "callable" deps as functions from the `app` + `request`
- [ ] make these callable deps injectable themselves

PRs are welcomed!

# [src/coderetreat_aiohttp/patmat.py]()

Here we just played a little with the pattern matching and dataclasses
