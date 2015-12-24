class ListingChannel:
    def __init__(self):
        self.HD = None
        self.Name = None
        self.Number = None
        self.Sort = None
        self.NetworkId = None
        self.FullName = None
        self.FilterNumber = None
        self.SourceId = None
        self.Logo = None


def json_to_object(json):
    channel = ListingChannel()

    for key, value in json.items():
        if getattr(channel, key) is None:
            setattr(channel, key, value)
    return channel
