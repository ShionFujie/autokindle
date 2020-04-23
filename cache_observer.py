import os
import re
import time
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler

target = os.path.join(os.environ["HOME"], "Desktop", "To Be Synced")

class CacheObserver:
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
        def on_created(event):
            src_path = event.src_path
            print(f"[CREATED] {src_path}")
        handler = RegexMatchingEventHandler(regexes=[r".*[.]epub"])
        handler.on_created = on_created
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

CacheObserver().run()