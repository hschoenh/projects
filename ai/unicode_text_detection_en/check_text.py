#!/usr/bin/env python3
"""Scan UTF-8 text for selected invisible or unusual Unicode characters."""
from pathlib import Path
import sys
import unicodedata

if len(sys.argv) != 2:
    sys.exit('Usage: python3 check_text.py FILE.txt')

path = Path(sys.argv[1])
text = path.read_text(encoding='utf-8-sig')
findings = []
for position, char in enumerate(text):
    category = unicodedata.category(char)
    cp = ord(char)
    if (category in ('Cf', 'Co', 'Cs')
            or (category == 'Zs' and char != ' ')
            or (category == 'Cc' and char not in '\n\r\t')
            or cp in (0xFEFF, 0x034F)):
        findings.append((position, f'U+{cp:04X}', unicodedata.name(char, 'UNKNOWN')))

print(f'File: {path.name}')
print(f'Total characters: {len(text)}')
print(f'Suspicious characters: {len(findings)}')
for pos, code, name in findings:
    print(f'  Position {pos:>5} | {code} | {name}')
