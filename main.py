import requests
from lxml import html
import icalendar

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

matches = page.cssselect(".infobox_matches_content")
important_matches = []
for match in matches:
    selected_match = match.cssselect("[title='Serral'], [title='Reynor']")
    if selected_match:
        teamleft = match.cssselect(".team-left") # Serral
        teamright = match.cssselect(".team-right") # Reynor
        format = match.cssselect(".versus abbr") # Bo9
        time = match.cssselect(".timer-object-date") # July 14, 2020 - 20:00
        timezone = match.cssselect("abbr [data-tz]")["data-tz"] # +2:00


