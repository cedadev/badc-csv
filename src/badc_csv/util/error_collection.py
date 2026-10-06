class ErrorCollection:
    """The ErrorCollection behaves like a list of error strings ('list[str]')
    when using functionality: [], len(), +, +=, 'append()';

    But can also store a warnings, also a list[str], which are accessed through
    class/member functions.
    """

    def __init__(self, errors: tuple[str] = (), warnings: tuple[str] = ()):
        self.__errors: list[str] = [e for e in errors]
        self.__warnings: list[str] = [w for w in warnings]

    def append(self, error: str) -> None:
        self.__errors.append(error)

    def add_warning(self, warning: str) -> None:
        self.__warnings.append(warning)

    def get_errors(self) -> tuple:
        return tuple(self.__errors)

    def get_warnings(self) -> tuple:
        return tuple(self.__warnings)

    def num_errors(self) -> int:
        return len(self.__errors)

    def num_warnings(self) -> int:
        return len(self.__warnings)

    def has_warnings(self) -> bool:
        return self.num_warnings() > 0

    def __len__(self):
        return len(self.__errors)

    def __getitem__(self, index):
        return self.__errors[index]

    def __add__(self, other: ErrorCollection):
        if not type(other) is ErrorCollection:
            raise TypeError(
                f"Can only add ErrorCollection to ErrorCollection, "
                f"got object {other} of {type(other)} instead."
            )

        return ErrorCollection(
            errors=self.get_errors() + other.get_errors(),
            warnings=self.get_warnings() + other.get_warnings(),
        )

    def __iadd__(self, other: ErrorCollection):
        if not type(other) is ErrorCollection:
            raise TypeError(
                f"Can only add ErrorCollection to ErrorCollection, "
                f"got object {other} of {type(other)} instead."
            )
        for e in other.get_errors():
            self.append(e)
        for w in other.get_warnings():
            self.add_warning(w)

        return self

    def __repr__(self):
        return self.__errors.__repr__()
