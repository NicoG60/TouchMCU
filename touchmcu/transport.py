from touchmcu.controls import create_button, create_led_button, create_led, create_fader
from touchmcu.touchosc import ButtonType, Color, Font, OutlineStyle, ColorEnum, Rect
from touchmcu.touchosc.controls import Group, Label
from touchmcu.touchosc.midi import MidiNotes

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