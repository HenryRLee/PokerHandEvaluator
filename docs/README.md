# PokerHandEvaluator documentation

The project documentation is a single [Sphinx](https://www.sphinx-doc.org/)
site published to GitHub Pages at
<https://henryrlee.github.io/PokerHandEvaluator> by the
`.github/workflows/docs.yml` workflow whenever changes land on `develop`.

It is organised into three sections:

- `algorithm/` — the description of the underlying perfect-hash algorithm,
  included from [`Documentation/Algorithm.md`](../Documentation/Algorithm.md).
- `cpp/` — usage and examples of the C/C++ library.
- `python/` — usage and API reference of the `phevaluator` Python package. The
  API reference is generated from the package's Google-style docstrings.

## Building locally

Install the documentation dependencies (declared in the Python package's
`docs` optional-dependency group) and build the HTML from this directory:

```shell
pip install '../python[docs]'
make html
```

The generated site is written to `_build/html`. Open `_build/html/index.html`
in a browser to preview it.

The native `phevaluator._pheval` C extension is mocked during the build (see
`conf.py`), so no C compiler is required to build the docs.
