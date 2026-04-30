class CRecord:
    def __init__(self, inputted_pymarc_record):
        raw_ocn = inputted_pymarc_record["001"]
        self.ocn = str(raw_ocn).replace("=001", "").strip()
        self.isbn = self.get_isbn(inputted_pymarc_record)
        self.ldr06 = (
            inputted_pymarc_record.leader[6]
            if len(str(inputted_pymarc_record)) > 6
            else None
        )

        self.ldr07 = (
            inputted_pymarc_record.leader[7]
            if len(str(inputted_pymarc_record)) > 7
            else None
        )
        self.field00703_list, self.field00704_list, self.field00706_list = (
            self.parse_007s(inputted_pymarc_record)
        )
        self.field100a = self.parse_100(inputted_pymarc_record)
        self.field264 = self.parse_264s(inputted_pymarc_record)

    def get_isbn(self, inputted_pymarc_record):
        isbn = inputted_pymarc_record.get('020')
        if isbn:
            return isbn.get('a', None)
        else:
            return None
        # Fancier version: return inputted_pymarc_record.get('020', {}).get('a', None)

    def parse_007s(self, inputted_pymarc_record):
        field00703_list = []
        field00704_list = []
        field00706_list = []
        if inputted_pymarc_record.get_fields("007"):
            for field in inputted_pymarc_record.get_fields("007"):
                field007data = str(field.value())
                field00703_list.append(
                    field007data[3] if len(field007data) >= 4 else ""
                )
                field00704_list.append(
                    field007data[4] if len(field007data) >= 5 else ""
                )
                field00706_list.append(
                    field007data[6] if len(field007data) >= 7 else ""
                )
        return field00703_list, field00704_list, field00706_list

    def parse_100(self, inputted_pymarc_record):
        if inputted_pymarc_record.get_fields("100"):
            field100 = inputted_pymarc_record["100"]
            field100a = field100.get_subfields("a")
            if field100a:
                field100a = field100a[0]
            else:
                field100a = str("No field 100a")
        else:
            field100a = str("No field 100")
        return field100a

    # 264 is a non-mandatory, repeatable field, which is a good test
    # of logic!
    def parse_264s(self, inputted_pymarc_record):
        field264s_raw = inputted_pymarc_record.get_fields("264")
        # For our output, let's initialize a dictionary of lists, one
        # per subfield we're interested in
        field264s_cleaned = {
            "a": [],
            "b": [],
            "c": [],
        }
        if field264s_raw:
            for field264 in field264s_raw:
                this_a_field = field264.get_subfields("a")
                if not this_a_field:
                    field264s_cleaned["a"].append("No field 264a")
                else:
                    for field264a in this_a_field:
                        field264s_cleaned["a"].append(field264a)
                this_b_field = field264.get_subfields("b")
                if not this_b_field:
                    field264s_cleaned["b"].append("No field 264b")
                else:
                    for field264b in this_b_field:
                        field264s_cleaned["b"].append(field264b)
                this_c_field = field264.get_subfields("c")
                if not this_c_field:
                    field264s_cleaned["c"].append("No field 264c")
                else:
                    for field264c in this_c_field:
                        field264s_cleaned["c"].append(field264c)
        else:
            field264s_cleaned = {
                "a": ["No field 264"],
                "b": ["No field 264"],
                "c": ["No field 264"],
            }
        return field264s_cleaned
