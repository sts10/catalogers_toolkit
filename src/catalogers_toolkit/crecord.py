class CRecord:
    def __init__(self, inputted_pymarc_record):
        raw_ocn = inputted_pymarc_record["001"]
        self.ocn = str(raw_ocn).replace("=001", "").strip()
        self.isbn = self.get_isbn(inputted_pymarc_record)
        self.title = inputted_pymarc_record.get("245", {}).get("a", None)
        # I don't know if we need this len check
        self.ldr06 = (
            inputted_pymarc_record.leader[6]
            if len(str(inputted_pymarc_record.leader)) > 6
            else None
        )
        self.ldr07 = (
            inputted_pymarc_record.leader[7]
            if len(str(inputted_pymarc_record.leader)) > 7
            else None
        )
        self.field00703_list, self.field00704_list, self.field00706_list = (
            self.parse_007s(inputted_pymarc_record)
        )
        # To save RAM, we could call this only when we need them, not on initalization
        self.field100a = self.parse_100(inputted_pymarc_record)
        self.field264 = self.parse_264s(inputted_pymarc_record)
        self.field008 = self.parse_008(inputted_pymarc_record)
        self.field502s = self.parse_502s(inputted_pymarc_record)
        self.field650s = self.parse_650s(inputted_pymarc_record)

    def get_isbn(self, inputted_pymarc_record):
        isbn = inputted_pymarc_record.get("020")
        if isbn:
            return isbn.get("a", None)
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

    # 008 is not repeatable, so we don't need to use a get_fields loop
    def parse_008(self, inputted_pymarc_record):
        # a bit unsure about this .value() call
        raw_008 = inputted_pymarc_record["008"].value()
        # We can do this more elegantly
        clean_008 = {}
        clean_008["21"] = raw_008[21] if len(raw_008) > 21 else ""
        clean_008["23"] = raw_008[23] if len(raw_008) > 23 else ""
        clean_008["26"] = raw_008[26] if len(raw_008) > 26 else ""
        clean_008["29"] = raw_008[29] if len(raw_008) > 29 else ""
        clean_008["33"] = raw_008[33] if len(raw_008) > 33 else ""
        return clean_008

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

    def parse_650s(self, inputted_pymarc_record):
        cleaned_subjects = []
        subjects = inputted_pymarc_record.get_fields("650")
        if not subjects:
            cleaned_subjects.append("No subjects")
        else:
            for subject in subjects:
                # I don't think we have to loop through all subfields here, right?
                # if subject.get("a"):
                #     cleaned_subjects.append(subject.get("a"))
                for code_value in subject:
                    if code_value.code == "a":
                        cleaned_subjects.append(str(code_value.value))
        return cleaned_subjects

    def parse_502s(self, inputted_pymarc_record):
        cleaned_502s = []
        raw_502s = inputted_pymarc_record.get_fields("502")
        if not raw_502s:
            cleaned_502s.append("No field 502")
        else:
            for field_502 in raw_502s:
                field_502as = field_502.get_subfields("a")
                if not field_502as:
                    cleaned_502s.append("No 502a")
                else:
                    for code_value in field_502as:
                        if code_value.code == "a":
                            cleaned_502s.append(str(code_value.value))
        return cleaned_502s

    def prep_aclr_csv_row(self):
        return [
            self.ocn,
            self.ldr06,
            self.ldr07,
            self.field008["21"],
            self.field008["23"],
            self.field008["26"],
            self.field008["29"],
            self.field008["33"],
            self.title,
            self.field650s,
            self.field502s,
            # Would it be better to join these lists in to a single 
            # string? using a space as a delimiter?
            # '|'.join(str(e) for e in self.field650s),
            # '|'.join(str(e) for e in self.field502s),
        ]
