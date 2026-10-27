"""Copies the RUBOVA font instances as "FC Font ..." (TTF + WOFF), rewriting their name tables.

Standard library only:  python make_fc_fonts.py
The originals are read, never written. Both source families are SIL Open Font License 1.1
(Archivo, Fraunces) with no Reserved Font Name, so renamed copies are allowed; the copyright
notice (nameID 0) and licence URL (nameID 13/14) are kept, and OFL.txt ships alongside.
"""
import os
import struct
import zlib

SRC = os.path.expandvars(r"%LOCALAPPDATA%\Microsoft\Windows\Fonts")
OUT = os.path.dirname(os.path.abspath(__file__))

FONTS = {  # source file -> (family, subfamily, css weight, css style, role)
    "RUBOVAArchivoInfo-Regular.ttf": ("FC Font Info", "Regular", 400, "normal", "body"),
    "RUBOVAArchivoInfoBold-Regular.ttf": ("FC Font Info Bold", "Regular", 700, "normal", "body bold"),
    "RUBOVAArchivoCaps-Regular.ttf": ("FC Font Caps", "Regular", 700, "normal", "labels, tickers, buttons"),
    "RUBOVAArchivoNet-Regular.ttf": ("FC Font Net", "Regular", 600, "normal", "small UI / ingredient lines"),
    "RUBOVAFrauncesWordmark-Regular.ttf": ("FC Font Wordmark", "Regular", 900, "normal", "display headlines"),
    "RUBOVAFrauncesStory-Regular.ttf": ("FC Font Story", "Regular", 400, "normal", "long-form display / quotes"),
    "RUBOVAFrauncesTagline-Italic.ttf": ("FC Font Tagline", "Italic", 400, "italic", "italic accents in headlines"),
    "RUBOVAFrauncesFlavour-Italic.ttf": ("FC Font Flavour", "Italic", 600, "italic", "flavour names"),
}


def checksum(b):
    b = b + b"\0" * (-len(b) % 4)
    return sum(struct.unpack(">%dI" % (len(b) // 4), b)) & 0xFFFFFFFF


def read_tables(data):
    num = struct.unpack(">H", data[4:6])[0]
    tabs = {}
    for i in range(num):
        tag, cs, off, ln = struct.unpack(">4sIII", data[12 + 16 * i:28 + 16 * i])
        tabs[tag] = data[off:off + ln]
    return data[:4], tabs


def build_name(old, family, sub):
    fmt, cnt, so = struct.unpack(">HHH", old[:6])
    recs = []
    for i in range(cnt):
        pid, eid, lid, nid, ln, o = struct.unpack(">HHHHHH", old[6 + 12 * i:18 + 12 * i])
        recs.append([pid, eid, lid, nid, old[so + o:so + o + ln]])
    full = family if sub == "Regular" else f"{family} {sub}"
    ps = (family.replace(" ", "") + "-" + sub.replace(" ", ""))
    new = {1: family, 2: sub, 3: f"{ps};fizzy-and-crush", 4: full, 6: ps}
    for r in recs:
        if r[3] in new:
            s = new[r[3]]
            r[4] = s.encode("utf-16-be") if r[0] in (0, 3) else s.encode("latin-1")
        elif r[3] in (16, 17, 21, 22):          # typographic names would point at the old family
            r[4] = (family if r[3] in (16, 21) else sub).encode("utf-16-be" if r[0] in (0, 3) else "latin-1")
    recs.sort(key=lambda r: (r[0], r[1], r[2], r[3]))
    storage = b""; out = []
    for pid, eid, lid, nid, s in recs:
        out.append(struct.pack(">HHHHHH", pid, eid, lid, nid, len(s), len(storage))); storage += s
    return struct.pack(">HHH", 0, len(recs), 6 + 12 * len(recs)) + b"".join(out) + storage


def write_ttf(flavor, tabs):
    tags = sorted(tabs)
    n = len(tags); es = 1 << (n.bit_length() - 1)
    head = struct.pack(">4sHHHH", flavor, n, es * 16, es.bit_length() - 1, n * 16 - es * 16)
    off = 12 + 16 * n; dirs = b""; body = b""
    tabs = dict(tabs)
    h = bytearray(tabs[b"head"]); h[8:12] = b"\0\0\0\0"; tabs[b"head"] = bytes(h)
    for t in tags:
        d = tabs[t]
        dirs += struct.pack(">4sIII", t, checksum(d), off + len(body), len(d))
        body += d + b"\0" * (-len(d) % 4)
    font = bytearray(head + dirs + body)
    adj = (0xB1B0AFBA - checksum(bytes(font))) & 0xFFFFFFFF
    hoff = struct.unpack(">I", dirs[16 * tags.index(b"head") + 8:16 * tags.index(b"head") + 12])[0]
    font[hoff + 8:hoff + 12] = struct.pack(">I", adj)
    return bytes(font)


def to_woff(ttf):
    flavor, tabs = read_tables(ttf)
    num = struct.unpack(">H", ttf[4:6])[0]
    entries = []
    for i in range(num):
        tag, cs, off, ln = struct.unpack(">4sIII", ttf[12 + 16 * i:28 + 16 * i])
        raw = ttf[off:off + ln]; comp = zlib.compress(raw, 9)
        entries.append((tag, cs, raw, comp if len(comp) < len(raw) else raw))
    off = 44 + 20 * num; dirs = b""; body = b""
    for tag, cs, raw, comp in entries:
        dirs += struct.pack(">4sIIII", tag, off + len(body), len(comp), len(raw), cs)
        body += comp + b"\0" * (-len(comp) % 4)
    total = 44 + len(dirs) + len(body)
    hdr = struct.pack(">4s4sIHHI HH IIIII".replace(" ", ""), b"wOFF", flavor, total, num, 0, len(ttf), 1, 0, 0, 0, 0, 0, 0)
    return hdr + dirs + body


css = ["/* FC Font - self-hosted. Files live in /fonts (public/fonts in the Lovable project). */"]
for src, (family, sub, weight, style, role) in FONTS.items():
    data = open(os.path.join(SRC, src), "rb").read()
    flavor, tabs = read_tables(data)
    tabs[b"name"] = build_name(tabs[b"name"], family, sub)
    ttf = write_ttf(flavor, tabs)
    base = family.replace(" ", "") + ("-" + sub if sub != "Regular" else "")
    open(os.path.join(OUT, base + ".ttf"), "wb").write(ttf)
    open(os.path.join(OUT, base + ".woff"), "wb").write(to_woff(ttf))
    css.append(f"""/* {role} */
@font-face {{
  font-family: "{family}";
  src: url("/fonts/{base}.woff") format("woff"), url("/fonts/{base}.ttf") format("truetype");
  font-weight: {weight}; font-style: {style}; font-display: swap;
}}""")
open(os.path.join(OUT, "fc-font.css"), "w", encoding="utf-8").write("\n".join(css) + "\n")
print("FC_FONTS_DONE", sorted(os.listdir(OUT)))
