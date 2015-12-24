import json
import HttpHelper
import datetime
import dateutil.parser

DATE_PARSER = "%A %B %-d %Y"
TIME_PARSER = "%-I %M %p"
TIME_PARSER = "%-I %M %p"
PARSER = dateutil.parser


class TvShow:
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
        self.airstamp = "Unknown"
        self.season = "Unknown"
        self.number = "Unknown"
        self.airdate = "Unknown"
        self.airtime = "Unknown"
        self.score = "Unknown"

    @staticmethod
    def json_to_object(show):
        tv_show = TvShow()
        # run through inner show content first
        if "show" in show:
            for show_key, item in show["show"].items():
                setattr(tv_show, show_key, item)

        for outer_key, outer_item in show.items():
            print outer_key, outer_item
            if outer_key == "show":
                continue
            else:
                if (getattr(tv_show, outer_key) == "Unknown"):
                    setattr(tv_show, outer_key, outer_item)

        return tv_show

    def get_current_episode_date(self):
        print self.airstamp
        date = PARSER.parse(self.airstamp)
        return "{} at {}".format(date.strftime(DATE_PARSER),
                                 date.strftime(TIME_PARSER).replace("00", ""))

    def get_current_episode_time(self):
        date = PARSER.parse(self.airstamp)
        return "{}".format(date.strftime(TIME_PARSER).replace("00", ""))

    def get_next_episode_date(self):
        if self.next_episode is None:
            if "nextepisode" in self._links:
                helper = HttpHelper.HttpHelper()
                self.next_episode = helper.get_episode(self._links["nextepisode"]["href"])
                date = PARSER.parse(self.next_episode["airstamp"])
                date = "{} at {}".format(date.strftime(DATE_PARSER), date.strftime(TIME_PARSER).replace("00", ""))
                return date
            else:
                None

    def get_prev_episode_date(self):
        if self.prev_episode is None:
            if "previousepisode" in self._links:
                helper = HttpHelper.HttpHelper()
                self.prev_episode = helper.get_episode(self._links["previousepisode"]["href"])
                date = PARSER.parse(self.prev_episode["airstamp"])
                date = "{} at {}".format(date.strftime(DATE_PARSER), date.strftime(TIME_PARSER).replace("00", ""))
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
