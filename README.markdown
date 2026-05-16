# Catalog's Toolkit

An experiment in adding a data-cleaning layer on top of [pymarc](https://gitlab.com/pymarc/pymarc), aimed at collection assessment.

Note that pymarc is NOT included as a dependency in this project at this time, and thus must be installed and imported separately.

Run `python examples/example.py` for an example of what this code can do.

## To use in a script

First, install the package from GitHub
```sh
pip install git+https://github.com/sts10/catalogers_toolkit.git
```

Then import the CRecord class:
```python
from catalogers_toolkit import CRecord
```

### When using a notebook like with Google Colab
I think for Google Colab, you'll want to start your file with something like this:
```
from google.colab import drive
pip install pymarc
pip install git+https://github.com/sts10/catalogers_toolkit.git

from pymarc import MARCReader
from catalogers_toolkit import CRecord

# Set a variable called marc_file

with open(marc_file, "rb") as fh:
    reader = MARCReader(fh, to_unicode=True, force_utf8=True, utf8_handling="replace")
    for record in reader:
        c_record = CRecord(record)
        print("OCN: " + c_record.ocn)
```

See the `/examples` directory for more example usage.
