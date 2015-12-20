import requests
import xml.etree.ElementTree as ET
from threading import Thread
import time
import Queue
import urlparse
from TvShow import TvShow
import json
SHOWS_WITH_NUMBERS = \
    {
        "the hundred": "The 100",
        "two broke girls": "2 Broke Girls",
        "hundred deeds for eddie mcdowd": "100 Deeds for Eddie McDowd",
        "hundred questions": "100 Questions",
        "hundred Winners": "100 Winners",
        "a thousand ways to die": "1000 Ways to Die",
        "ten things i hate about you": "10 Things I Hate About You",
        "one hundred one ways to leave a gameshow": "101 Ways to Leave a Gameshow",
        "twelve ounce mouse": "12 oz. Mouse",
        "fifteen love": "15/Love",
        "ten eight officers on duty": "10-8: Officers on Duty",
        "sixteen and pregnant": "16 and Pregnant",
        "eighteen to life": "18 to Life",
        "one hundred one dalmatians": "101 Dalmatians",
        "two d tv": "2DTV",
        "the twentieth century": "The 20th Century",
        "twenty one jump street": "21 Jump Street",
        "two hundred twenty seven": "227",
        "twenty four": "24",
        "twenty six men": "26 Men",
        "three pounds": "3 lbs",
        "three south": "3 South",
        "thirty rock": "30 Rock",
        "thirty seconds to fame": "30 Seconds to Fame",
        "thirty minutes": "31 Minutes",
        "third rock from the sun": "3rd Rock from the Sun",
        "the four thousand four hundred": "The 4400",
        "forty eight hours": "48 Hours",
        "fifty cent the money and the power": "50 Cent: The Money and the Power",
        "fifty fifty": "50/50",
        "sixty minutes": "60 Minutes",
        "six teen": "6teen",
        "the sixty four thousand dollar question": "The $64,000 Question",
        "sixty four zoo lane": "64 Zoo Lane",
        "six hundred sixty six park avenue": "666 Park Avenue",
        "seventh heaven": "7th Heaven",
        "seventy seven sunset strip": "77 Sunset Strip",
        "eight simple rules": "8 Simple Rules",
        "nine o two 1 o": "90210",
        "nine to five": "9 to 5"
    }


class HttpHelper:
    USER_ID = 224869
    HASH_KEY = "08262a6526df118d4d233879194e1e91"

    def __init__(self):
        self.running = True
        self.shows = []
        self.que = Queue.LifoQueue()

    # def get_tv_show_ids(self, tv_show_name):
    #     url = "http://next-episode.net/api/iphone/v351/services.php?service=search&query={}".format(tv_show_name) + \
    #           "&user_id={}&hash_key={}&time=-21600&myshows=0&offset=0&calendardays=0".format(self.USER_ID,
    #                                                                                          self.HASH_KEY)
    #     print("VEGAS!! -- {}".format(url))
    #     r = requests.get(url)
    #
    #     # successful request
    #     if r.status_code == 200:
    #         root = ET.fromstring(r.text)
    #         # get show ids
    #         for child in root.iter("showid"):
    #             self.shows[child.text] = None
    #         self.setup_urls()
    def add_urls(self, urls):
        for url in urls:
            self.que.put(url)
        self.start_minions()

    def get_tv_shows(self):
        while not self.que.empty():
            url = self.que.get()
            r = requests.get(url)
            if r.status_code == 200:
                self.shows = self.get_shows_objects(json.loads(r.text))
                self.que.task_done()
    def get_next_episode(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.text)
        return None

    def shows(self):
        return self.shows
    def get_shows_objects(self, results):
        shows = []
        for item in results:
            json_show = item
            show = TvShow().json_to_object(json_show["show"])
            shows.append(show)
        return shows


    def start_minions(self):
        for i in range(5):
            thread = Thread(target=self.get_tv_shows)
            thread.start()
        self.que.join()


        # start = time.clock()


helper = HttpHelper()
helper.add_urls(["http://api.tvmaze.com/search/shows?q=girl"])
helper.start_minions()
for show in helper.shows:
    print(show)


#print helper.shows
# r = requests.get("http://api.tvmaze.com/search/shows?q=2%20broke%20girls")
# if r.status_code == 200:
#     blah = json.loads(r.text)[0]["show"]
#     #print blah
#     show = TvShow().json_to_object(blah)
#     print show.image

