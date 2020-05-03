from watchdog.events import RegexMatchingEventHandler


def EpubFilesHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
    return handler


def KindleConnectionHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    return handler
