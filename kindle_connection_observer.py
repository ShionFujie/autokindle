import os
import re
import time
from observer_runner import ObserverRunner
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

def KindleConnectionObserver(path):
    observer = Observer()
    observer.schedule(event_handler=_get_kindle_connection_handler(), path=path)
    return observer

def _get_kindle_connection_handler():
    def on_any_event(event):
        type = event.event_type
        src_path = event.src_path
        print(f"[{type}] {src_path}")
    handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
    handler.on_any_event = on_any_event
    return handler

ObserverRunner().runObserver(KindleConnectionObserver(path='/Volumes'))