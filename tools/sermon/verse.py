"""verse.py [--NIV --MSG ...] "Joshua 14:6-14" ["Numbers 13:30"] ... : prints ESV (Bible Gateway) and TB (alkitab.mobi) text per verse.
Ranges within one chapter only."""
import sys, re, html, urllib.parse, urllib.request
BOOKS = dict(Genesis="Kej", Exodus="Kel", Leviticus="Im", Numbers="Bil", Deuteronomy="Ul", Joshua="Yos", Judges="Hak", Ruth="Rut",
 **{"1 Samuel":"1Sam","2 Samuel":"2Sam","1 Kings":"1Raj","2 Kings":"2Raj","1 Chronicles":"1Taw","2 Chronicles":"2Taw","Song of Songs":"Kid",
    "1 Corinthians":"1Kor","2 Corinthians":"2Kor","1 Thessalonians":"1Tes","2 Thessalonians":"2Tes","1 Timothy":"1Tim","2 Timothy":"2Tim",
    "1 Peter":"1Ptr","2 Peter":"2Ptr","1 John":"1Yoh","2 John":"2Yoh","3 John":"3Yoh"},
 Ezra="Ezr", Nehemiah="Neh", Esther="Est", Job="Ayb", Psalm="Mzm", Psalms="Mzm", Proverbs="Ams", Ecclesiastes="Pkh", Isaiah="Yes", Jeremiah="Yer",
 Lamentations="Rat", Ezekiel="Yeh", Daniel="Dan", Hosea="Hos", Joel="Yl", Amos="Am", Obadiah="Ob", Jonah="Yun", Micah="Mi", Nahum="Nah",
 Habakkuk="Hab", Zephaniah="Zef", Haggai="Hag", Zechariah="Za", Malachi="Mal", Matthew="Mat", Mark="Mrk", Luke="Luk", John="Yoh", Acts="Kis",
 Romans="Rm", Galatians="Gal", Ephesians="Ef", Philippians="Flp", Colossians="Kol", Titus="Tit", Philemon="Flm", Hebrews="Ibr", James="Yak",
 Jude="Yud", Revelation="Why")
get = lambda u: urllib.request.urlopen(urllib.request.Request(u, headers={"User-Agent": "Mozilla/5.0"}), timeout=60).read().decode()
clean = lambda s: re.sub(r'\s+([,.;:!?’”])', r'\1', re.sub(r'([“‘])\s+', r'\1', re.sub(r'\s+', ' ', html.unescape(re.sub(r'<[^>]+>', ' ', s))))).strip()
def esv(ref, ver="ESV"):
    t = get("https://www.biblegateway.com/passage/?search=%s&version=%s" % (urllib.parse.quote(ref), ver))
    t = t[t.find('class="passage-text"'):]
    for end in ('class="footnotes"', 'class="crossrefs', 'class="passage-other-trans"', 'Read full chapter'):
        if end in t: t = t[:t.find(end)]
    t = re.sub(r"<span[^>]*small-caps[^>]*>(.*?)</span>", lambda m: m.group(1).upper(), t, flags=re.S)
    t = re.sub(r'<sup[^>]*class=.(footnote|crossreference)[^>]*>.*?</sup>', '', t, flags=re.S)
    t = re.sub(r'<sup class="versenum[^"]*">.*?</sup>|<span class="chapternum">.*?</span>|<h[1-6].*?</h[1-6]>', '', t, flags=re.S)
    parts = re.split(r'<span[^>]*class="text [A-Za-z0-9]+-\d+-(\d+)"[^>]*>', t); out = {}
    for k in range(1, len(parts), 2):
        out[int(parts[k])] = (out.get(int(parts[k]), '') + ' ' + clean(parts[k+1])).strip()
    return out
def tb(book, ch, a, b):
    t = get("https://alkitab.mobi/tb/%s/%d/" % (BOOKS[book], ch)); out = {}
    for m in re.finditer(r'<a name=v(\d+)[^>]*>\d+</a></span>\s*<span[^>]*>(.*?)</span></p>', t, re.S):
        v = int(m.group(1))
        if a <= v <= b: out[v] = clean(m.group(2))
    return out
EXTRA = [a[2:] for a in sys.argv[1:] if a.startswith("--")]
for ref in [a for a in sys.argv[1:] if not a.startswith("--")]:
    m = re.fullmatch(r'(.+?) (\d+):(\d+)(?:-(\d+))?', ref); book, ch, a = m.group(1), int(m.group(2)), int(m.group(3)); b = int(m.group(4) or a)
    e, i = esv(ref), tb(book, ch, a, b); x = {v: esv(ref, v) for v in EXTRA}
    print("## " + ref)
    for v in range(a, b + 1):
        print("%d:%d ESV: %s" % (ch, v, e.get(v, "?? MISSING")))
        print("%d:%d TB : %s" % (ch, v, i.get(v, "?? MISSING")))
        for n, d in x.items(): print("%d:%d %s: %s" % (ch, v, n, d.get(v, "?? MISSING")))
    print()
