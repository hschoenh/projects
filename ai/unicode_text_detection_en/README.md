# Detecting Invisible Unicode Characters in Text

This project demonstrates how visually invisible Unicode characters can be detected in UTF-8 files using Python. It includes two English versions of the short story **The Lighthouse on the Silent Lake**. One has ten deliberately inserted characters, while the clean reference has none.

> **Scope:** This is a demonstration of Unicode artifacts, **not** proof of ChatGPT or other AI watermarking. Statistical AI watermarks, which can depend on word or token choices, cannot be detected or eliminated with this scanner.

## Files

| File | Description | Expected findings |
| --- | --- | ---: |
| `story_unicode_test.txt` | English story with 10 deliberately inserted Unicode characters | 10 |
| `story_clean.txt` | Same story without inserted characters | 0 |
| `check_text.py` | Local UTF-8 scanner, reporting position, Unicode code point, and name | — |
| `README.md` | Documentation and instructions | — |

## What is being detected?

Some Unicode code points are invisible or look almost identical to ordinary whitespace. The marked story includes one instance of each of the following:

| Code point | Name |
| --- | --- |
| `U+2060` | WORD JOINER |
| `U+200B` | ZERO WIDTH SPACE |
| `U+200D` | ZERO WIDTH JOINER |
| `U+200C` | ZERO WIDTH NON-JOINER |
| `U+00A0` | NO-BREAK SPACE |
| `U+202F` | NARROW NO-BREAK SPACE |
| `U+FEFF` | ZERO WIDTH NO-BREAK SPACE |
| `U+200E` | LEFT-TO-RIGHT MARK |
| `U+200F` | RIGHT-TO-LEFT MARK |
| `U+034F` | COMBINING GRAPHEME JOINER |

These characters can have legitimate linguistic or formatting purposes. Their presence does **not** identify an AI model or vendor.

## Why check text?

- **Text quality:** Invisible code points can affect searching, comparisons, parsers, configuration files, and version control.
- **Reproducibility:** Two texts that appear identical may differ at the character level.
- **Document hygiene:** Unintended characters can be identified before publication or release.

A result of zero findings does **not** prove that a text is AI-free, free of statistical watermarks, or untraceable.

## Requirements

Python 3 on macOS, Linux, or Windows. No additional Python dependencies are needed.

## How to test

Place all four files in one directory, open a terminal there, and run:

```bash
python3 check_text.py story_unicode_test.txt
```

Expected: `Suspicious characters: 10`.

```bash
python3 check_text.py story_clean.txt
```

Expected: `Suspicious characters: 0`.

### Compare the stories character by character

```python
from pathlib import Path
import difflib

a = Path('story_unicode_test.txt').read_text(encoding='utf-8')
b = Path('story_clean.txt').read_text(encoding='utf-8')
print('Character counts:', len(a), len(b))
print('Exactly identical:', a == b)
for change in difflib.ndiff(a, b):
    if change.startswith(('- ', '+ ')):
        print(change[:2], ascii(change[2:]))
```

This reveals invisible differences as readable escape sequences.

## How to prevent and remove unwanted characters

**Prevention:** Use a text editor that can display invisible characters, validate UTF-8 files before distribution, and consider adding Unicode linting to continuous integration for technical documentation.

**Selective cleanup:** Identify each character's purpose first. Joiners, bidirectional control marks, and non-breaking spaces can be valid. Never remove all non-ASCII text, as this would damage legitimate content.

For this **controlled demonstration only**, the exact ten added characters can be removed:

```python
from pathlib import Path

source = Path('story_unicode_test.txt').read_text(encoding='utf-8')
test_chars = '\u2060\u200b\u200d\u200c\u00a0\u202f\ufeff\u200e\u200f\u034f'
cleaned = source.translate({ord(c): None for c in test_chars})
Path('story_sanitized.txt').write_text(cleaned, encoding='utf-8')
reference = Path('story_clean.txt').read_text(encoding='utf-8')
print('Matches reference:', cleaned == reference)
```

Expected: `Matches reference: True`. Then run `python3 check_text.py story_sanitized.txt`, expecting 0 findings.

**In real documents**, replacing a non-breaking space (`U+00A0`, `U+202F`) with an ordinary space is usually preferable to deleting it. Otherwise, words may be joined together.

## Other provenance mechanisms

| Mechanism | Covered by this scanner? | Appropriate check |
| --- | --- | --- |
| Selected invisible Unicode characters | Yes | `check_text.py` |
| DOCX/PDF metadata | No | File properties or `exiftool` |
| Statistical AI text watermarks | No | Specialized validated detectors, if available |
| Writing-style AI classifiers | No | Probabilistic classification, not definitive proof |
| Published-text similarity | No | Source comparison |
| Server logs, accounts, or version history | No | Platform audit trails and permissions |

### Optional metadata check on macOS

```bash
brew install exiftool
exiftool -a -G1 -s document.pdf
exiftool -a -G1 -s document.docx
```

File metadata must be inspected separately from text.

## Conclusion

This project shows how to detect and selectively remove deliberately inserted Unicode artifacts. It cannot prove AI authorship, detect statistical AI watermarks, or guarantee that a document's origin cannot be established.
