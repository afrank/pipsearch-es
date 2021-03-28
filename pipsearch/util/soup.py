
import re
from bs4 import BeautifulSoup
import datetime

def parse_pkg_page(page):
    
    out = {}
    out["project_links"] = {}
    out["meta"] = {}
    out["releases"] = []
    out["maintainers"] = []
    out["latest_version"] = ""
    out["summary"] = ""
    out["description"] = ""

    #page = open(filename).read()

    soup = BeautifulSoup(page, 'html.parser')

    # get the latest version
    try:
        out["latest_version"] = soup.find('h1', class_='package-header__name').get_text().strip().split(' ')[1].strip()
    except:
        out["project_links"] = []
        out["meta"] = []
        return out

    # get the summary
    out["summary"] = soup.find('meta', property="og:description")["content"]

    sidebars = soup.find_all('div', class_="sidebar-section")

    for sidebar in sidebars:
        title = sidebar.find('h3', class_='sidebar-section__title').get_text()
        if title == "Project links":
            for link in sidebar.find_all('a'):
                href = link["href"]
                content = link.get_text().strip()
                out["project_links"][content] = href
        elif title == "Meta":
            for p in sidebar.find_all('p'):
                ret = re.match('<p><strong>(.*):</strong> (.*)</p>', str(p))
                if not ret:
                    continue
                key = ret.group(1)
                val = ret.group(2)
                out["meta"][key] = val
        elif title == "Maintainers":
            for a in sidebar.find_all('a'):
                href = a["href"]
                name = a.get("aria-label","")
                out["maintainers"] += [ href ]

    out["project_links"] = list(out["project_links"].items())
    out["meta"] = list(out["meta"].items())

    out["maintainers"] = list(set(out["maintainers"]))
    try:
        out["description"] = soup.find('div', class_='project-description').get_text() # TODO: store html or plaintext?
    except:
        out["description"] = ""

    # Release history
    for release in soup.find_all('a', class_='release__card'):
        ts = release.find('time')['datetime']
        dt = datetime.datetime.strptime(ts, '%Y-%m-%dT%H:%M:%S+0000')
        ts = int(dt.timestamp() * 1000)
        vers = release.find('p', class_='release__version').get_text().strip()
        out["releases"] += [ [vers, ts] ]

    return out
