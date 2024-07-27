
import genanki
import random
import json

random.seed(2)

def newid():
    return random.randrange(1<<30, 1<<32)

def field(field):
    return {'name': field}

def card(name, front, back):
    return {'name': name, 'qfmt': front, 'afmt': back}

cardsets = {}

all_hands = lambda tempo: ['left hand', 'right hand', 'boths hands'] if tempo == str(55) else ['both hands'] 
all_directions = ['ascending', 'descending', 'ascending then descending', 'descending then ascending']
all_lengths = ['one octave', 'two octaves']


# Cards for handedness, one and two octaves, ascending and descending, at various tempos
def make_cards(starting_tempo=55, ending_tempo=120):
    cards = []

    for tempo in map(str, range(starting_tempo, ending_tempo +1, 5)):
        for hands in all_hands(tempo):
            for direction in all_directions:
                for length in all_lengths:
                    front = "<br>".join([
                        'Play {{Major Scale}} scale with ' + hands + ' ' + direction + ' for ' + length + ' at tempo ' + tempo,
                        '{{Key Signature}}'
                    ])
                    tup = (tempo, hands, direction, length)
                    name = ' '.join(tup)
                    cardsets[tup] = name
                    cards.append(card(name, front, 'how did it go?'))
    return cards


# The notes have the key signature and the major and (natural) minor scale names

signatures = ["0_flats.webp","1_flats.webp","2_flats.jpg","3_flats.jpg","4_flats.jpg","5_flats.jpg","6_flats.jpg","7_flats.jpg"]
maj_scale = ["{} Major".format(k) for k in "C F B♭ E♭ A♭ D♭ G♭ C♭".split()]
min_scale = ["{} Natural Minor".format(k) for k in "A D G C F B♭ E♭ A♭".split()]


def mk_img(path):
    return '<img src="{}">'.format(path)

scale_model_id = newid()
note_name = 'Scale Signature'

scale_model = genanki.Model(scale_model_id, note_name,
                            fields=list(map(field, ['Key Signature', 'Major Scale', 'Natural Minor Scale']))
                            , templates=make_cards())


deck_id = newid()

deck = genanki.Deck(deck_id, 'Piano::Scales::Major')

for fields in zip(map(mk_img, signatures), maj_scale, min_scale):
    deck.add_note(genanki.Note(scale_model, fields=[f for f in fields]))


package = genanki.Package(deck)
package.media_files = ["files/" + s for s in signatures]


package.write_to_file('piano scales.apkg')


## gen rules

def any(*args):
    return ["any", [a for a in args]]

def cond(cards, condition):
    return {"cards": cards, "condition": condition}

def rule(trigger, action, auto_reverse=False):
    return {"trigger": trigger, "action": action}

def action(action, cards):
    return {'action': action, 'cards': cards}

def suspend(cards):
    return action('suspend', cards)

def unsuspend(cards):
    return action('unsuspend', cards)

def note_rules(note_type, *rules):
    return {note_type: [r for r in rules]}

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

tempo_pairs = chunks(range(55, 121, 5), 2)

rule_entries = []

for lower, higher in tempo_pairs:
    for hands in all_hands(lower):
        for direction in all_directions:
            for length in all_lengths:
                completed = " ".join((str(lower), hands, direction, length))
                unlocked = " ".join((str(higher), hands, direction, length))
                rule_entries.append(rule(cond(completed, ["young", "new"]),
                                         suspend(unlocked)))
                rule_entries.append(rule(cond(completed, "mature"), 
                     unsuspend(unlocked)))




rules = note_rules(note_name, *rule_entries)

print(json.dumps(rules))