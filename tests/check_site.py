#!/usr/bin/env python3
"""
Automated checks for the Netsafe IT static website.

Run from the project root before every publish:
    python3 tests/check_site.py

Uses only the Python standard library, so nothing needs installing.
Exits with code 0 if every check passes, 1 if any check fails.

What is checked (the written test plan):
  1. Required files exist (home page, 404 page, stylesheet, CNAME).
  2. The CNAME file contains exactly the custom domain GitHub Pages must serve.
  3. Every HTML page has a <title>, a meta description, a viewport meta tag
     and a language attribute (basic SEO and accessibility).
  4. Every <img> has alt text (accessibility).
  5. Every local link/stylesheet/script/image reference points at a file
     that actually exists (no broken internal links).
  6. Every in-page anchor link (e.g. href="#services") has a matching id.
  7. Key business details (phone, email) appear on the home page.
  8. No obvious secrets (passwords, API keys) have been committed.
"""

import os
import re
import sys
from html.parser import HTMLParser

# Project root is the folder above this tests/ folder
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

EXPECTED_DOMAIN = "www.netsafeit.co.uk"
REQUIRED_FILES = ["index.html", "404.html", "css/style.css", "CNAME"]
EXPECTED_PHONE = "0330 236 9980"
EXPECTED_EMAIL = "info@netsafeit.co.uk"

# Collected failure messages; empty at the end means success
failures = []


def fail(message):
    """Record a failed check so all problems are reported in one run."""
    failures.append(message)


class PageInspector(HTMLParser):
    """Walks an HTML page and records the tags and attributes we care about."""

    def __init__(self):
        super().__init__()
        self.html_lang = None
        self.title_text = ""
        self.in_title = False
        self.meta_names = set()
        self.ids = set()
        self.local_references = []   # paths to other files in the site
        self.anchor_links = []       # "#something" links within the page
        self.images_missing_alt = 0

    def handle_starttag(self, tag, attrs):
        attributes = dict(attrs)

        if tag == "html":
            self.html_lang = attributes.get("lang")
        if tag == "title":
            self.in_title = True
        if tag == "meta" and "name" in attributes:
            self.meta_names.add(attributes["name"].lower())
        if "id" in attributes:
            self.ids.add(attributes["id"])
        # alt="" is allowed: it is the correct way to mark a decorative image
        if tag == "img" and "alt" not in attributes:
            self.images_missing_alt += 1

        # Any attribute that can point at another file
        for attribute_name in ("href", "src"):
            target = attributes.get(attribute_name)
            if not target:
                continue
            if target.startswith("#"):
                self.anchor_links.append(target[1:])
            elif not re.match(r"^(https?:|mailto:|tel:|//)", target):
                # Strip any "#fragment" or "?query" before checking the file
                self.local_references.append(re.split(r"[#?]", target)[0])

    def handle_endtag(self, tag):
        if tag == "title":
            self.in_title = False

    def handle_data(self, data):
        if self.in_title:
            self.title_text += data


def check_required_files():
    for relative_path in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(PROJECT_ROOT, relative_path)):
            fail(f"Missing required file: {relative_path}")


def check_cname():
    cname_path = os.path.join(PROJECT_ROOT, "CNAME")
    if os.path.isfile(cname_path):
        with open(cname_path, encoding="utf-8") as cname_file:
            domain = cname_file.read().strip()
        if domain != EXPECTED_DOMAIN:
            fail(f"CNAME contains '{domain}', expected '{EXPECTED_DOMAIN}'")


def find_html_pages():
    """Return paths (relative to the project root) of every .html file."""
    pages = []
    for folder, _subfolders, files in os.walk(PROJECT_ROOT):
        if "/." in folder or "/tests" in folder:
            continue  # skip .git and the tests folder
        for file_name in files:
            if file_name.endswith(".html"):
                full_path = os.path.join(folder, file_name)
                pages.append(os.path.relpath(full_path, PROJECT_ROOT))
    return sorted(pages)


def check_page(relative_path):
    full_path = os.path.join(PROJECT_ROOT, relative_path)
    with open(full_path, encoding="utf-8") as page_file:
        page_source = page_file.read()

    inspector = PageInspector()
    inspector.feed(page_source)

    if not inspector.html_lang:
        fail(f"{relative_path}: <html> has no lang attribute")
    if not inspector.title_text.strip():
        fail(f"{relative_path}: missing or empty <title>")
    if "description" not in inspector.meta_names:
        fail(f"{relative_path}: missing <meta name=\"description\">")
    if "viewport" not in inspector.meta_names:
        fail(f"{relative_path}: missing <meta name=\"viewport\">")
    if inspector.images_missing_alt:
        fail(f"{relative_path}: {inspector.images_missing_alt} <img> without alt text")

    # Local file references are resolved relative to the page's own folder,
    # or to the site root if they start with "/"
    page_folder = os.path.dirname(full_path)
    for reference in inspector.local_references:
        if reference.startswith("/"):
            target = os.path.join(PROJECT_ROOT, reference.lstrip("/"))
        else:
            target = os.path.join(page_folder, reference)
        if os.path.isdir(target):
            target = os.path.join(target, "index.html")
        if not os.path.exists(target):
            fail(f"{relative_path}: broken link to '{reference}'")

    for anchor in inspector.anchor_links:
        if anchor and anchor not in inspector.ids:
            fail(f"{relative_path}: link to '#{anchor}' but no element has that id")

    return page_source


def check_business_details(home_page_source):
    for expected_text in (EXPECTED_PHONE, EXPECTED_EMAIL):
        if expected_text not in home_page_source:
            fail(f"index.html: expected to find '{expected_text}'")


def check_no_secrets():
    """Very simple scan for things that look like credentials."""
    suspicious = re.compile(
        r"(password\s*[=:]\s*\S+|api[_-]?key\s*[=:]\s*\S+|BEGIN (RSA |OPENSSH )?PRIVATE KEY)",
        re.IGNORECASE,
    )
    for folder, _subfolders, files in os.walk(PROJECT_ROOT):
        if "/." in folder or "/tests" in folder:
            continue
        for file_name in files:
            full_path = os.path.join(folder, file_name)
            try:
                with open(full_path, encoding="utf-8") as text_file:
                    if suspicious.search(text_file.read()):
                        fail(f"{os.path.relpath(full_path, PROJECT_ROOT)}: looks like it contains a secret")
            except UnicodeDecodeError:
                pass  # binary file such as an image, skip it


def main():
    check_required_files()
    check_cname()

    home_page_source = ""
    pages = find_html_pages()
    for page in pages:
        source = check_page(page)
        if page == "index.html":
            home_page_source = source

    check_business_details(home_page_source)
    check_no_secrets()

    print(f"Checked {len(pages)} page(s): {', '.join(pages) or 'none'}")
    if failures:
        print(f"\nFAILED - {len(failures)} problem(s):")
        for message in failures:
            print(f"  - {message}")
        sys.exit(1)
    print("All checks passed.")


if __name__ == "__main__":
    main()
