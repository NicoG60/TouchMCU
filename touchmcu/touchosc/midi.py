from enum import Enum, IntEnum

class MidiMessageType(Enum):
    CONTROL_CHANGE = 'CONTROLCHANGE'
    NOTE_ON = 'NOTE_ON'
    NOTE_OFF = 'NOTE_OFF'
    CHANNEL_PRESSURE = 'CHANNELPRESSURE'
    PITCH_BEND = 'PITCHBEND'
    POLY_PRESSURE = 'POLYPRESSURE'
    PROGRAM_CHANGE = 'PROGRAMCHANGE'
    SYSTEM_EXCLUSIVE = 'SYSTEMEXCLUSIVE'

def generate_midi_notes():
    notes = {}
    for oct in range(-1, 9):
        base = (oct+1) * 12

        suffix = f"_{oct}".replace('-', 'm')

        notes["C" + suffix]      = base + 0
        notes["CSharp" + suffix] = base + 1
        notes["DFlat" + suffix]  = base + 1
        notes["D" + suffix]      = base + 2
        notes["DSharp" + suffix] = base + 3
        notes["EFlat" + suffix]  = base + 3
        notes["E" + suffix]      = base + 4
        notes["F" + suffix]      = base + 5
        notes["FSharp" + suffix] = base + 6
        notes["GFlat" + suffix]  = base + 6
        notes["G" + suffix]      = base + 7
        notes["GSharp" + suffix] = base + 8
        notes["AFlat" + suffix]  = base + 8
        notes["A" + suffix]      = base + 9
        notes["ASharp" + suffix] = base + 10
        notes["BFlat" + suffix]  = base + 10
        notes["B" + suffix]      = base + 11

    return notes

MidiNotes = IntEnum('MidiNotes', generate_midi_notes(), module=__name__)
