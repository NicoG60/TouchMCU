import lxml.etree as et
import numbers

from touchmcu.touchosc import *

class Properties(dict):

    def get_prop(self, value):
        if isinstance(value, bool):
            return ('b', Bool(value))
        elif isinstance(value, numbers.Integral):
            return ('i', Integer(value))
        elif isinstance(value, float):
            return ('f', Float(value))
        elif isinstance(value, str):
            return ('s', String(value))
        elif isinstance(value, Rect):
            return ('r', value)
        elif isinstance(value, Color):
            return ('c', value)
        elif isinstance(value, ColorEnum):
            return ('c', value.value)
        else:
            raise ValueError(f"Unknown type '{type(value)}'")

    def to_xml(self, parent):
        props = et.SubElement(parent, 'properties')

        for k, v in self.items():
            type, obj = self.get_prop(v)
            prop = et.SubElement(props, 'property', type=type)

            key = et.SubElement(prop, 'key')
            String(k).to_xml(key)

            value = et.SubElement(prop, 'value')
            obj.to_xml(value)