import HttpHelper
helper = HttpHelper.HttpHelper()
helper.add_urls(["http://api.tvmaze.com/schedule?country=US&date=2015-12-20"])
helper.start_minions(helper.get_tv_shows)
for show in helper.shows:
    print("<p>Playing on {} at {} is {}</p> ".format(show.network["name"], show.get_current_episode_date(),show.name))