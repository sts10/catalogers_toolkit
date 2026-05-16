from catalogers_toolkit import CRecord
from catalogers_toolkit import RecordType
from pymarc import MARCReader

# marc_file = "./src/sample-marc-files.mrc"
marc_file = (
    "./test-files/metacoll.WVU.new.M20260327.T090358.CatalogerStatsPrintandE.1.mrc"
)

with open(marc_file, "rb") as fh:
    # Parse marc file with pymarc, as usual
    reader = MARCReader(fh)
    number_of_records_read = 0
    number_of_thesis = 0
    number_of_LHRs_found_by_pymarc = 0
    number_of_LHRs_found_by_ct = 0
    for record in reader:
        number_of_records_read = number_of_records_read + 1
        c_record = CRecord(record)
        if c_record.record_type == RecordType.LHR:
            number_of_LHRs_found_by_ct = number_of_LHRs_found_by_ct + 1
        if record.get("004"):
            number_of_LHRs_found_by_pymarc = number_of_LHRs_found_by_pymarc + 1
        if c_record.is_thesis:
            number_of_thesis = number_of_thesis + 1

    print(
        "Found "
        + str(number_of_records_read)
        + " records, "
        + str(number_of_LHRs_found_by_ct)
        + " were LHRs"
    )
    print("pymarc found " + str(number_of_LHRs_found_by_pymarc) + " LHRs")
    print("found " + str(number_of_thesis) + " theses")
    print("Done")
