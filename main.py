import requests
from lxml import html
from calendar import Calendar
from icalendar import vCalAddress, vText
from datetime import datetime
import pytz

response = requests.get(
    "https://liquipedia.net/starcraft2/api.php?action=parse&format=json&page=Liquipedia:Upcoming_and_ongoing_matches",
    {
        "Accept-Encoding": "gzip",
        "User-Agent": "Sc2Calendar/developer (mxboucher@gmail.com)",
    }
)

if response.status_code == 200:
    page = html.fromstring(response.json()["parse"]["text"]["*"])
else:
    print(response.status_code)

cal = Calendar()
cal.add("prodid", "-//Sc2Calendar//mxm.dk//")
cal.add("version", "2.0")

matches = page.cssselect(".infobox_matches_content")
for match in matches:
    selected_match = match.cssselect("[title='Serral'], [title='Reynor']")
    if selected_match:
        teamleft = match.cssselect(".team-left span[style='white-space:pre'] a")[0].text # Clem
        teamright = match.cssselect(".team-right span[style='white-space:pre'] a")[0].text # Reynor
        format = match.cssselect(".versus abbr")[0].text # Bo5
        time = match.cssselect("[data-timestamp]")[0].text # July 12, 2020 - 16:30 (UTC always)
        tournament = match.cssselect(".matchticker-tournament-name a")[0].text # DH Masters Summer: EU
        event = Event()
        event.add("summary", )
