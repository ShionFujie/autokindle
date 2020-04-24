import os
from observer_runner import ObserverRunner
from event_handlers import EpubFilesHandler, KindleConnectionHandler
from watchdog.observers import Observer

observer = Observer()
observer.schedule(
    path=os.path.join(os.environ["HOME"], "Desktop", "To Be Synced"),
    event_handler=EpubFilesHandler()
)
observer.schedule(
    path='/Volumes',
    event_handler=KindleConnectionHandler()
)
ObserverRunner().runObserver(observer)
