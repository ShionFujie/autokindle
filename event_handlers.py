from watchdog.events import RegexMatchingEventHandler


def EpubFilesHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
    return handler


def push_new_files(watchdog_handler):
    def _(observer, scheduler):
        def on_created(event):
            observer.on_next(dict(type='NEW_FILE', path=event.src_path))
        watchdog_handler.on_created = on_created
    return _


def KindleConnectionHandler():
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    return handler


def push_connection_statuses(watchdog_handler):
    def _(observer, scheduler):
        def on_created(_):
            observer.on_next(dict(type='CONNECTED'))
        def on_deleted(_):
            observer.on_next(dict(type='DISCONNECTED'))
        watchdog_handler.on_created = on_created
        watchdog_handler.on_deleted = on_deleted
    return _
