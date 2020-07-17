import redis as redis
import requests
from flask import Flask, request, make_response
from icalendar import Calendar, Event
from lxml import html
from datetime import datetime
import cssselect

app = Flask(__name__)

# Cache object represents Redis connection to cache Liquipedia API calls
class Cache:

    def __init__(self):
        self.client = self.connect()
        self.EXPIRE_TIME = 300

    def connect(self):
        try:
            client = redis.Redis(
                host="127.0.0.1",
                port=6379,
                db=0,
                socket_timeout=5,
            )
            ping = client.ping()
            if ping is True:
                return client
            else:
                return False
        except redis.AuthenticationError:
            print("Authentication to Redis failed.")


    def get_from_cache(self):
        data = self.client.get("data")
        if data is not None:
            return data
        else:
            data = self.get_data_from_liquipedia()
            if (data != False):
                self.client.setex("data", self.EXPIRE_TIME, data)
                return data
            else:
                print("API Request failed and cache inexistant.")

    def set_to_cache(self, value):
        return self.client.setex("data", self.EXPIRE_TIME, value)

    def get_data_from_liquipedia(self):
        # request to Liquipedia API
        response = requests.get(
            "https://liquipedia.net/starcraft2/api.php?action=parse&format=json&page=Liquipedia:Upcoming_and_ongoing_matches",
            {
                "Accept-Encoding": "gzip",
                "User-Agent": "Sc2Calendar/developer (mxboucher@gmail.com)",
            }
        )
        # parsing html
        if response.status_code == 200:
            return response.json()["parse"]["text"]["*"]
        else:
            print(response.status_code)
            return False

@app.route('/', methods=["GET"])
def main():
    # request = "Reynor,Serral"
    if "players" in request.args:
        players = request.args.get("players").split(",") # ["Serral", "Reynor"]
    else:
        players = ["Serral", "Reynor"]
    for i in range(0, len(players)):
        players[i] = "[title='" + players[i] + "']"
    selectorString = ', '.join(players) # [title='Serral'], [title='Reynor']
    cache = Cache()
    page = html.fromstring(cache.get_from_cache())
    # scrapping html to create icalendar
    cal = Calendar()
    cal.add("prodid", "-//Sc2Calendar//en//")
    cal.add("version", "2.0")
    matches = page.cssselect(".infobox_matches_content")
    for match in matches:
        selected_match = match.cssselect(selectorString)
        if selected_match:
            teamleft = match.cssselect(".team-left a")[0].text # Clem
            teamright = match.cssselect(".team-right span:not(.flag):not(.team-template-image):not(.team-template-team-short) a")[0].text # Reynor
            match_format = match.cssselect(".versus abbr")[0].text # Bo5
            time = int(match.cssselect("[data-timestamp]")[0].attrib['data-timestamp']) # 1596043800 (UTC always)
            tournament = match.cssselect(".match-filler div div a")[0].text # DH Masters Summer: EU
            event = Event()
            event.add("summary", teamleft + " - " + teamright)
            event.add("uid", (str(time) + teamleft + teamright + tournament + "@sc2calendar").replace(" ", ""))
            event.add("dtstamp", datetime.now())
            event.add("dtstart", datetime.fromtimestamp(time))
            event.add("dtend", datetime.fromtimestamp(time+3600))
            event.add("location", tournament + " (" + match_format + ")")
            cal.add_component(event)
    response = make_response(cal.to_ical())
    response.headers["Content-Disposition"] = "attachment; filename=sc2calendar.ics"
    return response


if __name__ == '__main__':
    app.run()
