#!/usr/bin/env python3
import sys
import urllib.parse
import subprocess
import re


def open_in_browser(url):
    # List of domains to open in Microsoft Edge
    edge_domains = [r"microsoft\.com$", r"sharepoint\.com$", r"outlook\.com$"]

    # Parse the URL to extract the domain
    parsed_url = urllib.parse.urlparse(url)
    domain = parsed_url.netloc.lower()
    if domain.startswith("www."):
        domain = domain[4:]

    # Check if the domain matches any of the Edge domains
    for edge_domain in edge_domains:
        if re.search(edge_domain, domain):
            # Open in Microsoft Edge
            subprocess.run(["microsoft-edge", url])
            return

    # Open in the default browser
    # subprocess.run(['xdg-open', url])
    subprocess.run(["brave-browser", url])


if __name__ == "__main__":
    # from pathlib import Path
    # with open(Path(__file__).parent.joinpath("log.txt"), mode="a+") as f:
    #     f.write(f"{sys.argv}")
    if len(sys.argv) < 2:
        print("Usage: url_dispatcher.py <URL>")
        sys.exit(1)
    url = sys.argv[1]
    open_in_browser(url)
