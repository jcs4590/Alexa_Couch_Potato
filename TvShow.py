class TvShow(object):

    def __init__(self, title, genre, creator, network, status, premiered, next_episode_date, next_episode_name,
                 count_down, current_season, previous_episode_date, seasons_lasted,active):
        self.title = title
        self.genre = genre
        self.creator = creator
        self.network = network
        self.status = status
        self.premiered = premiered
        self.next_episode_date = next_episode_date
        self.next_episode_name = next_episode_name
        self.count_down = count_down
        self.current_season = current_season
        self.previous_episode_date = previous_episode_date
        self.seasons_lasted = seasons_lasted
        self.active = active
  # #  def __str__(self):
  #  #     return "Title: {} \n Genre: {} \n Creator: {} \n".format(self.title, self.genre, self.creator) + \
  #           "Network: {} \n Status: {} \n Premiered: {} \n".format(self.network, self.status, self.premiered) + \
  #           "Next Epsiode Date: {} \n ".format(self.next_episode_date) + \
  #           "Next Episode Name: {} \n Count Down: {} \n ".format(self.next_episode_name, self.count_down) + \
  #           "Current SeasonL {} \n \n \n".format(self.current_season)
  #
