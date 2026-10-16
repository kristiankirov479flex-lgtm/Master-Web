# Page generator (optional, developer use)

The site is plain static files. These scripts only keep the **Bulgarian and English pages in sync**.
Edit the text and data in `build_pages.py` (dictionaries `L['bg']` and `L['en']`, plus `UNITS`, `GROUNDS`, `PERSONAS`, `BUBBLES`, `ROUTES`)
or the layout in `page_template.html`, then run:

    python tools/build_pages.py      # writes index.html, en/index.html and js/config.js
    python tools/build_privacy.py    # writes privacy.html and en/privacy.html

Needs Python 3 only. If you prefer, ignore these and edit the HTML files by hand (change both languages).
