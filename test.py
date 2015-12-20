import HttpHelper
helper = HttpHelper.HttpHelper()
helper.add_urls(["http://api.tvmaze.com/search/shows?q=empire"])
helper.start_minions(helper.get_tv_shows)
for show in helper.shows:
    print("<p>Playing on {} at {} is {}</p> ".format(show.network["name"], show.name))