import os
import subprocess
from autokindle.logging import getLogger, setupLogging
from autokindle.state import Store, reducer
from autokindle.watchdog.handlers import FileHandler, KindleConnectionHandler
from autokindle.watchdog import start_watching
from autokindle.state.observables import initialize, new_files, connection_statuses, failed_transfers
import rx


setupLogging()
logger = getLogger(__name__, 'main')


def on_each():
    logger.debug(store.getState().__dict__)


store = Store(reducer)
store.subscribe(on_each)
file_handler = FileHandler()
kindle_handler = KindleConnectionHandler()
rx.concat(
    initialize(),
    rx.merge(
        new_files(file_handler),
        connection_statuses(kindle_handler),
        failed_transfers(store),
    )
).subscribe(lambda action: store.dispatch(action))
start_watching(file_handler, kindle_handler)
