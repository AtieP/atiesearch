import time
import json
import requests
import sys
import os
from bs4 import BeautifulSoup as BS

if len(sys.argv) < 2:
    print("Usage: python spider.py [site]")
    sys.exit(1)

with open("sites.json", "r") as f:
    sites = json.load(f)

with open("sites.json", "w") as f:
    # Crawl thru the website, searching for other <a> tags
    # First save the inputted site
    base_site_url = sys.argv[1]
    base_site_url.rstrip("/")
    base_site_content = requests.get(base_site_url).text
    base_site_title = BS(base_site_content, "html.parser").find("title")
    if base_site_title:
        base_site_title = base_site_title.string
    if not base_site_title:
        base_site_title = base_site_url

    base_site_description = BS(base_site_content, "html.parser").find("meta", attrs={"name": "description"})
    if base_site_description:
        base_site_description = base_site_description["content"]
    if not base_site_description:
        base_site_description = BS(base_site_content, "html.parser").find("meta", property="og:description")
        if base_site_description:
            base_site_description = base_site_description["content"]
        if not base_site_description:
            base_site_description = "No description available."

    base_site_keywords = BS(base_site_content, "html.parser").find("meta", attrs={"name": "keywords"})
    if base_site_keywords:
        base_site_keywords = base_site_keywords["content"].strip().split(",")
    else:
        base_site_keywords = []

    sites[base_site_title.lower()] = {
        "title": base_site_title,
        "description": base_site_description.strip(),
        "url": base_site_url,
        "keywords": base_site_keywords
    }

    try:
        # Now search for sites
        for site_url in BS(base_site_content, "html.parser").find_all("a", href=True):
            time.sleep(0.5)
            site_url = site_url["href"].lstrip("/")
            if site_url.startswith("http"):
                pass
            elif site_url.startswith("ftp://"):
                continue
            else:
                site_url = base_site_url + "/" + site_url

            print(site_url)
            try:
                site = requests.get(site_url)
                print(site.status_code)
                if site.status_code != 200:
                    continue
                site_content = site.text
            except requests.exceptions.InvalidURL:
                continue
            except requests.exceptions.ConnectionError:
                continue

            site_title = BS(site_content, "html.parser").find("title")
            if site_title:
                site_title = site_title.string
            if not site_title:
                site_title = site_url

            site_description = BS(site_content, "html.parser").find("meta", attrs={"name": "description"})
            if site_description:
                site_description = site_description["content"]
            if not site_description:
                site_description = BS(site_content, "html.parser").find("meta", property="og:description")
                if site_description:
                    site_description = site_description["content"]
                if not site_description:
                    site_description = "No description available."

            site_keywords = BS(site_content, "html.parser").find("meta", attrs={"name": "keywords"})
            if site_keywords:
                site_keywords = site_keywords["content"].strip().split(",")
            else:
                site_keywords = []

            sites[site_title.lower()] = {
                "title": site_title,
                "description": site_description.strip(),
                "url": site_url,
                "keywords": site_keywords
            }
    except KeyboardInterrupt:
        pass

    json.dump(sites, f, indent=4)