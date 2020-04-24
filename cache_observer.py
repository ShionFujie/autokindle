import os
import re
from event_handlers import EpubFilesHandler
from observer_runner import ObserverRunner
from watchdog.observers import Observer


observer = Observer()
observer.schedule(
    path=os.path.join(os.environ["HOME"], "Desktop", "To Be Synced"),
    event_handler=EpubFilesHandler()
)
ObserverRunner().runObserver(observer)
