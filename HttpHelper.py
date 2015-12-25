import requests
import threading
import Queue
import TvShow
import json


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
            b = 1
            self.que.put(url)

    def get_tv_shows(self):
        while not self.que.empty():
            url = self.que.get()
            r = requests.get(url, timeout=10)
            if r.status_code == 200:
                self.shows = self.get_shows_objects(json.loads(r.text))
                self.que.task_done()

    ##############################################################################

    def get_tv_shows_for_date(self):
            while not self.que.empty():
                url = self.que.get()
                r = requests.get(url, timeout=10)
                if r.status_code == 200:
                    self.shows = self.get_shows_objects(json.loads(r.text))
                    self.que.task_done()



#################################################
    def get_episode(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return json.loads(r.text)
        return None


    def get_shows_objects_from_session(self, results):
        shows = []
        for json_show in results:
            show = TvShow.TvShow().json_to_object(json_show)
            shows.append(show)
        return shows

    def get_shows_objects(self, results):
        shows = []
        for json_show in results:
            show = TvShow.TvShow().json_to_object(json_show)
            shows.append(show)
        return shows


    def start_minions(self,target):
        for i in range(5):
            thread = threading.Thread(target=target)
            thread.start()
        self.que.join()


        # start = time.clock()

#




