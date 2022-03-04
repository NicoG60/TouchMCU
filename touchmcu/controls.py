import copy
from touchmcu.midi import midi_encoder, midi_fader, midi_note_bang

from touchmcu.touchosc import ButtonType, CursorDisplay, Shape, Rect, Color, ColorEnum
from touchmcu.touchosc.controls import Button, Encoder, Fader, Label


def create_led(parent, name, note=None, frame=Rect(x=0, y=0, w=16, h=16), color=ColorEnum.RED):
    btn = Button(
        parent=parent,
        name=name,
        frame=frame,
        color=color,
        shape=Shape.CIRCLE,
        outline=False,
        buttonType=ButtonType.TOGGLE_PRESS,
        interactive=False
    )
    
    if note is not None:
        btn.messages.extend(midi_note_bang(note, send=False))

    return btn

def create_button(parent,
                         name,
                         note,
                         frame=Rect(x=0, y=0, w=46, h=46),
                         color=ColorEnum.GREY,
                         labelColor=ColorEnum.WHITE,
                         type=ButtonType.TOGGLE_PRESS,
                         label=None,
                         label1=None,
                         label2=None,
                         textSize=14,
                         textSize2=12):

    btn = Button(
        parent=parent,
        name=name,
        frame=frame,
        color=color,
        outline=False,
        buttonType=type
    )

    btn.messages.extend(midi_note_bang(note, send=True, receive=(type==ButtonType.TOGGLE_PRESS)))

    if label is not None:
        lb = Label(
            parent=parent,
            name=f"lb_{name}",
            frame=frame,
            outline=False,
            background=False,
            textSize=textSize,
            textColor=labelColor
        )
        lb["text"] = label

    if label1 is not None:
        lb1_frame = copy.deepcopy(frame)
        lb1_frame.resize(frame["w"], frame["h"]/2)
        lb1 = Label(
            parent=parent,
            name=f"lb1_{name}",
            frame=lb1_frame,
            outline=False,
            background=False,
            textSize=textSize2,
            textColor=labelColor
        )
        lb1["text"] = label1

    if label2 is not None:
        lb2_frame = copy.deepcopy(frame)
        lb2_frame.resize(frame["w"], frame["h"]/2)
        lb2_frame.move(0, frame["h"]/2, relative=True)

        lb2 = Label(
            parent=parent,
            name=f"lb2_{name}",
            frame=lb2_frame,
            outline=False,
            background=False,
            textSize=textSize2,
            textColor=labelColor
        )
        lb2["text"] = label2

    return btn

def create_led_button(parent,
                      name,
                      note,
                      frame=Rect(x=0, y=0, w=46, h=46),
                      led_frame=None,
                      color=ColorEnum.RED,
                      btn_color=ColorEnum.GREY,
                      label=None,
                      label1=None,
                      label2=None):

    btn = create_button(
        parent=parent,
        name=f"btn_{name}",
        note=note,
        frame=frame,
        color=btn_color,
        type=ButtonType.MOMENTARY,
        label=label,
        label1=label1,
        label2=label2
    )

    if led_frame is None:
        led_frame = Rect(x=0, y=0, w=14, h=14)
        led_frame.move_center(*frame.center())
        led_frame.move_bottom(frame.bottom()-2)

    led = create_led(
        parent=parent,
        name=f"led_{name}",
        note=note,
        frame=led_frame,
        color=color
    )

    return btn, led


def create_encoder(parent, name, frame=Rect(x=0, y=0, w=100, h=100), color=ColorEnum.GREY, cc=None):
    enc = Encoder(
        parent=parent,
        name=name,
        frame=frame,
        color=color.value if isinstance(color, ColorEnum) else color,
        cursorDisplay=CursorDisplay.ACTIVE,
        grid=False
    )

    if cc is not None:
        enc.messages.extend(midi_encoder(cc))

    return enc


def create_fader(parent, name, frame=Rect(x=0, y=0, w=60, h=350), color=ColorEnum.GREY, note=None, ch=None):
    fd = Fader(
        parent=parent,
        name=name,
        frame=frame,
        color=color.value if isinstance(color, ColorEnum) else color,
        grid=False,
        outline=False
    )

    if note is not None and ch is not None:
        fd.messages.extend(midi_fader(note, ch))

    return fd