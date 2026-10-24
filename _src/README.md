# AiEngineered website source (aiengineered.co.uk)

Plain static HTML, so search engines and AI crawlers read every word.

- `data.py`: business types, jobs and guide prices (copied from the two calculators), plus page copy.
- `guides.py`: the guide articles.
- `build.py`: builds every page, sitemap.xml, robots.txt, llms.txt and vercel.json.
- `static/`: stylesheet, script, icons and share image.

Rebuild after changes:

    cd _src && REDIRECT_VERCEL_HOST=1 python3 build.py && cp -r out/. ..

Set CONTACT_EMAIL=hello@aiengineered.co.uk once that address forwards to your inbox.
The built files at the top of this branch are what Vercel serves (project: aiengineered).
