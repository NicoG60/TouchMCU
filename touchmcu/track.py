from touchmcu import load_all_scripts
from touchmcu.controls import *
from touchmcu.midi import midi_led_ring, midi_vu
from touchmcu.touchosc import Color, ColorEnum, OutlineStyle, Font
from touchmcu.touchosc.controls import Group, Label, Text
from touchmcu.touchosc.midi import MidiNotes


def create_track_lcd(parent, trackid):
    lcd = Text(
        parent=parent,
        name="lcd",
        tag=str(trackid),
        font=Font.MONOSPACE,
        textSize=22,
        color=ColorEnum.BLUE.value,
        textColor=ColorEnum.BLUE.value,
        outline=True,
        outlineStyle=OutlineStyle.EDGES
    )
    lcd["frame"].resize(100, 60)
    lcd["text"] = ""
    return lcd


def create_vpot(parent, trackid):
    root = Group(
        parent=parent,
        name="vpot"
    )
    root["frame"].resize(100, 100)

    enc = create_encoder(root, "pot", cc=16+trackid)

    btn_frame = Rect(w=30, h=30)
    btn_frame.move_center(*root["frame"].center())
    btn = create_button(root, "pot_select", note=MidiNotes.GSharp_1+trackid, frame=btn_frame, type=ButtonType.MOMENTARY)
    btn["shape"] = Shape.CIRCLE


    ring = Group(
        parent=root,
        name="let_ring"
    )
    ring["frame"].resize(100, 100)
    ring.messages.extend(midi_led_ring(48+trackid))
    ring["script"] = load_all_scripts(
        "bit_utils.lua",
        "led_utils.lua",
        "led_ring.lua"
    )


    xc, yc = ring["frame"].center()
    angle = 210
    step = 24
    for i in range(11):
        led = create_led(ring, f"led{i+1}")
        led["background"] = False
        led["frame"].move_center_polar(xc, yc, 40, angle)
        angle-=step

    ledc_frame=Rect(x=0, y=0, w=14, h=14)
    ledc_frame.move_center(xc, yc+40)
    ledc = create_led(ring, f"led_c", frame=ledc_frame)
    ledc["background"] = False

    return root



def create_vu(parent, trackid):
    root = Group(
        parent=parent,
        name="vu"
    )
    root["frame"].resize(14, 12*14)


    root.messages.extend(midi_vu())


    # This is a lua header that declare on which track the vu meter is
    header=f"""
--------------------------------------------------------------------------------
-- Change that variable to match the track index (0-7 for track 1-8)
local track = {trackid}
--------------------------------------------------------------------------------

"""

    root["script"] = header + load_all_scripts(
        "bit_utils.lua",
        "led_utils.lua",
        "vu.lua"
    )


    for i in range(12):
        if i == 11:
            color = ColorEnum.RED
        elif i >= 8:
            color = ColorEnum.ORANGE
        else:
            color = ColorEnum.GREEN

        led_frame = Rect(x=0, y=14*(11-i), w=14, h=14)
        create_led(root, f"led{i+1}", frame=led_frame, color=color)

    return root




def create_track(parent, overlay, trackid):
    root = Group(
        parent=parent,
        name=f"track_{trackid+1}"
    )
    root["frame"].resize(100, 714)

    lcd = create_track_lcd(root, trackid)
    lcd["frame"].move(0, 2)

    vpot = create_vpot(root, trackid)
    vpot["frame"].move(0, 64)

    btn_rec = create_button(
        root,
        "rec",
        label=overlay["rec"],
        frame=Rect(x=27, y=176, w=46, h=46),
        color=ColorEnum.RED,
        note=(MidiNotes.C_m1 + trackid)
    )
    btn_rec["outline"] = True

    create_button(
        root,
        "solo",
        label=overlay["solo"],
        frame=Rect(x=15, y=234, w=70, h=34),
        color=ColorEnum.ORANGE,
        note=(MidiNotes.GSharp_m1 + trackid)
    )

    create_button(
        root,
        "mute",
        label=overlay["mute"],
        frame=Rect(x=15, y=270, w=70, h=34),
        color=ColorEnum.RED,
        note=(MidiNotes.E_0 + trackid)
    )

    create_button(
        root,
        "sel",
        label=overlay["sel"],
        frame=Rect(x=15, y=306, w=70, h=34),
        color=ColorEnum.BLUE,
        note=(MidiNotes.C_1 + trackid)
    )

    lb_track = Label(
        parent=root,
        name="lb_track",
        color=ColorEnum.GREY.value,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=342, w=100, h=20)
    )
    lb_track["text"] = str(trackid+1)

    create_fader(
        root,
        "fader",
        frame=Rect(x=20, y=364, w=60, h=350),
        note=MidiNotes.GSharp_7+trackid,
        ch=trackid
    )

    vu = create_vu(root, trackid)
    vu["frame"].move_left(82)
    vu["frame"].move_bottom(714)

    return root