from catalogers_toolkit import CRecord
from catalogers_toolkit import RecordType
from pymarc import MARCReader
import csv

# marc_file = "./src/sample-marc-files.mrc"
marc_file = (
    "./test-files/metacoll.WVU.new.M20260327.T090358.CatalogerStatsPrintandE.1.mrc"
)

aclr_bib_rows = []
aclr_item_rows = []
# read in binary mode
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
        # Only write Bibs 
        if c_record.record_type == RecordType.BIB:
            this_aclr_row = c_record.prep_bib_aclr_csv_row()
            aclr_bib_rows.append(this_aclr_row)
        if c_record.record_type == RecordType.LHR:
            # needs raw record from pymarc, for now
            these_alcr_rows = c_record.prep_item_aclr_csv_rows(record)
            # Rather than append, let's concatenate
            aclr_item_rows = aclr_item_rows + these_alcr_rows

with open("aclr-bibs.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "OCN",
            "LDR06",
            "LDR07",
            "field00821",
            "field00823",
            "field00826",
            "field00829",
            "field00833",
            "title",
            "subjects",
            "field502",
        ]
    )
    for aclr_bib_row in aclr_bib_rows:
        writer.writerow(aclr_bib_row)

with open("aclr-items.csv", "w", newline="") as file:
    writer = csv.writer(file)
    writer.writerow(
        [
            "LCN",
            "LHRLDR06",
            "LOCN",
            "Location",
            "ShelvingLocation",
            "CopyInitialsList",
            "ItemInitialsList",
            "Barcode",
        ]
    )
    for aclr_item_row in aclr_item_rows:
        writer.writerow(aclr_item_row)
