## Enums for Bib vs. LCH

```python
from enum import Enum

class RecordType(Enum):
    BIB = "Bibliographic Record"
    LHR = "Local Holding Record"

class CRecord:
    def __init__(self, inputted_pymarc_record):
        # Other stuff here
        self.record_type = self.determine_record_type(inputted_pymarc_record)

    def determine_record_type(self, inputted_pymarc_record):
        # insert record_type determination logic here
        return RecordType.BIB
```

## A safe get function for classes

```python 
class MyClass:
    def __init__(self, name):
        self.name = name

    def get(self, attr_name, default=None):
        """Safely retrieve an attribute or return a default value."""
        return getattr(self, attr_name, default)

# Usage
obj = MyClass("Alice")

print(obj.get("name"))          # Output: Alice
print(obj.get("age", "N/A"))    # Output: N/A (Attribute doesn't exist)
print(obj.get("age"))           # Output: None (Default behavior)
```

For our purposes:
```python 
class MyClass:
    def __init__(self, name):
        self.name = name

    def get(self, attr_name, default=None):
        """Safely retrieve an attribute or return a default value."""
        if default == None:
            default = "No {0}".format(attr_name.replace("_", " "))
        return getattr(self, attr_name, default)

# Usage
obj = MyClass("Alice")

print(obj.get("name"))          # Output: Alice
print(obj.get("age", "N/A"))    # Output: N/A (Attribute doesn't exist)
print(obj.get("age"))           # Output: "No age"

```


```python
def get_leader_position(self, record, position):
    """Safely extract a leader position from a MARC record."""
    """# Usage"""
    """self.ldr07 = self.get_leader_position(inputted_pymarc_record, 7)"""
    try:
        leader = record.leader
        if leader and len(leader) > position:
            return leader[position]
    except (AttributeError, TypeError):
        pass # do nothing at all
    # Effectively return None if error
    return None
```

## LHR notes

1 LHR can contain multiple ITEMS, each with a unique barcode (876)

We want one CSV of BIBs, one CSV of ITEMs (not LHRs).

### Columns for our Items CSV?
From Session 1, 00:36:11
LCN -- MARC 001
LHRLDR06 -- Leader 6
LOCN -- MARC 004
Location -- 852$b
ShelvingLocation -- 852$c
CopyInitialsList -- 852$x (Can be multiple, we want a list)
BarcodeList -- 876$p


To make the ITEMS CSV:
```python
for barcode in barcode_list:
    csv_out.writerow([LCN, LDR06, LOCN, Location, ShelvingLocation, CopyInitialsList, barcode)

```

So we probably want a new, separate Item (or Barcode) Class!

Any Bib that does not have an associated LHR is a e-resource?!
