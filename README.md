# BIBLE STUDY

Sermon notes kept like books, on the same reader as SECONDBRAIN. Each sermon gets its own notebook: the message retold step by step with its reasoning made explicit, every Bible verse quoted in full with its translation named, and no quizzes or exams.

Open `index.html` in any browser, or host the folder on a static host such as GitHub Pages.

## Notebooks on the shelf

- **Still Got That Spark** (`notes/2026-11-15-still-got-that-spark.html`): Pastor Sam, IFGF Bandung Sunday Service, 15 November 2026, series "Dreams and Visions". Main text Joshua 14:6-14. Caleb at 85 and the three marks of a lasting spark: excitement, expectation, experience. Quotes ESV for English and TB (Terjemahan Baru) for the passages read in Indonesian, plus NIV and The Message where the preacher read them.

## How a sermon notebook is made

Each sermon lives in `packs/<date>-<slug>/`:

| File | What it is |
|---|---|
| `notebook.json` | Title, preacher, church, date, main text, shelf card |
| `walkthrough.html` | The book: chapters, figures, verse quotations, appendices |
| `transcript.md` | Machine transcript of the sermon, with livestream timestamps |
| `sermon-map.md` | Outline, exact taglines, the argument as a chain of reasons |
| `scripture-check.md` | Every passage used, exact text in each version, and whether it says what it was used for |
| `sources.md` | Which part of the sermon fed which chapter, gaps and points needing care |

The work is split into steps:

1. **Transcribe.** Get the service audio, cut the sermon portion, and transcribe it with `tools/sermon/tx.py` (faster-whisper, `large-v3-turbo`):
   ```bash
   ffmpeg -ss <start seconds> -i service.m4a -ac 1 -ar 16000 sermon.wav
   python3 tools/sermon/tx.py sermon.wav transcript.txt <start seconds> id
   ```
2. **Understand.** Map the outline, the preacher's exact lines and the logic of the argument (`sermon-map.md`).
3. **Check the Scripture.** Fetch every verse exactly with `tools/sermon/verse.py` (ESV and others from Bible Gateway, TB from alkitab.mobi) and check each use (`scripture-check.md`):
   ```bash
   python3 -I tools/sermon/verse.py --NIV --MSG "Joshua 14:6-14" "Psalm 34:5"
   ```
4. **Write.** Write `walkthrough.html` in the SECONDBRAIN notebook format, quoting verses with the `verse` block:
   ```html
   <div class="verse"><p><sup>24</sup>But my servant Caleb, ...</p><cite>Numbers 14:24 · ESV</cite></div>
   ```
5. **Build.** `python3 -I tools/build_notebook.py packs/<pack>` writes `notes/<slug>.html` and adds the card to the shelf.

Style rules for every notebook: no em dashes, no quizzes or exams, every verse cited with its translation, and the preacher's reasoning set out step by step without adding outside theology. Where a detail needs care against the text, a short "Reading it carefully" box says what was said, what the verse says, and whether the point still stands.

## Shared files

- `assets/scripture.css`: verse quotation blocks
- `assets/secondbrain.css`, `assets/notebook.css`, `assets/book.css`: themes, notebook and book layout (from SECONDBRAIN)
- `assets/reader.js`, `assets/secondbrain.js`, `assets/boot.js`: Scroll and Slide modes, contents, highlights, preferences
- `tools/shell.html`: page head and header that every notebook page is built on
- `tools/build_notebook.py`: builds a notebook from a pack
