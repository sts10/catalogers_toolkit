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


