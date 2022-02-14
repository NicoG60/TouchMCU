import copy
from email import message
import lxml.etree as et
import uuid
from enum import Enum
import math

from touchmcu.touchosc import AlignH, AlignV, ButtonType, CursorDisplay, Orientation, OutlineStyle, PointerPriority, RadioType, Response, Shape, Font, Color, Rect, ColorEnum

from touchmcu.touchosc.properties import Properties
from touchmcu.touchosc.values import NodeValues
from touchmcu.touchosc.messages import MidiMessage

class ControlType(Enum):
    BOX = 'BOX'
    BUTTON = 'BUTTON'
    LABEL = 'LABEL'
    TEXT = 'TEXT'
    FADER = 'FADER'
    XY = 'XY'
    RADIAL = 'RADIAL'
    ENCODER = 'ENCODER'
    RADAR = 'RADAR'
    RADIO = 'RADIO'
    GROUP = 'GROUP'
    PAGER = 'PAGER'
    GRID = 'GRID'


class Control:
    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        self.properties = Properties()
        self.values = NodeValues()
        self.messages = []
        self.children = []
        self.parent = None

        if not self.type:
            raise ValueError("Instantiation of abstract control")

        if "parent" in kwargs:
            self.parent = kwargs["parent"]
            kwargs["parent"].children.append(self)

        self.properties["name"]            = kwargs.get('name', 'node')
        self.properties["tag"]             = kwargs.get('tag', '')
        self.properties["frame"]           = copy.deepcopy(kwargs.get('frame', Rect(x=0, y=0, w=16, h=16)))
        self.properties["color"]           = kwargs.get('color', ColorEnum.BLACK)
        self.properties["visible"]         = kwargs.get('visible', True)
        self.properties["interactive"]     = kwargs.get('interactive', True)
        self.properties["background"]      = kwargs.get('background', True)
        self.properties["outline"]         = kwargs.get('outline', True)
        self.properties["outlineStyle"]    = kwargs.get('outlineStyle', OutlineStyle.CORNERS)
        self.properties["grabFocus"]       = kwargs.get('grabFocus', False)
        self.properties["pointerPriority"] = kwargs.get('pointerPriority', PointerPriority.OLDEST)
        self.properties["cornerRadius"]    = kwargs.get('cornerRadius', 1)
        self.properties["orientation"]     = kwargs.get('orientation', Orientation.NORTH)
        self.properties["script"]          = kwargs.get('script', '')

        self.values["touch"] = False

    def __getitem__(self, item):
        if item in self.properties:
            return self.properties[item]
        elif item in self.values:
            return self.values[item]
        else:
            raise KeyError(f"Unknown item '{item}'")

    def __setitem__(self, item, value):
        if item in self.properties:
            self.properties[item] = value
        elif item in self.values:
            self.values[item] = value
        else:
            raise KeyError(f"Unknown item '{item}'")
    

    def expand_children(self):
        for c in self.children:
            c.expand_children()


    def to_xml(self, parent):
        node = et.SubElement(parent, 'node', attrib={
            "ID": str(self.id),
            "type": self.type.value
        })

        self.properties.to_xml(node)
        self.values.to_xml(node)

        if len(self.messages) > 0:
            messages = et.SubElement(node, 'messages')
            for msg in self.messages:
                msg.to_xml(messages)
        
        if len(self.children) > 0:
            children = et.SubElement(node, 'children')
            for child in self.children:
                child.to_xml(children)

class Group(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.GROUP
        self.expand_myself = True
        kwargs["interactive"] = kwargs.get('interactive', False)
        kwargs["background"] = kwargs.get('background', False)
        kwargs["outline"]    = kwargs.get('outline', False)
        super().__init__(**kwargs)

    def expand_children(self):
        if self.expand_myself:
            self["frame"].expand(5, 5, 5, 5)
            for c in self.children:
                c["frame"].move(5, 5, relative=True)
                c.expand_children()
        else:
            super().expand_children()

class Box(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.BOX
        super().__init__(**kwargs)
        self.properties["shape"] = kwargs.get('shape', Shape.RECTANGLE)

class Button(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.BUTTON
        super().__init__(**kwargs)
        self.properties["shape"]         = kwargs.get('shape', Shape.RECTANGLE)
        self.properties["buttonType"]    = kwargs.get('buttonType', ButtonType.MOMENTARY)
        self.properties["press"]         = kwargs.get('press', True)
        self.properties["release"]       = kwargs.get('release', True)
        self.properties["valuePosition"] = kwargs.get('valuePosition', False)

        self.values["x"] = 0

class Label(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.LABEL
        kwargs["interactive"] = kwargs.get('interactive', False)
        super().__init__(**kwargs)
        self.properties["font"]       = kwargs.get('font', Font.DEFAULT)
        self.properties["textSize"]   = kwargs.get('textSize', 14)
        self.properties["textLength"] = kwargs.get('textLength', 0)
        self.properties["textAlignH"] = kwargs.get('textAlignH', AlignH.CENTER)
        self.properties["textAlignV"] = kwargs.get('textAlignV', AlignV.MIDDLE)
        self.properties["textColor"]  = kwargs.get('textColor', ColorEnum.WHITE)
        self.properties["textClip"]   = kwargs.get('textClip', True)

        self.values["text"] = "Label"

class Text(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.TEXT
        super().__init__(**kwargs)
        self.properties["font"]       = kwargs.get('font', Font.DEFAULT)
        self.properties["textSize"]   = kwargs.get('textSize', 14)
        self.properties["textAlignH"] = kwargs.get('textAlignH', AlignH.CENTER)
        self.properties["textColor"]  = kwargs.get('textColor', ColorEnum.WHITE)

        self.values["text"] = "Text"

class Fader(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.FADER
        super().__init__(**kwargs)
        self.properties["cursor"]         = kwargs.get('cursor', True)
        self.properties["cursorDisplay"]  = kwargs.get('cursorDisplay', CursorDisplay.ALWAYS)
        self.properties["bar"]            = kwargs.get('bar', True)
        self.properties["barDisplay"]     = kwargs.get('barDisplay', CursorDisplay.ALWAYS)
        self.properties["centered"]       = kwargs.get('centered', False)
        self.properties["response"]       = kwargs.get('response', Response.ABSOLUTE)
        self.properties["responseFactor"] = kwargs.get('responseFactor', 100)
        self.properties["grid"]           = kwargs.get('grid', True)
        self.properties["gridSteps"]      = kwargs.get('gridSteps', 20)

        self.values["x"] = 0

class XY(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.XY
        super().__init__(**kwargs)
        self.properties["cursor"]         = kwargs.get('cursor', True)
        self.properties["cursorDisplay"]  = kwargs.get('cursorDisplay', CursorDisplay.ALWAYS)
        self.properties["lines"]          = kwargs.get('lines', True)
        self.properties["linesDisplay"]   = kwargs.get('linesDisplay', CursorDisplay.ALWAYS)
        self.properties["lockX"]          = kwargs.get('lockX', False)
        self.properties["lockX"]          = kwargs.get('lockX', False)
        self.properties["response"]       = kwargs.get('response', Response.ABSOLUTE)
        self.properties["responseFactor"] = kwargs.get('responseFactor', 100)
        self.properties["gridX"]          = kwargs.get('gridX', True)
        self.properties["gridY"]          = kwargs.get('gridX', True)
        self.properties["gridStepsX"]     = kwargs.get('gridStepsX', 20)
        self.properties["gridStepsX"]     = kwargs.get('gridStepsY', 20)

        self.values["x"] = 0
        self.values["y"] = 0

class Radial(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.XY
        super().__init__(**kwargs)
        self.properties["inverted"]        = kwargs.get('inverted', False)
        self.properties["centered"]       = kwargs.get('centered', False)
        self.properties["response"]       = kwargs.get('response', Response.ABSOLUTE)
        self.properties["responseFactor"] = kwargs.get('responseFactor', 100)
        self.properties["grid"]           = kwargs.get('grid', True)
        self.properties["gridSteps"]      = kwargs.get('gridSteps', 20)

        self.values["x"] = 0

class Encoder(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.ENCODER
        super().__init__(**kwargs)
        self.properties["cursor"]         = kwargs.get('cursor', True)
        self.properties["cursorDisplay"]  = kwargs.get('cursorDisplay', CursorDisplay.ALWAYS)
        self.properties["response"]       = kwargs.get('response', Response.ABSOLUTE)
        self.properties["responseFactor"] = kwargs.get('responseFactor', 100)
        self.properties["grid"]           = kwargs.get('grid', True)
        self.properties["gridSteps"]      = kwargs.get('gridSteps', 20)

        self.values["x"] = 0
        self.values["y"] = 0

class Radar(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.RADAR
        super().__init__(**kwargs)
        self.properties["cursor"]         = kwargs.get('cursor', True)
        self.properties["cursorDisplay"]  = kwargs.get('cursorDisplay', CursorDisplay.ALWAYS)
        self.properties["lines"]          = kwargs.get('lines', True)
        self.properties["linesDisplay"]   = kwargs.get('linesDisplay', CursorDisplay.ALWAYS)
        self.properties["lockX"]          = kwargs.get('lockX', False)
        self.properties["lockX"]          = kwargs.get('lockX', False)
        self.properties["response"]       = kwargs.get('response', Response.ABSOLUTE)
        self.properties["responseFactor"] = kwargs.get('responseFactor', 100)
        self.properties["gridX"]          = kwargs.get('gridX', True)
        self.properties["gridY"]          = kwargs.get('gridX', True)
        self.properties["gridStepsX"]     = kwargs.get('gridStepsX', 20)
        self.properties["gridStepsX"]     = kwargs.get('gridStepsY', 20)

        self.values["x"] = 0
        self.values["y"] = 0

class Radio(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.RADIO
        super().__init__(**kwargs)
        self.properties["steps"]     = kwargs.get('gridStepsY', 5)
        self.properties["radioType"] = kwargs.get('radioType', RadioType.SELECT)

        self.values["x"] = 0

class Page(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.GROUP
        kwargs["outline"]    = kwargs.get('outline', False)
        super().__init__(**kwargs)
        self.properties["tabLabel"]     = kwargs.get('tabLabel', 'label')
        self.properties["tabColorOff"]  = kwargs.get('tabColorOff', Color("#1A1A1AFF"))
        self.properties["tabColorOn"]   = kwargs.get('tabColorOn', Color("#404040FF"))
        self.properties["textColorOff"] = kwargs.get('textColorOff', ColorEnum.WHITE)
        self.properties["textColorOn"]  = kwargs.get('textColorOn', ColorEnum.WHITE)


class Pager(Control):
    def __init__(self, **kwargs):
        self.type = ControlType.PAGER
        kwargs["background"] = kwargs.get('background', False)
        kwargs["outline"]    = kwargs.get('outline', False)
        super().__init__(**kwargs)
        self.properties["tabbar"]          = kwargs.get('tabbar', True)
        self.properties["tabbarSize"]      = kwargs.get('tabbarSize', 40)
        self.properties["tabbarDoubleTap"] = kwargs.get('tabbarDoubleTap', False)
        self.properties["tabLabels"]       = kwargs.get('tabLabels', True)
        self.properties["textSizeOff"]     = kwargs.get('textSizeOff', 14)
        self.properties["textSizeOn"]      = kwargs.get('textSizeOn', 14)

        self.values["x"] = 0