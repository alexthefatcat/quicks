
_MISSING = object()




class CircularList(list):
    def __init__(self, *args, index=0):
        super().__init__(args)
        if not self:
            raise ValueError("CircularList requires at least one item.")
        self.index = index % len(self)

    @property
    def current(self):
        return self[self.index]

    def cycle(self, step=1):
        """Advance the index forward (or backward with negative step) and return the current item."""
        self.index = (self.index + step) % len(self)
        return self()

    def index_of(self, value):
        """Return index of item or raise ValueError."""
        # Must use super().index because self.index is an integer attribute
        return super().index(value)

    def __iadd__(self, step: int):
        """Handles `color += step`"""
        if isinstance(step, int):
            self.cycle(step)
            return self
        return NotImplemented

    def __isub__(self, step: int):
        """Handles `color -= step`"""
        if isinstance(step, int):
            self.cycle(-step)
            return self
        return NotImplemented

    def copy(self, index=None):
        """Create a new copy of the CircularList."""
        if index is False:
            target_index = 0
        elif index is None:
            target_index = self.index
        else:
            target_index = int(index)

        return self.__class__(*self, index=target_index)

    def __eq__(self, other):
        """Compare with another CircularList instance (items + index) or direct value."""
        if isinstance(other, CircularList):
            return super().__eq__(other) and self.index == other.index
        return self.current == other

    def __repr__(self):
        return f"CircularList(current={self.current!r}, index={self.index})"

    def __call__(self, value=_MISSING):
        """
        - color()        -> Returns active value ('blue')
        - color('red')   -> Sets option by value and returns self
        - color(1)       -> Sets option by index and returns self
        """
        if value is _MISSING:
            return self.current

        if isinstance(value, int):
            self.index = value % len(self)
        else:
            self.index = self.index_of(value)

        return self  # Returning self keeps the object reference intact

    def set(self, value):
        """Set current option by value."""
        return self(value)

    # def __call__(self):
    #     return self.current

    # def set(self, value):
    #     """Set current option by value."""
    #     self.index = self.index_of(value)
    #     return self()

    
color = CircularList('Blue','Green','Yellow','Orange','Red','Purple')

print(color())
color.cycle()
print(color())
color +=1
print(color())
color2 = color.copy(index=False)
color3 = color.copy(index=2)
color4 = color.copy()
color2 != color
color4 == color

color = color('Blue')


for clr in color:
    print(clr)














