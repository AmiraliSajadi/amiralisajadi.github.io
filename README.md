# Amirali Sajadi’s website

A static personal website ready for `AmiraliSajadi/amiralisajadi.github.io`. The HTML, CSS, JavaScript, figures, photos, and PDFs are included. No package installation or build service is required.

## Publish on GitHub Pages

1. Extract the archive and copy its contents into the root of your existing `amiralisajadi.github.io` checkout. Replace the old website files, while preserving the checkout’s `.git` directory.
2. Commit the replacement files and push them to `main`.
3. In the repository, open **Settings → Pages**.
4. Under **Build and deployment**, choose **Deploy from a branch**, then **main** and **/(root)**. Save.
5. Once GitHub finishes its Pages deployment, open <https://amiralisajadi.github.io/>.

The included `.nojekyll` file tells GitHub to publish the prepared static files directly. If an older custom Pages workflow is still deploying your previous website, disable that old workflow.

[GitHub’s publishing-source documentation](https://docs.github.com/en/pages/getting-started-with-github-pages/configuring-a-publishing-source-for-your-github-pages-site)

## Edit the website

- `scripts/render-pages.py` contains the page copy, navigation, research topic order, and HTML templates.
- `research.json` contains publication details and image references.
- `style.css` controls the layout and appearance.
- `script.js` controls research filters, image enlargement, and the Contact animation.
- `assets/tehran-philadelphia.svg` is the editable Contact illustration and its animation styles.
- `assets/personal/` contains the About gallery photos.
- `assets/papers/` contains linked manuscripts. `assets/cv.pdf` is the CV.
- `assets/report-illustration.png` is the report project’s concept illustration, created with built-in image generation. Its exact generation prompt is in `design/report-illustration-prompt.txt`.

After changing page copy or publication details, regenerate the four HTML pages from the repository root:

```sh
python3 scripts/render-pages.py
```

Commit the generated HTML files together with their source changes. Python is only used locally to generate static HTML; GitHub does not need to run it.

## Preview locally

From the repository root:

```sh
python3 -m http.server 8000
```

Open <http://localhost:8000/>. Use this local server instead of opening `index.html` directly, so the root-relative links and research data load correctly.
