import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

target = '/Volumes'

class KindleConnectionObserver:
    def __init__(self):
        pass
    
    def run(self):
        observer = self.get_observer(target)
        observer.start()
        print("observer started")
        self.run_until_interrupted(self.OnInterruptedListener(observer))
        observer.join()

    def get_observer(self, path):
        observer = Observer()
        observer.schedule(event_handler=self.get_epub_files_handler(), path=path)
        return observer
    
    def get_epub_files_handler(self):
        def on_any_event(event):
            type = event.event_type
            src_path = event.src_path
            print(f"[{type}] {src_path}")
        handler = RegexMatchingEventHandler(regexes=[r".*/Kindle"])
        handler.on_any_event = on_any_event
        return handler

    def run_until_interrupted(self, onInterrupted):
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            onInterrupted()

    def OnInterruptedListener(self, observer):
        def onInterrupted():
            observer.stop()
            print("observer stopped")
        return onInterrupted

KindleConnectionObserver().run()