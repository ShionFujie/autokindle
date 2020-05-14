import os
import subprocess
from autokindle.logging import getLogger
from autokindle.state import Store, reducer
from autokindle.watchdog.handlers import FileHandler, KindleConnectionHandler
from autokindle.watchdog import start_watching
from autokindle.state.observables import events
import rx


logger = getLogger(__name__, 'main')


def on_each():
    logger.debug(store.getState().__dict__)


store = Store(reducer)
store.subscribe(on_each)
file_handler = FileHandler()
kindle_handler = KindleConnectionHandler()

events(file_handler, kindle_handler, store).subscribe(
    lambda action: store.dispatch(action))
logger.debug('Subscribed')
start_watching(file_handler, kindle_handler)
