# Page generator (optional, developer use)

The site is plain static files. These scripts only keep the **Bulgarian and English pages in sync**.
Edit the text in `build_pages.py` (dictionaries `L['bg']` and `L['en']`, plus the menu and gallery lists)
or the layout in `page_template.html`, then run:

    python tools/build_pages.py      # writes index.html and en/index.html
    python tools/build_privacy.py    # writes privacy.html and en/privacy.html

Needs Python 3 only. If you prefer, ignore these and edit the HTML files by hand (change both languages).
