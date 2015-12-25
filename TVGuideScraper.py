import requests
import threading
import Queue
import json
import ListingChannel
import DBHelper
import TvProgram
import time, datetime, calendar
from pytz import timezone

import sys, curses

PROVIDER_IDS = \
    {
        "DirectvLosAngeles": "889053",
        "DirectvFargo": "76967"
    }

TV_GUIDE_URLS = \
    {
        "shows_for_start_date": "http://mobilelistings.tvguide.com/Listingsweb/"
                                "ws/rest/schedules/{}/start/{}/duration/720?formattype=json",
        "provides_for_zip_code": "http://mobilelistings.tvguide.com/Listingsweb/ws/rest/serviceproviders/zipcode/{}?formattype=json"
    }
UTC_TIMES = {"3pm": 21, "11pm":5, "7am":13}


def get_guide_for_start_date(start_date):
    headers = {"User-Agent": "TVGuide/5.0 iOS/9.0.2 Manufacturer/Apple Device/iPhone8,2 Interface/Phone"}
    r = requests.get(TV_GUIDE_URLS["shows_for_start_date"].format(76967, start_date), headers=headers)
    if r.status_code == 200:
        insert_to_db(json.loads(r.text))
def get_epochs_for_days(days):
    current_date = datetime.datetime.now().replace(minute=0, second=0)
    dates = []
    dates.extend(get_epoch_for_time(current_date))
    i = 0
    while i < days:
        if current_date.day + 1 < calendar.monthrange(current_date.year, current_date.month)[1]:
            current_date = current_date.replace(day=current_date.day+1, minute=0, second=0)
        elif current_date.month < 12:
            current_date = current_date.replace(month=current_date.month+1, day=1, minute=0, second=0)
        else:
            current_date = current_date.replace(year=current_date.year+1, day=1, month=1, minute=0, second=0)
        dates.extend(get_epoch_for_time(current_date))
        i += 1
    return dates
def get_epoch_for_time(date):
    return [calendar.timegm(date.replace(hour=UTC_TIMES["7am"], minute=0, second=0).timetuple()),
            calendar.timegm(date.replace(hour=UTC_TIMES["3pm"], minute=0, second=0).timetuple()),
            calendar.timegm(date.replace(day=date.day+1, hour=UTC_TIMES["11pm"], minute=0, second=0).timetuple())]
def get_current_time_in_epoch():
    return calendar.timegm(time.gmtime())
def insert_to_db(json):
    CHANNELS_INSERTED = 0
    PROGRAMS_INSERTED = 0
    cur = DBHelper.conn.cursor()
    last_channel = None
    total = len(json)
    CHANNELS_INSERTED = total
    for index, section in enumerate(json):
        index += 1
        sys.stdout.write("\r%d%%" % index)
        percent = float(index) / total
        hashes = '#' * int(percent * 50)
        spaces = '-' * (50 - len(hashes))
        sys.stdout.write("\rPercent: [{0}] {1}%".format(hashes + spaces, int(percent * 100)))
        sys.stdout.flush()
        item = section["Channel"]
        channel = ListingChannel.json_to_object(item)
        last_channel = channel.SourceId
        cur.callproc("AddChannel", [channel.Name, channel.Sort, channel.NetworkId, channel.FullName,
                                    channel.FilterNumber, channel.SourceId, 76967])

        item = section["ProgramSchedules"]
        PROGRAMS_INSERTED += len(item)
        for goods in item:
            program = TvProgram.json_to_object(goods)

            cur.callproc("AddProgram", [program.AiringAttrb,
                                        program.CatId,
                                        datetime.datetime.fromtimestamp(program.EndTime),
                                        program.ProgramId, datetime.datetime.fromtimestamp(program.StartTime),
                                        program.TVObjectId,
                                        program.TVObjectTypeId,
                                        program.Title,
                                        program.Rating,
                                        program.EpisodeTitle,
                                        program.AiringAttrib,
                                        int(program.IsSportsEvent),
                                        program.SubCatId,
                                        program.SubCatFilterNum,
                                        program.ParentProgramId,
                                        program.CatFilterNum,
                                        program.CopyText,
                                        last_channel])
            DBHelper.conn.commit()

    cur.close()
    print("\n\n ************* Results ************* \n Channels: {} \n Programs: {}\n".format(CHANNELS_INSERTED,
                                                                                              PROGRAMS_INSERTED))
##to epoch
# (datetime(2015, 12, 21, 5, 30) - datetime(1970,1,1)).total_seconds()

dates = get_epochs_for_days(3)
for date in dates:
    get_guide_for_start_date(date)
DBHelper.conn.close()




