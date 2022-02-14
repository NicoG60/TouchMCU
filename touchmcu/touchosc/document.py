import lxml.etree as et
import io
import zlib

from touchmcu.touchosc.controls import Group

class Document:

    def __init__(self, w, h):
        self.root = Group(name="root")
        self.root.expand_myself = False
        self.root["frame"].resize(w, h)

    def finalise(self):
        self.root.expand_children()

    def to_xml(self):
        xml_root = et.Element('lexml', attrib={"version":"3"})
        self.root.to_xml(xml_root)
        return xml_root

    def save_clear(self, path):
        tree = et.ElementTree(self.to_xml())
        tree.write(path, encoding='utf-8', xml_declaration=True)

    def save(self, path):
        with io.BytesIO() as buf:
            tree = et.ElementTree(self.to_xml())
            tree.write(buf, encoding='utf-8', xml_declaration=True)

            data = zlib.compress(buf.getvalue())

            with open(path, 'bw+') as fp:
                fp.write(data)
