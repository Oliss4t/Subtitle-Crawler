class OpenSubtitleSearchError(Exception):
    """
    Exception raised for errors in the openSubtitleSearch if the returned status is not 200
    """
    def __init__(self, message="not 200"):
        self.message = 'The openSubtitleSearch returned a status that is: ' + message
        super().__init__(self.message)


class OpenSubtitleDownloadError(Exception):
    """
    Exception raised for errors in the OpenSubtitleDownload if the returned status is not 200
    """
    def __init__(self, message="not 200"):
        self.message = 'The OpenSubtitleDownloadError returned a status that is: ' + message
        super().__init__(self.message)

class OpenSubtitlSaveFilesError(Exception):
    """
    An Exception occured during OpenSubtitlSaveFilesError
    """
    def __init__(self, message=None):
        self.message = 'An OpenSubtitlSaveFilesError occured: ' + "while saving the file" if message is None else message
        super().__init__(self.message)

class ImdbDownloadError(Exception):
    """
    An Exception occured during ImdbDownloadError
    """
    def __init__(self, message=None):
        self.message = 'An OpenSubtitlSaveFilesError occured: ' + "not 200" if message is None else message
        super().__init__(self.message)

class ImdbSaveInfoError(Exception):
    """
    An Exception occured during ImdbSaveInfoError
    """
    def __init__(self, message=None):
        self.message = 'An ImdbSaveInforError occured: ' + "while saving the info" if message is None else message
        super().__init__(self.message)

class ImdbSaveImageError(Exception):
    """
    An Exception occured during ImdbSaveImageError
    """
    def __init__(self, message=None):
        self.message = 'An ImdbSaveImageError occured: ' + "while saving the image" if message is None else message
        super().__init__(self.message)

