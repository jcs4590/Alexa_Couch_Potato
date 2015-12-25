import HttpHelper
import  Enums
request_helper = HttpHelper.HttpHelper()
request_helper.add_urls([Enums.API_URLS["show_search"].format("transparent")])
request_helper.start_minions(request_helper.get_tv_shows)
print(request_helper.shows)
shows = request_helper.shows
