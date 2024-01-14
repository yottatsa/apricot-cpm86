#!/usr/bin/env python3
import sys
from difflib import SequenceMatcher
from typing import NamedTuple

class FileMatch(NamedTuple):
    a: int
    b: int
    size: int
    fname: str

def locate(a, b, d=256):
    result = []
    seq = SequenceMatcher(None, a, b)
    len_b = len(b)
    def matcher(l, r):
        match = seq.find_longest_match(l, r, 0, len_b)
        if match.size >= d:
            result.append(match)
            matcher(l, match.a)
            matcher(match.a + match.size, r)
    matcher(0, len(a))
    return result

if __name__ == "__main__":
    if len(sys.argv) < 3:
        raise SystemExit
    with open(sys.argv[1], "rb") as f:
        hay = f.read()
    result = []
    for fname in sys.argv[2:]:
        with open(fname, "rb") as f:
            needle = f.read()
        for match in  locate(hay, needle):
            result.append(FileMatch(fname=fname, a=match.a, b=match.b, size=match.size))

    for match in sorted(result, key=lambda i: i.a):
        print(f"{hex(match.a)}:{hex(match.a+match.size)} from {match.fname}:{hex(match.b)}")
