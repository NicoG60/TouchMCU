from touchmcu import load_all_scripts
from touchmcu.midi import midi_timecode
from touchmcu.controls import create_button, create_led_button, create_led, create_fader
from touchmcu.touchosc import ButtonType, Color, Font, OutlineStyle, ColorEnum, Rect
from touchmcu.touchosc.controls import Group, Label
from touchmcu.touchosc.midi import MidiNotes


def create_timecode(parent, overlay):
    root = Group(
        parent=parent,
        name="timecode"
    )
    root["frame"].resize(202, 84)

    tc = Label(
        parent=root,
        name="lb_timecode",
        color=ColorEnum.RED,
        frame=Rect(x=0, y=2, w=202, h=60),
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
        frame=Rect(x=0, y=64, w=45, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_smpte["text"] = overlay["smpte"]
    create_led(root, "led_smpte", frame=Rect(x=45, y=67, w=14, h=14), note=MidiNotes.F_8)

    lb_beats = Label(
        parent=root,
        name="lb_beats",
        frame=Rect(x=59, y=64, w=45, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_beats["text"] = overlay["beats"]
    create_led(root, "led_beats", frame=Rect(x=104, y=67, w=14, h=14), note=MidiNotes.FSharp_8)

    lb_rude = Label(
        parent=root,
        name="lb_rude",
        frame=Rect(x=118, y=64, w=70, h=20),
        textSize=11,
        outline=False,
        background=False,
    )
    lb_rude["text"] = overlay["rude_solo"]
    create_led(root, "led_rude", frame=Rect(x=188, y=67, w=14, h=14), note=MidiNotes.G_8)

    return root


def create_assignment(parent, overlay):
    root = Group(
        parent=parent,
        name="assignment"
    )
    root["frame"].resize(202, 220)

    lb_assign = Label(
        parent=root,
        name="lb_assign",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=100, h=20)
    )
    lb_assign["text"] = overlay["vpot_assignment"]

    create_led_button(
        root,
        "track",
        label1=overlay["track"],
        frame=Rect(x=0, y=40, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.E_2
    )

    create_led_button(
        root,
        "send",
        label1=overlay["send"],
        frame=Rect(x=54, y=40, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.F_2
    )

    create_led_button(
        root,
        "pan",
        label1=overlay["pan"],
        frame=Rect(x=0, y=90, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.FSharp_2
    )

    create_led_button(
        root,
        "plugin",
        label1=overlay["plugin"],
        frame=Rect(x=54, y=90, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.G_2
    )

    create_led_button(
        root,
        "eq",
        label1=overlay["eq"],
        frame=Rect(x=0, y=140, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.GSharp_2
    )

    create_led_button(
        root,
        "instr",
        label1=overlay["instruments"],
        frame=Rect(x=54, y=140, w=46, h=36),
        color=ColorEnum.GREEN,
        note=MidiNotes.A_2
    )

    # ==========================================================================

    lb_display = Label(
        parent=root,
        name="lb_display",
        color=ColorEnum.GREY,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=102, y=0, w=100, h=20)
    )
    lb_display["text"] = overlay["display"]

    create_button(
        root,
        "name",
        label1=overlay["name_value1"],
        label2=overlay["name_value2"],
        frame=Rect(x=102, y=40, w=46, h=36),
        note=MidiNotes.E_3,
        type=ButtonType.MOMENTARY
    )

    create_button(
        root,
        "smpte",
        label1=overlay["smpte_beats1"],
        label2=overlay["smpte_beats2"],
        frame=Rect(x=156, y=40, w=46, h=36),
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
        frame=Rect(x=102, y=94, w=100, h=20)
    )
    lb_assign_lcd["text"] = "Assignment"

    assign_lcd = Label(
        parent=root,
        name="assign_lcd",
        color=ColorEnum.RED,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=102, y=116, w=100, h=60),
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


def create_fader_banks(parent, overlay):
    root = Group(
        parent=parent,
        name="fader_banks"
    )
    root["frame"].resize(100, 220)

    lb_bank = Label(
        parent=root,
        name="lb_bank",
        color=ColorEnum.GREY.value,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=100, h=20)
    )
    lb_bank["text"] = overlay["fader_banks"]

    create_button(
        root,
        "bank_left",
        label=overlay["bank_left"],
        frame=Rect(x=0, y=40, w=46, h=36),
        type=ButtonType.MOMENTARY,
        note=MidiNotes.ASharp_2
    )

    create_button(
        root,
        "bank_right",
        label=overlay["bank_right"],
        frame=Rect(x=54, y=40, w=46, h=36),
        type=ButtonType.MOMENTARY,
        note=MidiNotes.B_2
    )

    create_button(
        root,
        "channel_left",
        label=overlay["channel_left"],
        frame=Rect(x=0, y=90, w=46, h=36),
        type=ButtonType.MOMENTARY,
        note=MidiNotes.C_3
    )

    create_button(
        root,
        "channel_right",
        label=overlay["channel_right"],
        frame=Rect(x=54, y=90, w=46, h=36),
        type=ButtonType.MOMENTARY,
        note=MidiNotes.CSharp_3
    )

    create_led_button(
        root,
        "flip",
        label1=overlay["flip"],
        color=ColorEnum.RED,
        frame=Rect(x=0, y=140, w=46, h=36),
        note=MidiNotes.D_3
    )

    create_led_button(
        root,
        "global",
        label1=overlay["global_view"],
        color=ColorEnum.GREEN,
        frame=Rect(x=54, y=140, w=46, h=36),
        note=MidiNotes.DSharp_3
    )

    return root

def create_master_fader(parent):
    root = Group(
        parent=parent,
        name="master"
    )
    root["frame"].resize(100, 372)

    lb_bank = Label(
        parent=root,
        name="lb_master",
        color=ColorEnum.RED,
        outline=True,
        outlineStyle=OutlineStyle.EDGES,
        frame=Rect(x=0, y=0, w=100, h=20)
    )
    lb_bank["text"] = "Master"

    create_fader(
        root,
        "master_fader",
        frame=Rect(x=20, y=22, w=60, h=350),
        color=ColorEnum.RED,
        note=MidiNotes.E_8,
        ch=8
    )

    return root