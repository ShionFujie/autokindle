import os
import subprocess
from store import Store
from observer_runner import ObserverRunner
from event_handlers import EpubFilesHandler, push_new_files, KindleConnectionHandler, push_connection_statuses
import rx
from rx import operators
from watchdog.observers import Observer


class State:
    def __init__(self, paths=[], is_connected=False):
        self.paths = paths
        self.is_connected = is_connected

    def is_idle(self):
        return not self.paths and not self.is_connected

    def needs_sync(self):
        return self.paths and not self.is_connected

    def awaits_files(self):
        return not self.paths and self.is_connected

    def is_syncing(self):
        return self.paths and self.is_connected

    def copy(self, **updates):
        return State(**{**self.__dict__, **updates})


def reducer(state=State(), action=None):
    if action is None:
        return state
    if action['type'] == 'NEW_FILE':
        return state.copy(paths=[*state.paths, action['path']])
    elif action['type'] == 'CONNECTED':
        return state.copy(is_connected=True)
    elif action['type'] == 'DISCONNECTED':
        return state.copy(is_connected=False)
    else:
        return state


store = Store(reducer)


def on_each():
    print(store.getState().__dict__)


store.subscribe(on_each)


def mapToConvertedFile(new_file):
    def change_extension_to_epub(path):
        return f"{os.path.splitext(path)[0]}.epub"
    def push_converted_files(observer, scheduler):
        src_path = new_file['path']
        subprocess.run(
            [os.path.join(os.environ["HOME"], "Desktop", "room of machinery", "bin", "kindlegen"), src_path], 
            cwd=os.path.join(os.environ["HOME"], "Desktop", "To Be Synced")
        )
        subprocess.run(['rm', src_path])
        observer.on_next({**new_file, **{'path': change_extension_to_epub(src_path)}})
        observer.on_completed()
    return rx.create(push_converted_files)


observer = Observer()
epub_handler = EpubFilesHandler()
kindle_handler = KindleConnectionHandler()
new_files = rx.create(push_new_files(epub_handler)).pipe(
    operators.flat_map(mapToConvertedFile)
)
connection_statuses = rx.create(push_connection_statuses(kindle_handler))
rx.merge(new_files, connection_statuses).subscribe(
    lambda action: store.dispatch(action))
observer.schedule(
    path=os.path.join(os.environ["HOME"], "Desktop", "To Be Synced"),
    event_handler=epub_handler
)
observer.schedule(
    path='/Volumes',
    event_handler=kindle_handler
)
ObserverRunner().runObserver(observer)
