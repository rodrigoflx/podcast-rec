class Episode:
    def __init__(self, itunesId, title, medialink):
        self.title = title
        self.itunesID = itunesId
        self.medialink = medialink

    def unpack(self):
        return (self.itunesId, self.title, self.medialink)
