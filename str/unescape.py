#!/usr/bin/env python3
import sys

def unescape(s:str)->str:
    out = s.encode().decode('unicode_escape')
    return out

if __name__ == '__main__':
    s = sys.stdin.read()
    print(unescape(s))
