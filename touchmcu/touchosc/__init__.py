import lxml.etree as et
import math
from enum import Enum, IntEnum

class Color(dict):
    def __init__(self, hex=None, **kwargs):
        if hex is None:
            super().__init__(**kwargs)
            return
        elif isinstance(hex, int):
            r = (hex & 0xFF000000) >> 24
            g = (hex & 0x00FF0000) >> 16
            b = (hex & 0x0000FF00) >> 8
            a = (hex & 0x000000FF) >> 0
        elif isinstance(hex, str):
            if hex[0] == '#':
                hex = hex[1:]

            if len(hex) == 6:
                hex += 'FF'

            if len(hex) != 8:
                raise ValueError

            r = int(hex[0:2], 16)
            g = int(hex[2:4], 16)
            b = int(hex[4:6], 16)
            a = int(hex[6:8], 16)
        else:
            raise ValueError

        super().__init__(r=(r/255.0), g=(g/255.0), b=(b/255.0), a=(a/255.0))

    def to_xml(self, parent):
        for k in ['r', 'g', 'b', 'a']:
            e = et.SubElement(parent, k)
            e.text = str(self.get(k, 0))

class Rect(dict):

    def position(self):
        return (
            self.get("x", 0),
            self.get("y", 0)
        )

    def center(self):
        return (
            self.get("x", 0) + (self.get("w", 0)/2),
            self.get("y", 0) + (self.get("h", 0)/2)
        )
    
    def top(self):
        return self.get("y", 0)

    def bottom(self):
        return self.get("y", 0) + self.get("h", 0)

    def left(self):
        return self.get("x", 0)

    def right(self):
        return self.get("x", 0) + self.get("w", 0)

    def resize(self, w, h):
        if w < 0 or h < 0:
            raise ValueError("Negative size")

        self["w"] = w
        self["h"] = h

    def move(self, x, y, relative=False):
        if relative:
            self["x"] = self.get("x", 0) + x
            self["y"] = self.get("y", 0) + y
        else:
            self["x"] = x
            self["y"] = y

    def move_center(self, x, y):
        self["x"] = x - (self.get("w", 0)/2)
        self["y"] = y - (self.get("h", 0)/2)

    def move_top(self, top):
        self["y"] = top

    def move_bottom(self, bottom):
        self["y"] = bottom - self.get("h", 0)

    def move_left(self, left):
        self["x"] = left

    def move_right(self, right):
        self["x"] = right - self.get("w", 0)

    def move_center_polar(self, xc, yc, r, a):
        rad = a * 2 * math.pi / 360.0
        dx = r * math.cos(rad)
        dy = -r * math.sin(rad)
        self.move_center(xc + dx, yc + dy)

    def expand(self, t, r, b, l):
        self["x"] = self.get("x", 0) - l
        self["y"] = self.get("y", 0) - t
        self["w"] = self.get("w", 0) + l+r
        self["h"] = self.get("h", 0) + t+b

    def shrink(self, t, r, b, l):
        self.expand(-t, -r, -b, -l)

    def to_xml(self, parent):
        for k in ['x', 'y', 'w', 'h']:
            e = et.SubElement(parent, k)
            e.text = str(int(self.get(k, 0)))

class String(str):
    def to_xml(self, parent):
        parent.text = et.CDATA(self)

class Bool:
    def __init__(self, value=False):
        self.value=bool(value)

    
    def to_xml(self, parent):
        parent.text = str(1) if self.value else str(0)

class Float:
    def __init__(self, value=0):
        self.value=float(value)

    
    def to_xml(self, parent):
        parent.text = str(self.value)

class Integer:
    def __init__(self, value=0):
        self.value=int(value)

    
    def to_xml(self, parent):
        parent.text = str(int(self.value))

class ColorEnum(Enum):
    GREY   = Color('#666666FF')
    RED    = Color('#FF0000FF')
    ORANGE = Color('#FF9900FF')
    GREEN  = Color('#00FF00FF')
    BLUE   = Color('#00C0FFFF')
    BLACK  = Color('#000000FF')
    WHITE  = Color('#FFFFFFFF')

class Condition(Enum):
    ANY = 'ANY'
    RISE = 'RISE'
    FALL = 'FALL'

class OutlineStyle(IntEnum):
    FULL = 0
    CORNERS = 1
    EDGES = 2

class PointerPriority(IntEnum):
    OLDEST = 0
    NEWEST = 1

class Orientation(IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

class Shape(IntEnum):
    RECTANGLE = 1
    CIRCLE = 2
    TRIANGLE = 3
    DIAMOND = 4
    PENTAGON = 5
    HEXAGON = 6

class ButtonType(IntEnum):
    MOMENTARY = 0
    TOGGLE_RELEASE = 1
    TOGGLE_PRESS = 2

class AlignH(IntEnum):
    LEFT = 0
    RIGHT = 1
    CENTER = 2

class AlignV(IntEnum):
    TOP = 0
    BOTTOM = 1
    MIDDLE = 2

class Font(IntEnum):
    DEFAULT = 0
    MONOSPACE = 1

class CursorDisplay(IntEnum):
    ALWAYS = 0
    ACTIVE = 1
    INACTIVE = 2

class Response(IntEnum):
    ABSOLUTE = 0
    RELATIVE = 1

class RadioType(IntEnum):
    SELECT = 0
    METER = 1