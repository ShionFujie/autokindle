import os
from observer_runner import ObserverRunner
from event_handlers import EpubFilesHandler, KindleConnectionHandler
from watchdog.observers import Observer


def on_new_file(path):
    print("[NEW_FILE] %s" % path)


def on_connect():
    print('[CONNECT]')


def on_disconnect():
    print('[DISCONNECT]')


observer = Observer()
observer.schedule(
    path=os.path.join(os.environ["HOME"], "Desktop", "To Be Synced"),
    event_handler=EpubFilesHandler(on_new_file)
)
observer.schedule(
    path='/Volumes',
    event_handler=KindleConnectionHandler(on_connect, on_disconnect)
)
ObserverRunner().runObserver(observer)
