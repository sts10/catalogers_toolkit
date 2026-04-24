# Catalog's Toolkit

An experiment in adding a data-cleaning layer on top of [pymarc](https://gitlab.com/pymarc/pymarc). Note that pymarc is NOT included as a dependency in this project at this time, and thus must be installed and imported separately.

Run `python example.py` for an example of what this code can do.

## To use in a script

First, install the package from GitHub
```sh
pip install git+https://github.com/sts10/catalogers_toolkit.git
```

Then import the CRecord class:
```python
from catalogers_toolkit import CRecord
```

Full example in `src/example.py`
