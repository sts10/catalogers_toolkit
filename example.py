from catalogers_toolkit import CRecord
from pymarc import MARCReader

marc_file = "./src/sample-marc-files.mrc"

with open(marc_file, "rb") as fh:
    # Parse marc file with pymarc, as usual
    reader = MARCReader(fh)
    for record in reader:
        # Check that we can read a field
        print(record["245"]["a"])
        print(record.get("020", {}).get("a", None))
        # Now the key move: pass this pymarc-created record object
        # to catalogers_toolkit's CRecord (clean record) class
        c_record = CRecord(record)
        # Now we can call any variable we want, parsed and cleaned
        # exactly as defined in catalogers_toolkit's CRecord class
        # definition
        print("OCN: " + c_record.ocn)
        print("ISBN: {0}".format(c_record.isbn))
        print("007 03: {0}".format(c_record.field00703_list))
        print("007 04:{0}".format( c_record.field00704_list))
        print("007 06: {0}".format(c_record.field00706_list))
        print("100a: {0}".format(c_record.field100a))
        print("264: {0}".format(c_record.field264))
        print("Record type: {0}".format(c_record.record_type.value))
        print("Location: " + c_record.location + ", " + c_record.shelving_location)
        print("ACLR row:")
        print(c_record.prep_aclr_csv_row())
