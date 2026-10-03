# netsafeituk.github.io

Website for Netsafe IT Limited. A hand-written static site (plain HTML and CSS,
no build step), hosted free on **GitHub Pages** at
`https://netsafeituk.github.io/`.

## Files

| File / folder   | Purpose |
|-----------------|---------|
| `index.html`    | The home page (all main content) |
| `404.html`      | Shown by GitHub Pages for any address that doesn't exist |
| `privacy-policy.html`, `cookie-policy.html` | Legal pages linked from every footer. Update the "Last updated" date when you change them |
| `css/style.css` | All styling; colours are variables at the top |
| `favicon.svg`   | Shield mark used in the browser tab; page headers and footers use the Netsafe IT wordmark |
| `.nojekyll`     | Tells GitHub to publish files as-is (skip its Jekyll processor) |
| `robots.txt`, `sitemap.xml` | Help search engines index the site |
| `tests/check_site.py` | Automated checks; run before every publish |

## Editing and previewing

1. Edit the files in VS Code.
2. Preview locally:
   ```bash
   python3 -m http.server 8000
   ```
   then open http://localhost:8000 (press Ctrl+C to stop).
3. Run the checks:
   ```bash
   python3 tests/check_site.py
   ```

## Publishing

Every push to the `main` branch on GitHub goes live within about a minute:

```bash
git add -A
git commit -m "Describe the change"
git push
```

## Hosting

This repository is published directly from GitHub Pages at
`https://netsafeituk.github.io/`.

The old custom-domain redirect has been disabled, so the GitHub Pages URL is now
used as the canonical site address. If a custom domain is ever added again, it
should be configured in GitHub Pages and a matching `CNAME` file should be kept in
this repository.
