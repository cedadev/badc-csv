from enum import Enum

from badc_csv.check_types_bool import getCheckFunction
from badc_csv.mandatory_info_data import mandatory_info, mandatory_info_order

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
        self.global_flag = global_flag
        self.column_flag = column_flag
        self.min_count = min_count
        self.max_count = max_count
        self.mandatory_basic = MANDATORY_CLASS(mandatory_basic)
        self.mandatory_complete = MANDATORY_CLASS(mandatory_complete)


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
