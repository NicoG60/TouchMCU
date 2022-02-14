import subprocess

from touchmcu.master import create_assignment, create_fader_banks, create_master_fader, create_timecode
from touchmcu.touchosc import Rect
from touchmcu.touchosc.controls import Pager, Page
from touchmcu.touchosc.document import Document
from touchmcu.touchosc.midi import MidiNotes

from touchmcu import load_all_scripts, load_overlay
from touchmcu.track import create_track



# ====== OVERLAY ===============================================================

overlay = load_overlay("default.yml")

# ====== DOCUMENT ==============================================================

doc = Document(1024, 768)

doc.root["script"] = load_all_scripts(
    "table_utils.lua",
    "lcd.lua"
)

pager = Pager(
    parent=doc.root,
    name="pager",
    frame=doc.root["frame"]
)

# ====== TRACKS ================================================================

track_page = Page(
    parent=pager,
    name="track_page",
    tabLabel="Tracks",
    frame=Rect(
        x=0,
        y=pager["tabbarSize"],
        w=pager["frame"]["w"],
        h=pager["frame"]["h"] - pager["tabbarSize"]
    )
)

for i in range(8):
    tr = create_track(track_page, overlay, i)
    tr["frame"].move(2+102*i, 0)

tc = create_timecode(track_page, overlay)
tc["frame"].move(820, 0)

assign = create_assignment(track_page, overlay)
assign["frame"].move(820, 106)

banks = create_fader_banks(track_page, overlay)
banks["frame"].move(820, 342)

master = create_master_fader(track_page)
master["frame"].move(922, 342)

# ====== TRANSPORT =============================================================

transport_page = Page(
    parent=pager,
    name="transport_page",
    tabLabel="Transport",
    frame=Rect(
        x=0,
        y=pager["tabbarSize"],
        w=pager["frame"]["w"],
        h=pager["frame"]["h"] - pager["tabbarSize"]
    )
)

doc.finalise()
doc.save_clear("./touchMCU.xml")
doc.save("./touchMCU.tosc")

subprocess.call(["open", "./touchMCU.tosc"])