import json
import HttpHelper
import datetime
import dateutil.parser

DATE_PARSER = "%A %B %d %Y"
TIME_PARSER = "%I %M %p"


class TvShow(object):
    def __init__(self):
        self.id = "Unknown"
        self.name = "Unknown"
        self.type = "Unknown"
        self.url = "Unknown"
        self.language = "Unknown"
        self.genres = "Unknown"
        self.status = "Unknown"
        self.runtime = "Unknown"
        self.premiered = "Unknown"
        self.schedule = "Unknown"
        self.rating = "Unknown"
        self.weight = "Unknown"
        self.network = "Unknown"
        self.webChannel = "Unknown"
        self.externals = "Unknown"
        self.image = "Unknown"
        self.summary = "Unknown"
        self.updated = "Unknown"
        self._links = "Unknown"
        self.next_episode = None
        self.prev_episode = None
        self.parser = dateutil.parser

    def json_to_object(self, show):
        tv_show = TvShow()
        for key, item in show.items():
            setattr(tv_show, key, item)
        return tv_show

    def get_next_episode_date(self):
        if self.next_episode is None:
            if "nextepisode" in self._links:
                helper = HttpHelper()
                self.next_episode = helper.get_next_episode(self._links["nextepisode"]["href"])
                date = self.parser.parse(self.next_episode["airstamp"])
                date = "{} at {}".format(date.strftime(DATE_PARSER), date.strftime(TIME_PARSER))
                return date
            else:
                None

    def get_prev_episode_date(self):
        if self.prev_episode is None:
            if "previousepisode" in self._links:
                helper = HttpHelper()
                self.next_episode = helper.get_next_episode(self._links["previousepisode"]["href"])
                date = self.parser.parse(self.prev_episode["airstamp"])
                date = "{} at {}".format(date.strftime(DATE_PARSER), date.strftime(TIME_PARSER))
                return date
            else:
                None

    def __repr__(self):
        return "Show(%s, %s)" % (self.id, self.name)

    def __eq__(self, other):
        if isinstance(other, TvShow):
            return ((self.id == other.id) and (self.id == other.id))
        else:
            return False

    def __ne__(self, other):
        return (not self.__eq__(other))

    def __hash__(self):
        return hash(self.__repr__())


        # #  def __str__(self):
        #  #     return "Title: {} \n Genre: {} \n Creator: {} \n".format(self.title, self.genre, self.creator) + \
        #           "Network: {} \n Status: {} \n Premiered: {} \n".format(self.network, self.status, self.premiered) + \
        #           "Next Epsiode Date: {} \n ".format(self.next_episode_date) + \
        #           "Next Episode Name: {} \n Count Down: {} \n ".format(self.next_episode_name, self.count_down) + \
        #           "Current SeasonL {} \n \n \n".format(self.current_season)
        #
