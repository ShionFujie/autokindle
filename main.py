import os
from store import Store
from observer_runner import ObserverRunner
from event_handlers import EpubFilesHandler, KindleConnectionHandler
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

def on_new_file(path):
    store.dispatch(dict(type='NEW_FILE', path=path))


def on_connect():
    store.dispatch(dict(type='CONNECTED'))


def on_disconnect():
    store.dispatch(dict(type='DISCONNECTED'))


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
