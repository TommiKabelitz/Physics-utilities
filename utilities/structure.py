from collections.abc import Sequence

_quarks = ["u", "d", "s", "nl", "nh", "l", "h"]


class Structure(Sequence):
    def __init__(self, structure: str | list):
        if isinstance(structure, str):
            quark_1, quark_2, quark_3 = self.parse_structure_string(structure)
        elif isinstance(structure, (tuple, list)):
            quark_1, quark_2, quark_3 = structure
        else:
            raise TypeError("structure must be str, list or tuple")

        self._structure_list = [quark_1, quark_2, quark_3]
        self._structure_str = quark_1 + quark_2 + quark_3

    @staticmethod
    def parse_structure_string(structure_string):
        str_iter = iter(structure_string)
        quark = ""
        struct = []
        try:
            while True:
                quark += next(str_iter)
                if quark in _quarks:
                    struct.append(quark)
                    quark = ""
        except StopIteration:
            if len(struct) != 3 or "".join(struct) != structure_string:
                raise ValueError(f"Failed to parse structure string.")
            return struct

    def __str__(self):
        return self._structure_str

    def __repr__(self):
        return str(list(self))

    def __list__(self):
        return self._structure_list

    def as_dict(self):
        return dict(zip(("u", "d", "s"), list(self)))

    def __iter__(self):
        return iter(self._structure_list)

    def __getitem__(self, i):
        return self._structure_list[i]

    def __len__(self):
        return len(self._structure_list)
