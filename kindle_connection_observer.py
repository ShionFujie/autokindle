import os
import re
import time
from observer_runner import ObserverRunner
from event_handlers import KindleConnectionHandler
from watchdog.observers import Observer
from watchdog.events import RegexMatchingEventHandler


observer = Observer()
observer.schedule(
    path='/Volumes',
    event_handler=KindleConnectionHandler()
)
ObserverRunner().runObserver(observer)
