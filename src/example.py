from crecord import CRecord
from pymarc import MARCReader

marc_file = "./src/sample-marc-files.mrc"

with open(marc_file, 'rb') as fh:
    reader = MARCReader(fh)
    for record in reader:
        print(record['245']['a'])
        this_record = CRecord(record)
        print(this_record.ocn)
        print(this_record.field00703_list)
        print(this_record.field00704_list)
        print(this_record.field00706_list)
        print(this_record.field100a)
