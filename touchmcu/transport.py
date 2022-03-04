from touchmcu.controls import create_button, create_encoder, create_led_button, create_led, create_fader
from touchmcu.touchosc import ButtonType, Color, Font, OutlineStyle, ColorEnum, Rect
from touchmcu.touchosc.controls import Group, Label
from touchmcu.touchosc.midi import MidiNotes
from touchmcu import load_all_scripts
from touchmcu.midi import midi_timecode

def create_global_view(parent, overlay):
    root = Group(
        parent=parent,
        name="global_view"
    )
    root["frame"].resize(660, 80)

    label = Label(
        parent=root,
        name="lb_global_view",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=660, h=20)
    )
    label["text"] = overlay["global_view_header"]

    keys=["midi_tracks", "inputs", "audio_tracks", "audio_instrument", "aux", "busses", "outputs", "user"]

    for i in range(len(keys)):
        create_button(
            parent=root,
            name=keys[i],
            note=MidiNotes.D_4 + i,
            frame=Rect(x=20+i*80, y=40, w=60, h=40),
            label=overlay[keys[i]],
            type=ButtonType.MOMENTARY
        )

    return root



def create_function_select(parent, overlay):
    root = Group(
        parent=parent,
        name="functions"
    )
    root["frame"].resize(660, 80)

    label = Label(
        parent=root,
        name="lb_function",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=660, h=20)
    )
    label["text"] = overlay["function_select"]

    for i in range(8):
        k = f"f{i + 1}"
        create_button(
            parent=root,
            name=k,
            note=MidiNotes.FSharp_3 + i,
            frame=Rect(x=20+i*80, y=40, w=60, h=40),
            label=overlay[k],
            type=ButtonType.MOMENTARY
        )

    return root


def create_modifiers(parent, overlay):
    root = Group(
        parent=parent,
        name="modifiers"
    )
    root["frame"].resize(180, 160)

    label = Label(
        parent=root,
        name="lb_modifier",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=180, h=20)
    )
    label["text"] = overlay["modifiers"]

    keys=["shift", "option", "control", "alt"]

    for i in range(4):
        if i < 2:
            x = 20+i*80
            y = 40
        else:
            x = 20+(i-2)*80
            y = 100
        create_button(
            parent=root,
            name=keys[i],
            note=MidiNotes.ASharp_4 + i,
            frame=Rect(x=x, y=y, w=60, h=40),
            label=overlay[keys[i]],
            type=ButtonType.MOMENTARY
        )

    return root


def create_utilities(parent, overlay):
    root = Group(
        parent=parent,
        name="utilities"
    )
    root["frame"].resize(180, 160)

    label = Label(
        parent=root,
        name="lb_utilities",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=180, h=20)
    )
    label["text"] = overlay["utilities"]


    create_led_button(
        parent=root,
        name="save",
        note=MidiNotes.GSharp_5,
        frame=Rect(x=20, y=40, w=60, h=40),
        label1=overlay["save"],
        color=ColorEnum.RED
    )

    create_led_button(
        parent=root,
        name="undo",
        note=MidiNotes.A_5,
        frame=Rect(x=100, y=40, w=60, h=40),
        label1=overlay["undo"],
        color=ColorEnum.GREEN
    )


    create_button(
        parent=root,
        name="cancel",
        note=MidiNotes.ASharp_5,
        frame=Rect(x=20, y=100, w=60, h=40),
        label=overlay["cancel"],
        type=ButtonType.MOMENTARY
    )

    create_button(
        parent=root,
        name="enter",
        note=MidiNotes.B_5,
        frame=Rect(x=100, y=100, w=60, h=40),
        label=overlay["enter"],
        type=ButtonType.MOMENTARY
    )

    return root


def create_automation(parent, overlay):
    root = Group(
        parent=parent,
        name="automation"
    )
    root["frame"].resize(260, 160)

    label = Label(
        parent=root,
        name="lb_automation",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=260, h=20)
    )
    label["text"] = overlay["automation"]

    keys=["read_off", "write", "trim", "touch", "latch", "group"]
    colors=[ColorEnum.GREEN, ColorEnum.RED, ColorEnum.RED, ColorEnum.RED, ColorEnum.RED, ColorEnum.GREEN]

    for i in range(6):
        if i < 3:
            x = 20+i*80
            y = 40
        else:
            x = 20+(i-3)*80
            y = 100
        create_led_button(
            parent=root,
            name=keys[i],
            note=MidiNotes.D_5 + i,
            frame=Rect(x=x, y=y, w=60, h=40),
            label1=overlay[keys[i]],
            color=colors[i]
        )

    return root


def create_transport(parent, overlay):
    root = Group(
        parent=parent,
        name="transport"
    )
    root["frame"].resize(660, 250)

    label = Label(
        parent=root,
        name="lb_transport",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=660, h=20)
    )
    label["text"] = overlay["transport"]

    for i, k in enumerate(["markers", "nudge"]):
        create_led_button(
            parent=root,
            name=k,
            note=MidiNotes.C_6 + i,
            frame=Rect(x=20+i*80, y=40, w=60, h=40),
            label1=overlay[k],
            color=ColorEnum.GREEN
        )

    for i, k in enumerate(["cycle", "drop", "replace"]):
        create_led_button(
            parent=root,
            name=k,
            note=MidiNotes.D_6 + i,
            frame=Rect(x=220+i*80, y=40, w=60, h=40),
            label1=overlay[k],
            color=ColorEnum.GREEN if i == 0 else ColorEnum.RED
        )

    for i, k in enumerate(["click", "tr_solo"]):
        create_led_button(
            parent=root,
            name=k,
            note=MidiNotes.F_6 + i,
            frame=Rect(x=500+i*80, y=40, w=60, h=40),
            label1=overlay[k],
            color=ColorEnum.GREEN if i == 0 else ColorEnum.RED
        )

    create_button(
        root,
        "rewind",
        label=overlay["rewind"],
        frame=Rect(x=20, y=154, w=100, h=80),
        color=ColorEnum.GREY,
        note=MidiNotes.G_6,
        textSize=36
    )

    create_button(
        root,
        "forward",
        label=overlay["forward"],
        frame=Rect(x=140, y=154, w=100, h=80),
        color=ColorEnum.GREY,
        note=MidiNotes.GSharp_6,
        textSize=36
    )

    create_button(
        root,
        "stop",
        label=overlay["stop"],
        
        frame=Rect(x=260, y=154, w=100, h=80),
        color=ColorEnum.ORANGE,
        note=MidiNotes.A_6,
        textSize=36
    )

    create_button(
        root,
        "play",
        label=overlay["play"],
        frame=Rect(x=380, y=154, w=100, h=80),
        color=ColorEnum.GREEN,
        note=MidiNotes.ASharp_6,
        textSize=36
    )

    create_button(
        root,
        "record",
        label=overlay["record"],
        frame=Rect(x=540, y=154, w=100, h=80),
        color=ColorEnum.RED,
        note=MidiNotes.B_6,
        textSize=36
    )

    return root




def create_transport_timecode(parent, overlay):
    root = Group(
        parent=parent,
        name="timecode"
    )
    root["frame"].resize(340, 80)

    label = Label(
        parent=root,
        name="lb_timecode",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=340, h=20)
    )
    label["text"] = overlay["timecode"]

    tc = Label(
        parent=root,
        name="lb_timecode",
        color=ColorEnum.RED,
        frame=Rect(x=140, y=22, w=200, h=58),
        font=Font.MONOSPACE,
        textSize=24,
        textLength=19,
        textColor=ColorEnum.RED,
        outlineStyle=OutlineStyle.EDGES
    )
    tc["text"] = "000.00.00.000"
    tc.messages.extend(midi_timecode())

    header="""
--------------------------------------------------------------------------------
-- Change that to match the range of CC to listen to
local start=0x40
local stop =0x49
--------------------------------------------------------------------------------

"""
    tc["script"] = header + load_all_scripts(
        "bit_utils.lua",
        "timecode.lua"
    )

    lb_smpte = Label(
        parent=root,
        name="lb_smpte",
        frame=Rect(x=0, y=20, w=120, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_smpte["text"] = overlay["smpte"]
    create_led(root, "led_smpte", frame=Rect(x=120, y=23, w=14, h=14), note=MidiNotes.F_8)

    lb_beats = Label(
        parent=root,
        name="lb_beats",
        frame=Rect(x=0, y=40, w=120, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_beats["text"] = overlay["beats"]
    create_led(root, "led_beats", frame=Rect(x=120, y=43, w=14, h=14), note=MidiNotes.FSharp_8)

    lb_rude = Label(
        parent=root,
        name="lb_rude",
        frame=Rect(x=0, y=60, w=120, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_rude["text"] = overlay["rude_solo"]
    create_led(root, "led_rude", frame=Rect(x=120, y=63, w=14, h=14), note=MidiNotes.G_8)

    return root





def create_transport_assignment(parent, overlay):
    root = Group(
        parent=parent,
        name="assignment"
    )
    root["frame"].resize(340, 80)

    lb_display = Label(
        parent=root,
        name="lb_display",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=180, h=20)
    )
    lb_display["text"] = overlay["display"]

    create_button(
        root,
        "name",
        label1=overlay["name_value1"],
        label2=overlay["name_value2"],
        frame=Rect(x=20, y=40, w=60, h=40),
        note=MidiNotes.E_3,
        type=ButtonType.MOMENTARY
    )

    create_button(
        root,
        "smpte",
        label1=overlay["smpte_beats1"],
        label2=overlay["smpte_beats2"],
        frame=Rect(x=100, y=40, w=60, h=40),
        note=MidiNotes.F_3,
        type=ButtonType.MOMENTARY
    )

    # ==========================================================================

    lb_assign_lcd = Label(
        parent=root,
        name="lb_assign_lcd",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=238, y=0, w=100, h=20)
    )
    lb_assign_lcd["text"] = "Assignment"

    assign_lcd = Label(
        parent=root,
        name="assign_lcd",
        color=ColorEnum.RED,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=238, y=22, w=100, h=58),
        font=Font.MONOSPACE,
        textSize=45,
        textColor=ColorEnum.RED.value,
    )
    assign_lcd["text"] = ""
    assign_lcd.messages.extend(midi_timecode(start=0x4A, end=0x4B))

    header="""
--------------------------------------------------------------------------------
-- Change that to match the range of CC to listen to
local start=0x4A
local stop =0x4B
--------------------------------------------------------------------------------

"""
    assign_lcd["script"] = header + load_all_scripts(
        "bit_utils.lua",
        "timecode.lua"
    )

    return root


def create_jog(parent, overlay):
    root = Group(
        parent=parent,
        name="jogs"
    )
    root["frame"].resize(340, 500)
    xc, xy = root["frame"].center()

    create_button(
        root,
        "up",
        label=overlay["up"],
        frame=Rect(x=xc-30, y=0, w=60, h=40),
        note=MidiNotes.C_7,
        type=ButtonType.MOMENTARY
    )

    create_button(
        root,
        "left",
        label=overlay["left"],
        frame=Rect(x=xc-110, y=60, w=60, h=40),
        note=MidiNotes.E_7,
        type=ButtonType.MOMENTARY
    )

    create_led_button(
        root,
        "zoom",
        label1=overlay["zoom"],
        frame=Rect(x=xc-30, y=60, w=60, h=40),
        note=MidiNotes.DSharp_7
    )

    create_button(
        root,
        "right",
        label=overlay["right"],
        frame=Rect(x=xc+50, y=60, w=60, h=40),
        note=MidiNotes.F_7,
        type=ButtonType.MOMENTARY
    )

    create_button(
        root,
        "down",
        label=overlay["down"],
        frame=Rect(x=xc-30, y=120, w=60, h=40),
        note=MidiNotes.CSharp_7,
        type=ButtonType.MOMENTARY
    )

    create_encoder(
        root,
        "jog",
        frame=Rect(x=xc - (264/2), y=200, w=264, h=264),
        cc=60
    )

    r = Rect(x=0, y=200, w=60, h=40)
    r.move_right(root["frame"].right())
    s = create_led_button(
        root,
        "scrub",
        label1=overlay["scrub"],
        frame=r,
        note=MidiNotes.D_7
    )
    

    return root