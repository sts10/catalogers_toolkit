from .record_type import RecordType
import sys


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
        # Determine if Bib or LHR
        self.record_type = self.determine_record_type(inputted_pymarc_record)
        # Determine if thesis or not
        self.is_thesis = self.determine_if_thesis(inputted_pymarc_record)

        self.field00703_list, self.field00704_list, self.field00706_list = (
            self.parse_007s(inputted_pymarc_record)
        )
        # To save RAM, we could call this only when we need them, not on initalization
        self.field004 = self.parse_004(inputted_pymarc_record)

        self.field100a = self.parse_100(inputted_pymarc_record)
        self.field264 = self.parse_264s(inputted_pymarc_record)
        self.field008 = self.parse_008(inputted_pymarc_record)
        self.field502s = self.parse_502s(inputted_pymarc_record)
        self.field650s = self.parse_650s(inputted_pymarc_record)

        self.location = inputted_pymarc_record.get("852", {}).get("b", "No Branch")
        self.shelving_location = inputted_pymarc_record.get("852", {}).get(
            "c", "No shelving location"
        )

    def pretty_print(self, attr_name, default=None):
        """Safely retrieve an attribute. If not found, return string of 'No [attribute] found'."""
        """Usage:"""
        """print(obj.get("name"))          # Output: Alice"""
        """print(obj.get("age", "N/A"))    # Output: N/A (Attribute doesn't exist)"""
        if default is None:
            # We could return None here, but for fun, let's overwrite the default
            # to reference the field name, e.g. "No isbn".
            default = "No {0}".format(attr_name.replace("_", " "))
        return getattr(self, attr_name, default)

    def get_leader_position(self, record, position):
        """Safely extract a leader position from a MARC record."""
        """Usage:"""
        """self.ldr07 = self.get_leader_position(inputted_pymarc_record, 7)"""
        try:
            leader = record.leader
            if leader and len(leader) > position:
                return leader[position]
        except (AttributeError, TypeError):
            pass  # do nothing at all
        # Effectively return None if error
        return None

    def get_isbn(self, inputted_pymarc_record):
        isbn = inputted_pymarc_record.get("020")
        if isbn:
            return isbn.get("a", None)
        else:
            return None
        # Fancier version: return inputted_pymarc_record.get('020', {}).get('a', None)

    def parse_004(self, inputted_pymarc_record):
        """Warning that this field only parses the FIRST instance of field 004, which may be repeatable?"""
        if inputted_pymarc_record.get_fields("004"):
            return (
                str(inputted_pymarc_record.get_fields("004")[0])
                .replace("=004", "")
                .strip()
            )
        else:
            return "No field 004"

    def determine_record_type(self, inputted_pymarc_record):
        # Check if field 004 is empty or not (we used to check ldr6 of u, v, x, or y)
        if inputted_pymarc_record.get_fields("004") != []:
            # Note that LHRs may NOT have 245s or other fields
            # that are mandatory for Bib records!
            return RecordType.LHR
        else:
            return RecordType.BIB

    # 007 is not mandatory and effectively not repeatable
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
                if subject.get_subfields("a"):
                    cleaned_subjects = cleaned_subjects + subject.get_subfields("a")
        return cleaned_subjects

    def determine_if_thesis(self, inputted_pymarc_record):
        return inputted_pymarc_record.get_fields("502") != []

    def parse_502s(self, inputted_pymarc_record):
        """Thesis notes"""
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
                    for subfield in field_502as:
                        # Treading carefully here, because sometimes a subfield is just a string
                        # And we don't want to error out
                        if (
                            subfield
                            and hasattr(subfield, "code")
                            and callable(subfield.code)
                            and subfield.code == "a"
                        ):
                            cleaned_502s.append(str(subfield.value))
        return cleaned_502s

    def prep_bib_aclr_csv_row(self):
        """Only write BIBs here"""
        if self.record_type == RecordType.BIB:
            return [
                self.ocn,  # strip of left 0s?
                self.ldr06,
                self.ldr07,
                self.field008["21"],
                self.field008["23"],
                self.field008["26"],
                self.field008["29"],
                self.field008["33"],
                self.title,
                "|".join(str(e) for e in self.field650s),
                "|".join(str(e) for e in self.field502s),
            ]
        else:
            print("Tried to write a Bib ACLR CSV row for a non-Bib record type!")
            sys.exit(1)

    def parse_copy_initials(self, inputted_pymarc_record):
        cleaned_copy_initials = []
        location = inputted_pymarc_record.get("852")
        if not location:
            cleaned_copy_initials.append("No copy initials")
        else:
            if location.get_subfields("x"):
                cleaned_copy_initials = (
                    cleaned_copy_initials + cleaned_copy_initials.get_subfields("x")
                )
        if cleaned_copy_initials == []:
            return ["No copy initials"]
        else:
            return cleaned_copy_initials

    def parse_barcodes(self, inputted_pymarc_record):
        cleaned_barcodes = []
        item_info = inputted_pymarc_record.get_fields("876")
        if not item_info:
            cleaned_barcodes.append("No barcodes")
        else:
            for piece_of_item_info in item_info:
                if piece_of_item_info.get_subfields("p"):
                    # Guessing that there can be multiple barcodes for one item
                    barcodes = piece_of_item_info.get_subfields("p")
                    # so we'll append them all
                    for barcode in barcodes:
                        cleaned_barcodes.append(barcode)
        return cleaned_barcodes

    def parse_item_initials(self, inputted_pymarc_record):
        cleaned_item_initials = []
        item_info = inputted_pymarc_record.get_fields("876")
        if not item_info:
            cleaned_item_initials.append("No item initials")
        else:
            for piece_of_item_info in item_info:
                if piece_of_item_info.get_subfields("x"):
                    # x subfield is technically repeatable,
                    # so if there's more than one, we'll join with |
                    item_initials = "|".join(piece_of_item_info.get_subfields("x"))
                    cleaned_item_initials.append(item_initials)
        if cleaned_item_initials == []:
            return ["No item initials"]
        else:
            return cleaned_item_initials

    def prep_item_aclr_csv_rows(self, inputted_pymarc_record):
        """This method loops through all records looking for LHRs"""
        """When it finds one, it loops through all of that LHRs barcodes"""
        """creating a fresh list (which will become a single CSV row) for each _barcode_ (not LHR)"""
        csv_rows = []
        if self.record_type == RecordType.LHR:
            barcodes = self.parse_barcodes(inputted_pymarc_record)
            if barcodes:
                # Again, a given record could have multiple barcodes, each representing one
                # item. So we iterate through each barcode and make a separate row for each.
                for barcode in barcodes:
                    this_item_record = [
                        self.ocn,  # in the case of an LHR, it's an "LCN"?!?
                        self.ldr06,
                        self.field004,  # LOCN -- MARC 004
                        self.location,  # Location -- 852$b
                        self.shelving_location,  # ShelvingLocation -- 852$c
                        "|".join(
                            str(ele)
                            for ele in self.parse_copy_initials(inputted_pymarc_record)
                        ),
                        "|".join(
                            str(ele)
                            for ele in self.parse_item_initials(inputted_pymarc_record)
                        ),
                        barcode,  # Kind of think this should be the first column? If it's the unique identifier?
                    ]
                    csv_rows.append(this_item_record)
        else:
            print("Tried to write an Item ACLR CSV row for a non-Item record type!")
            # Consider this a fatal error for now
            sys.exit(1)
        return csv_rows
