import os
import subprocess
from autokindle.constants import paths
from autokindle.logging import getLogger, setupLogging
from autokindle.state import Store, reducer
from autokindle.watchdog.observer_runner import ObserverRunner
from autokindle.watchdog.handlers import FileHandler, KindleConnectionHandler
from autokindle.state.observables import new_files, connection_statuses, failed_transfers
import rx
from rx.subject import Subject
from rx import operators
from watchdog.observers import Observer


setupLogging()
logger = getLogger(__name__, 'main')


def on_each():
    logger.debug(store.getState().__dict__)


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
