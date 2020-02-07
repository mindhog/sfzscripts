#!/usr/bin/python3

import sys
import os
import math
import argparse
import re

# This will match some note names that will never be used, like "b#", but that's
# ok.
NOTES = dict(zip('cdefgab', (0, 2, 4, 5, 7, 9, 11)))
SHARPS = {'': 0, 's': 1, '#': 1}
FILE_RX = re.compile(r'([a-g])([s#]?)([1-7])')
def GetNote(str, file):
    m = FILE_RX.match(str)
    if m:
        return 12 + int(m.group(3)) * 12 + NOTES[m.group(1)] + SHARPS[m.group(2)]
    else:
        print("***** No note value for string {} in file {}".format(str,file))
        sys.exit(1)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Output sfz file sample regions for selected files")
    parser.add_argument('file', type=str,nargs='+',help='Sample files')
    parser.add_argument('-n','--noteloc', type=int, help='Note value location')
    parser.add_argument('--line','-l',type=str,nargs=1,help='string to add each sample line')
    args = parser.parse_args()
    samples = []
    # collect sample files to list
    for f in args.file:
        note = GetNote(f[args.noteloc:args.noteloc+4],f)
        samples.append( dict(file = f,
                                note = note))

    # generate
    for note in range(1,127):
        cs = []
        # collect valid samples
        for c in samples:
            if (c['note'] <= note+2 and c['note'] >= note-2):
                cs.append(c)
        seq=1
        for s in cs:
            print("<region> sample={file} lokey={note} hikey={note} pitch_keycenter={orgnote} seq_length={seqlen} seq_position={seq} {line}".format(file=s['file'],note=note,orgnote=s['note'],seq=seq,seqlen=len(cs),line=args.line[0]))
            seq += 1




