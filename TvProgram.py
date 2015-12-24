class TvProgram:
    def __init__(self):
        self.AiringAttrb = None
        self.CatId = None
        self.EndTime = None
        self.ProgramId = None
        self.StartTime = None
        self.TVObjectId = None
        self.TVObjectTypeId = None
        self.Title = None
        self.Rating = None
        self.EpisodeTitle = None
        self.AiringAttrib = None
        self.IsSportsEvent = None
        self.SubCatId = None
        self.TVObject = None
        self.SubCatFilterNum = None
        self.ParentProgramId = None
        self.CatFilterNum = None
        self.CopyText = None
        self.RelatedTvObjects = None

def json_to_object(json):
    program = TvProgram()

    for key, value in json.items():
        if getattr(program, key) is None:
            if isinstance(value, unicode):
                value = value.encode('ascii', 'ignore')
            setattr(program, key, value)
    return program


