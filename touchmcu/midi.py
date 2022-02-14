from touchmcu.touchosc import Condition
from touchmcu.touchosc.midi import MidiMessageType
from touchmcu.touchosc.values import MessageValues
from touchmcu.touchosc.messages import MidiMessage

def midi_note_bang(note, send=True, receive=True):

    result = []

    if send:
        pressed = MidiMessage()
        pressed.receive = False
        pressed.triggers["touch"] = Condition.ANY
        pressed.type = MidiMessageType.NOTE_ON
        pressed.data1 = note
        pressed.data2 = 127
        pressed.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed.values.append({
            "type": MessageValues.Type.VALUE,
            "key": "touch",
            "min": 0,
            "max": 127
        })

        pressed_off = MidiMessage()
        pressed_off.receive = False
        pressed_off.triggers["touch"] = Condition.ANY
        pressed_off.type = MidiMessageType.NOTE_OFF
        pressed_off.data1 = note
        pressed_off.data2 = 0
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": "",
        })

        result += [pressed, pressed_off]

    if receive:
        update = MidiMessage()
        update.send = False
        update.triggers["x"] = Condition.ANY
        update.type = MidiMessageType.NOTE_ON
        update.data1 = note
        update.data2 = 127
        update.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        update.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        update.values.append({
            "type": MessageValues.Type.VALUE,
            "key": "x",
            "min": 0,
            "max": 127
        })

        result.append(update)

    return result

def midi_encoder(cc):
    enc = MidiMessage()
    enc.send = True
    enc.receive = False
    enc.triggers["x"] = Condition.ANY
    enc.type = MidiMessageType.CONTROL_CHANGE
    enc.data1 = cc
    enc.data2 = 0
    enc.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })
    enc.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })
    enc.values.append({
        "type": MessageValues.Type.VALUE,
        "key": "y",
        "min": 65,
        "max": 1
    })

    return [enc]

def midi_led_ring(cc):

    lr = MidiMessage()
    lr.send = False
    lr.receive = True
    lr.triggers["x"] = Condition.ANY
    lr.type = MidiMessageType.CONTROL_CHANGE
    lr.data1 = cc
    lr.data2 = 0
    lr.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })
    lr.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })
    lr.values.append({
        "type": MessageValues.Type.VALUE,
        "key": "touch",
        "min": 0,
        "max": 1
    })

    return [lr]

def midi_fader(note, ch, send=True, receive=True):

    result = []

    if send:
        pressed = MidiMessage()
        pressed.receive = False
        pressed.triggers["touch"] = Condition.ANY
        pressed.type = MidiMessageType.NOTE_ON
        pressed.data1 = note
        pressed.data2 = 127
        pressed.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed.values.append({
            "type": MessageValues.Type.VALUE,
            "key": "touch",
            "min": 0,
            "max": 127
        })

        pressed_off = MidiMessage()
        pressed_off.receive = False
        pressed_off.triggers["touch"] = Condition.ANY
        pressed_off.type = MidiMessageType.NOTE_OFF
        pressed_off.data1 = note
        pressed_off.data2 = 0
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        pressed_off.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": "",
        })

        result += [pressed, pressed_off]

    if receive:
        move = MidiMessage()
        move.triggers["x"] = Condition.ANY
        move.type = MidiMessageType.PITCH_BEND
        move.channel = ch
        move.data1 = 0
        move.data2 = 0
        move.values.append({
            "type": MessageValues.Type.CONSTANT,
            "key": ""
        })
        move.values.append({
            "type": MessageValues.Type.VALUE,
            "key": "x",
            "min": 0,
            "max": 16383
        })

        result.append(move)

    return result

def midi_vu(ch):

    vu = MidiMessage()
    vu.send = False
    vu.receive = True
    vu.triggers["x"] = Condition.ANY
    vu.type = MidiMessageType.CHANNEL_PRESSURE
    vu.channel = ch
    vu.data1 = 0
    vu.data2 = 0
    vu.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })
    vu.values.append({
        "type": MessageValues.Type.VALUE,
        "key": "touch",
        "min": 0,
        "max": 1
    })
    vu.values.append({
        "type": MessageValues.Type.CONSTANT,
        "key": ""
    })

    return [vu]

