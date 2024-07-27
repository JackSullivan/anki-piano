import argparse

def f_and_l(l):
    return "{}-{}".format(l[0], l[-1])

def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]

def stringescape(s):
    return s.replace(",",'",')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog='gen_piece',
                                     description='Generate anki CSV for a piece')
    parser.add_argument('name')
    parser.add_argument('composer')
    parser.add_argument('measures', type=int)
    parser.add_argument('-t', '--tempo', type=int)
    parser.add_argument('--two_hands', action='store_true')

    args = parser.parse_args()

    ms = range(1, args.measures + 1)

    parts = []
    parts += ms
    for sz in [2,4,8]:
        parts += list(map(f_and_l, chunks(ms, sz)))



    if args.two_hands:
        hands = ["right", "left", "both"]
    else:
        hands = [""]

    if args.tempo:
        tempos = ["no metronome"] + list(range(55, args.tempo, 5))[:-1] + [args.tempo]
    else:
        tempos = [""]

    for tempo in tempos:
        for part in parts:
            for hand in hands:
                print(",".join([args.name, args.composer, str(part), str(tempo), hand]))


