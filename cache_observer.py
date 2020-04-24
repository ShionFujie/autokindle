import os
import re
from observer_runner import ObserverRunner
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler


def CacheObserver(path):
    observer = Observer()
    observer.schedule(event_handler=_get_epub_files_handler(), path=path)
    return observer


def _get_epub_files_handler():
    def on_created(event):
        src_path = event.src_path
        print(f"[CREATED] {src_path}")
    handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
    handler.on_created = on_created
    return handler


target = os.path.join(os.environ["HOME"], "Desktop", "To Be Synced")
ObserverRunner().runObserver(CacheObserver(target))
