import lxml.etree as et
from enum import Enum

from touchmcu.touchosc import *

class NodeValues(dict):

    def to_xml(self, parent):
        values = et.SubElement(parent, 'values')

        for k, v in self.items():
            value = et.SubElement(values, 'value')

            String(k).to_xml(et.SubElement(value, 'key'))
            et.SubElement(value, 'locked').text = '0'
            et.SubElement(value, 'lockedDefaultCurrent').text = '0'
            et.SubElement(value, 'defaultPull').text = '0'
            String(v).to_xml(et.SubElement(value, 'default'))

class MessageValues(list):
    class Type(Enum):
        CONSTANT = 'CONSTANT'
        INDEX = 'INDEX'
        VALUE = 'VALUE'

    def to_xml(self, parent):
        values = et.SubElement(parent, 'values')

        for obj in self:
            if not isinstance(obj, dict):
                continue

            value = et.SubElement(values, 'value')

            et.SubElement(value, 'type').text = obj.get('type', self.Type.CONSTANT).value
            String(obj.get('key', '')).to_xml(et.SubElement(value, 'key'))
            et.SubElement(value, 'scaleMin').text = str(obj.get('min', '0'))
            et.SubElement(value, 'scaleMax').text = str(obj.get('max', '1'))