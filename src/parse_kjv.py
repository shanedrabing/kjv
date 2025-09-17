import re
import csv
from pathlib import Path


# ----------------------
# CONSTANTS
# ----------------------


BOOK_MAPPING = {
    "The First Book of Moses: Called Genesis": "Genesis",
    "The Second Book of Moses: Called Exodus": "Exodus",
    "The Third Book of Moses: Called Leviticus": "Leviticus",
    "The Fourth Book of Moses: Called Numbers": "Numbers",
    "The Fifth Book of Moses: Called Deuteronomy": "Deuteronomy",
    "The Book of Joshua": "Joshua",
    "The Book of Judges": "Judges",
    "The Book of Ruth": "Ruth",
    "The First Book of Samuel": "1 Samuel",
    "The Second Book of Samuel": "2 Samuel",
    "The First Book of the Kings": "1 Kings",
    "The Second Book of the Kings": "2 Kings",
    "The First Book of the Chronicles": "1 Chronicles",
    "The Second Book of the Chronicles": "2 Chronicles",
    "Ezra": "Ezra",
    "The Book of Nehemiah": "Nehemiah",
    "The Book of Esther": "Esther",
    "The Book of Job": "Job",
    "The Book of Psalms": "Psalms",
    "The Proverbs": "Proverbs",
    "Ecclesiastes": "Ecclesiastes",
    "The Song of Solomon": "Song of Solomon",
    "The Book of the Prophet Isaiah": "Isaiah",
    "The Book of the Prophet Jeremiah": "Jeremiah",
    "The Lamentations of Jeremiah": "Lamentations",
    "The Book of the Prophet Ezekiel": "Ezekiel",
    "The Book of Daniel": "Daniel",
    "Hosea": "Hosea",
    "Joel": "Joel",
    "Amos": "Amos",
    "Obadiah": "Obadiah",
    "Jonah": "Jonah",
    "Micah": "Micah",
    "Nahum": "Nahum",
    "Habakkuk": "Habakkuk",
    "Zephaniah": "Zephaniah",
    "Haggai": "Haggai",
    "Zechariah": "Zechariah",
    "Malachi": "Malachi",
    "The Gospel According to Saint Matthew": "Matthew",
    "The Gospel According to Saint Mark": "Mark",
    "The Gospel According to Saint Luke": "Luke",
    "The Gospel According to Saint John": "John",
    "The Acts of the Apostles": "Acts",
    "The Epistle of Paul the Apostle to the Romans": "Romans",
    "The First Epistle of Paul the Apostle to the Corinthians": "1 Corinthians",
    "The Second Epistle of Paul the Apostle to the Corinthians": "2 Corinthians",
    "The Epistle of Paul the Apostle to the Galatians": "Galatians",
    "The Epistle of Paul the Apostle to the Ephesians": "Ephesians",
    "The Epistle of Paul the Apostle to the Philippians": "Philippians",
    "The Epistle of Paul the Apostle to the Colossians": "Colossians",
    "The First Epistle of Paul the Apostle to the Thessalonians": "1 Thessalonians",
    "The Second Epistle of Paul the Apostle to the Thessalonians": "2 Thessalonians",
    "The First Epistle of Paul the Apostle to Timothy": "1 Timothy",
    "The Second Epistle of Paul the Apostle to Timothy": "2 Timothy",
    "The Epistle of Paul the Apostle to Titus": "Titus",
    "The Epistle of Paul the Apostle to Philemon": "Philemon",
    "The Epistle of Paul the Apostle to the Hebrews": "Hebrews",
    "The General Epistle of James": "James",
    "The First Epistle General of Peter": "1 Peter",
    "The Second General Epistle of Peter": "2 Peter",
    "The First Epistle General of John": "1 John",
    "The Second Epistle General of John": "2 John",
    "The Third Epistle General of John": "3 John",
    "The General Epistle of Jude": "Jude",
    "The Revelation of Saint John the Divine": "Revelation",
}

CANON_ORDER = [
    "Genesis",
    "Exodus",
    "Leviticus",
    "Numbers",
    "Deuteronomy",
    "Joshua",
    "Judges",
    "Ruth",
    "1 Samuel",
    "2 Samuel",
    "1 Kings",
    "2 Kings",
    "1 Chronicles",
    "2 Chronicles",
    "Ezra",
    "Nehemiah",
    "Esther",
    "Job",
    "Psalms",
    "Proverbs",
    "Ecclesiastes",
    "Song of Solomon",
    "Isaiah",
    "Jeremiah",
    "Lamentations",
    "Ezekiel",
    "Daniel",
    "Hosea",
    "Joel",
    "Amos",
    "Obadiah",
    "Jonah",
    "Micah",
    "Nahum",
    "Habakkuk",
    "Zephaniah",
    "Haggai",
    "Zechariah",
    "Malachi",
    "Matthew",
    "Mark",
    "Luke",
    "John",
    "Acts",
    "Romans",
    "1 Corinthians",
    "2 Corinthians",
    "Galatians",
    "Ephesians",
    "Philippians",
    "Colossians",
    "1 Thessalonians",
    "2 Thessalonians",
    "1 Timothy",
    "2 Timothy",
    "Titus",
    "Philemon",
    "Hebrews",
    "James",
    "1 Peter",
    "2 Peter",
    "1 John",
    "2 John",
    "3 John",
    "Jude",
    "Revelation",
]

TESTAMENT_INFO = {
    "The Old Testament of the King James Version of the Bible": (
        "Old Testament",
        1,
    ),
    "The New Testament of the King James Bible": ("New Testament", 2),
}

BOOKNUM = {name: i + 1 for i, name in enumerate(CANON_ORDER)}

CV_RE = re.compile(r"(\d{1,3}):(\d{1,3})")
SPACE_RE = re.compile(r"\s+")


# ----------------------
# FUNCTIONS
# ----------------------


def unwrap(text):
    out, buf = [], []
    for line in text.splitlines():
        if line.strip():
            buf.append(line.strip())
        else:
            if buf:
                out.append(" ".join(buf))
                buf = []
            out.append("")
    if buf:
        out.append(" ".join(buf))
    return "\n".join(out)


def parse_index(index_text):
    pairs = []
    for block in index_text.strip().split("\n\n"):
        lines = [ln.strip() for ln in block.splitlines() if ln.strip()]
        testament = lines[0]
        for book in lines[1:]:
            pairs.append((testament, book))
    return pairs


def build_anchors(chunks, index_pairs):
    anchors, cursor = [], 0
    for testament, book in index_pairs:
        for i in range(cursor, len(chunks)):
            if chunks[i] == book:
                anchors.append((i, testament, book))
                cursor = i + 1
                break
    return anchors


def slice_chunks(chunks, anchors):
    slices = []
    for j, (pos, testament, book) in enumerate(anchors):
        end = anchors[j + 1][0] if j + 1 < len(anchors) else len(chunks)
        slices.append(
            {
                "testament": testament,
                "book": book,
                "chunks": chunks[pos + 1 : end],
            }
        )
    return slices


def concat_slices(slices):
    out = []
    for s in slices:
        t_label, t_code = TESTAMENT_INFO[s["testament"]]
        book_short = BOOK_MAPPING[s["book"]]
        # filter out testament headers
        filtered_chunks = [c for c in s["chunks"] if c not in TESTAMENT_INFO]
        text = " ".join(filtered_chunks).strip()
        out.append(
            {
                "testament": t_label,
                "t_code": t_code,
                "book": book_short,
                "text": text,
            }
        )
    return out


def parse_verses(blocks):
    verses = []
    for blk in blocks:
        matches = list(CV_RE.finditer(blk["text"]))
        for i, m in enumerate(matches):
            chap, vs = int(m.group(1)), int(m.group(2))
            start = m.end()
            end = (
                matches[i + 1].start()
                if i + 1 < len(matches)
                else len(blk["text"])
            )
            txt = SPACE_RE.sub(" ", blk["text"][start:end].strip())
            verses.append(
                {
                    "testament": blk["testament"],
                    "t_code": blk["t_code"],
                    "book": blk["book"],
                    "chapter": chap,
                    "verse": vs,
                    "text": txt,
                }
            )
    return verses


def enrich_and_sort(verses):
    out = []
    for v in verses:
        bnum = BOOKNUM[v["book"]]
        vid = f"{v['t_code']}-{bnum:02d}-{v['chapter']:03d}-{v['verse']:03d}"
        out.append(
            {
                "id": vid,
                "testament": v["testament"],
                "book": v["book"],
                "chapter": v["chapter"],
                "verse": v["verse"],
                "text": v["text"],
            }
        )
    return sorted(out, key=lambda r: r["id"])


def export_csv(rows, path):
    fields = ["id", "testament", "book", "chapter", "verse", "text"]
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# ----------------------
# SCRIPT
# ----------------------


if __name__ == "__main__":
    base = Path("data")
    index_text = (base / "txt" / "kjv_index.txt").read_text("utf-8-sig")
    raw_text = (base / "txt" / "kjv_raw.txt").read_text("utf-8-sig")

    index_pairs = parse_index(index_text)
    chunks = [x.strip() for x in unwrap(raw_text).split("\n\n")]

    anchors = build_anchors(chunks, index_pairs)
    slices = slice_chunks(chunks, anchors)
    blocks = concat_slices(slices)
    verses = parse_verses(blocks)
    final = enrich_and_sort(verses)

    export_csv(final, base / "csv" / "kjv.csv")
