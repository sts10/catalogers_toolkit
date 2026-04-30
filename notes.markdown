## Enums for Bib vs. LCH

```python
from enum import Enum

class RecordType(Enum):
    BIB = "Bibliographic Record"
    LHR = "Local Holding Record"

class CRecord:
    def __init__(self, inputted_pymarc_record):
        # Other stuff here
        self.record_type = determine_record_type(inputted_pymarc_record)

    def determine_record_type(self, inputted_pymarc_record):
        # insert record_type determination logic here
        return RecordType.BIB
```
