from catalogers_toolkit import CRecord
from pymarc import MARCReader

marc_file = "./src/sample-marc-files.mrc"

with open(marc_file, "rb") as fh:
    # Parse marc file with pymarc, as usual
    reader = MARCReader(fh)
    for record in reader:
        # Check that we can read a field
        print(record["245"]["a"])
        # Now the key move: pass this pymarc-created record object
        # to catalogers_toolkit's CRecord (clean record) class
        c_record = CRecord(record)
        # Now we can call any variable we want, parsed and cleaned
        # exactly as defined in catalogers_toolkit's CRecord class
        # definition
        print(c_record.ocn)
        print(c_record.field00703_list)
        print(c_record.field00704_list)
        print(c_record.field00706_list)
        print(c_record.field100a)
