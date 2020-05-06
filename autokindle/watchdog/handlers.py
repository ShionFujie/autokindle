from watchdog.events import RegexMatchingEventHandler


def FileHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*[.](epub|pdf|mobi)"])
    return handler


def KindleConnectionHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    return handler
