# www.netsafeit.co.uk

Website for Netsafe IT Limited. A hand-written static site (plain HTML and CSS,
no build step), hosted free on **GitHub Pages** with the custom domain
`www.netsafeit.co.uk`.

## Files

| File / folder   | Purpose |
|-----------------|---------|
| `index.html`    | The home page (all main content) |
| `404.html`      | Shown by GitHub Pages for any address that doesn't exist |
| `css/style.css` | All styling; colours are variables at the top |
| `favicon.svg`   | Shield mark used in the browser tab; page headers and footers use the Netsafe IT wordmark |
| `CNAME`         | Tells GitHub Pages which custom domain to serve. **Don't delete.** |
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

## DNS (at Fasthosts / LiveDomains)

| Type  | Host  | Value |
|-------|-------|-------|
| CNAME | `www` | `netsafeituk.github.io` |
| A     | `@`   | `185.199.108.153` |
| A     | `@`   | `185.199.109.153` |
| A     | `@`   | `185.199.110.153` |
| A     | `@`   | `185.199.111.153` |

The `A` records make the bare `netsafeit.co.uk` redirect to `www.netsafeit.co.uk`.
