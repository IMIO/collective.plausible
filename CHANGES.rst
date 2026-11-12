Changelog
=========


1.0a7 (unreleased)
------------------

- Fix: ``@@plausible-view``, ``@@plausible-healthcheck`` and the tracking
  snippet only treat Plausible as set when it is enabled and its URL and site
  are filled in (they always did before). The object menu links no longer
  require the token.
  [remdub]

- Fix: the healthcheck calls the Plausible API once per page with a 5 s
  timeout, and shows the PostgreSQL and sites cache statuses instead of
  repeating ClickHouse's.
  [remdub]

- Modernize package: Plone 6.1 / 6.2 and Python 3.10 to 3.13 only, PEP 420
  native namespace, plone.meta, metadata in ``pyproject.toml``, uv Makefile.
  Drop Plone 5.2 / 6.0 support.
  [remdub]


1.0a6 (2024-03-08)
------------------

- Fix : action names
  [remdub]


1.0a5 (2024-03-08)
------------------

- Refactor : collective.plausible is now based on a behavior
  [remdub]

- Add viewlet to insert plausible tracking code in the page
  [remdub]

- Refactor : server healthcheck is now a separate view @@plausible-healthcheck
  [remdub]

1.0a4 (2024-02-22)
------------------

- Add plausible server healthcheck into plausible control panel
  [remdub]


1.0a3 (2024-02-20)
------------------

- Add an optional link to statistics browserview in user menu
  [remdub]


1.0a2 (2024-02-16)
------------------

- Rename package to collective.plausible
  [remdub]


1.0a1 (2024-02-15)
------------------

- Initial release.
  [remdub]
