# did-sdk-py

[![Release](https://img.shields.io/github/v/release/hashgraph/did-sdk-py)](https://img.shields.io/github/v/release/hashgraph/did-sdk-py)
[![Build status](https://img.shields.io/github/actions/workflow/status/hashgraph/did-sdk-py/main.yml?branch=main)](https://github.com/hashgraph/did-sdk-py/actions/workflows/main.yml?query=branch%3Amain)
[![codecov](https://codecov.io/gh/hashgraph/did-sdk-py/branch/main/graph/badge.svg)](https://codecov.io/gh/hashgraph/did-sdk-py)
[![Commit activity](https://img.shields.io/github/commit-activity/m/hashgraph/did-sdk-py)](https://img.shields.io/github/commit-activity/m/hashgraph/did-sdk-py)
[![License](https://img.shields.io/github/license/hashgraph/did-sdk-py)](https://img.shields.io/github/license/hashgraph/did-sdk-py)

The repository contains the Python SDK for managing DID Documents and AnonCreds Verifiable Credentials registry using
Hedera Consensus Service.

Documentation:

- See [SDK docs](https://hashgraph.github.io/did-sdk-py/)
- Design documentation can be found in [repo folder](docs/design)

## Getting started

### Prerequisites

- Python 3.12+
- [Poetry](https://python-poetry.org/) (at least 1.8.4)
- NodeJS and npm (used by pre-commit hooks)
- Tools for Makefile support (Windows only)
  - Can be installed with [chocolatey](https://chocolatey.org/): `choco install make`

### Environment

The project uses Makefile for dev scripts. You can view available commands by running:

```bash
make help
```

Core commands are listed below:

#### Install dependencies and tools

```bash
make install
```

#### Run code quality checks

```bash
make check
```

#### Run tests

```bash
make test
```

#### Build artifacts

```bash
make build
```

## Releasing a new version

- Create an API Token on [PyPI](https://pypi.org/)
- Add the API Token to your projects secrets with the name `PYPI_TOKEN` by
  visiting [this page](https://github.com/hashgraph/did-sdk-py/settings/secrets/actions/new)
- Create a [new release](https://github.com/hashgraph/did-sdk-py/releases/new) on GitHub
- Create a new tag in the form `*.*.*`
