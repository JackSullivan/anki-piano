import genanki
import random
import math
import json

random.seed(1)

def newid():
    return random.randrange(1<<30, 1<<32)

def field(field):
    return {'name': field}

def card(name, front, back):
    return {'name': name, 'qfmt': front, 'afmt': back}



cardsets = {}


def make_cards():
    cards = []

    for sz in ['One', 'Two', 'Four', 'Eight']:
        for tempo in (['any tempo'] if sz == 'One' else []) + [str(t) for t in range(55, 121, 5)]:
            for hands in ['left handed', 'right handed', 'both hands'] if (sz == 'One' and tempo == 'any tempo') else ['both hands']:
                front = "\n".join([
                    '{{#' + sz + ' Measure}}',
                    '  Play {{Piece}}<br><b>' + hands + '</b> at ' + tempo + ' measure: {{Measure}}',
                    '{{/' + sz + ' Measure}}'
                ])
                name = " ".join([hands, sz, tempo])
                cards.append(card(name, front, 'How did it go?'))
                #cardsets[(hands, sz, tempo)] = " ".join([hands, sz, tempo]) 
                if hands not in cardsets:
                    cardsets[hands] = []
                cardsets[hands].append(name)
                if sz not in cardsets:
                    cardsets[sz] = []
                cardsets[sz].append(name)
                if tempo not in cardsets:
                    cardsets[tempo] = []
                cardsets[tempo].append(name)
    return cards

piece_model_id = newid()
note_name = 'Piano Piece'

piece_model = genanki.Model(piece_model_id, note_name,
                            fields=list(map(field, ['Composer', 'Piece', 'Measure', 'One Measure', 'Two Measure', 'Four Measure', 'Eight Measure'])),
                             templates=make_cards())

def f_and_l(l):
    return "{}-{}".format(l[0], l[-1])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

# nutcracker
def mask(n):
    l = [''] * 4
    l[int(math.log2(n))] = 'True'
    return l

ms = list(range(1, 17))
parts = []
parts += [(m, mask(1)) for m in ms]

for sz in [2,4,8]:
    parts += [(f_and_l(c), mask(sz)) for c in chunks(ms, sz)]
    
#print(parts)

piec = 'Nutcracker March'
comp = 'Tchaicovsky'

nut_id = newid()

deck = genanki.Deck(nut_id, 'Piano Rep2::Nutcracker')

for (m, msk) in parts:
    deck.add_note(genanki.Note(piece_model, fields=[comp, piec, str(m)] + msk))


genanki.Package(deck).write_to_file('piano rep.apkg')

#print(cardsets)

## gen rules

def any(*args):
    return ["any", [a for a in args]]

def cond(cards, condition):
    return {"cards": cards, "condition": condition}

def rule(trigger, action):
    return {"trigger": trigger, "action": action}

def action(action, cards):
    return {'action': action, 'cards': cards}

def suspend(cards):
    return action('suspend', cards)

def note_rules(note_type, *rules):
    return {note_type: [r for r in rules]}

### Start by suspending cards that we haven't gotten to

def all_cardsets_where(*keys):
    w = []
    for k in keys:
        w += cardsets[k]
    return list(set(w))


rules = note_rules(note_name, 
           rule(any(
               *[cond(card, state) for card in (cardsets['left handed'] + cardsets['right handed'])
                 for state in ["young", "new"]]
                 ), suspend(all_cardsets_where('both hands'))))

print(json.dumps(rules))