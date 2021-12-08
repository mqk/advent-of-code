import pandas as pd
from collections import Counter

DIGITS = {
    '0':set(list('ABCEFG')),
    '1':set(list('CF')),
    '2':set(list('ACDEG')),
    '3':set(list('ACDFG')),
    '4':set(list('BCDF')),
    '5':set(list('ABDFG')),
    '6':set(list('ABDEFG')),
    '7':set(list('ACF')),
    '8':set(list('ABCDEFG')),
    '9':set(list('ABCDFG')),
}

def deduce_segment_mapping(digits):
    # Convert the list of digit words into a pandas Series of sets
    # of the letters of each word, whose index is equal to length
    # of the word.
    srs = pd.Series(digits).apply(lambda x: set(list(x)))
    srs.index = srs.apply(len)

    # Apply the constraints from the four unique length words,
    # corresponding to digits 1 (length=2), 4 (4), 7 (3), and 8 (7).
    segments = {
        'A':srs[3] - srs[2],
        'B':srs[4] - srs[2],
        'C':srs[2],
        'D':srs[4] - srs[2],
        'E':srs[7] - srs[3] - srs[4],
        'F':srs[2],
        'G':srs[7] - srs[3] - srs[4]
    }

    # Of the three l=5 words, the letters that appear just once are B and E.
    c = Counter()
    for i in range(3):
        c.update(srs[5].iloc[i])

    s = set([k for k,v in c.items() if v==1])
    segments['B'] = segments['B'] & s
    segments['D'] = segments['D'] - segments['B']
    segments['E'] = segments['E'] & s
    segments['G'] = segments['G'] - segments['E']

    # Of the three l=6 words, the letter that appears exactly twice
    # and is not already uniquely mapped is C.
    c = Counter()
    for i in range(3):
        c.update(srs[6].iloc[i])

    s = set([k for k,v in c.items() if v==2])
    m = set([list(v)[0] for v in segments.values() if len(v) == 1])
    segments['C'] = s - m
    segments['F'] = segments['F'] - segments['C']
        
    return segments

def decode(s, segments):
    to_segments = {list(v)[0]:k for k,v in segments.items()}
    o = set([to_segments[x] for x in list(s)])
    return [k for k,v in DIGITS.items() if v == o][0]



# filename = 'input_test.txt'
filename = 'input.txt'
lines = [x.strip() for x in open(filename, 'r').readlines()]
digits_list = [x.split(' | ')[0].split() for x in lines]
outputs_list = [x.split(' | ')[1].split() for x in lines]

values = []
for digits, outputs in zip(digits_list, outputs_list):
    segments = deduce_segment_mapping(digits)
    values.append( int(''.join([decode(x, segments) for x in outputs])) )

print(sum(values))
