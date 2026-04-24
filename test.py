from pymarc import MARCReader

marc_file = "/home/sschlinkert/code/marc-reader/test-data/test_10.mrc"

class CRecord:
    def __init__(self, inputted_pymarc_record):
        raw_ocn = inputted_pymarc_record['001']
        self.ocn = str(raw_ocn).replace('=001', '').strip()
        self.ldr06 = inputted_pymarc_record.leader[6] if len(str(inputted_pymarc_record)) > 6 else None
        self.ldr07 = inputted_pymarc_record.leader[7] if len(str(inputted_pymarc_record)) > 7 else None
        self.field00703_list, self.field00704_list, self.field00706_list = self.parse_007s(inputted_pymarc_record)
        self.field100a = self.parse_100(inputted_pymarc_record)

    def parse_007s(self, inputted_pymarc_record):
        field00703_list = []
        field00704_list = []
        field00706_list = []
        if inputted_pymarc_record.get_fields('007'):
            for field in record.get_fields('007'):
                field007data = str(field.value()) 
                field00703_list.append(field007data[3] if len(field007data) >= 4 else '')
                field00704_list.append(field007data[4] if len(field007data) >= 5 else '')
                field00706_list.append(field007data[6] if len(field007data) >= 7 else '')
        return field00703_list, field00704_list, field00706_list

    def parse_100(self, inputted_pymarc_record):
        if record.get_fields('100'):
            field100 = record['100']
            field100a = field100.get_subfields('a')
            if field100a:
                field100a = field100a[0]
            else:
                field100a = str("No field 100a")
        else:
            field100a = str("No field 100")
        return field100a
    


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
