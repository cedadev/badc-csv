from enum import Enum

from badc_csv.check_types_bool import getCheckFunction
from badc_csv.error_collection import ErrorCollection
from badc_csv.mandatory_info_data import mandatory_info, mandatory_info_order
from badc_csv.metadata import MetadataGlobalLabel

MANDATORY_CLASS = Enum(
    "MANDATORY_CLASS",
    [("NOT_MANDATORY", 0), ("MANDATORY", 1), ("ALL_COLUMNS", 2)],
)


class MandatoryLabel:
    def __init__(
        self,
        label: str,
        flags: tuple[int],
        label_type: str,
        description: str,
    ):
        self.label = label
        self.__set_flags(*flags)
        self.expected_type = label_type
        self.type_check = getCheckFunction(label_type)

    def __set_flags(
        self,
        global_flag: int,  # 0 or 1
        column_flag: int,  # 0 or 1
        min_count: int,  # 0+
        max_count: int,  # 0+, or -1 if no maximum
        mandatory_basic: int,  # 0,1,2
        mandatory_complete: int,  # 0,1,2
    ):
        self.global_flag: bool = bool(global_flag)
        self.column_flag: bool = bool(column_flag)
        self.min_count: int = int(min_count)
        self.max_count: int = int(max_count)
        self.mandatory_basic: MANDATORY_CLASS = MANDATORY_CLASS(mandatory_basic)
        self.mandatory_complete: MANDATORY_CLASS = MANDATORY_CLASS(
            mandatory_complete
        )

    def check_label(self, label, colname, multiline_values) -> ErrorCollection:
        errors = ErrorCollection()
        # Global flag, Column flag
        if colname is MetadataGlobalLabel:
            # column is "Global"
            if not self.global_flag:
                # global must have global flag
                errors.append(f"Global cannot have label '{label}'.")
        elif not self.column_flag:
            # specific column / non-global must have column flag
            errors.append(f"Non-global column cannot have label '{label}'.")

        # Do for each 'line' of values separately.
        for values in multiline_values:
            # Number of "values" in a label
            num_values = len(values)
            if self.min_count <= num_values and (
                num_values <= self.max_count or self.max_count == -1
            ):
                pass  # Valid parameters
            else:
                # -1 indicates unbounded maximum
                # Unclear how this should be implemented for multiple lines.
                message = (
                    f"For label '{label}' column '{colname}': Number of values must be between "
                    f"{self.min_count} and {self.max_count} (inc). Instead got {num_values}."
                )
                if label == "comments":
                    errors.add_warning(message)
                else:
                    errors.append(message)

            # Type Check the values (of the metadata)
            type_check_result: bool = self.type_check(values)
            if not type_check_result:
                errors.append(
                    f"TypeCheck error for label '{label}' on column '{colname}'. "
                    f"Expected type '{self.expected_type}'."
                )
        return errors


class MandatoryClassifications:
    def __init__(self):
        self.labels = [
            MandatoryLabel(label, *mandatory_info[label])
            for label in mandatory_info_order
        ]

    def get_label(self, label) -> MandatoryLabel:
        if label not in mandatory_info_order:
            return None
        index = mandatory_info_order.index(label)
        return self.labels[index]

    def get_label_names(self) -> set[str]:
        return {l.label for l in self.labels}

    def basic_labels(self):
        return [
            label
            for label in self.labels
            if label.mandatory_basic != MANDATORY_CLASS.NOT_MANDATORY
        ]

    def complete_labels(self):
        return [
            label
            for label in self.labels
            if label.mandatory_complete != MANDATORY_CLASS.NOT_MANDATORY
        ]
