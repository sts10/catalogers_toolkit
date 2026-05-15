from catalogers_toolkit import CRecord
from catalogers_toolkit import RecordType
from pymarc import MARCReader
import csv

# marc_file = "./src/sample-marc-files.mrc"
marc_file = "./test-files/metacoll.WVU.new.M20260327.T090358.CatalogerStatsPrintandE.1.mrc"

aclr_rows = []
with open(marc_file, "rb") as fh:
    # Parse marc file with pymarc, as usual
    reader = MARCReader(fh)
    for record in reader:
        # Pass this pymarc-created record object
        # to catalogers_toolkit's CRecord (clean record) class
        c_record = CRecord(record)
        # Now we can call any variable we want, parsed and cleaned
        # exactly as defined in catalogers_toolkit's CRecord class
        # definition
        this_aclr_row = c_record.prep_aclr_csv_row()
        # This is likely inefficent
        aclr_rows.append(this_aclr_row)

with open('aclr.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['OCN', 'LDR6', 'LDR7', '821', '00823', '00826', '00829', '00833', 'title', 'subjects', 'thesis notes'])
    for aclr_row in aclr_rows:
        writer.writerow(aclr_row)

