#!/usr/bin/env python3
"""
~/.local/bin/brave-browser-router

Single entry point for all browser invocations. Routes URLs to Zen or Brave
based on domain rules. Handles both xdg-open style (plain URL) and
Chromium/Omarchy style (--app=URL) invocations.
"""

import sys
import re
import subprocess
from urllib.parse import urlparse

# ---------- Configuration ----------

ZEN = "zen-browser"
BRAVE = "brave"
DEFAULT_BROWSER = ZEN

# (pattern, browser) — first match wins
DOMAIN_ROUTES = [
    # Microsoft 365 → Brave
    (r'(^|\.)(microsoft|office|sharepoint|outlook|live|office365)\.com$', BRAVE),
    (r'(^|\.)teams\.microsoft\.com$', BRAVE),
    (r'(^|\.)login\.microsoftonline\.com$', BRAVE),

    # DRM streaming → Brave (Widevine)
    (r'(^|\.)(netflix|spotify|hulu|max|hbomax|disneyplus|primevideo|audible|peacocktv|paramountplus)\.com$', BRAVE),
    (r'(^|\.)apple\.com$', BRAVE),  # Apple Music / TV+
]

# ---------- Core logic ----------

def pick_browser(url):
    """Return the browser binary to use for this URL."""
    try:
        domain = urlparse(url).netloc.lower().removeprefix("www.")
    except Exception:
        return DEFAULT_BROWSER
    for pattern, browser in DOMAIN_ROUTES:
        if re.search(pattern, domain):
            return browser
    return DEFAULT_BROWSER

def parse_args(argv):
    """
    Extract URL, webapp mode, and passthrough flags from args.
    Handles both styles:
      - plain URL:       browser-router https://foo.com
      - Chromium --app=: browser-router --app=https://foo.com --class=Foo
    """
    url = None
    webapp = False
    passthrough = []

    for arg in argv:
        if arg.startswith("--app="):
            url = arg[len("--app="):]
            webapp = True
        elif arg.startswith(("http://", "https://", "file://", "about:")):
            url = arg
        else:
            passthrough.append(arg)

    return url, webapp, passthrough

def launch(binary, url=None, webapp=False, passthrough=None):
    """Build and exec the browser command via uwsm for proper session integration."""
    cmd = ["uwsm", "app", "--", binary]

    if webapp and binary == BRAVE and url:
        cmd.append(f"--app={url}")
        url = None  # --app consumes the URL

    if passthrough:
        cmd.extend(passthrough)
    if url:
        cmd.append(url)

    subprocess.Popen(cmd)

def main():
    url, webapp, passthrough = parse_args(sys.argv[1:])

    # No URL → launch default browser interactively
    if not url:
        launch(DEFAULT_BROWSER, passthrough=passthrough)
        return

    binary = pick_browser(url)

    # Webapp mode requires Chromium (Zen/Firefox can't do --app)
    if webapp and binary != BRAVE:
        binary = BRAVE

    launch(binary, url=url, webapp=webapp, passthrough=passthrough)

if __name__ == "__main__":
    main()
