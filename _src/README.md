# AiEngineered website source

The site is plain static HTML (no JavaScript framework), so search engines and AI crawlers read every word.

- `data.py`: business types, jobs and guide prices (copied from the two calculators), plus page copy.
- `build.py`: builds every page, sitemap.xml, robots.txt and llms.txt.
- `static/`: stylesheet, script, icons and share image.

Rebuild after changes (and when the custom domain changes):

    cd _src && SITE_BASE=https://aiengineered.co.uk python3 build.py && cp -r out/. ..

The built files at the top of this branch are what Vercel serves (project: aiengineered).
