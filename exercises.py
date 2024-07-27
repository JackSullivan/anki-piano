import abjad


major_triad = "M3 m3"

def make_figure(tonic, intervals):
    intervals = [abjad.NamedInterval(i) for i in intervals.split()]
    pitch = abjad.NamedPitch(tonic)

    pitches = []
    pitches.append(pitch)
    for interval in intervals:
        pitch = pitch + interval
        pitches.append(pitch)
    return pitches

notes = [abjad.Note(n, (1,4)) for n in make_figure("c'", major_triad)]

v = abjad.Voice(notes, name="Example Voice")

s = abjad.Staff([v], name = "Example Staff")

ks = abjad.KeySignature(abjad.NamedPitchClass("c"), abjad.Mode("major"))
abjad.attach(ks, abjad.select.note(s, 0))

print(s)
abjad.LilyPondFile([s], "test2.ly")