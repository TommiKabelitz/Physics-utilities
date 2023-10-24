import re

shift_regex = re.compile(r"([xyzt]\d{2})")


class Shift:
    coords = ("x", "y", "z", "t")

    def __init__(
        self,
        shift_str: str = None,
        x: int = None,
        y: int = None,
        z: int = None,
        t: int = None,
    ):
        if not any((shift_str, x, y, z, t)):
            raise ValueError("One of shift_str, x, y, z, t must be non-None")

        if shift_str is None:
            self._init_from_xyzt(x, y, z, t)
        elif any((x, y, z, t)):
            self._init_from_str(shift_str)
            if (self.x, self.y, self.z, self.t) != (x, y, z, t):
                raise ValueError(f"{shift_str=} and {(x,y,z,t)=} do not agree.")
        else:
            self._init_from_str(shift_str)

    def _init_from_str(self, shift_str: str):
        """Initialise from specified shift string"""
        groups = re.findall(shift_regex, shift_str)

        for group in groups:
            setattr(self, group[0], int(group[1:]))
        self.shift_str = shift_str
        self._check_missing()

    def _init_from_xyzt(
        self, x: int = None, y: int = None, z: int = None, t: int = None
    ):
        """Initialise from specified coordinates"""
        if not any(x, y, z, t):
            raise ValueError(f"One of x,y,z,t must be non-None.")
        for coord, val in zip(self.coords, (x, y, z, t)):
            if val is not None:
                setattr(self, coord, int(val))
        self._check_missing()

    def _check_missing(self):
        """Set any missing shift directions to zero."""
        for coord in self.coords:
            if not hasattr(self, coord):
                setattr(self, coord, 0)

    # Allows iteration through shift and casting to tuple
    def __iter__(self):
        for val in (self.x, self.y, self.z, self.t):
            yield val

    def __hash__(self):
        return hash(tuple(self))

    def __eq__(self, other):
        return tuple(self) == tuple(other)

    def __neq__(self, other):
        return not (self == other)

    def __str__(self):
        return self.shift_str

    def __repr__(self):
        return self.shift_str

    @property
    def as_dict(self):
        return dict(zip(self.coords, self.values))

    @property
    def values(self):
        return tuple(self)

    @property
    def format_shift(x: int = None, y: int = None, z: int = None, t: int = None) -> str:
        string = ""
        for coord, val in zip(Shift.coords, (x,y,z,t)):
            if val is not None:
                string += f"{coord}{val:02}"
        if string == "":
            return "t00"
        
    def format_for_cola(self, shift_type: str):
        if shift_type == "full":
            return f"{self.x} {self.y} {self.z} {self.t}"
        elif shift_type == "emode":
            return f"{self.x} {self.y} {self.z} 0"
        elif shift_type == "lpsink":
            return f"0 0 0 {self.t}"
        else:
            raise ValueError("shift_type must be 'full', 'emode', or 'lpsink'")