# KJV

Computational exegesis of the King James Version (KJV) of the Bible.

This project provides the full text of the KJV in a structured,
machine-readable format. Each verse is extracted and stored as a row in a CSV
file with consistent metadata.

## Dataset

Each record includes:

- A canonical verse identifier (`T-BB-CCC-VVV`):
  - `T` = 1 (Old Testament) or 2 (New Testament).
  - `BB` = zero-padded book number.
  - `CCC` = zero-padded chapter number.
  - `VVV` = zero-padded verse number.
- Testament (Old Testament or New Testament).
- Book name.
- Chapter number.
- Verse number.
- Verse text.

Example:

```csv
id,testament,book,chapter,verse,text
1-01-001-001,Old Testament,Genesis,1,1,In the beginning God created the heaven and the earth.
1-01-001-002,Old Testament,Genesis,1,2,"And the earth was without form, and void; ..."
```

The parsing script (`parse_kjv.py`) is included for transparency and to
document how the dataset was generated.

## Source Text

This project uses a modified version of the King James Bible text distributed
by [Project Gutenberg, eBook #10](https://www.gutenberg.org/ebooks/10).

The King James Bible itself is in the public domain. The Project Gutenberg
edition is subject to the Project Gutenberg™ License. A copy of that license is
provided in this repository as
[`gutenberg_license.txt`](gutenberg_license.txt).

## License

- Code: MIT License (see `LICENSE`).
- Text: Public domain (via the King James Bible), distributed under the
  [Project Gutenberg™ License](gutenberg_license.txt).
