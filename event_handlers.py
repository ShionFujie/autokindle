from watchdog.events import RegexMatchingEventHandler


def EpubFilesHandler():
    def on_created(event):
        src_path = event.src_path
        print(f"[CREATED] {src_path}")
    handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
    handler.on_created = on_created
    return handler


def KindleConnectionHandler():
    def on_any_event(event):
        type = event.event_type
        src_path = event.src_path
        print(f"[{type}] {src_path}")
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    handler.on_any_event = on_any_event
    return handler
