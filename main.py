import os
import subprocess
from constants import paths
from store import Store
from observer_runner import ObserverRunner
from event_handlers import FileHandler, KindleConnectionHandler
from observables import new_files, connection_statuses, failed_transfers
import rx
from rx.subject import Subject
from rx import operators
from watchdog.observers import Observer


class State:
    def __init__(self, paths=[], is_connected=False, processing=[]):
        self.paths = paths
        self.is_connected = is_connected
        self.processing = processing

    def is_idle(self):
        return not self.paths and not self.is_connected

    def needs_sync(self):
        return self.paths and not self.is_connected

    def awaits_files(self):
        return not self.paths and self.is_connected

    def is_syncing(self):
        return self.paths and self.is_connected

    def copy(self, processing=[], **updates):
        return State(**{**self.__dict__, **updates, 'processing': processing})


def reducer(state=State(), action=None):
    if action is None:
        return state
    if action['type'] == 'CONNECTED':
        return State(is_connected=True, paths=[], processing=state.paths)
    elif action['type'] == 'DISCONNECTED':
        return state.copy(is_connected=False)
    elif action['type'] == 'NEW_FILE':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
    elif action['type'] == 'TRANSFER_FAILED':
        if (state.is_connected):
            return state.copy(processing=[action['path']])
        else:
            return state.copy(paths=[*state.paths, action['path']])
        return
    else:
        return state


def on_each():
    print(store.getState().__dict__)


def start_watching(epub_handler, kindle_handler):
    observer = Observer()
    observer.schedule(
        path=paths.BUCKET,
        event_handler=epub_handler
    )
    observer.schedule(
        path=paths.VOLUMES,
        event_handler=kindle_handler
    )
    ObserverRunner().runObserver(observer)


store = Store(reducer)
store.subscribe(on_each)
file_handler = FileHandler()
kindle_handler = KindleConnectionHandler()
rx.merge(
    new_files(file_handler),
    connection_statuses(kindle_handler),
    failed_transfers(store),
).subscribe(lambda action: store.dispatch(action))
start_watching(file_handler, kindle_handler)
