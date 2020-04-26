from watchdog.events import RegexMatchingEventHandler


def EpubFilesHandler(on_new_file):
    def on_created(event):
        on_new_file(event.src_path)
    handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
    handler.on_created = on_created
    return handler


def KindleConnectionHandler(on_connect, on_disconnect):
    def on_created(_):
        on_connect()
    def on_deleted(_):
        on_disconnect()
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    handler.on_created = on_created
    handler.on_deleted = on_deleted
    return handler
