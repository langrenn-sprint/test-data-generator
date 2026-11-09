# test-data-generator

Simple CLI tool to generate random contestant lists for testing langrenn-sprint, in the iSonen or Sportsadmin CSV format. It uses the [Faker](https://faker.readthedocs.io/en/master/) library to generate the data. The columns of each format are documented in `formats/`.

## Requirements

- [uv](https://docs.astral.sh/uv/)

## Installation

```bash
% git clone git@github.com:langrenn-sprint/test-data-generator.git
% cd test-data-generator
% uv sync
```

## Usage

```bash
% uv run test-data-generator --help
```

## Development

Formatting

```bash
% uv run ruff format
```

Linting

```bash
% uv run ruff check --fix
```
Typing

```bash
% uv run ty check
```

Dependency management

```bash
% uv run deptry
```

Audit

```bash
% uv run pip-audit
```

Testing

```bash
% uv run pytest
```

## Reference
- [Building and Publishing](https://packaging.python.org/en/latest/guides/section-build-and-publish/)
