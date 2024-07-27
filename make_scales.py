from musthe import *

from tempfile import NamedTemporaryFile
import subprocess


lilypond = '/Users/johsulli/Downloads/lilypond-2.24.0/bin/lilypond'

def comp_note(n):
    return n.to_octave(0)

def enharmonic(s1, s2):
    return set(map(comp_note, s1.notes)) == set(map(comp_note, s2.notes))

def scale_to_lilypond(s):
    n = s.root.lilypond_notation()
    m = 'minor' if 'minor' in s.name else s.name
    paper_size = '''
    #(set! paper-alist 
      (cons '("flashcard" . (cons (* 5 cm) (* 3 cm))) paper-alist))
    \paper { #(set-paper-size "flashcard") }
    '''
    return paper_size + '\\version "2.24.0" \\relative { \\key ' + n + " \\" + m + " c'4 }"

def lilypond_chord(c):
    root = c.notes[0]
    o = root.octave - 1
    lily = '<'
    for i, n in enumerate(c.notes):
        lily += n.lilypond_notation()
        #if i == 0:
        #    lily += '{}'.format(o)
        if n.octave > o:
            lily += ("'" * (n.octave - o))
        elif n.octave < o:
            lily += (',' * (o - n.octave))
        if i + 1 == len(c.notes):
            lily += '>'
        else:
            lily += ' '
    return lily
            

def chord_to_lilypond(c):
    paper_size = '''
    #(set! paper-alist 
      (cons '("flashcard" . (cons (* 5 cm) (* 3 cm))) paper-alist))
    \paper { #(set-paper-size "flashcard") }
    '''
    return paper_size + '\\version "2.24.0" { \\clef treble ' + lilypond_chord(c) + ' }'


def gen_lilypond(lp_text, file):
    tmp = NamedTemporaryFile('w')
    tmp.write(lp_text)
    tmp.flush()

    subprocess.run([lilypond, '--png', '-o', file, tmp.name])
    tmp.close()


circle_of_fifths = [ 
                    [('C', 'major'), ('A', 'natural_minor')],
                    [('G', 'major'), ('E', 'natural_minor')],
                    [('D', 'major'), ('B', 'natural_minor')],
                    [('A', 'major'), ('F#', 'natural_minor')],
                    [('E', 'major'), ('C#', 'natural_minor')],
                    [('B', 'major'), ('Cb', 'major'), ('G#', 'natural_minor')],
                    [('F#', 'major'), ('Gb', 'major'), ('Eb', 'natural_minor'), ('D#', 'natural_minor')],
                    [('Db', 'major'), ('C#', 'major'), ('Bb', 'natural_minor')],
                    [('Ab', 'major'), ('F', 'natural_minor')],
                    [('Eb', 'major'), ('C', 'natural_minor')],
                    [('Bb', 'major'), ('G', 'natural_minor')], 
                    [('F', 'major'), ('D', 'natural_minor')]
                    ]

def scales():
    copy_root = '/Users/johsulli/Documents/log/pages'

    for i, enharmonics in enumerate(circle_of_fifths):
        es = [Scale(n, m) for n, m in enharmonics]
        gen_lilypond(scale_to_lilypond(es[0]), "/Users/johsulli/dev/music/cof_{}".format(i))
        maj_scales = ', '.join(str(e) for e in es if e.name == 'major')
        min_scales = ', '.join(str(e) for e in es if e.name == 'natural_minor')
        print("\t- #### What *major* scale(s) are in this signature:\n\t ![cof](" + copy_root + "/cof_" + str(i) + ".png) #card #scale {{cloze " + maj_scales + "}}")
        print("\t- #### What *minor* scale(s) are in this signature:\n\t ![cof](" + copy_root + "/cof_" + str(i) + ".png) #card #scale {{cloze " + min_scales + "}}")


def intervals():
    for n in Note.all():
         for i in Interval.all():
             print("\t- #### What is a " + str(i) + " above " + str(n) + "?\n\t#card #interval {{cloze " + str(n + i) + "}}")
             print("\t- #### What is a " + str(i) + " below " + str(n) + "?\n\t#card #interval {{cloze " + str(n - i) + "}}")

def basic_chords():
    c_types = 'maj min aug dim dom7 min7 maj7 aug7 dim7 m7dim5'.split()

    for c in Chord.all():
        root = c.notes[0]
        if not root.accidental and c.chord_type in c_types:
            gen_lilypond(chord_to_lilypond(c), "/Users/johsulli/dev/music/basic_chord_{}".format(str(root) + c.chord_type))
            print("\t- #### Play or spell a " + str(c) + " chord\n\t#card #chord {{cloze ![chord](../assets/basic_chord_" + str(root) + c.chord_type + ".png)" + ' '.join(str(n) for n in c.notes)  + " }}")
            print("\t- #### Spell a " + str(root) + c.chord_type + " chord\n\t#card #chord {{cloze ![chord](../assets/basic_chord_" + str(root) + c.chord_type + ".png)" + ' '.join(str(n) for n in c.notes) + " }}")

if __name__ == '__main__':
    #scales()
    #intervals()
    basic_chords()

