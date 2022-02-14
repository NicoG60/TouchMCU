import lxml.etree as et

from touchmcu.touchosc import Bool, String, Integer
from touchmcu.touchosc.midi import MidiMessageType
from touchmcu.touchosc.values import MessageValues

class MidiMessage:

    def __init__(self):
        self.enabled = True
        self.send    = True
        self.receive = True
        self.triggers = {}
        self.type = MidiMessageType.CONTROL_CHANGE
        self.channel = 0
        self.data1 = 0
        self.data2 = 0
        self.values = MessageValues()

    def to_xml(self, parent):
        midi = et.SubElement(parent, 'midi')

        Bool(self.enabled).to_xml(et.SubElement(midi, 'enabled'))
        Bool(self.send).to_xml(et.SubElement(midi, 'send'))
        Bool(self.receive).to_xml(et.SubElement(midi, 'receive'))
        et.SubElement(midi, 'feedback').text = '0'
        et.SubElement(midi, 'connections').text = '00001'

        triggers = et.SubElement(midi, 'triggers')
        for k, v in self.triggers.items():
            trigger = et.SubElement(triggers, 'trigger')
            String(k).to_xml(et.SubElement(trigger, 'var'))
            et.SubElement(trigger, 'condition').text = v.value

        msg = et.SubElement(midi, 'message')
        et.SubElement(msg, 'type').text = self.type.value
        Integer(self.channel).to_xml(et.SubElement(msg, 'channel'))
        Integer(self.data1).to_xml(et.SubElement(msg, 'data1'))
        Integer(self.data2).to_xml(et.SubElement(msg, 'data2'))

        self.values.to_xml(midi)