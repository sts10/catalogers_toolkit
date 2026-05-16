from catalogers_toolkit import CRecord
from catalogers_toolkit import RecordType
from pymarc import MARCReader

marc_file = (
    "./test-files/metacoll.WVU.new.M20260327.T090358.CatalogerStatsPrintandE.1.mrc"
)

i = 0
with open(marc_file, "rb") as fh:
    # Parse marc file with pymarc, as usual
    reader = MARCReader(fh, to_unicode=True, force_utf8=True, utf8_handling="replace")
    for record in reader:
        c_record = CRecord(record)
        if c_record.record_type == RecordType.BIB:
            print("Subjects: " + str(c_record.field650s))
            i = i + 1
            if i > 15:
                break
